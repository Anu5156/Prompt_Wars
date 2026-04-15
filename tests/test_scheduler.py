from scheduler import generate_schedule
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_schedule_output():
    result = generate_schedule(
        total_hours=4,
        subjects=["TOC", "DBMS"],
        priorities={"TOC": "high", "DBMS": "low"},
        days=2,
        hours_per_day=2
    )

    assert isinstance(result, dict)
    assert "study_plan" in result
    assert "time_slots" in result
    assert len(result["study_plan"]) == 2


def test_time_distribution():
    result = generate_schedule(
        total_hours=2,
        subjects=["A", "B"],
        priorities={"A": "high", "B": "low"},
        days=1,
        hours_per_day=2
    )

    assert result["study_plan"]["A"] >= result["study_plan"]["B"]