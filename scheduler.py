from datetime import datetime, timedelta


# ⏰ FAST + INTERLEAVED TIME SLOT GENERATION
def generate_time_slots(schedule, days, hours_per_day, start_time="09:00"):
    slots = []

    STUDY_BLOCK = 90   # 🔥 increased for performance
    BREAK_BLOCK = 10

    subjects = list(schedule.keys())
    remaining = schedule.copy()

    total_remaining = sum(remaining.values())

    # 🔥 CONTINUOUS MODE (days = 0)
    if days == 0 or hours_per_day is None:
        current = datetime.strptime(start_time, "%H:%M")

        while total_remaining > 0:
            for sub in subjects:
                if remaining[sub] <= 0:
                    continue

                chunk = min(STUDY_BLOCK, remaining[sub])

                end = current + timedelta(minutes=chunk)

                slots.append({
                    "subject": sub,
                    "start": current.strftime("%H:%M"),
                    "end": end.strftime("%H:%M")
                })

                current = end + timedelta(minutes=BREAK_BLOCK)

                remaining[sub] -= chunk
                total_remaining -= chunk

                if total_remaining <= 0:
                    break

        return slots

    # 🔥 DAY-BASED MODE (INTERLEAVED)
    for day in range(1, days + 1):
        current = datetime.strptime(start_time, "%H:%M")
        daily_limit = hours_per_day * 60
        used = 0

        while used < daily_limit and total_remaining > 0:
            for sub in subjects:
                if remaining[sub] <= 0:
                    continue

                chunk = min(STUDY_BLOCK, remaining[sub])

                if used + chunk > daily_limit:
                    break

                end = current + timedelta(minutes=chunk)

                slots.append({
                    "day": day,
                    "subject": sub,
                    "start": current.strftime("%H:%M"),
                    "end": end.strftime("%H:%M")
                })

                current = end + timedelta(minutes=BREAK_BLOCK)

                remaining[sub] -= chunk
                total_remaining -= chunk
                used += chunk + BREAK_BLOCK

                if total_remaining <= 0:
                    break

    return slots


# 🧠 SCORE CALCULATION
def calculate_score(schedule, priorities):
    weight_map = {"high": 3, "medium": 2, "low": 1}

    if len(set(priorities.values())) == 1:
        return 85

    actual = sum(schedule[s] * weight_map.get(priorities.get(s, "medium"), 2) for s in schedule)
    max_score = sum(schedule[s] * 3 for s in schedule)

    return int((actual / max_score) * 100) if max_score else 0


# 📆 DAY-WISE SPLIT
def split_across_days(schedule, days):
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
            sub, time = items[i]

            if time <= 0:
                continue

            portion = min(time, remaining)

            day_plan[key][sub] = portion
            items[i] = (sub, time - portion)

            remaining -= portion

            if remaining <= 0:
                break

    return day_plan


# 🚀 MAIN SCHEDULER
def generate_schedule(total_hours, subjects, priorities, days=0, hours_per_day=None):
    total_minutes = int(total_hours * 60)

    weight_map = {"high": 3, "medium": 2, "low": 1}
    subjects = [s.strip().upper() for s in subjects]

    weights = [weight_map.get(priorities.get(s, "medium"), 2) for s in subjects]
    total_weight = sum(weights) or 1

    # 📊 ALLOCATION
    schedule = {
        subjects[i]: int((weights[i] / total_weight) * total_minutes)
        for i in range(len(subjects))
    }

    # ⏸ BREAK TIME
    break_time = total_hours * 5

    # 🔁 REVISION TIME
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