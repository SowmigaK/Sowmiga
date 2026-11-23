import pytest

from sqlbuddy.sandbox import DEFAULT_QUERY, Sandbox, SandboxError, is_read_only
from sqlbuddy.schema_viz import schema_to_dot


@pytest.fixture
def sb():
    return Sandbox()


@pytest.mark.parametrize("sql", [
    "SELECT 1", "select * from employees;", "  WITH x AS (SELECT 1) SELECT * FROM x",
    "-- note\nSELECT 1", "/* hi */ SELECT 1",
])
def test_is_read_only_accepts_selects(sql):
    assert is_read_only(sql)


@pytest.mark.parametrize("sql", [
    "", "DELETE FROM employees", "DROP TABLE employees", "SELECT 1; DROP TABLE employees",
    "UPDATE employees SET salary = 0", "PRAGMA query_only = OFF", "ATTACH DATABASE 'x.db' AS x",
])
def test_is_read_only_rejects_everything_else(sql):
    assert not is_read_only(sql)


def test_run_default_query(sb):
    columns, rows = sb.run(DEFAULT_QUERY)
    assert columns == ["department_name", "avg_salary"]
    assert len(rows) == 3


def test_run_rejects_write(sb):
    with pytest.raises(SandboxError):
        sb.run("DELETE FROM employees")
    assert sb.run("SELECT COUNT(*) FROM employees")[1] == [(6,)]


def test_run_reports_sql_errors_as_sandbox_error(sb):
    with pytest.raises(SandboxError, match="SQL error"):
        sb.run("SELECT missing_column FROM employees")


def test_max_rows_is_enforced(sb):
    _, rows = sb.run("SELECT * FROM employees", max_rows=2)
    assert len(rows) == 2


def test_runaway_query_is_stopped():
    sb = Sandbox(timeout=0.2)
    with pytest.raises(SandboxError):
        sb.run("WITH RECURSIVE c(x) AS (SELECT 1 UNION ALL SELECT x + 1 FROM c) SELECT COUNT(*) FROM c")


def test_load_blocks_attach():
    with pytest.raises(SandboxError):
        Sandbox("ATTACH DATABASE '/tmp/evil.db' AS evil;")


def test_failed_load_keeps_old_tables(sb):
    with pytest.raises(SandboxError):
        sb.load("CREATE TABLE broken (")
    assert "employees" in sb.tables()


def test_load_replaces_tables(sb):
    sb.load("CREATE TABLE pets (id INTEGER PRIMARY KEY, name TEXT); INSERT INTO pets VALUES (1, 'Mochi');")
    assert list(sb.tables()) == ["pets"]
    assert sb.run("SELECT name FROM pets")[1] == [("Mochi",)]


def test_describe_and_foreign_keys(sb):
    text = sb.describe()
    assert "Table: employees" in text and "salary INTEGER" in text
    assert ("employees", "dept_id", "departments", "dept_id") in sb.foreign_keys()


def test_schema_to_dot_contains_tables_and_edges(sb):
    dot = schema_to_dot(sb.tables(), sb.foreign_keys())
    assert dot.startswith("digraph") and dot.rstrip().endswith("}")
    assert '"employees"' in dot and '"departments"' in dot and "->" in dot


def test_schema_to_dot_escapes_html():
    dot = schema_to_dot({"t": [("a<b", "TEXT", False)]}, [])
    assert "a&lt;b" in dot


from sqlbuddy.datasets import PRESETS  # noqa: E402
from sqlbuddy.sandbox import sanitize_identifier  # noqa: E402


@pytest.mark.parametrize("raw, expected", [
    ("My File.csv", "My_File_csv"), ("2024 sales", "_2024_sales"), ("", "col"), ("a-b", "a_b"),
])
def test_sanitize_identifier(raw, expected):
    assert sanitize_identifier(raw) == expected


def test_add_table_from_upload(sb):
    name = sb.add_table("my data", [("id", "INTEGER"), ("city name", "TEXT")], [(1, "Chennai"), (2, None)])
    assert name == "my_data"
    assert sb.run("SELECT city_name FROM my_data WHERE id = 1")[1] == [("Chennai",)]
    with pytest.raises(SandboxError):
        sb.run("DELETE FROM my_data")


def test_add_table_failure_leaves_no_table(sb):
    with pytest.raises(SandboxError):
        sb.add_table("bad", [("a", "INTEGER"), ("a", "TEXT")], [(1, "x")])
    with pytest.raises(SandboxError):
        sb.add_table("employees", [("a", "INTEGER")], [(1,)])
    assert "bad" not in sb.tables()


def test_every_preset_loads_and_its_examples_run():
    for name, dataset in PRESETS.items():
        sb = Sandbox(dataset.setup)
        assert sb.tables(), name
        for label, sql in dataset.examples:
            columns, rows = sb.run(sql)
            assert columns and rows, f"{name}: {label}"
