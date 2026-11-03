"""
MCP Server - Agentic AI Template (MCPServer + Streamable HTTP) — mcp SDK v2
Runs as a standalone HTTP server supporting multiple clients.
Tools: add, subtract, price (Alpha Vantage), query_db, list_tables,
       describe_table (PostgreSQL), write_csv, export_query_to_csv

Install dependencies:
    pip install "mcp>=2,<3" httpx asyncpg python-dotenv

Run:
    python mcp_server.py
Clients connect to:
    http://localhost:8000/mcp

Logging:
    LOG_LEVEL=INFO   (default) one CALL line and one OK/ERROR line per tool call
    LOG_LEVEL=DEBUG  also logs result previews and SDK internals
    On EC2 (systemd):  sudo journalctl -u mcp -f
"""

import os
import csv
import time
import logging
import functools
import inspect
import itertools

import httpx
import asyncpg
from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer

load_dotenv()

# ── Logging setup ────────────────────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)-7s [%(name)s] %(message)s",
)
logger = logging.getLogger("mcp_server")

# httpx logs full request URLs at INFO, and the Alpha Vantage URL contains the
# API key as a query parameter. Keep these quiet so the key never hits the logs.
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

# v2: host/port are no longer constructor args — they move to run()
mcp = MCPServer("calculator-server")

AV_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),  # asyncpg uses "database", not "db"
}

# CSV files are confined to one folder; path components in filenames are stripped.
OUTPUT_DIR = os.getenv("OUTPUT_DIR", os.path.abspath("output"))
os.makedirs(OUTPUT_DIR, exist_ok=True)


def safe_path(filename: str) -> str:
    if not filename.endswith(".csv"):
        filename += ".csv"
    return os.path.join(OUTPUT_DIR, os.path.basename(filename))


# ── Logging helpers ──────────────────────────────────────────────────────────
_call_counter = itertools.count(1)


def _short(value, limit=300) -> str:
    """Compact, single-line, length-capped representation for log lines."""
    if isinstance(value, (list, tuple)):
        return f"<{type(value).__name__} len={len(value)}>"
    text = value if isinstance(value, str) else repr(value)
    text = text.replace("\n", " ")
    if len(text) > limit:
        return f"{text[:limit]}... [{len(text)} chars]"
    return text


def _fmt_args(args, kwargs) -> str:
    parts = [_short(a) for a in args]
    parts += [f"{k}={_short(v)}" for k, v in kwargs.items()]
    return ", ".join(parts)


def logged(func):
    """
    Log every tool call: arguments, duration, result size, and any exception
    (with traceback). Apply *under* @mcp.tool():

        @mcp.tool()
        @logged
        async def my_tool(...): ...
    """
    name = func.__name__

    if inspect.iscoroutinefunction(func):

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cid = next(_call_counter)
            logger.info("[#%d] CALL  %s(%s)", cid, name, _fmt_args(args, kwargs))
            start = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
            except Exception:
                ms = (time.perf_counter() - start) * 1000
                logger.exception("[#%d] ERROR %s failed after %.0f ms", cid, name, ms)
                raise
            ms = (time.perf_counter() - start) * 1000
            logger.info("[#%d] OK    %s %.0f ms, result=%d chars", cid, name, ms, len(str(result)))
            logger.debug("[#%d] result preview: %s", cid, _short(result, 500))
            return result

    else:

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cid = next(_call_counter)
            logger.info("[#%d] CALL  %s(%s)", cid, name, _fmt_args(args, kwargs))
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
            except Exception:
                ms = (time.perf_counter() - start) * 1000
                logger.exception("[#%d] ERROR %s failed after %.0f ms", cid, name, ms)
                raise
            ms = (time.perf_counter() - start) * 1000
            logger.info("[#%d] OK    %s %.0f ms, result=%d chars", cid, name, ms, len(str(result)))
            logger.debug("[#%d] result preview: %s", cid, _short(result, 500))
            return result

    return wrapper


async def db_connect():
    """Open a DB connection, logging target and failures (never the password)."""
    target = f"{DB_CONFIG['user']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    start = time.perf_counter()
    try:
        conn = await asyncpg.connect(**DB_CONFIG, timeout=10)
    except Exception:
        logger.exception("DB connect FAILED to %s", target)
        raise
    logger.debug("DB connected to %s in %.0f ms", target, (time.perf_counter() - start) * 1000)
    return conn


# ── Tools ────────────────────────────────────────────────────────────────────

@mcp.tool()
@logged
def add(a: float, b: float) -> str:
    """Adds two numbers together."""
    return f"{a} + {b} = {a + b}"


@mcp.tool()
@logged
def subtract(a: float, b: float) -> str:
    """Subtracts the second number from the first."""
    return f"{a} - {b} = {a - b}"


