import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scheduler import generate_schedule


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


def test_zero_hours():
    result = generate_schedule(
        total_hours=0,
        subjects=["A"],
        priorities={"A": "high"},
        days=1,
        hours_per_day=1
    )

    assert result["study_plan"]["A"] == 0


def test_daywise_plan_exists():
    result = generate_schedule(
        total_hours=4,
        subjects=["A", "B"],
        priorities={"A": "high", "B": "low"},
        days=2,
        hours_per_day=2
    )

    assert result["day_wise_plan"] is not None


def test_time_slots_structure():
    result = generate_schedule(
        total_hours=3,
        subjects=["A"],
        priorities={"A": "high"},
        days=1,
        hours_per_day=3
    )

    assert len(result["time_slots"]) > 0

    slot = result["time_slots"][0]

    assert "start" in slot
    assert "end" in slot
    assert "subject" in slot