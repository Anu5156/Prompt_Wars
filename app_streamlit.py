import streamlit as st
import pandas as pd
from scheduler import generate_schedule
from calendar_integration import create_events
from fpdf import FPDF
from collections import defaultdict

# ⚙️ PAGE CONFIG
st.set_page_config(
    page_title="Accessible Smart Study Planner",
    page_icon="🧠",
    layout="wide"
)

# 📄 PDF GENERATION
def generate_pdf(result):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Smart Study Timetable", ln=True, align='C')
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 10)
    pdf.cell(30, 10, "Day", 1)
    pdf.cell(40, 10, "Start", 1)
    pdf.cell(40, 10, "End", 1)
    pdf.cell(60, 10, "Subject", 1)
    pdf.ln()

    pdf.set_font("Arial", size=10)

    for slot in result["time_slots"]:
        day = slot.get('day', 'Full Plan')
        pdf.cell(30, 10, str(day), 1)
        pdf.cell(40, 10, slot["start"], 1)
        pdf.cell(40, 10, slot["end"], 1)
        pdf.cell(60, 10, slot["subject"], 1)
        pdf.ln()

    file_path = "study_plan.pdf"
    pdf.output(file_path)
    return file_path


# 🧠 TITLE
st.title("🧠 Smart Study Planner")
st.caption("This tool helps you create structured and optimized study schedules easily.")

# 🎯 PROBLEM ALIGNMENT
st.markdown("""
### 🎯 Problem
Students struggle to effectively manage study time and prioritize subjects.

### 💡 Solution
This application intelligently allocates study time based on subject priority.

### 🧠 Approach
- Priority-based allocation
- Interleaved scheduling
- Optimized learning efficiency
""")

st.divider()

# 📘 HOW TO USE
st.markdown("""
### 📘 How to Use

1. Enter subjects (comma separated)
2. Enter priorities (high/medium/low)
3. Set available time
4. Click Generate Study Plan
""")

# 📥 INPUT
with st.container():
    st.markdown("## 📥 Input Details")
    st.caption("Provide your study preferences below")

col1, col2, col3 = st.columns(3)

with col1:
    days = st.number_input("Days (0 = total time)", min_value=0, value=0)

with col2:
    hours = st.number_input("Hours per day", min_value=0, value=0, help="Number of study hours each day")

with col3:
    minutes = st.number_input("Minutes", min_value=0, value=0)

st.caption("Enter subjects and priorities carefully (comma-separated)")

subjects_input = st.text_input(
    "Subjects (comma separated)",
    placeholder="TOC, DBMS, FSD",
    help="Example: TOC, DBMS, FSD"
)

priority_input = st.text_input(
    "Priorities (high/medium/low)",
    placeholder="high, medium, low",
    help="Enter one priority per subject in the same order"
)

# 🔥 EMPTY STATE
if not subjects_input and not priority_input:
    st.info("👆 Enter subjects and priorities to see suggestions")

# 💡 SUGGESTION ENGINE
if subjects_input and priority_input:
    subjects_temp = [s.strip().upper() for s in subjects_input.split(",")]
    priorities_temp = [p.strip().lower() for p in priority_input.split(",")]

    if len(subjects_temp) == len(priorities_temp):
        weight_map = {"high": 3, "medium": 2, "low": 1}
        total_weight = sum(weight_map.get(p, 2) for p in priorities_temp)

        if total_weight > 0:
            st.info("💡 Suggested Time Distribution")
            for i, sub in enumerate(subjects_temp):
                percent = (weight_map.get(priorities_temp[i], 2) / total_weight) * 100
                st.write(f"{sub} → {int(percent)}%")

st.divider()

# 🔥 STATUS MESSAGE
if "result" not in st.session_state:
    st.warning("⚠️ Please enter inputs and generate a study plan")
else:
    st.success("✅ Study plan generated successfully")

