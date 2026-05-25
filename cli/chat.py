from __future__ import annotations

import asyncio
import json

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from a2a.client import A2AClient
from a2a.types import Message, TaskRequest, TaskState, TextPart

console = Console()

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

    console.print(Panel.fit(summary, title=f"[bold cyan]Invoice Analysis — {qtype}[/bold cyan]"))

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
