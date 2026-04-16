from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

# 🔧 Logging setup
logging.basicConfig(level=logging.INFO)

# 🔧 Constants
STUDY_BLOCK = 90
BREAK_BLOCK = 10
MIN_BLOCK = 30


def generate_time_slots(
    schedule: Dict[str, int],
    days: int,
    hours_per_day: Optional[int],
    start_time: str = "09:00"
) -> List[Dict]:
    """
    Generates time slots for study sessions.

    Args:
        schedule (dict): Subject → allocated minutes
        days (int): Number of days
        hours_per_day (int): Daily available hours
        start_time (str): Start time of schedule

    Returns:
        list: List of time slots with subject, start, end, and day
    """

    logging.info("Generating time slots...")

    slots = []
    subjects = list(schedule.keys())
    remaining = schedule.copy()
    total_remaining = sum(remaining.values())

    # 🔥 Continuous Mode
    if days == 0 or hours_per_day is None:
        current = datetime.strptime(start_time, "%H:%M")

        while total_remaining > 0:
            for subject in subjects:
                if remaining[subject] <= 0:
                    continue

                chunk = min(STUDY_BLOCK, remaining[subject])
                chunk = max(chunk, MIN_BLOCK)

                end = current + timedelta(minutes=chunk)

                slots.append({
                    "subject": subject,
                    "start": current.strftime("%H:%M"),
                    "end": end.strftime("%H:%M")
                })

                current = end + timedelta(minutes=BREAK_BLOCK)
                remaining[subject] -= chunk
                total_remaining -= chunk

                if total_remaining <= 0:
                    break

        return slots

    # 🔥 Day-based Mode
    for day in range(1, days + 1):
        current = datetime.strptime(start_time, "%H:%M")
        daily_limit = hours_per_day * 60
        used = 0

        while used < daily_limit and total_remaining > 0:
            for subject in subjects:
                if remaining[subject] <= 0:
                    continue

                chunk = min(STUDY_BLOCK, remaining[subject])

                if used + chunk > daily_limit:
                    chunk = daily_limit - used

                chunk = max(chunk, MIN_BLOCK)

                if chunk <= 0:
                    used = daily_limit
                    break

                end = current + timedelta(minutes=chunk)

                slots.append({
                    "day": f"Day {day}",
                    "subject": subject,
                    "start": current.strftime("%H:%M"),
                    "end": end.strftime("%H:%M")
                })

                current = end + timedelta(minutes=BREAK_BLOCK)
                remaining[subject] -= chunk
                total_remaining -= chunk
                used += chunk + BREAK_BLOCK

                if total_remaining <= 0:
                    break

    return slots


def calculate_score(schedule: Dict[str, int], priorities: Dict[str, str]) -> int:
    """
    Calculates efficiency score based on priority distribution.

    Args:
        schedule (dict): Subject → allocated minutes
        priorities (dict): Subject → priority level

    Returns:
        int: Efficiency score (0–100)
    """

    weight_map = {"high": 3, "medium": 2, "low": 1}

    if len(set(priorities.values())) == 1:
        return 85

    actual = sum(
        schedule[s] * weight_map.get(priorities.get(s, "medium"), 2)
        for s in schedule
    )
    max_score = sum(schedule[s] * 3 for s in schedule)

    return int((actual / max_score) * 100) if max_score else 0


def split_across_days(schedule: Dict[str, int], days: int) -> Optional[Dict]:
    """
    Splits study plan across multiple days.

    Args:
        schedule (dict): Subject → allocated minutes
        days (int): Number of days

    Returns:
        dict or None: Day-wise distribution
    """

    if days == 0:
        return None

    day_plan = {}
    total = sum(schedule.values())
    per_day = max(1, total // days)

    items = list(schedule.items())

    for day in range(1, days + 1):

        if day == 1:
            label = "🧠 Deep Focus"
        elif day == days:
            label = "🔁 Revision Focus"
        else:
            label = "⚖️ Balanced Learning"

        key = f"Day {day} ({label})"
        day_plan[key] = {}

        remaining = per_day

        for i in range(len(items)):
            subject, time = items[i]

            if time <= 0:
                continue

            portion = min(time, remaining)

            day_plan[key][subject] = portion
            items[i] = (subject, time - portion)

            remaining -= portion

            if remaining <= 0:
                break

    return day_plan


def generate_schedule(
    total_hours: float,
    subjects: List[str],
    priorities: Dict[str, str],
    days: int = 0,
    hours_per_day: Optional[int] = None
) -> Dict:
    """
    Main function to generate study schedule.

    Args:
        total_hours (float): Total available study time
        subjects (list): List of subjects
        priorities (dict): Subject → priority
        days (int): Number of days
        hours_per_day (int): Daily hours

    Returns:
        dict: Complete schedule output
    """

    logging.info(f"Generating schedule for subjects: {subjects}")

    # 🔒 Input validation
    if total_hours < 0:
        raise ValueError("Total hours cannot be negative")

    if not subjects:
        raise ValueError("Subjects list cannot be empty")

    if len(subjects) != len(priorities):
        raise ValueError("Subjects and priorities must match")

    total_minutes = int(total_hours * 60)

    weight_map = {"high": 3, "medium": 2, "low": 1}
    priorities = {k.upper(): v for k, v in priorities.items()}

    weights = [
        weight_map.get(priorities.get(s, "medium"), 2)
        for s in subjects
    ]
    total_weight = sum(weights) or 1

    # 📊 Allocation
    schedule = {
        subjects[i]: int((weights[i] / total_weight) * total_minutes)
        for i in range(len(subjects))
    }

    break_time = total_hours * 5

    # 🔁 Revision
    if total_hours >= 4:
        revision = int(0.15 * total_minutes)
    elif total_hours >= 2:
        revision = int(0.10 * total_minutes)
    else:
        revision = int(0.05 * total_minutes)

    return {
        "study_plan": schedule,
        "day_wise_plan": split_across_days(schedule, days),
        "time_slots": generate_time_slots(schedule, days, hours_per_day),
        "score": calculate_score(schedule, priorities),
        "break_time": break_time,
        "revision_time": revision
    }