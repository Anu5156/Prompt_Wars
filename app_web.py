from flask import Flask, request, jsonify
from scheduler import generate_schedule

app = Flask(__name__)

@app.route("/")
def home():
    return "Smart Study Planner API is running"

@app.route("/plan", methods=["POST"])
def create_plan():
    data = request.json

    subjects = data.get("subjects", [])
    priorities = data.get("priorities", {})
    total_hours = data.get("total_hours", 4)

    result = generate_schedule(total_hours, subjects, priorities)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)