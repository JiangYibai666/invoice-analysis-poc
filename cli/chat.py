from __future__ import annotations

import asyncio
import json
import re

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from a2a.client import A2AClient
from a2a.types import Message, TaskRequest, TaskState, TextPart

console = Console()


def _render_summary(text: str, title: str) -> None:
    """Display the summary Panel and, if the LLM included a markdown table, render it."""
    table_re = re.compile(r"(\n?(?:\|[^\n]+\|\n?)+)", re.MULTILINE)
    matches = list(table_re.finditer(text))

    if not matches:
        console.print(Panel.fit(text, title=title))
        return

    cursor = 0
    printed_panel = False
    for match in matches:
        before_table = text[cursor:match.start()].strip()
        if before_table:
            if printed_panel:
                console.print(f"\n{before_table}")
            else:
                console.print(Panel.fit(before_table, title=title))
                printed_panel = True

        _render_markdown_table(match.group(1).strip())
        cursor = match.end()

    tail = text[cursor:].strip()
    if tail:
        if printed_panel:
            console.print(f"\n{tail}")
        else:
            console.print(Panel.fit(tail, title=title))
            printed_panel = True


def _strip_markdown_tables(text: str) -> str:
    """Remove markdown table blocks from text, leaving surrounding prose."""
    return re.sub(r"\n?(?:\|[^\n]+\|\n?)+", "\n", text).strip()


def _render_markdown_table(md: str) -> None:
    """Parse a GitHub-flavoured markdown table string and render it with rich."""
    lines = [ln.strip() for ln in md.splitlines() if ln.strip()]
    # Filter out the separator row (e.g. |---|---|)
    data_lines = [ln for ln in lines if not re.match(r"^\|[-| :]+\|$", ln)]
    if not data_lines:
        return

    def _parse_row(line: str) -> list[str]:
        return [cell.strip() for cell in line.strip("|").split("|")]

    headers = _parse_row(data_lines[0])
    tbl = Table(show_lines=True)
    for h in headers:
        tbl.add_column(h)
    for row_line in data_lines[1:]:
        cells = _parse_row(row_line)
        # Pad or truncate to match header count
        cells = (cells + [""] * len(headers))[: len(headers)]
        tbl.add_row(*cells)
    console.print(tbl)


_HELP = """
Available queries by category (natural language):

  ── Invoice Analytics (InvoiceAgent) ──────────────────────────────────────────
  • "Which invoices have been pending for more than 60 days?"
  • "Show me the top 10 suppliers by invoice count"
  • "Which suppliers have the highest total invoice amounts?"
  • "Which buyers have the most unpaid invoices?"
  • "List all invoices with payment status OVERDUE"
  • "Show invoices submitted this month grouped by currency"
  • "Which invoices are still in non-terminal status?"
  • "What is the total invoice amount per supplier for SGD invoices?"
  • "Show the 5 largest invoices by total amount"
  • "How many invoices are in each invoice_status?"

  ── Purchase Order Analytics (PurchaseOrderAgent) ─────────────────────────────
  • "Show top 10 purchase orders by value"
  • "Which 3 suppliers have the most amount of PO?"
  • "Which buyers have raised the most purchase orders?"
  • "List all open POs that have not been fully received"
  • "Show POs by status and count"
  • "Which POs have the highest tax amount?"
  • "Show all POs raised this year grouped by supplier"
  • "What is the total PO value per currency?"
  • "List contracted PO items with their net prices"

  ── Delivery Order Analytics (DeliveryOrderAgent) ─────────────────────────────
  • "Which 3 suppliers have the most amount of DO?"
  • "Which delivery orders are pending?"
  • "Show DOs with the highest total received quantity"
  • "Which buyers have the most delivery orders?"
  • "List DOs that have rejected quantities"
  • "Show delivery orders grouped by status"
  • "Which DOs are linked to the most PO items?"
  • "List DOs delivered this month"

  ── Document Matching (PurchaseOrderAgent + DeliveryOrderAgent) ───────────────
  • "Check invoice INV-00000001" and its related PO"  (invoice ↔ PO)
  • "Does invoice INV-00000001 match its delivery order?"  (invoice ↔ DO)
  • "Check latest 5 DO, and show me related invoice and PO"  (DO ↔ invoice + PO)
  • "Is INV-00000002 matched against its PO?"
  • "Show matching result for invoice INV-00000005"

  ── Batch Document Matching (no specific invoice number needed) ───────────────
  • "Check latest 5 invoices three-way matching"
  • "Check invoice-to-PO matching for the last 10 invoices"
  
  ── Cross-domain Analysis (multiple agents) ───────────────────────────────────
  • "Which 3 suppliers have the most PO and DO?"
  • "Compare PO and DO counts by supplier"

Type 'help' to show this message, 'exit' to quit.
""".strip()


