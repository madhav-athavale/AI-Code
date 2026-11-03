---
name: stock-report
description: Use this skill when asked to look up a stock price, pull related 
  historical data from the database, or produce a saved report combining both. 
  Covers the standard workflow for combining the price, query_db, and write_csv 
  MCP tools into a consistent report format.
---

# Stock Report Workflow

This skill defines how to produce a stock report using the `price`, `query_db`, 
and `write_csv` tools together.

## When to use this

Trigger this workflow when the user asks for:
- A current stock price with supporting context ("get me AAPL with some history")
- A saved report combining live price + database records
- Multiple tickers compared side by side

## Steps

0. If you don't know the exact table/column names, call `list_tables` 
   and `describe_table` first rather than guessing.

## Important: describe_table and list_tables do NOT return row data

    `describe_table` and `list_tables` only return schema information (table/column 
    names) — they never return actual records. Before calling `write_csv`, you must 
    call `query_db` with a real SELECT statement to fetch the actual data rows. 
    Never pass column names from `describe_table` as if they were data rows.

1. **Validate the ticker** before calling any tool. Tickers are 1-5 uppercase 
   letters (e.g. AAPL, MSFT, IBM). If the user gives a company name instead of 
   a ticker ("Apple"), resolve it to the ticker yourself first and confirm with 
   the user if ambiguous.

2. **Call `price`** for each ticker requested. If the tool returns a "Could not 
   get price" error, tell the user immediately rather than proceeding to the 
   next steps with partial data.

3. **Call `query_db`** to pull historical context, using this query pattern:
```sql
   SELECT * FROM stock_history WHERE ticker = '<TICKER>' 
   ORDER BY date DESC LIMIT 30
```
   If `query_db` returns "Query returned no results," note that in the report 
   rather than treating it as a failure — not all tickers have historical 
   records yet.

4. **Only call `write_csv` if the user asked to save/export.** Do not write a 
   CSV just because data was fetched — many requests just want the numbers 
   shown in chat.

5. **When writing CSV, always use this header format:**

headers = ["Ticker", "Price", "Open", "High", "Low", "Volume", "Change", "Change %"]

   Keep this consistent across all reports so files are easy to compare later.

6. **Summarize in plain language after tool calls**, don't just dump raw tool 
   output. Mention the current price, notable change, and whether historical 
   data was found.

## Example

User: "Get me IBM's price and save a report"

1. Call `price` with `symbol="IBM"`
2. Call `query_db` with the historical query above, `ticker='IBM'`
3. Call `write_csv` with the standard headers, filename `ibm_report.csv`
4. Reply: "IBM is currently at $XXX.XX (up/down X% today). Saved a report 
   with 30 days of history to ibm_report.csv."