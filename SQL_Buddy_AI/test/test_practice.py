import pytest

from sqlbuddy.practice import CHALLENGES, check_answer
from sqlbuddy.sandbox import Sandbox


@pytest.fixture
def sb():
    return Sandbox()


def _ch(cid):
    return next(c for c in CHALLENGES if c.id == cid)


def test_challenge_ids_are_unique():
    ids = [c.id for c in CHALLENGES]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize("challenge", CHALLENGES)
def test_every_solution_passes_its_own_check(challenge):
    assert check_answer(Sandbox(), challenge, challenge.solution).correct


def test_different_wording_same_result_is_correct(sb):
    assert check_answer(sb, _ch("b2"), "select employee_name from employees where 50000 < salary").correct


def test_wrong_column_count_is_reported(sb):
    result = check_answer(sb, _ch("b2"), "SELECT employee_name, salary FROM employees WHERE salary > 50000")
    assert not result.correct and "column" in result.message


def test_wrong_row_count_is_reported(sb):
    result = check_answer(sb, _ch("b2"), "SELECT employee_name FROM employees")
    assert not result.correct and "row" in result.message


def test_order_matters_only_when_challenge_says_so(sb):
    ascending = "SELECT employee_name FROM employees ORDER BY salary ASC"
    assert not check_answer(sb, _ch("b4"), ascending).correct
    assert check_answer(sb, _ch("b2"), "SELECT employee_name FROM employees WHERE salary > 50000 ORDER BY 1 DESC").correct


def test_average_ignores_rounding_noise_but_not_wrong_values(sb):
    assert check_answer(sb, _ch("i2"), "SELECT AVG(salary) FROM employees").correct
    assert not check_answer(sb, _ch("i2"), "SELECT ROUND(AVG(salary), 0) FROM employees").correct


def test_write_and_broken_queries_are_rejected_safely(sb):
    assert not check_answer(sb, _ch("b1"), "DELETE FROM employees").correct
    assert not check_answer(sb, _ch("b1"), "SELEC * FROM employees").correct
    assert sb.run("SELECT COUNT(*) FROM employees")[1] == [(6,)]