def _strip_post_summary_content(text: str) -> str:
    """Keep everything up to and including the 'In summary:' sentence.

    Discards table heading lines and markdown tables that the LLM places after
    'In summary:', since the CLI renders raw DB tables separately instead.
    Falls back to stripping bare markdown tables when there is no 'In summary:'.
    """
    match = re.search(r"\bIn summary:[^\n]*", text)
    if match:
        return text[:match.end()].strip()
    return _strip_markdown_tables(text)


_DISPLAY_ROW_DEFAULT = 20
_DISPLAY_ROW_MAX = 200


def _display_row_count(query: str, available: int) -> int:
    """Return how many rows to show in a DB result table.

    Defaults to 20.  Respects an explicit count in the query
    (e.g. 'top 50') or 'show all' / 'list all'.
    """
    if re.search(
        r"\b(?:show|list|display)\s+all\b|\ball\s+(?:records?|rows?|results?)\b",
        query,
        re.IGNORECASE,
    ):
        return min(available, _DISPLAY_ROW_MAX)
    patterns = (
        r"\b(?:top|first|latest|last|limit|show|list)\s+(\d{1,3})\b",
        r"\b(\d{1,3})\s+(?:rows?|records?|items?|invoices?|purchase\s+orders?|delivery\s+orders?)\b",
    )
    for pattern in patterns:
        m = re.search(pattern, query, re.IGNORECASE)
        if m:
            return min(max(1, int(m.group(1))), available, _DISPLAY_ROW_MAX)
    return min(_DISPLAY_ROW_DEFAULT, available)


def _render_db_result_table(
    columns: list[str],
    rows: list[dict],
    title: str,
    display_columns: list[str] | None = None,
    row_limit: int | None = None,
) -> None:
    """Render raw DB query result columns/rows as a Rich table.

    If *display_columns* is provided (LLM-selected subset), only those columns
    are shown so the table fits comfortably in the terminal.
    *row_limit* caps how many rows are shown; defaults to _DISPLAY_ROW_DEFAULT.
    """
    if not columns or not rows:
        return
    show_cols = display_columns if display_columns else columns
    # Keep only names that actually exist in the result set
    show_cols = [c for c in show_cols if c in columns] or columns
    cap = row_limit if row_limit is not None else _DISPLAY_ROW_DEFAULT
    display_rows = rows[:cap]
    tbl = Table(title=title, show_lines=True)
    for col in show_cols:
        tbl.add_column(str(col))
    for row in display_rows:
        tbl.add_row(*[str(row.get(col, "")) if row.get(col) is not None else "" for col in show_cols])
    console.print(tbl)
    if len(rows) > cap:
        console.print(f"[dim]... {len(rows) - cap} more row(s) not shown[/dim]")


