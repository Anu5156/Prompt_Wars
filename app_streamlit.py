import streamlit as st
import pandas as pd
from scheduler import generate_schedule
from calendar_integration import create_events
from fpdf import FPDF

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
st.caption("Accessible and user-friendly study planner with structured output")

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

# 📥 INPUT
st.subheader("📥 Input Details")

col1, col2, col3 = st.columns(3)

with col1:
    days = st.number_input("Days (0 = total time)", min_value=0, value=0)

with col2:
    hours = st.number_input("Hours", min_value=0, value=0)

with col3:
    minutes = st.number_input("Minutes", min_value=0, value=0)

st.caption("Enter subjects and priorities carefully (comma-separated)")

subjects_input = st.text_input(
    "Subjects",
    placeholder="TOC, DBMS, FSD",
    help="Enter subjects separated by commas"
)

priority_input = st.text_input(
    "Priorities",
    placeholder="high, medium, low",
    help="Enter priority for each subject"
)

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
        st.error("⚠️ Subjects and priorities must match")
        st.stop()

    priorities = {subjects[i]: priorities_list[i] for i in range(len(subjects))}

    # ✅ FIXED TIME CALCULATION
    if days == 0:
        total_minutes = (hours * 60) + minutes
    else:
        total_minutes = days * ((hours * 60) + minutes)

    if total_minutes <= 0:
        st.error("⚠️ Time must be greater than 0")
        st.stop()

    # ✅ EXTRA VALIDATION
    if days > 0 and hours <= 0:
        st.error("⚠️ Hours per day must be greater than 0")
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

    col1, col2, col3 = st.columns(3)
    col1.metric("Break Time", f"{result['break_time']} mins")
    col2.metric("Revision Time", f"{result['revision_time']} mins")
    col3.metric("Efficiency", f"{result['score']}%")

    # 📊 ANALYTICS
    st.subheader("📊 Study Analytics")

    df_chart = pd.DataFrame(
        list(result["study_plan"].items()),
        columns=["Subject", "Minutes"]
    )

    # ✅ GREEN BAR CHART
    st.bar_chart(df_chart.set_index("Subject"), color="#2ecc71")

    # 🤖 AI INSIGHT
    top_subject = max(result["study_plan"], key=result["study_plan"].get)
    st.success(f"🔥 Focus more on: {top_subject}")

    st.divider()

    # 📅 STUDY PLAN
    st.subheader("📅 Study Plan")

    for sub, mins in result["study_plan"].items():
        st.write(f"{sub} → {mins} mins")

    # 📊 TIMETABLE (FIXED DAY FORMAT)
    st.subheader("📊 Timetable")

    table_data = []

    for slot in result["time_slots"]:
        table_data.append({
            "Day": slot["day"] if "day" in slot else "Full Plan",  # ✅ FIXED
            "Start": slot["start"],
            "End": slot["end"],
            "Subject": slot["subject"]
        })

    df = pd.DataFrame(table_data)

    if "Day" in df.columns:
        df = df.sort_values(by=["Day", "Start"])

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # 📅 GOOGLE CALENDAR
    if st.button("📅 Add to Google Calendar"):
        try:
            create_events(result["time_slots"])
            st.success("✅ Added to Google Calendar!")
        except Exception as e:
            st.error(str(e))

    # 📄 PDF DOWNLOAD
    if st.button("📄 Generate PDF"):
        file_path = generate_pdf(result)
        with open(file_path, "rb") as f:
            st.download_button("⬇ Download PDF", f, "study_plan.pdf")