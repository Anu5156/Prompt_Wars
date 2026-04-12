from datetime import datetime, timedelta


def generate_time_slots(schedule, days, hours_per_day, start_time="09:00"):
    slots = []

    STUDY_BLOCK = 50
    BREAK_BLOCK = 10
    MIN_BLOCK = 20

    # 🔥 continuous mode (days = 0 case)
    if hours_per_day is None:
        current = datetime.strptime(start_time, "%H:%M")

        for sub, minutes in schedule.items():
            remaining = minutes

            while remaining > 0:
                chunk = STUDY_BLOCK if remaining >= STUDY_BLOCK else remaining

                if chunk < MIN_BLOCK:
                    break

                end = current + timedelta(minutes=chunk)

                slots.append({
                    "subject": sub,
                    "start": current.strftime("%H:%M"),
                    "end": end.strftime("%H:%M")
                })

                current = end + timedelta(minutes=BREAK_BLOCK)
                remaining -= chunk

        return slots

    # 🔥 day-based mode
    total_daily_minutes = hours_per_day * 60
    subjects = list(schedule.items())
    subject_index = 0

    for day in range(1, days + 1):
        current = datetime.strptime(start_time, "%H:%M")
        used_today = 0

        while used_today < total_daily_minutes and subject_index < len(subjects):

            sub, remaining = subjects[subject_index]

            if remaining <= 0:
                subject_index += 1
                continue

            chunk = STUDY_BLOCK if remaining >= STUDY_BLOCK else remaining

            if chunk < MIN_BLOCK:
                subject_index += 1
                continue

            if used_today + chunk > total_daily_minutes:
                break

            end = current + timedelta(minutes=chunk)

            slots.append({
                "day": day,
                "subject": sub,
                "start": current.strftime("%H:%M"),
                "end": end.strftime("%H:%M")
            })

            current = end + timedelta(minutes=BREAK_BLOCK)
            used_today += chunk + BREAK_BLOCK

            subjects[subject_index] = (sub, remaining - chunk)

    return slots


def calculate_score(schedule, priorities):
    weight_map = {"high": 3, "medium": 2, "low": 1}

    if len(set(priorities.values())) == 1:
        return 85

    actual = sum(schedule[s] * weight_map[priorities.get(s, "medium")] for s in schedule)
    max_score = sum(schedule[s] * 3 for s in schedule)

    return int((actual / max_score) * 100) if max_score else 0


def split_across_days(schedule, days):
    if days == 0:
        return None

    day_plan = {}
    total = sum(schedule.values())
    per_day = max(1, total // days)

    items = list(schedule.items())

    for day in range(1, days + 1):
        label = "🧠 Deep Focus" if day == 1 else "🔁 Revision Focus" if day == days else "⚖️ Balanced Learning"
        key = f"Day {day} ({label})"
        day_plan[key] = {}

        remaining = per_day

        for i, (sub, time) in enumerate(items):
            if time <= 0:
                continue

            portion = min(time, remaining)

            if portion < 20:
                continue

            day_plan[key][sub] = portion
            items[i] = (sub, time - portion)

            remaining -= portion

            if remaining <= 0:
                break

    return day_plan


def generate_schedule(total_hours, subjects, priorities, days=0, hours_per_day=None):
    total_minutes = total_hours * 60

    weight_map = {"high": 3, "medium": 2, "low": 1}
    subjects = [s.strip() for s in subjects]

    weights = [weight_map.get(priorities.get(s, "medium"), 2) for s in subjects]
    total_weight = sum(weights) or 1

    schedule = {
        subjects[i]: int((weights[i] / total_weight) * total_minutes)
        for i in range(len(subjects))
    }

    break_time = total_hours * 5

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