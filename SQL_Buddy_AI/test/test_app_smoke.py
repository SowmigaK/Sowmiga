"""End-to-end UI tests with Streamlit's AppTest, in demo mode (no network, no API key)."""
from pathlib import Path

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

from sqlbuddy.practice import CHALLENGES  # noqa: E402

APP = str(Path(__file__).resolve().parent.parent / "app.py")


@pytest.fixture
def at(monkeypatch):
    monkeypatch.setenv("SQLBUDDY_DEMO", "1")
    app = AppTest.from_file(APP, default_timeout=30)
    app.run()
    return app


def _button(app, text):
    return next(b for b in app.button if text in b.label)


def test_app_loads_without_errors(at):
    assert not at.exception
    assert len(at.tabs) == 5


def test_generate_flow(at):
    at.text_area(key="generate_question").set_value("employees with salary above 30000")
    _button(at, "Generate SQL").click()
    at.run()
    assert not at.exception
    assert any("SELECT" in m.value for m in at.markdown)


def test_empty_question_warns(at):
    _button(at, "Generate SQL").click()
    at.run()
    assert any("Type a question" in w.value for w in at.warning)


def test_sample_data_runs_example_query(at):
    _button(at, "Run query").click()
    at.run()
    assert not at.exception and not at.error
    assert len(at.dataframe) >= 1


def test_practice_correct_and_wrong_answers(at):
    first = CHALLENGES[0]
    at.text_area(key=f"answer_{first.id}").set_value("SELECT employee_name FROM employees")
    _button(at, "Check answer").click()
    at.run()
    assert any("column" in e.value for e in at.error)
    at.text_area(key=f"answer_{first.id}").set_value(first.solution)
    _button(at, "Check answer").click()
    at.run()
    assert any("Correct" in s.value for s in at.success)


def test_floating_chat_round_trip(at):
    at.text_input(key="chat_text").set_value("how does a join work?")
    _button(at, "Send").click()
    at.run()
    assert not at.exception
    assert len(at.chat_message) == 2
