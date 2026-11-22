"""Prompt builders and small text helpers. Pure functions, no I/O."""
from __future__ import annotations

import re

DIALECTS = ["MySQL", "PostgreSQL", "SQLite"]
MAX_CHAT_MESSAGES = 8

CHAT_SYSTEM = """You are SQL Buddy, a concise SQL assistant.
Dialect: {database}
Known tables:
{schema}

Rules:
- Answer in at most 80 words unless the user asks for more detail.
- Lead with the answer. Put any query in a single ```sql block, then one or two short sentences of explanation.
- Ask at most one clarifying question, and only if you truly cannot answer without it.
- If the question is not about SQL or databases, say so in one sentence and offer to help with SQL.
- Never invent tables or columns that are not listed; state what you assumed.
- Never claim to have run a query."""

_SQL_BLOCK = re.compile(r"```sql\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)


def generate_prompt(question: str, schema: str, database: str) -> str:
    return f"""You are an expert {database} developer and teacher.

User question:
{question.strip()}

Database structure:
{schema.strip() if schema and schema.strip() else "Not provided"}

Reply in this format:
1. The query in one ```sql block (valid {database} syntax).
2. A short line-by-line explanation.
3. A small example of the expected output.
4. Assumptions (only if the structure is missing).

Use simple English. Do not execute the query."""


def fix_prompt(wrong_query: str, error: str, database: str) -> str:
    return f"""You are an expert {database} developer.

Incorrect SQL query:
{wrong_query.strip()}

Error message:
{error.strip() if error and error.strip() else "No error message provided"}

Reply in this format:
1. The mistake, in one sentence.
2. The corrected query in one ```sql block.
3. A short explanation in simple English.

Do not execute the query."""


def learn_prompt(topic: str, database: str) -> str:
    return f"""You are a friendly SQL teacher. The learner uses {database}.

Teach me about the SQL topic: {topic}

Explain:
1. What it is
2. Why it is used
3. Simple syntax
4. Easy examples (in ```sql blocks)
5. Common mistakes

Use simple English."""


def trim_history(history: list[dict], max_messages: int = MAX_CHAT_MESSAGES) -> list[dict]:
    """Keep only the latest messages (controls cost) and start on a user turn."""
    trimmed = list(history[-max_messages:])
    while trimmed and trimmed[0]["role"] != "user":
        trimmed.pop(0)
    return trimmed


def chat_messages(history: list[dict], database: str, schema: str) -> list[dict]:
    system = CHAT_SYSTEM.format(database=database, schema=schema.strip() or "None provided")
    return [{"role": "system", "content": system}, *trim_history(history)]


def extract_sql(text: str) -> str | None:
    """Return the first ```sql block from an AI answer, or None."""
    match = _SQL_BLOCK.search(text or "")
    return match.group(1).strip() if match else None


def explain_prompt(sql: str, database: str) -> str:
    return f"""Explain this SQL query for a beginner. The database is {database}.

{sql.strip()}

Reply with: one sentence on what it returns, then a short step-by-step walk through each clause.
Use simple English."""


def optimize_prompt(sql: str, database: str) -> str:
    return f"""Optimize this SQL query for {database}.

{sql.strip()}

Reply with: the improved query in one ```sql block, then at most 4 short bullet points on what changed and why.
If it is already good, say so and explain why."""


def convert_prompt(sql: str, source: str, target: str) -> str:
    return f"""Convert this SQL query from {source} to {target}.

{sql.strip()}

Reply with: the converted query in one ```sql block, then a short list of syntax differences you changed."""


def practice_feedback_prompt(question: str, attempt: str, problem: str, database: str) -> str:
    return f"""A student is practising {database}. Give a short hint about their mistake without giving the full answer.

Question: {question}

The student's attempt:
{attempt.strip()}

What the checker found: {problem}

Reply in at most 3 sentences."""
