from __future__ import annotations

import multiprocessing as mp
import os
import socket
import time
import webbrowser
from urllib.parse import urlparse

import uvicorn
from dotenv import load_dotenv

from storage.task_store import init_db


DEFAULT_BIND_HOST = "127.0.0.1"
DEFAULT_AGENT_PORTS = {
    "HostAgent": 10000,
    "InvoiceAgent": 10001,
    "PurchaseOrderAgent": 10002,
    "DeliveryOrderAgent": 10003,
}
AGENT_URL_ENV = {
    "HostAgent": "HOST_AGENT_URL",
    "InvoiceAgent": "INVOICE_AGENT_URL",
    "PurchaseOrderAgent": "PURCHASE_ORDER_AGENT_URL",
    "DeliveryOrderAgent": "DELIVERY_ORDER_AGENT_URL",
}
AGENT_PORT_ENV = {
    "HostAgent": "HOST_AGENT_PORT",
    "InvoiceAgent": "INVOICE_AGENT_PORT",
    "PurchaseOrderAgent": "PURCHASE_ORDER_AGENT_PORT",
    "DeliveryOrderAgent": "DELIVERY_ORDER_AGENT_PORT",
}


def _serve(app_import_str: str, host: str, port: int) -> None:
    uvicorn.run(app_import_str, host=host, port=port, log_level="warning")


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer, got {raw!r}") from exc


def _port_from_url(raw_url: str | None, default: int) -> int:
    if not raw_url:
        return default
    parsed = urlparse(raw_url)
    return parsed.port or default


def _service_url(host: str, port: int) -> str:
    browser_host = "127.0.0.1" if host in {"0.0.0.0", "::"} else host
    return f"http://{browser_host}:{port}"


def _connect_host(host: str) -> str:
    return "127.0.0.1" if host in {"0.0.0.0", "::"} else host


def _is_port_free(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.2)
        return s.connect_ex((_connect_host(host), port)) != 0


def _wait_for_port(host: str, port: int, timeout: float = 10.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((_connect_host(host), port), timeout=0.2):
                return True
        except OSError:
            time.sleep(0.15)
    return False


def _agent_port(agent_name: str) -> int:
    url_default = _port_from_url(
        os.getenv(AGENT_URL_ENV[agent_name]),
        DEFAULT_AGENT_PORTS[agent_name],
    )
    return _env_int(AGENT_PORT_ENV[agent_name], url_default)


def _configure_agent_urls(host: str, ports: dict[str, int]) -> None:
    for agent_name, port in ports.items():
        if os.getenv(AGENT_PORT_ENV[agent_name]) or not os.getenv(AGENT_URL_ENV[agent_name]):
            os.environ[AGENT_URL_ENV[agent_name]] = _service_url(host, port)


def _configure_default_cors(frontend_url: str) -> None:
    frontend_port = urlparse(frontend_url).port
    origins = [frontend_url, f"http://localhost:{frontend_port}"]
    os.environ.setdefault("DOXA_CORS_ORIGINS", ",".join(dict.fromkeys(origins)))


def main() -> None:
    load_dotenv()
    init_db()

    host = os.getenv("DOXA_BIND_HOST", DEFAULT_BIND_HOST)
    agent_ports = {agent_name: _agent_port(agent_name) for agent_name in DEFAULT_AGENT_PORTS}
    frontend_port = _env_int("DOXA_FRONTEND_PORT", 8080)
    frontend_url = _service_url(host, frontend_port)
    _configure_agent_urls(host, agent_ports)
    _configure_default_cors(frontend_url)

    configs = [
        ("HostAgent", "agents.host_agent.server:app", agent_ports["HostAgent"]),
        ("InvoiceAgent", "agents.invoice_agent.server:app", agent_ports["InvoiceAgent"]),
        ("PurchaseOrderAgent", "agents.purchase_order_agent.server:app", agent_ports["PurchaseOrderAgent"]),
        ("DeliveryOrderAgent", "agents.delivery_order_agent.server:app", agent_ports["DeliveryOrderAgent"]),
        ("Frontend", "frontend_app:app", frontend_port),
    ]

    blocked = [
        (label, port)
        for label, _, port in configs
        if not _is_port_free(host, port)
    ]
    if blocked:
        for label, port in blocked:
            print(f"✗ Port {port} ({label}) is already in use — stop the previous run first.")
        return

    processes = [
        mp.Process(target=_serve, args=(app_str, host, port), daemon=True)
        for _, app_str, port in configs
    ]

    for proc in processes:
        proc.start()

    frontend_ready = False
    for proc, (label, _, port) in zip(processes, configs):
        ok = _wait_for_port(host, port)
        alive = proc.is_alive()
        if ok and alive:
            print(f"✓ {label} listening on {_service_url(host, port)}")
            if label == "Frontend":
                frontend_ready = True
        elif ok and not alive:
            print(f"✗ {label}: process exited unexpectedly")
        else:
            print(f"⚠  {label}: did not respond on port {port}")

    print("✓ PostgreSQL task store initialised")
    if frontend_ready:
        print(f"✓ Frontend available at {frontend_url}/")
        if os.getenv("DOXA_OPEN_FRONTEND", "1").lower() not in {"0", "false", "no"}:
            webbrowser.open(f"{frontend_url}/")

    from cli.chat import run_cli
    try:
        run_cli()
    finally:
        for proc in processes:
            proc.terminate()


if __name__ == "__main__":
    main()
