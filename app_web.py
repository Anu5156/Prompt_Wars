"""
📘 FILE: app_web.py

🌐 PURPOSE:
Backend API for Smart Study Planner

FEATURES:
- Generate schedule
- AI insights
- Distribution analysis
- What-if simulation

🚀 RUN:
python app_web.py
"""

from flask import Flask, request, jsonify

from scheduler import generate_schedule, simulate_change
from ai_optimizer import improve_plan, evaluate_plan

app = Flask(__name__)


@app.route("/")
def home():
    return "🚀 Smart Study Planner API is running"


@app.route("/plan", methods=["POST"])
def create_plan():
    data = request.json

    subjects = data.get("subjects", [])
    priorities = data.get("priorities", {})
    total_hours = data.get("total_hours", 4)

    result = generate_schedule(total_hours, subjects, priorities)

    # 🤖 AI layer
    result["ai_improvement"] = improve_plan(result)
    result["ai_evaluation"] = evaluate_plan(result)

    return jsonify(result)


# 🔥 WOW FEATURE: SIMULATION API
@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.json

    schedule = data.get("schedule", {})
    subject = data.get("subject")
    change = data.get("change_percent", 10)

    sim_result = simulate_change(schedule, subject, change)

    return jsonify(sim_result)


if __name__ == "__main__":
    app.run(debug=True)