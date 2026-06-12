from __future__ import annotations

import pytest

from tools import sql_query


def test_validate_sql_allows_single_select_and_strips_trailing_semicolon() -> None:
    assert sql_query.validate_sql(" SELECT * FROM public.invoice; ") == "SELECT * FROM public.invoice"


@pytest.mark.parametrize(
    "statement",
    [
        "UPDATE public.invoice SET total_amount = 0",
        "SELECT * FROM public.invoice; DROP TABLE public.invoice",
        "DELETE FROM public.invoice",
    ],
)
def test_validate_sql_rejects_dangerous_or_multi_statement_sql(statement: str) -> None:
    with pytest.raises(ValueError):
        sql_query.validate_sql(statement)


def test_count_sql_removes_top_level_order_by_and_limit() -> None:
    count_sql = sql_query._count_sql_for(
        "SELECT invoice_no, total_amount FROM public.invoice "
        "ORDER BY total_amount DESC NULLS LAST LIMIT 5"
    )

    assert count_sql == (
        "SELECT COUNT(*) AS total FROM "
        "(SELECT invoice_no, total_amount FROM public.invoice) AS _count_subq"
    )


def test_count_sql_keeps_nested_order_by_inside_subquery() -> None:
    count_sql = sql_query._count_sql_for(
        "SELECT * FROM (SELECT * FROM public.invoice ORDER BY id DESC) ranked "
        "ORDER BY total_amount DESC LIMIT 5"
    )

    assert "SELECT * FROM public.invoice ORDER BY id DESC" in count_sql
    assert count_sql.endswith(") ranked) AS _count_subq")


def test_execute_safe_sql_sets_timeouts_and_adds_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    executed: list[tuple[str, object | None]] = []
    connections: list[FakeConnection] = []

    def fake_connect(**params: object) -> "FakeConnection":
        conn = FakeConnection()
        conn.params = params
        connections.append(conn)
        return conn

    monkeypatch.setattr(sql_query.psycopg2, "connect", fake_connect)
    monkeypatch.setenv("SQL_CONNECT_TIMEOUT_SECONDS", "7")
    monkeypatch.setenv("SQL_STATEMENT_TIMEOUT_MS", "1234")

    FakeCursor.executed = executed
    result = sql_query.execute_safe_sql("SELECT invoice_no FROM public.invoice")

    assert connections[0].params["connect_timeout"] == 7
    assert connections[0].readonly is True
    assert connections[0].autocommit is True
    assert executed[0] == ("SET statement_timeout = %s", (1234,))
    assert executed[1][0].startswith("SELECT COUNT(*) AS total FROM")
    assert executed[2] == ("SELECT invoice_no FROM public.invoice LIMIT 200", None)
    assert result == {
        "columns": ["invoice_no"],
        "rows": [{"invoice_no": "INV-1"}],
        "count": 1,
        "total_count": 1,
    }


class FakeConnection:
    params: dict[str, object]

    def __init__(self) -> None:
        self.readonly = False
        self.autocommit = False

    def set_session(self, *, readonly: bool, autocommit: bool) -> None:
        self.readonly = readonly
        self.autocommit = autocommit

    def cursor(self, cursor_factory: object | None = None) -> "FakeCursor":
        return FakeCursor()

    def close(self) -> None:
        pass


class FakeCursor:
    executed: list[tuple[str, object | None]] = []

    def __init__(self) -> None:
        self.description = [("invoice_no",)]
        self._last_sql = ""

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        return None

    def execute(self, sql: str, params: object | None = None) -> None:
        self._last_sql = sql
        self.executed.append((sql, params))

    def fetchone(self) -> dict[str, int]:
        return {"total": 1}

    def fetchall(self) -> list[dict[str, str]]:
        return [{"invoice_no": "INV-1"}]