# 🚀 GENERATE
if st.button("🚀 Generate Study Plan", use_container_width=True):

    if not subjects_input.strip():
        st.error("⚠️ Subjects cannot be empty")
        st.stop()

    if not priority_input.strip():
        st.error("⚠️ Priorities cannot be empty")
        st.stop()

    subjects = [s.strip().upper() for s in subjects_input.split(",")]
    priorities_list = [p.strip().lower() for p in priority_input.split(",")]

    if len(subjects) != len(priorities_list):
        st.error("⚠️ Subjects and priorities must match in count (e.g., 3 subjects → 3 priorities)")
        st.stop()

    priorities = {subjects[i]: priorities_list[i] for i in range(len(subjects))}

    # ⏳ LOADING STATE
    with st.spinner("⏳ Generating your optimized study plan..."):

        if days == 0:
            total_minutes = (hours * 60) + minutes
        else:
            total_minutes = days * ((hours * 60) + minutes)

        if total_minutes <= 0:
            st.error("⚠️ Time must be greater than 0")
            st.stop()

        try:
            result = generate_schedule(total_minutes / 60, subjects, priorities, days, hours)
            st.session_state["result"] = result
            st.success("✅ Plan Generated!")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.stop()

# 📊 OUTPUT
if "result" in st.session_state:

    result = st.session_state["result"]

    st.subheader("📊 Overview")

    # 📖 SUMMARY
    st.markdown("### 📖 Summary")
    total_time = sum(result["study_plan"].values())
    num_subjects = len(result["study_plan"])
    st.write(f"You will study {num_subjects} subjects with total time {total_time} minutes.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Break Time", f"{result['break_time']} mins")
    col2.metric("Revision Time", f"{result['revision_time']} mins")
    col3.metric("Efficiency", f"{result['score']}%")

    # 📊 ANALYTICS
    st.subheader("📊 Study Analytics")
    st.caption("Bar chart showing time allocated per subject")

    df_chart = pd.DataFrame(
        list(result["study_plan"].items()),
        columns=["Subject", "Minutes"]
    )

    st.bar_chart(df_chart.set_index("Subject"), color="#2ecc71")

    total_time = sum(result["study_plan"].values())
    num_subjects = len(result["study_plan"])

    st.info(f"📊 Total Study Time: {total_time} mins")
    st.info(f"📚 Subjects Covered: {num_subjects}")

    top_subject = max(result["study_plan"], key=result["study_plan"].get)
    st.success(f"🔥 Focus more on: {top_subject}")

    max_time = max(result["study_plan"].values())
    min_time = min(result["study_plan"].values())

    if max_time > 2 * min_time:
        st.warning("⚠️ Study plan is unbalanced. Consider adjusting priorities.")
    else:
        st.success("✅ Well-balanced study plan!")

    if result["score"] > 85:
        st.success("🔥 Excellent planning strategy!")
    elif result["score"] > 60:
        st.info("👍 Good plan, slight improvements possible.")
    else:
        st.warning("⚠️ Consider adjusting priorities for better efficiency.")

    st.divider()

    # 📅 STUDY PLAN
    st.subheader("📅 Study Plan")

    for sub, mins in result["study_plan"].items():
        st.markdown(f"- **{sub}** → {mins} mins")

    # 📊 TIMETABLE
    st.subheader("📊 Timetable")

    table_data = []

    for slot in result["time_slots"]:
        table_data.append({
            "Day": slot.get("day", "Full Plan"),
            "Start": slot["start"],
            "End": slot["end"],
            "Subject": slot["subject"]
        })

    df = pd.DataFrame(table_data)

    if "Day" in df.columns:
        df = df.sort_values(by=["Day", "Start"])

    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption("Tabular view of your study schedule showing day, time, and subject")

    # 🔥 CSV Export
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇ Download CSV", csv, "study_plan.csv")

    st.divider()

    # 🔥 Progress Tracking (Improved)
    st.subheader("✅ Mark Completed Sessions")

    day_wise_slots = defaultdict(list)
    for slot in result["time_slots"]:
        day = slot.get("day", "Full Plan")
        day_wise_slots[day].append(slot)

    for day, slots in day_wise_slots.items():
        st.markdown(f"### 📅 {day}")
        for i, slot in enumerate(slots):
            st.checkbox(
                f"{slot['start']} → {slot['subject']}",
                key=f"{day}_{i}"
            )

    st.divider()

    # 📅 GOOGLE CALENDAR
    if st.button("📅 Add to Google Calendar"):
        try:
            count = create_events(result["time_slots"])
            st.success(f"✅ {count} events added to Google Calendar!")
        except Exception as e:
            st.error(str(e))

    # 📄 PDF DOWNLOAD
    if st.button("📄 Generate PDF"):
        file_path = generate_pdf(result)
        with open(file_path, "rb") as f:
            st.download_button("⬇ Download PDF", f, "study_plan.pdf")

    # 🔄 RESET BUTTON
    if st.button("🔄 Reset Plan"):
        st.session_state.clear()
        st.rerun()