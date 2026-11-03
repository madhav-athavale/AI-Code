# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an experimental repository for building agentic AI applications using the Model Context Protocol (MCP) and Claude's API. The codebase contains multiple implementations demonstrating different transport mechanisms (stdio, SSE, HTTP) for MCP servers and clients that expose tools (calculator, stock prices, MySQL queries, CSV writing) to Claude agents.

## Architecture

### Core Pattern: MCP Server + Client + Agent Loop

The repository follows a three-layer architecture:

1. **MCP Servers** - Expose tools (functions) that Claude can call
   - `mcp_server.py` - Basic stdio server (calculator + stock + DB)
   - `mcp_sse_server.py` - SSE transport server with all tools including write_csv
   - `mcp_http_server.py` - StreamableHTTP server using FastMCP
   - `mcp_http_web_server.py` - HTTP variant with web interface

2. **MCP Clients** - Connect to servers and orchestrate Claude API calls
   - `mcp_client.py` - Interactive stdio client with agentic loop
   - `mcp_sse_client.py` - SSE client for remote server connections
   - `mcp_http_client.py` - HTTP client for StreamableHTTP transport

3. **Specialized Workflows**
   - `query_to_csv.py` - Hybrid pattern: Claude interprets NL→SQL, then direct CSV write (no Claude)
   - `agent_with_df.py` - Pass pandas DataFrame to Claude, which decides how to write CSV
   - `direct_tool_call.py` - Direct MCP tool invocation without Claude in the loop
   - `streamlit_app.py` - Web UI with live agent trace visualization

### Key Concepts

**Transport Mechanisms:**
- **stdio**: Server runs as subprocess, communicates via stdin/stdout (local only)
- **SSE**: Server-Sent Events over HTTP for remote connections
- **StreamableHTTP**: FastMCP's HTTP transport (single `/mcp` endpoint)

**Agent Loop Pattern:**
All clients implement the same agentic loop:
1. Send user query + available tools to Claude
2. Claude returns text and/or tool_use blocks
3. Execute tool calls on MCP server
4. Feed tool results back to Claude as tool_result
5. Repeat until Claude returns no more tool_use blocks

**Tool Chaining:**
- `query_to_csv.py` demonstrates optimal efficiency: use Claude only where reasoning is needed (NL→SQL), then call deterministic tools directly (write_csv) to avoid unnecessary API calls

## Environment Setup

### Required API Keys

Copy `.env-template` to `.env` and populate:

```bash
ALPHAVANTAGE_API_KEY=    # For stock price tool
ANTHROPIC_API_KEY=       # For Claude API
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=northwind        # Or your database name
BRAVE_API_KEY=           # (unused in current code)
```

### Dependencies

Install MCP and Claude dependencies:
```bash
pip install "mcp[client]" "mcp[server]" anthropic httpx httpx-sse aiomysql pandas python-dotenv
```

For web servers:
```bash
pip install uvicorn starlette fastmcp
```

For Streamlit UI:
```bash
pip install streamlit
```

## Running the Code

### Basic Stdio Setup (Local)

Terminal 1 - Server runs automatically when client starts:
```bash
python mcp_client.py
```

The client spawns the server as a subprocess and handles stdio communication automatically.

### SSE Setup (Remote-capable)

Terminal 1 - Start SSE server:
```bash
python mcp_sse_server.py
# Listens on http://0.0.0.0:8000/sse
```

Terminal 2 - Run client:
```bash
python mcp_sse_client.py
```

### StreamableHTTP Setup (Recommended)

Terminal 1 - Start HTTP server:
```bash
python mcp_http_server.py
# Endpoint: http://localhost:8000/mcp
```

Terminal 2 - Run client:
```bash
python mcp_http_client.py
```

Or use the web UI:
```bash
streamlit run streamlit_app.py
```

### Specialized Workflows

Query natural language → SQL → CSV (efficient):
```bash
# Ensure SSE server is running first
python query_to_csv.py
```

DataFrame → Claude → CSV:
```bash
# Ensure SSE server is running first
python agent_with_df.py
```

## Available Tools

All servers expose these tools to Claude:

- **add(a, b)** - Adds two numbers
- **subtract(a, b)** - Subtracts b from a
- **price(a)** - Fetches stock quote from Alpha Vantage (ticker symbol)
- **query_db(query)** - Executes SELECT query on MySQL database
- **write_csv(filename, headers, rows)** - Writes structured data to CSV file

Note: `query_db` and `write_csv` are only available in SSE and HTTP servers, not the basic stdio server.

## Database Configuration

The servers connect to a MySQL database. Current default configuration points to a local `northwind` database. Update `DB_CONFIG` in server files or set environment variables in `.env`.

## File Organization

- **Server implementations**: `mcp_server.py`, `mcp_sse_server.py`, `mcp_http_server.py`, `mcp_http_web_server.py`
- **Client implementations**: `mcp_client.py`, `mcp_sse_client.py`, `mcp_http_client.py`
- **Workflow patterns**: `query_to_csv.py`, `agent_with_df.py`, `direct_tool_call.py`
- **UI**: `streamlit_app.py`
- **Tests**: `google_search_test.py`

## Important Notes

- Hardcoded paths: `mcp_client.py` has `SERVER_SCRIPT` hardcoded to absolute path - update for your environment
- Security: Never commit the `.env` file (already in `.gitignore`)
- Database credentials: Currently some servers have hardcoded credentials (e.g., `mcp_sse_server.py` line 35) - these should be removed in favor of environment variables
- Model: All clients default to `claude-sonnet-4-6`
- The `query_to_csv.py` pattern is recommended when you need both Claude reasoning and deterministic operations - it minimizes API calls by only using Claude where necessary

## Debugging

To see the full request/response cycle:
- Clients print tool calls and results to stdout
- Streamlit app shows live agent trace with color-coded tool badges
- Check server logs for tool execution details
