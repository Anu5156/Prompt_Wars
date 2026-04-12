from scheduler import generate_schedule
from calendar_integration import create_events
from prompt_parser import extract_subjects_and_priority


def get_time_input():
    print("\nEnter your available study time:")

    try:
        days_input = input("Days (0 if total time): ").strip()
        days = int(days_input) if days_input else 0
    except:
        days = 0

    try:
        hours_input = input("Hours: ").strip()
        hours = int(hours_input) if hours_input else 0
    except:
        hours = 0

    try:
        minutes_input = input("Extra minutes (Enter if none): ").strip()
        minutes = int(minutes_input) if minutes_input else 0
    except:
        minutes = 0

    if days == 0:
        total_minutes = (hours * 60) + minutes
        hours_per_day = None
    else:
        total_minutes = (days * hours * 60) + minutes
        hours_per_day = hours

    total_hours = total_minutes / 60

    return total_hours, days, hours_per_day


def manual_mode():
    total_hours, days, hours_per_day = get_time_input()

    subjects = input("Enter subjects (comma separated): ").split(",")

    print("Enter priority (high/medium/low):")
    priorities = {}

    for sub in subjects:
        p = input(f"{sub.strip()}: ").lower()
        if p not in ["high", "medium", "low"]:
            print("⚠️ Invalid input, defaulting to medium")
            p = "medium"
        priorities[sub.strip()] = p

    return generate_schedule(total_hours, subjects, priorities, days, hours_per_day)


def ai_mode():
    user_input = input("\nEnter your study request: ")

    subjects, priorities_list = extract_subjects_and_priority(user_input)

    if not subjects:
        print("❌ No subjects detected.")
        exit()

    priorities = {subjects[i]: priorities_list[i] for i in range(len(subjects))}

    total_hours, days, hours_per_day = get_time_input()

    return generate_schedule(total_hours, subjects, priorities, days, hours_per_day)


def display_output(result):
    print("\n📅 OPTIMIZED STUDY PLAN:\n")

    for sub, time in result["study_plan"].items():
        print(f"{sub} → {time} mins")

    print(f"\n⏸ Break Time: {result['break_time']} mins")
    print(f"🔁 Revision Time: {result['revision_time']} mins")

    print(f"\n🧠 Plan Efficiency Score: {result['score']}%")

    if result["score"] >= 80:
        print("🔥 Excellent Plan")
    elif result["score"] >= 60:
        print("⚖️ Good Plan")
    else:
        print("⚠️ Needs Improvement")

    print("\n💡 Suggestions:")
    if result["score"] < 70:
        print("• Add more revision")
    print("• Follow 50-10 focus cycles")

    if result["day_wise_plan"]:
        print("\n📆 DAY-WISE PLAN:\n")
        for day, subs in result["day_wise_plan"].items():
            print(day)
            for sub, mins in subs.items():
                print(f"  {sub} → {mins} mins")
            print()

    print("\n⏰ TIME-SLOT PLAN:\n")
    for slot in result["time_slots"]:
        if "day" in slot:
            print(f"Day {slot['day']} | {slot['start']} - {slot['end']} → {slot['subject']}")
        else:
            print(f"{slot['start']} - {slot['end']} → {slot['subject']}")


def main():
    print("\n🧠 AI STUDY ASSISTANT")

    mode = input("Choose mode (1: Manual, 2: AI Mode): ")

    if mode == "1":
        result = manual_mode()
    elif mode == "2":
        result = ai_mode()
    else:
        print("❌ Invalid choice")
        return

    display_output(result)

    use_calendar = input("\nAdd this to Google Calendar? (y/n): ")

    if use_calendar.lower() == 'y':
        create_events(result["study_plan"])


if __name__ == "__main__":
    main()