from sqlbuddy import prompts


def test_generate_prompt_includes_inputs():
    p = prompts.generate_prompt("top 3 salaries", "Table: employees", "PostgreSQL")
    assert "PostgreSQL" in p and "top 3 salaries" in p and "Table: employees" in p


def test_generate_prompt_marks_missing_schema():
    assert "Not provided" in prompts.generate_prompt("q", "   ", "MySQL")


def test_fix_prompt_handles_missing_error():
    assert "No error message provided" in prompts.fix_prompt("SELECT", "", "SQLite")


def test_extract_sql_returns_first_sql_block():
    text = "Here:\n```sql\nSELECT 1;\n```\nand\n```sql\nSELECT 2;\n```"
    assert prompts.extract_sql(text) == "SELECT 1;"


def test_extract_sql_ignores_other_blocks_and_empty():
    assert prompts.extract_sql("```text\nhello\n```") is None
    assert prompts.extract_sql("") is None


def test_trim_history_limits_size_and_starts_with_user():
    history = [{"role": "user" if i % 2 == 0 else "assistant", "content": str(i)} for i in range(20)]
    trimmed = prompts.trim_history(history, max_messages=5)
    assert len(trimmed) <= 5
    assert trimmed[0]["role"] == "user"
    assert trimmed[-1]["content"] == "19"


def test_chat_messages_starts_with_system_prompt_containing_schema():
    msgs = prompts.chat_messages([{"role": "user", "content": "hi"}], "SQLite", "Table: t")
    assert msgs[0]["role"] == "system"
    assert "Table: t" in msgs[0]["content"] and "SQLite" in msgs[0]["content"]
    assert msgs[-1] == {"role": "user", "content": "hi"}