@mcp.tool()
@logged
async def price(symbol: str) -> str:
    """Find the current stock price for a ticker symbol, e.g. MSFT, AAPL."""
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": AV_API_KEY,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.alphavantage.co/query", params=params)
    logger.info("Alpha Vantage responded HTTP %s for %s", response.status_code, symbol)

    data = response.json()
    quote = data.get("Global Quote", {})
    price_val = quote.get("05. price", "")

    if not price_val:
        # Alpha Vantage reports rate limits / bad keys under "Note" or "Information"
        logger.warning("No price for %s. Response keys=%s detail=%s",
                       symbol, list(data.keys()),
                       _short(data.get("Note") or data.get("Information") or data, 200))
        return f"Could not get price for {symbol}. API response: {data}"

    return (
        f"{symbol}: price=${float(price_val):.2f}, "
        f"open=${float(quote.get('02. open', 0)):.2f}, "
        f"high=${float(quote.get('03. high', 0)):.2f}, "
        f"low=${float(quote.get('04. low', 0)):.2f}, "
        f"volume={quote.get('06. volume', '')}, "
        f"change={quote.get('09. change', '')}, "
        f"change_pct={quote.get('10. change percent', '')}"
    )


@mcp.tool()
@logged
async def query_db(query: str) -> str:
    """Execute a SELECT query on the PostgreSQL database and return the results."""
    conn = await db_connect()
    try:
        rows = await conn.fetch(query)
    finally:
        await conn.close()

    logger.info("query_db returned %d rows", len(rows))
    if not rows:
        return "Query returned no results."

    return "\n".join(str(dict(row)) for row in rows)


@mcp.tool()
@logged
async def list_tables() -> str:
    """
    List all table names in the public schema.
    Call this first if you're unsure what tables exist before writing a query.
    """
    conn = await db_connect()
    try:
        rows = await conn.fetch(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
            """
        )
    finally:
        await conn.close()

    logger.info("list_tables found %d tables", len(rows))
    if not rows:
        return "No tables found in the public schema."

    return "\n".join(r["table_name"] for r in rows)


@mcp.tool()
@logged
async def describe_table(table_name: str) -> str:
    """
    Get column names and data types for a specific table.
    Call this before writing a query if you're unsure of a table's exact
    column names (e.g. whether it's 'name' or 'customer_name').
    """
    conn = await db_connect()
    try:
        rows = await conn.fetch(
            """
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = $1
            ORDER BY ordinal_position
            """,
            table_name,
        )
    finally:
        await conn.close()

    if not rows:
        logger.warning("describe_table: no columns found for '%s'", table_name)
        return f"No columns found for table '{table_name}'. It may not exist — try list_tables first."

    lines = [f"{r['column_name']}: {r['data_type']} (nullable={r['is_nullable']})" for r in rows]
    return "\n".join(lines)


@mcp.tool()
@logged
def write_csv(filename: str, headers: list[str], rows: list[list[str]]) -> str:
    """
    Write data to a CSV file on the server.
    Use this when the data has already been seen/transformed by the model
    (e.g. after price, or after filtering/reshaping query_db results) — the
    caller must supply the actual row data as 'rows'.

    For exporting a raw query result straight to CSV with no transformation,
    use export_query_to_csv instead — it's much faster since the row data
    never has to be generated as model output.
    """
    filepath = safe_path(filename)
    if os.path.basename(filename) != filename:
        logger.warning("write_csv: path components stripped from %r -> %s", filename, filepath)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    logger.info("write_csv wrote %s (%d rows, %d cols, %d bytes)",
                filepath, len(rows), len(headers), os.path.getsize(filepath))
    return f"CSV written successfully: {filepath} ({len(rows)} rows, {len(headers)} columns)"


@mcp.tool()
@logged
async def export_query_to_csv(query: str, filename: str) -> str:
    """
    Run a SELECT query and write the results directly to a CSV file on the
    server, without the row data passing through the conversation. Prefer
    this over query_db + write_csv whenever the request is a straight export
    with no filtering/transformation needed — it's much faster for large
    results since the model never has to re-generate the row data as output.
    """
    conn = await db_connect()
    try:
        rows = await conn.fetch(query)
    finally:
        await conn.close()

    if not rows:
        logger.warning("export_query_to_csv: query returned no rows, no file written")
        return "Query returned no results — no file written."

    headers = list(rows[0].keys())
    filepath = safe_path(filename)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow([str(v) for v in row.values()])

    logger.info("export_query_to_csv wrote %s (%d rows, %d cols, %d bytes)",
                filepath, len(rows), len(headers), os.path.getsize(filepath))
    return f"CSV written successfully: {filepath} ({len(rows)} rows, {len(headers)} columns)"


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    host = os.getenv("MCP_HOST", "127.0.0.1")
    port = int(os.getenv("MCP_PORT", 8000))

    logger.info("Starting MCP server (Streamable HTTP) on http://%s:%d/mcp", host, port)
    logger.info("Log level: %s | Output dir: %s", LOG_LEVEL, OUTPUT_DIR)
    logger.info("DB target: %s@%s:%s/%s",
                DB_CONFIG["user"], DB_CONFIG["host"], DB_CONFIG["port"], DB_CONFIG["database"])
    if not AV_API_KEY:
        logger.warning("ALPHAVANTAGE_API_KEY is not set: the price tool will fail")
    missing = [k for k in ("user", "password", "database") if not DB_CONFIG[k]]
    if missing:
        logger.warning("DB config missing values for: %s", ", ".join(missing))

    mcp.run(transport="streamable-http", host=host, port=port)
