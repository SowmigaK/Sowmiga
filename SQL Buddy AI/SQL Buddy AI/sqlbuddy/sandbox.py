"""Read-only in-memory SQLite sandbox so users can safely run generated SQL."""
from __future__ import annotations

import re
import sqlite3
import time

DEFAULT_SETUP_SQL = """CREATE TABLE departments (
    dept_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL
);
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    employee_name TEXT NOT NULL,
    salary INTEGER,
    dept_id INTEGER REFERENCES departments(dept_id)
);
INSERT INTO departments VALUES (1, 'Engineering'), (2, 'Sales'), (3, 'HR');
INSERT INTO employees VALUES
    (1, 'Asha', 52000, 1), (2, 'Ravi', 48000, 1), (3, 'Meena', 31000, 2),
    (4, 'Karthik', 29000, 2), (5, 'Divya', 35000, 3), (6, 'Arun', 61000, 1);
"""

DEFAULT_QUERY = (
    "SELECT d.department_name, ROUND(AVG(e.salary)) AS avg_salary\n"
    "FROM employees e JOIN departments d ON d.dept_id = e.dept_id\n"
    "GROUP BY d.department_name;"
)

_COMMENT = re.compile(r"--[^\n]*|/\*.*?\*/", re.DOTALL)


class SandboxError(Exception):
    """A user-facing, safe-to-display error."""


def is_read_only(sql: str) -> bool:
    """True only for a single SELECT / WITH statement (semicolons in string literals are rejected)."""
    cleaned = _COMMENT.sub(" ", sql or "").strip().rstrip(";").strip()
    if not cleaned or ";" in cleaned:
        return False
    return cleaned.split(None, 1)[0].lower() in {"select", "with"}


def _deny_attach(action, *_args):
    if action in (sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH):
        return sqlite3.SQLITE_DENY  # no access to files on the server
    return sqlite3.SQLITE_OK


def sanitize_identifier(name, fallback: str = "col") -> str:
    """Make a safe table/column name from a file name or CSV header."""
    cleaned = re.sub(r"\W+", "_", str(name).strip(), flags=re.ASCII).strip("_") or fallback
    return "_" + cleaned if cleaned[0].isdigit() else cleaned


def _quote(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


class Sandbox:
    def __init__(self, setup_sql: str = DEFAULT_SETUP_SQL, timeout: float = 2.0):
        self.timeout = timeout
        self._conn: sqlite3.Connection | None = None
        self.load(setup_sql)

    def _arm_timeout(self, conn: sqlite3.Connection) -> None:
        deadline = time.monotonic() + self.timeout
        conn.set_progress_handler(lambda: 1 if time.monotonic() > deadline else 0, 10_000)

    def load(self, setup_sql: str) -> None:
        """Replace the database with the one defined by setup_sql. Keeps the old one on failure."""
        conn = sqlite3.connect(":memory:", check_same_thread=False)
        conn.set_authorizer(_deny_attach)
        self._arm_timeout(conn)
        try:
            conn.executescript(setup_sql)
            conn.execute("PRAGMA query_only = ON")
        except sqlite3.Error as exc:
            conn.close()
            raise SandboxError(f"Could not load the tables: {exc}") from exc
        if self._conn is not None:
            self._conn.close()
        self._conn = conn

    def run(self, sql: str, max_rows: int = 500) -> tuple[list[str], list[tuple]]:
        if not is_read_only(sql):
            raise SandboxError("The playground runs one SELECT query at a time.")
        self._arm_timeout(self._conn)
        try:
            cur = self._conn.execute(sql.strip())
            columns = [d[0] for d in cur.description or []]
            rows = cur.fetchmany(max_rows)
        except sqlite3.Error as exc:
            raise SandboxError(f"SQL error: {exc}") from exc
        return columns, rows

    def add_table(self, name: str, columns: list[tuple[str, str]], rows: list[tuple]) -> str:
        """Create a table from uploaded data. columns = [(name, 'INTEGER'|'REAL'|'TEXT')]. Returns the table name."""
        if not columns:
            raise SandboxError("The file has no columns.")
        table = sanitize_identifier(name, "data")
        col_defs = ", ".join(f"{_quote(sanitize_identifier(c))} {t}" for c, t in columns)
        marks = ", ".join("?" for _ in columns)
        try:
            self._conn.execute("PRAGMA query_only = OFF")
            self._conn.execute(f"CREATE TABLE {_quote(table)} ({col_defs})")
            try:
                self._conn.executemany(f"INSERT INTO {_quote(table)} VALUES ({marks})", rows)
                self._conn.commit()
            except sqlite3.Error:
                self._conn.rollback()
                self._conn.execute(f"DROP TABLE IF EXISTS {_quote(table)}")
                raise
        except sqlite3.Error as exc:
            raise SandboxError(f"Could not add the table: {exc}") from exc
        finally:
            self._conn.execute("PRAGMA query_only = ON")
        return table

    def tables(self) -> dict[str, list[tuple[str, str, bool]]]:
        """{table: [(column, type, is_primary_key), ...]}"""
        names = [r[0] for r in self._conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
        return {
            n: [(c[1], c[2], bool(c[5])) for c in self._conn.execute(f"PRAGMA table_info({_quote(n)})")]
            for n in names
        }

    def foreign_keys(self) -> list[tuple[str, str, str, str]]:
        """[(from_table, from_column, to_table, to_column), ...]"""
        fks = []
        for table in self.tables():
            for row in self._conn.execute(f"PRAGMA foreign_key_list({_quote(table)})"):
                fks.append((table, row[3], row[2], row[4] or ""))
        return fks

    def describe(self) -> str:
        """Plain-text schema, ready to drop into a prompt."""
        parts = []
        for table, cols in self.tables().items():
            col_text = ", ".join(
                f"{name} {ctype}".strip() + (" PRIMARY KEY" if pk else "") for name, ctype, pk in cols
            )
            parts.append(f"Table: {table}\nColumns: {col_text}")
        return "\n\n".join(parts)