def _render_report(report: dict) -> None:
    qtype = report.get("query_type", "unknown")
    summary = report.get("summary", "")
    raw = report.get("raw_data", {})

    title = f"[bold cyan]Invoice Analysis — {qtype}[/bold cyan]"
    query = report.get("query", "")
    # Analysis types that render a raw DB table: strip any LLM-generated tables
    # and their heading lines from the summary text to avoid duplicates.
    _analysis_qtypes = {"invoice_analysis", "purchase_order_analysis", "delivery_order_analysis"}
    has_db_rows = bool(raw.get("columns") and raw.get("rows"))
    if qtype == "multi_agent_analysis":
        # _build_summary already formats the multi-agent text correctly (no trailing
        # tables).  Only strip any stray bare markdown tables as a safety net.
        summary_text = _strip_markdown_tables(summary)
    elif qtype in _analysis_qtypes and has_db_rows:
        # Single-agent: remove the LLM's embedded table and its heading line,
        # keeping the prose body and the "In summary:" sentence.
        summary_text = _strip_post_summary_content(summary)
    else:
        summary_text = summary
    _render_summary(summary_text, title)

    if qtype == "document_matching":
        po_match = raw.get("po_match", {})
        do_match = raw.get("do_match", {})

        po_lines = po_match.get("lines", [])
        if po_lines:
            tbl = Table(title="Invoice to PO Matching", show_lines=True)
            tbl.add_column("Invoice Item", justify="right", style="cyan")
            tbl.add_column("Item")
            tbl.add_column("PO No")
            tbl.add_column("Inv Net", justify="right")
            tbl.add_column("PO Net", justify="right")
            tbl.add_column("Variance", justify="right")
            tbl.add_column("Match")
            for line in po_lines[:20]:
                tbl.add_row(
                    str(line.get("invoice_item_id") or ""),
                    str(line.get("item_name") or line.get("item_code") or ""),
                    str(line.get("po_number") or line.get("invoice_item_po_number") or ""),
                    f"{float(line['invoice_net_price']):,.2f}" if line.get("invoice_net_price") is not None else "",
                    f"{float(line['matched_po_net_price']):,.2f}" if line.get("matched_po_net_price") is not None else "",
                    f"{float(line['net_amount_variance']):,.2f}" if line.get("net_amount_variance") is not None else "",
                    "yes" if line.get("net_amount_match") is True else "no",
                )
            console.print(tbl)
        elif po_match.get("results"):
            _render_batch_match_results(po_match)

        do_lines = do_match.get("lines", [])
        if do_lines:
            tbl = Table(title="Invoice to DO Matching", show_lines=True)
            tbl.add_column("Invoice Item", justify="right", style="cyan")
            tbl.add_column("Item")
            tbl.add_column("DO No")
            tbl.add_column("Inv Qty", justify="right")
            tbl.add_column("DO Qty", justify="right")
            tbl.add_column("Variance", justify="right")
            tbl.add_column("Covered")
            for line in do_lines[:20]:
                tbl.add_row(
                    str(line.get("invoice_item_id") or ""),
                    str(line.get("item_name") or line.get("item_code") or ""),
                    str(line.get("delivery_order_number") or line.get("invoice_item_do_number") or ""),
                    f"{float(line['invoice_qty']):,.4f}" if line.get("invoice_qty") is not None else "",
                    f"{float(line['matched_do_quantity']):,.4f}" if line.get("matched_do_quantity") is not None else "",
                    f"{float(line['quantity_variance']):,.4f}" if line.get("quantity_variance") is not None else "",
                    "yes" if line.get("quantity_covered") is True else "no",
                )
            console.print(tbl)
        elif do_match.get("results"):
            _render_batch_match_results(do_match)

    elif qtype == "multi_agent_analysis":
        for agent_name, agent_data in raw.get("agent_results", {}).items():
            cols = agent_data.get("columns") or []
            agent_rows = agent_data.get("rows") or []
            if cols and agent_rows:
                display_cols = agent_data.get("display_columns") or None
                row_lim = _display_row_count(query, len(agent_rows))
                _render_db_result_table(cols, agent_rows, f"{agent_name} — Query Results", display_cols, row_lim)

    elif qtype.endswith("_error") or qtype == "error":
        console.print(f"[bold red]Error:[/bold red] {raw.get('error', 'Unknown error')}")

    else:
        cols = raw.get("columns") or []
        agent_rows = raw.get("rows") or []
        if cols and agent_rows:
            display_cols = raw.get("display_columns") or None
            row_lim = _display_row_count(query, len(agent_rows))
            _render_db_result_table(cols, agent_rows, "Query Results", display_cols, row_lim)


