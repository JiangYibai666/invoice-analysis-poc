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
    # Split out any embedded markdown table block.
    # A table block is one or more consecutive lines that start with '|'.
    table_re = re.compile(r"(\n?(?:\|[^\n]+\|\n?)+)", re.MULTILINE)
    match = table_re.search(text)

    if match:
        before_table = text[: match.start()].strip()

        # Everything up to and including "In summary:" goes in the Panel.
        # Any lines after "In summary:" (the table intro) are printed between
        # the Panel and the table.
        lines = before_table.splitlines()
        panel_lines: list[str] = []
        intro_lines: list[str] = []
        past_summary = False
        for line in lines:
            if not past_summary:
                panel_lines.append(line)
                if line.strip().lower().startswith("in summary:"):
                    past_summary = True
            else:
                intro_lines.append(line)

        console.print(Panel.fit("\n".join(panel_lines).strip() or " ", title=title))
        intro = "\n".join(intro_lines).strip()
        if intro:
            console.print(f"\n{intro}")
        _render_markdown_table(match.group(1).strip())
    else:
        console.print(Panel.fit(text, title=title))


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
Available queries (natural language):
  • "Which invoices have been pending for more than 60 days?"
  • "Show me the top 10 suppliers by invoice count"
  • "Which suppliers have the highest invoice amounts?"
  • "Which suppliers have the lowest total invoice amounts?"
  • "Give me a full invoice analysis"

Type 'help' to show this message, 'exit' to quit.
""".strip()


def _render_report(report: dict) -> None:
    qtype = report.get("query_type", "unknown")
    summary = report.get("summary", "")
    raw = report.get("raw_data", {})

    title = f"[bold cyan]Invoice Analysis — {qtype}[/bold cyan]"
    _render_summary(summary, title)

    if qtype == "long_pending_invoices":
        invoices = raw.get("invoices", [])
        if invoices:
            tbl = Table(title=f"Long-Pending Invoices (>{raw.get('threshold_days')} days)", show_lines=True)
            tbl.add_column("Invoice No", style="cyan")
            tbl.add_column("Supplier")
            tbl.add_column("Days Pending", justify="right", style="red")
            tbl.add_column("Status")
            tbl.add_column("Amount", justify="right")
            tbl.add_column("Currency")
            for inv in invoices:
                tbl.add_row(
                    str(inv.get("invoice_no") or ""),
                    str(inv.get("supplier_name") or ""),
                    str(inv.get("days_pending") or ""),
                    str(inv.get("invoice_status") or ""),
                    f"{float(inv['total_amount']):,.2f}" if inv.get("total_amount") else "",
                    str(inv.get("currency_code") or ""),
                )
            console.print(tbl)
            total_count = raw.get("count", len(invoices))
            if total_count > len(invoices):
                console.print(f"[dim]Showing {len(invoices)} of {total_count} matching invoices.[/dim]")

    elif qtype == "supplier_frequency":
        suppliers = raw.get("suppliers", [])
        if suppliers:
            tbl = Table(title="Supplier Invoicing Frequency", show_lines=True)
            tbl.add_column("Rank", justify="right", style="cyan")
            tbl.add_column("Supplier")
            tbl.add_column("Code")
            tbl.add_column("Invoice Count", justify="right", style="green")
            tbl.add_column("First Invoice")
            tbl.add_column("Last Invoice")
            for i, s in enumerate(suppliers, 1):
                tbl.add_row(
                    str(i),
                    str(s.get("supplier_name") or ""),
                    str(s.get("supplier_code") or ""),
                    str(s.get("invoice_count") or ""),
                    str((s.get("first_invoice_date") or "")[:10]),
                    str((s.get("last_invoice_date") or "")[:10]),
                )
            console.print(tbl)

    elif qtype == "supplier_amount":
        suppliers = raw.get("suppliers", [])
        if suppliers:
            tbl = Table(title=f"Supplier Invoicing Amount ({raw.get('order', '')})", show_lines=True)
            tbl.add_column("Rank", justify="right", style="cyan")
            tbl.add_column("Supplier")
            tbl.add_column("Currency")
            tbl.add_column("Total Amount", justify="right", style="green")
            tbl.add_column("Avg Amount", justify="right")
            tbl.add_column("Min", justify="right")
            tbl.add_column("Max", justify="right")
            tbl.add_column("Count", justify="right")
            for i, s in enumerate(suppliers, 1):
                tbl.add_row(
                    str(i),
                    str(s.get("supplier_name") or ""),
                    str(s.get("currency") or ""),
                    f"{float(s['total_amount']):,.2f}" if s.get("total_amount") else "",
                    f"{float(s['avg_amount']):,.2f}" if s.get("avg_amount") else "",
                    f"{float(s['min_amount']):,.2f}" if s.get("min_amount") else "",
                    f"{float(s['max_amount']):,.2f}" if s.get("max_amount") else "",
                    str(s.get("invoice_count") or ""),
                )
            console.print(tbl)

    elif qtype == "all":
        raw_data = report.get("raw_data", {})
        for sub_key in ("long_pending_invoices", "supplier_frequency", "supplier_amount_highest"):
            sub = raw_data.get(sub_key)
            if sub:
                _render_report({"query_type": sub.get("query_type"), "summary": sub.get("summary", ""), "raw_data": sub})

    elif qtype == "document_matching":
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

    elif qtype == "llm_query":
        pass

    elif qtype == "error":
        console.print(f"[bold red]Error:[/bold red] {raw.get('error', 'Unknown error')}")


async def ask_once(query: str) -> None:
    request = TaskRequest(
        source_agent="CLI",
        target_agent="HostAgent",
        message=Message(role="user", parts=[TextPart(text=query)]),
    )
    client = A2AClient(timeout=120.0)
    try:
        response = await client.send(request)
        if response.state == TaskState.FAILED:
            console.print(f"[red]{response.error or 'HostAgent request failed'}[/red]")
            return
        if response.artifact is not None:
            for part in response.artifact.parts:
                if getattr(part, "type", "") == "data":
                    _render_report(part.data)
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
