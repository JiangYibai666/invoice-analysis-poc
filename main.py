from __future__ import annotations

import multiprocessing as mp
import os
import socket
import time
import webbrowser

import uvicorn
from dotenv import load_dotenv

from storage.task_store import init_db


def _serve(app_import_str: str, port: int) -> None:
    uvicorn.run(app_import_str, host="127.0.0.1", port=port, log_level="warning")


def _is_port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.2)
        return s.connect_ex(("127.0.0.1", port)) != 0


def _wait_for_port(port: int, timeout: float = 10.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.2):
                return True
        except OSError:
            time.sleep(0.15)
    return False


def main() -> None:
    load_dotenv()
    init_db()

    configs = [
        ("HostAgent", "agents.host_agent.server:app", 10000),
        ("InvoiceAgent", "agents.invoice_agent.server:app", 10001),
        ("PurchaseOrderAgent", "agents.purchase_order_agent.server:app", 10002),
        ("DeliveryOrderAgent", "agents.delivery_order_agent.server:app", 10003),
        ("Frontend", "frontend_app:app", 8080),
    ]

    blocked = [
        (label, port)
        for label, _, port in configs
        if not _is_port_free(port)
    ]
    if blocked:
        for label, port in blocked:
            print(f"✗ Port {port} ({label}) is already in use — stop the previous run first.")
        return

    processes = [
        mp.Process(target=_serve, args=(app_str, port), daemon=True)
        for _, app_str, port in configs
    ]

    for proc in processes:
        proc.start()

    frontend_ready = False
    for proc, (label, _, port) in zip(processes, configs):
        ok = _wait_for_port(port)
        alive = proc.is_alive()
        if ok and alive:
            print(f"✓ {label} listening on http://localhost:{port}")
            if label == "Frontend":
                frontend_ready = True
        elif ok and not alive:
            print(f"✗ {label}: process exited unexpectedly")
        else:
            print(f"⚠  {label}: did not respond on port {port}")

    print("✓ PostgreSQL task store initialised")
    if frontend_ready:
        frontend_url = "http://127.0.0.1:8080/"
        print(f"✓ Frontend available at {frontend_url}")
        if os.getenv("DOXA_OPEN_FRONTEND", "1").lower() not in {"0", "false", "no"}:
            webbrowser.open(frontend_url)

    from cli.chat import run_cli
    try:
        run_cli()
    finally:
        for proc in processes:
            proc.terminate()


if __name__ == "__main__":
    main()
