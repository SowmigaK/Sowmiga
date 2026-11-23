"""Practice challenges. An answer is correct when its RESULT matches, not its exact wording."""
from __future__ import annotations

from dataclasses import dataclass

from sqlbuddy.sandbox import Sandbox, SandboxError

LEVELS = ["Beginner", "Intermediate", "Advanced"]


@dataclass(frozen=True)
class Challenge:
    id: str
    level: str
    title: str
    concept: str
    question: str
    hint: str
    solution: str
    ordered: bool = False  # True when the row order is part of the question


@dataclass
class CheckResult:
    correct: bool
    message: str
    columns: list
    rows: list


CHALLENGES = [
    Challenge("b1", "Beginner", "All employees", "SELECT",
              "Show every column for every employee.",
              "Use * to pick all columns.",
              "SELECT * FROM employees"),
    Challenge("b2", "Beginner", "High earners", "WHERE",
              "List the names of employees who earn more than 50000.",
              "Filter rows with WHERE salary > ...",
              "SELECT employee_name FROM employees WHERE salary > 50000"),
    Challenge("b3", "Beginner", "Top earner", "ORDER BY, LIMIT",
              "Show the name and salary of the highest-paid employee.",
              "Sort by salary from high to low, then keep one row.",
              "SELECT employee_name, salary FROM employees ORDER BY salary DESC LIMIT 1"),
    Challenge("b4", "Beginner", "Salary ranking", "ORDER BY",
              "List employee names from the highest salary to the lowest.",
              "ORDER BY salary DESC. Order matters here.",
              "SELECT employee_name FROM employees ORDER BY salary DESC", ordered=True),
    Challenge("i1", "Intermediate", "Headcount", "GROUP BY",
              "For each dept_id, show the dept_id and how many employees it has.",
              "COUNT(*) together with GROUP BY dept_id.",
              "SELECT dept_id, COUNT(*) FROM employees GROUP BY dept_id"),
    Challenge("i2", "Intermediate", "Average pay", "Aggregates",
              "What is the average salary of all employees? Return one number.",
              "AVG(salary). Rounding to 2 decimals is fine.",
              "SELECT ROUND(AVG(salary), 2) FROM employees"),
    Challenge("i3", "Intermediate", "Names with departments", "JOIN",
              "Show each employee's name next to their department name.",
              "Join employees to departments on dept_id.",
              "SELECT e.employee_name, d.department_name FROM employees e "
              "JOIN departments d ON d.dept_id = e.dept_id"),
    Challenge("a1", "Advanced", "Payroll by department", "JOIN + GROUP BY",
              "Show each department name with the total salary of its employees.",
              "Join first, then SUM(salary) grouped by the department name.",
              "SELECT d.department_name, SUM(e.salary) FROM employees e "
              "JOIN departments d ON d.dept_id = e.dept_id GROUP BY d.department_name"),
    Challenge("a2", "Advanced", "Big departments", "HAVING",
              "Which departments have more than 2 employees? Show only the department name.",
              "Filter groups, not rows: use HAVING COUNT(*) > 2.",
              "SELECT d.department_name FROM employees e "
              "JOIN departments d ON d.dept_id = e.dept_id "
              "GROUP BY d.department_name HAVING COUNT(*) > 2"),
    Challenge("a3", "Advanced", "Above average", "Subquery",
              "List the names of employees who earn more than the company average.",
              "Put SELECT AVG(salary) FROM employees inside parentheses in your WHERE.",
              "SELECT employee_name FROM employees WHERE salary > (SELECT AVG(salary) FROM employees)"),
]


def _number_or_value(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return round(float(value), 2)
    return value


def _normalize(rows):
    return [tuple(_number_or_value(v) for v in row) for row in rows]


def check_answer(sandbox: Sandbox, challenge: Challenge, user_sql: str) -> CheckResult:
    try:
        columns, rows = sandbox.run(user_sql)
    except SandboxError as exc:
        return CheckResult(False, str(exc), [], [])
    _, expected_rows = sandbox.run(challenge.solution)
    got, want = _normalize(rows), _normalize(expected_rows)

    if got and want and len(got[0]) != len(want[0]):
        message = f"Your result has {len(got[0])} column(s) but the question needs {len(want[0])}."
    elif len(got) != len(want):
        message = f"Your result has {len(got)} row(s) but the correct one has {len(want)}."
    else:
        same = got == want if challenge.ordered else sorted(got, key=str) == sorted(want, key=str)
        if same:
            return CheckResult(True, "Correct! Your query returns the right result.", columns, rows)
        message = ("The rows are right but in the wrong order." if sorted(got, key=str) == sorted(want, key=str)
                   else "The number of rows is right, but some values are different.")
    return CheckResult(False, message, columns, rows)
