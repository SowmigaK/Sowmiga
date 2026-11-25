"""LLM clients: a real Groq client and a deterministic mock for demos and tests."""
from __future__ import annotations

from typing import Protocol

DEFAULT_MODEL = "openai/gpt-oss-120b"
_ROLES = {"system": "system", "user": "human", "assistant": "ai"}


class LLM(Protocol):
    is_demo: bool

    def ask(self, prompt: str) -> str: ...
    def chat(self, messages: list[dict]) -> str: ...


def _text(response) -> str:
    content = getattr(response, "content", response)
    return content if isinstance(content, str) else str(content)


class GroqLLM:
    is_demo = False

    def __init__(self, api_key: str | None = None, model: str = DEFAULT_MODEL,
                 temperature: float = 0.2, client=None):
        if client is None:  # lazy import keeps tests free of network packages
            from langchain_groq import ChatGroq
            client = ChatGroq(groq_api_key=api_key, model=model, temperature=temperature,
                              timeout=30, max_retries=2)
        self._client = client

    def ask(self, prompt: str) -> str:
        return _text(self._client.invoke(prompt))

    def chat(self, messages: list[dict]) -> str:
        return _text(self._client.invoke([(_ROLES[m["role"]], m["content"]) for m in messages]))


class MockLLM:
    """Canned answers. Used when no API key is set (demo mode) and in tests."""

    is_demo = True

    def __init__(self):
        self.calls: list[str] = []

    def ask(self, prompt: str) -> str:
        self.calls.append(prompt)
        return self._reply(prompt)

    def chat(self, messages: list[dict]) -> str:
        last_user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        self.calls.append(last_user)
        return self._reply(last_user)

    @staticmethod
    def _reply(text: str) -> str:
        t = text.lower()
        if "explain this sql query" in t:
            return ("**Demo answer.** This query reads rows from a table and filters or groups them.\n\n"
                    "1. `FROM` picks the table.\n2. `WHERE` keeps matching rows.\n3. `SELECT` chooses the columns.")
        if "optimize this sql query" in t:
            return ("**Demo answer.**\n\n```sql\nSELECT employee_name, salary FROM employees WHERE salary > 30000;\n```\n"
                    "- Select only the columns you need instead of `*`.")
        if "convert this sql query" in t:
            return ("**Demo answer.**\n\n```sql\nSELECT employee_name FROM employees LIMIT 5;\n```\n"
                    "- `TOP 5` becomes `LIMIT 5`.")
        if "student's attempt" in t:
            return "**Demo hint.** Re-read the question and compare the columns and rows you return with what it asks for."
        if "incorrect sql query" in t:
            return ("**Demo answer.** The `WHERE` clause has no value after `>`.\n\n"
                    "```sql\nSELECT employee_name FROM employees WHERE salary > 30000;\n```\n"
                    "A comparison needs a value on both sides.")
        if "teach me about" in t:
            return ("**Demo answer.** `SELECT` reads columns from a table.\n\n"
                    "```sql\nSELECT employee_name, salary FROM employees;\n```")
        if "join" in t:
            return ("**Demo answer.** A `JOIN` combines rows from two tables on a shared key.\n\n"
                    "```sql\nSELECT e.employee_name, d.department_name\n"
                    "FROM employees e JOIN departments d ON d.dept_id = e.dept_id;\n```")
        if "salary" in t or "employee" in t:
            return ("**Demo answer.**\n\n```sql\nSELECT employee_name, salary\n"
                    "FROM employees\nWHERE salary > 30000\nORDER BY salary DESC;\n```\n"
                    "Filters employees by salary and sorts the highest first.")
        return ("**Demo answer.** Add a `GROQ_API_KEY` to get live answers.\n\n"
                "```sql\nSELECT * FROM employees LIMIT 5;\n```")


def build_llm(api_key: str | None, model: str = DEFAULT_MODEL, demo: bool = False) -> LLM:
    if demo or not api_key:
        return MockLLM()
    return GroqLLM(api_key=api_key, model=model)
