import streamlit as st
import pandas as pd
from scheduler import generate_schedule
from calendar_integration import create_events
from fpdf import FPDF

# 📄PDF GENERATION

def generate_pdf(result):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # Title
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, "Smart Study Timetable", ln=True, align='C')
    pdf.ln(5)

    # Table Header
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(30, 10, "Day", 1)
    pdf.cell(40, 10, "Start", 1)
    pdf.cell(40, 10, "End", 1)
    pdf.cell(60, 10, "Subject", 1)
    pdf.ln()

    # Table Data (🔥 TIME SLOTS)
    pdf.set_font("Arial", size=10)

    for slot in result["time_slots"]:
        day = str(slot.get("day", "-"))
        start = slot["start"]
        end = slot["end"]
        subject = slot["subject"]

        pdf.cell(30, 10, day, 1)
        pdf.cell(40, 10, start, 1)
        pdf.cell(40, 10, end, 1)
        pdf.cell(60, 10, subject, 1)
        pdf.ln()

    pdf.ln(5)

    # Summary Section
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, "Summary", ln=True)

    pdf.set_font("Arial", size=10)
    pdf.cell(200, 8, f"Break Time: {result['break_time']} mins", ln=True)
    pdf.cell(200, 8, f"Revision Time: {result['revision_time']} mins", ln=True)
    pdf.cell(200, 8, f"Efficiency Score: {result['score']}%", ln=True)

    file_path = "study_plan.pdf"
    pdf.output(file_path)

    return file_path


# ⚙️ PAGE CONFIG
st.set_page_config(page_title="Smart Study Planner", page_icon="🧠", layout="wide")

st.title("🧠 Smart Study Planner")
st.caption("AI-powered personalized study scheduling")

st.divider()

# 📥 INPUT SECTION
# 📥 INPUT SECTION
st.subheader("📥 Input Details")

col1, col2, col3 = st.columns(3)

with col1:
    days = st.number_input(
        "Days (0 = total time)",
        min_value=0,
        value=0,
        help="Set 0 if you want total time planning"
    )

with col2:
    hours = st.number_input(
        "Hours",
        min_value=0,
        value=0,  # ✅ FIXED (was 4 before)
        help="Hours per day if days > 0"
    )

with col3:
    minutes = st.number_input(
        "Minutes",
        min_value=0,
        value=0,
        help="Extra minutes"
    )

subjects_input = st.text_input(
    "Subjects (comma separated)",
    placeholder="TOC, DBMS, FSD"
)

priority_input = st.text_input(
    "Priorities (high/medium/low)",
    placeholder="high, medium, low"
)

# 💡 SUGGESTION ENGINE
if subjects_input and priority_input:
    subjects = [s.strip().upper() for s in subjects_input.split(",")]
    priorities_list = [p.strip().lower() for p in priority_input.split(",")]

    if len(subjects) == len(priorities_list):
        weight_map = {"high": 3, "medium": 2, "low": 1}
        total_weight = sum(weight_map.get(p, 2) for p in priorities_list)

        if total_weight > 0:
            st.info("💡 Suggested Time Distribution")
            for i, sub in enumerate(subjects):
                percent = (weight_map.get(priorities_list[i], 2) / total_weight) * 100
                st.write(f"{sub} → {int(percent)}%")

st.divider()

# 🚀 GENERATE PLAN
if st.button("🚀 Generate Study Plan", use_container_width=True):

    if not subjects_input or not priority_input:
        st.error("Enter subjects and priorities")
        st.stop()

    subjects = [s.strip().upper() for s in subjects_input.split(",")]
    priorities_list = [p.strip().lower() for p in priority_input.split(",")]

    if len(subjects) != len(priorities_list):
        st.error("Subjects and priorities must match")
        st.stop()

    priorities = {subjects[i]: priorities_list[i] for i in range(len(subjects))}

    if days == 0:
        total_minutes = (hours * 60) + minutes
        hours_per_day = None
    else:
        total_minutes = (days * hours * 60) + minutes
        hours_per_day = hours

    if total_minutes <= 0:
        st.error("Time must be greater than 0")
        st.stop()

    total_hours = total_minutes / 60

    result = generate_schedule(
        total_hours=total_hours,
        subjects=subjects,
        priorities=priorities,
        days=days,
        hours_per_day=hours_per_day
    )

    st.session_state["result"] = result
    st.success("✅ Plan Generated!")

# 📊 OUTPUT SECTION
if "result" in st.session_state:

    result = st.session_state["result"]

    st.subheader("📊 Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Break Time", f"{result['break_time']} mins")
    col2.metric("Revision Time", f"{result['revision_time']} mins")
    col3.metric("Efficiency", f"{result['score']}%")

    st.divider()

    # 🎨 CARD UI
    st.subheader("📅 Study Plan")

    for sub, mins in result["study_plan"].items():
        st.markdown(
            f"""
            <div style="
                padding:15px;
                margin:10px 0;
                border-radius:10px;
                background:#111827;
                border:1px solid #374151;
            ">
                <h4 style="color:#60a5fa;">{sub}</h4>
                <p style="color:white;">⏱ {mins} mins</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 📊 TABLE TIMETABLE
    st.subheader("📊 Timetable")

    table_data = []

    for slot in result["time_slots"]:
        if "day" in slot:
            table_data.append({
                "Day": slot["day"],
                "Start": slot["start"],
                "End": slot["end"],
                "Subject": slot["subject"]
            })
        else:
            table_data.append({
                "Day": "-",
                "Start": slot["start"],
                "End": slot["end"],
                "Subject": slot["subject"]
            })

    df = pd.DataFrame(table_data)

    st.dataframe(df, use_container_width=True)

    st.divider()

    # 📅 GOOGLE CALENDAR
    if st.button("📅 Add to Google Calendar"):
        create_events(result["study_plan"])
        st.success("Added to Calendar!")

    # 📄 PDF DOWNLOAD
    if st.button("📄 Generate PDF"):
        file_path = generate_pdf(result)

        with open(file_path, "rb") as f:
            st.download_button(
                "⬇ Download PDF",
                f,
                "study_plan.pdf",
                "application/pdf"
            )