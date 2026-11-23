from types import SimpleNamespace
from unittest.mock import MagicMock

from sqlbuddy import prompts
from sqlbuddy.llm import GroqLLM, MockLLM, build_llm


def test_build_llm_uses_mock_without_key():
    assert isinstance(build_llm(api_key=None), MockLLM)
    assert isinstance(build_llm(api_key="k", demo=True), MockLLM)


def test_mock_generate_answer_contains_runnable_sql():
    llm = MockLLM()
    answer = llm.ask(prompts.generate_prompt("employees with salary above 30000", "", "SQLite"))
    assert prompts.extract_sql(answer).lower().startswith("select")
    assert len(llm.calls) == 1


def test_mock_fix_and_learn_branches():
    llm = MockLLM()
    assert "WHERE salary > 30000" in llm.ask(prompts.fix_prompt("SELECT x WHERE", "", "MySQL"))
    assert "SELECT" in llm.ask(prompts.learn_prompt("SELECT", "MySQL"))


def test_mock_chat_answers_last_user_message():
    llm = MockLLM()
    msgs = prompts.chat_messages([{"role": "user", "content": "explain a join"}], "SQLite", "")
    assert "JOIN" in llm.chat(msgs)


def test_groq_llm_ask_passes_prompt_and_returns_text():
    client = MagicMock()
    client.invoke.return_value = SimpleNamespace(content="SELECT 1;")
    assert GroqLLM(client=client).ask("hello") == "SELECT 1;"
    client.invoke.assert_called_once_with("hello")


def test_groq_llm_chat_maps_roles():
    client = MagicMock()
    client.invoke.return_value = SimpleNamespace(content="ok")
    msgs = [{"role": "system", "content": "s"}, {"role": "user", "content": "u"},
            {"role": "assistant", "content": "a"}]
    assert GroqLLM(client=client).chat(msgs) == "ok"
    client.invoke.assert_called_once_with([("system", "s"), ("human", "u"), ("ai", "a")])


def test_mock_new_modes_return_distinct_answers():
    llm = MockLLM()
    assert "FROM" in llm.ask(prompts.explain_prompt("SELECT 1 FROM t JOIN u", "MySQL"))
    assert prompts.extract_sql(llm.ask(prompts.optimize_prompt("SELECT * FROM t", "MySQL")))
    assert "LIMIT" in llm.ask(prompts.convert_prompt("SELECT TOP 5 x FROM t", "SQLite", "MySQL"))
    assert "hint" in llm.ask(prompts.practice_feedback_prompt("q", "SELECT 1", "wrong", "MySQL")).lower()
