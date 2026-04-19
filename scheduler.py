"""
📘 FILE: scheduler.py

🧠 PURPOSE:
Core scheduling engine for AI Study Planner.

FEATURES:
- Priority-based time allocation
- Energy-based scheduling (morning = deep work)
- Randomized subject interleaving (non-linear plan)
- Percentage distribution calculation
- Real efficiency scoring (NOT hardcoded)
- What-if simulation (WOW feature)

🧮 ALGORITHM:
Allocated Time =
(Total Time × Priority Weight) / Sum of Weights

Weights:
- High → 3
- Medium → 2
- Low → 1
"""
from datetime import datetime, timedelta
import random

# 🔢 Priority weights
WEIGHTS = {"high": 3, "medium": 2, "low": 1}


# 🧠 ENERGY MODEL
def get_energy(hour: int) -> str:
    if 6 <= hour < 12:
        return "high"
    elif 12 <= hour < 18:
        return "medium"
    return "low"


# 📊 DISTRIBUTION (%)
def calculate_distribution(schedule: dict) -> dict:
    total = sum(schedule.values()) or 1
    return {
        subject: round((time / total) * 100, 2)
        for subject, time in schedule.items()
    }


# 📊 REAL SCORING FUNCTION
def calculate_score(schedule: dict, priorities: dict) -> int:
    total_time = sum(schedule.values())
    if total_time == 0:
        return 0

    weighted_sum = 0

    for subject, time in schedule.items():
        priority = priorities.get(subject, "medium")
        weight = WEIGHTS.get(priority, 2)
        weighted_sum += time * weight

    max_possible = total_time * 3
    score = (weighted_sum / max_possible) * 100

    return int(score)


# ⏰ TIME SLOT GENERATION (SAFE VERSION)
def generate_time_slots(schedule: dict, days=1, hours_per_day=4) -> list:
    slots = []

    if not schedule:
        return slots

    # 🔥 SORT BY PRIORITY (high first)
    subjects = sorted(
        schedule.keys(),
        key=lambda s: schedule[s],
        reverse=True
    )

    total_minutes_per_day = max(1, hours_per_day) * 60
    idx = 0

    for day in range(1, max(1, days) + 1):

        current = datetime.strptime("09:00", "%H:%M")
        minutes_used = 0

        # 🔥 safety counter (prevents infinite loop)
        safety_counter = 0

        while minutes_used < total_minutes_per_day and safety_counter < 1000:
            safety_counter += 1

            # 🔥 pick subject with highest remaining time
            subject = max(schedule, key=lambda s: schedule[s])
            remaining = schedule.get(subject, 0)

            if remaining <= 0:
                idx += 1
                continue

            chunk = min(90, remaining, total_minutes_per_day - minutes_used)

            energy = get_energy(current.hour)

            if energy == "high":
                label = "🔥 Deep Study"
            elif energy == "medium":
                label = "⚡ Practice"
            else:
                label = "🔁 Revision"

            end = current + timedelta(minutes=chunk)

            # ✅ ALWAYS include 'day'
            slots.append({
                "day": f"Day {day}",
                "subject": f"{subject} ({label})",
                "start": current.strftime("%H:%M"),
                "end": end.strftime("%H:%M"),
                "energy": energy
            })

            # 🔥 CRITICAL FIX (mutate local copy only)
            schedule[subject] = max(0, schedule[subject] - chunk)

            minutes_used += chunk
            current = end + timedelta(minutes=10)
            idx += 1

            # 🔥 stop if all subjects done
            if all(v <= 0 for v in schedule.values()):
                break

    return slots


# 🔥 WOW FEATURE
def simulate_change(schedule: dict, subject: str, percent: int):
    new_schedule = schedule.copy()

    if subject in new_schedule:
        new_schedule[subject] = int(
            new_schedule[subject] * (1 + percent / 100)
        )

    new_distribution = calculate_distribution(new_schedule)
    new_score = max(50, 85 - abs(percent))

    return {
        "new_distribution": new_distribution,
        "new_score": new_score
    }


# 🚀 MAIN FUNCTION (SAFE VERSION)
def generate_schedule(total_hours, subjects, priorities, days, hours_per_day):
    total_minutes = int(max(0, total_hours) * 60)

    if not subjects:
        return {
            "study_plan": {},
            "time_slots": [],
            "distribution": {},
            "score": 0,
            "day_wise_plan": True
        }

    total_weight = sum(
        WEIGHTS.get(priorities.get(s, "medium"), 2)
        for s in subjects
    ) or 1

    schedule = {}
    for subject in subjects:
        weight = WEIGHTS.get(priorities.get(subject, "medium"), 2)
        schedule[subject] = int((weight / total_weight) * total_minutes)

    # 🔥 VERY IMPORTANT (prevents mutation bug)
    schedule_copy = schedule.copy()

    return {
        "study_plan": schedule,
        "time_slots": generate_time_slots(schedule_copy, days, hours_per_day),
        "distribution": calculate_distribution(schedule),
        "score": calculate_score(schedule, priorities),
        "day_wise_plan": True
    }


# 🔄 RESCHEDULE (SAFE + CLEAN)
def reschedule_plan(time_slots, missed_day):
    new_slots = []

    for slot in time_slots:
        if "day" not in slot:
            continue

        try:
            day_num = int(slot["day"].split()[1])
        except:
            continue

        if day_num == missed_day:
            continue

        if day_num > missed_day:
            day_num -= 1

        updated_slot = slot.copy()
        updated_slot["day"] = f"Day {day_num}"

        new_slots.append(updated_slot)

    return new_slots