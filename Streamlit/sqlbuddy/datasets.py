"""Ready-made sample databases for the 'Try it on sample data' tab."""
from __future__ import annotations

from dataclasses import dataclass

from sqlbuddy.sandbox import DEFAULT_SETUP_SQL

SHOP_SETUP_SQL = """CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    city TEXT
);
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    order_date TEXT,
    amount REAL,
    status TEXT
);
INSERT INTO customers VALUES (1, 'Priya', 'Chennai'), (2, 'Vikram', 'Mumbai'), (3, 'Anita', 'Chennai'), (4, 'Rahul', 'Delhi');
INSERT INTO orders VALUES
    (101, 1, '2026-01-05', 1200.50, 'delivered'), (102, 1, '2026-02-11', 560.00, 'delivered'),
    (103, 2, '2026-02-14', 899.99, 'cancelled'), (104, 3, '2026-03-02', 2300.00, 'delivered'),
    (105, 3, '2026-03-19', 150.25, 'pending'),  (106, 4, '2026-04-01', 720.00, 'delivered'),
    (107, 2, '2026-04-09', 430.00, 'delivered');
"""


@dataclass(frozen=True)
class Dataset:
    setup: str
    examples: list  # [(label, sql)]


PRESETS = {
    "Employees (sample)": Dataset(DEFAULT_SETUP_SQL, [
        ("Average salary per department",
         "SELECT d.department_name, ROUND(AVG(e.salary)) AS avg_salary\n"
         "FROM employees e JOIN departments d ON d.dept_id = e.dept_id\n"
         "GROUP BY d.department_name;"),
        ("Who earns more than 40000?",
         "SELECT employee_name, salary FROM employees WHERE salary > 40000 ORDER BY salary DESC;"),
        ("Headcount per department",
         "SELECT d.department_name, COUNT(*) AS people\n"
         "FROM employees e JOIN departments d ON d.dept_id = e.dept_id\n"
         "GROUP BY d.department_name;"),
    ]),
    "Online shop (sample)": Dataset(SHOP_SETUP_SQL, [
        ("Total spent per customer (delivered only)",
         "SELECT c.customer_name, SUM(o.amount) AS total_spent\n"
         "FROM customers c JOIN orders o ON o.customer_id = c.customer_id\n"
         "WHERE o.status = 'delivered'\nGROUP BY c.customer_name\nORDER BY total_spent DESC;"),
        ("Orders per status",
         "SELECT status, COUNT(*) AS orders FROM orders GROUP BY status;"),
        ("Revenue per month",
         "SELECT substr(order_date, 1, 7) AS month, SUM(amount) AS revenue\n"
         "FROM orders WHERE status = 'delivered' GROUP BY month ORDER BY month;"),
    ]),
}

DEFAULT_DATASET = "Employees (sample)"
UPLOAD_MODE = "Upload a CSV"
OWN_MODE = "Write my own tables"
CUSTOM_MODES = [UPLOAD_MODE, OWN_MODE]
