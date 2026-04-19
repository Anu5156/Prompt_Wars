"""
📘 FILE: motivation_engine.py

💬 PURPOSE:
Generates motivational feedback based on user priorities.

🎯 FUNCTION:
generate_motivation(subjects, priorities)

🧠 LOGIC:
- Detects high-priority subject
- Generates targeted motivational message
- Falls back to general motivational lines

💡 EXAMPLE:
"🔥 Focus on TOC — this will change your result!"

🚀 WHY IMPORTANT:
Improves:
- User engagement
- Emotional connection
- Perceived intelligence
"""
import random

def generate_motivation(subjects, priorities):
    high = [s for s in subjects if priorities[s] == "high"]
    if high:
        return f"🔥 Focus on {high[0]} — high impact subject!"
    return random.choice([
        "Consistency beats intensity",
        "Start now, not later",
        "Discipline = success"
    ])