def _render_batch_match_results(match: dict) -> None:
    """Render per-invoice rows from a po_batch_match or do_batch_match result."""
    results = match.get("results", [])
    if not results:
        return

    is_po = "po" in match.get("query_type", "")
    title = "Invoice-to-PO Batch Matching" if is_po else "Invoice-to-DO Batch Matching"
    tbl = Table(title=title, show_lines=True)
    tbl.add_column("Invoice No", style="cyan")
    tbl.add_column("Found")
    tbl.add_column("Result")
    tbl.add_column("Lines", justify="right")
    if is_po:
        tbl.add_column("Missing PO", justify="right")
        tbl.add_column("Mismatched", justify="right")
        tbl.add_column("Inv Total", justify="right")
        tbl.add_column("PO Total", justify="right")
        tbl.add_column("Variance", justify="right")
    else:
        tbl.add_column("Missing DO", justify="right")
        tbl.add_column("Uncovered", justify="right")

    for r in results:
        inv_no = str(r.get("invoice_no") or "")
        found = "yes" if r.get("found") else "no"
        if not r.get("found"):
            result_cell = "not found"
        elif r.get("matched"):
            result_cell = "[green]pass[/green]"
        else:
            result_cell = "[red]review[/red]"
        lines = str(r.get("line_count") or 0)
        if is_po:
            tbl.add_row(
                inv_no,
                found,
                result_cell,
                lines,
                str(r.get("missing_po_lines") or 0),
                str(r.get("mismatched_lines") or 0),
                f"{float(r['invoice_line_total']):,.2f}" if r.get("invoice_line_total") is not None else "",
                f"{float(r['po_line_total']):,.2f}" if r.get("po_line_total") is not None else "",
                f"{float(r['amount_variance']):,.2f}" if r.get("amount_variance") is not None else "",
            )
        else:
            tbl.add_row(
                inv_no,
                found,
                result_cell,
                lines,
                str(r.get("missing_do_lines") or 0),
                str(r.get("uncovered_lines") or 0),
            )
    console.print(tbl)


def _display_routing(message: str) -> None:
    """Parse a HostAgent routing event and print which agents are being used."""
    # Message format: "HostAgent: route=<task_type> targets=AgentA,AgentB"
    if "targets=" not in message:
        return
    agents_str = message.split("targets=", 1)[1].strip()
    agents = [a.strip() for a in agents_str.split(",") if a.strip()]
    agent_labels = ", ".join(f"[bold magenta]{a}[/bold magenta]" for a in agents)
    console.print(f"[dim]→ Routing to:[/dim] {agent_labels}")


async def ask_once(query: str) -> None:
    import httpx as _httpx
    request = TaskRequest(
        source_agent="CLI",
        target_agent="HostAgent",
        message=Message(role="user", parts=[TextPart(text=query)]),
    )
    # connect/write timeout of 15 s; read timeout disabled so long-running
    # multi-agent SSE streams are not cut off mid-flight.
    streaming_timeout = _httpx.Timeout(connect=15.0, read=None, write=30.0, pool=15.0)
    client = A2AClient(timeout=streaming_timeout)
    try:
        async for event in client.send_subscribe(request):
            if event.state == TaskState.FAILED:
                console.print(f"[red]{event.message or 'HostAgent request failed'}[/red]")
                return
            if event.state == TaskState.WORKING and event.message and "targets=" in event.message:
                _display_routing(event.message)
            if event.state == TaskState.COMPLETED and event.artifact is not None:
                for part in event.artifact.parts:
                    if getattr(part, "type", "") == "data":
                        _render_report(part.data)
    except _httpx.ReadTimeout:
        console.print("[red]Request timed out waiting for the agent to respond. "
                      "The query may be too complex or the backend is overloaded.[/red]")
    except _httpx.ConnectError:
        console.print("[red]Could not connect to HostAgent. Is the server running?[/red]")
    finally:
        await client.close()


def run_cli() -> None:
    console.print(Panel.fit("Invoice Analysis CLI  (type 'help' or 'exit')", title="invoice-analysis-poc"))
    while True:
        try:
            query = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not query:
            continue
        if query.lower() in ("exit", "quit", "q"):
            break
        if query.lower() == "help":
            console.print(_HELP)
            continue
        asyncio.run(ask_once(query))
