"""
📘 FILE: app_streamlit.py

🧠 PURPOSE:
Main UI for Adaptive AI Study Planner

✨ FEATURES:
- AI parsing
- Smart scheduling
- Green analytics graph
- Timetable + CSV + PDF
- Google Calendar integration
- Conversational AI (WOW)
"""

import streamlit as st
import pandas as pd
import altair as alt
from fpdf import FPDF
import random

from scheduler import generate_schedule, reschedule_plan
from calendar_integration import create_events
from ai_optimizer import improve_plan, evaluate_plan, chat_with_ai
from prompt_parser import extract_subjects_and_priority
from motivation_engine import generate_motivation


# ⚙️ CONFIG
st.set_page_config(page_title="Adaptive AI Study Planner", layout="wide")

# ==========================
# 📄GENERATE  PDF
# ==========================
def generate_pdf(dataframe):
    from fpdf import FPDF
    import random

    pdf = FPDF()
    pdf.add_page()

    # ==========================
    # 🧠 TITLE
    # ==========================
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Smart Study Planner", ln=True, align="C")

    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, "Personalized Study Timetable", ln=True, align="C")

    pdf.ln(8)

    # ==========================
    # 📊 TABLE HEADER
    # ==========================
    pdf.set_fill_color(40, 40, 40)  # dark header
    pdf.set_text_color(255, 255, 255)

    pdf.set_font("Arial", "B", 10)

    pdf.cell(30, 8, "Day", border=1, fill=True)
    pdf.cell(50, 8, "Time", border=1, fill=True)
    pdf.cell(110, 8, "Subject", border=1, fill=True)
    pdf.ln()

    # ==========================
    # 📄 TABLE CONTENT
    # ==========================
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(0, 0, 0)

    def clean_text(text):
        return str(text).encode("latin-1", "ignore").decode("latin-1")

    fill = False  # alternate row color

    for _, row in dataframe.iterrows():
        if fill:
            pdf.set_fill_color(245, 245, 245)
        else:
            pdf.set_fill_color(255, 255, 255)

        pdf.cell(30, 8, clean_text(row["day"]), border=1, fill=True)
        pdf.cell(50, 8, f"{row['start']} - {row['end']}", border=1, fill=True)
        pdf.cell(110, 8, clean_text(row["subject"]), border=1, fill=True)
        pdf.ln()

        fill = not fill

    # ==========================
    # 💬 MOTIVATION
    # ==========================
    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)

    slogans = [
        "Stay consistent!",
        "Push your limits!",
        "Discipline beats motivation!",
        "Focus -> Success!"   # ✅ SAFE TEXT
    ]

    pdf.cell(0, 10, random.choice(slogans), ln=True, align="C")

    # ==========================
    # 📁 SAVE FILE
    # ==========================
    file_path = "study_plan.pdf"
    pdf.output(file_path)

    return file_path


def generate_ics(time_slots, start_date):
    from datetime import datetime, timedelta

    def clean_text(text):
        return text.encode("ascii", "ignore").decode()

    base_date = datetime.combine(start_date, datetime.min.time())

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//AI Study Planner//EN"
    ]

    for slot in time_slots:
        day_num = int(slot["day"].split()[1])

        start_dt = base_date + timedelta(days=day_num - 1)
        end_dt = base_date + timedelta(days=day_num - 1)

        start_time = datetime.strptime(slot["start"], "%H:%M")
        end_time = datetime.strptime(slot["end"], "%H:%M")

        start_final = start_dt.replace(hour=start_time.hour, minute=start_time.minute)
        end_final = end_dt.replace(hour=end_time.hour, minute=end_time.minute)

        lines.extend([
            "BEGIN:VEVENT",
            f"SUMMARY:{clean_text(slot['subject'])}",
            f"DTSTART:{start_final.strftime('%Y%m%dT%H%M%S')}",
            f"DTEND:{end_final.strftime('%Y%m%dT%H%M%S')}",
            "END:VEVENT"
        ])

    lines.append("END:VCALENDAR")

    file_path = "study_plan.ics"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return file_path

# ==========================
# 🎨 PREMIUM UI STYLING
# ==========================
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

/* Titles */
h1, h2, h3 {
    color: #f8fafc;
    font-weight: 700;
}

/* Glass card effect */
.block-container {
    padding-top: 2rem;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.6em 1.2em;
    font-weight: bold;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
}

/* Input boxes */
.stTextInput input, .stNumberInput input {
    border-radius: 10px;
    border: 1px solid #334155;
    background-color: #020617;
    color: white;
}

/* Dataframe */
.css-1d391kg {
    background-color: rgba(255,255,255,0.05);
    border-radius: 10px;
}

/* Success box */
.stAlert {
    border-radius: 12px;
}

/* Chat box */
.stChatMessage {
    border-radius: 12px;
    padding: 10px;
}

/* Divider */
hr {
    border: 1px solid #1e293b;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center; font-size:40px;'>
🧠 Adaptive AI Study Planner
</h1>
<p style='text-align:center; color:#94a3b8;'>
Energy-based • AI Optimized • Adaptive Scheduling
</p>
""", unsafe_allow_html=True)

st.divider()


# ==========================
# 🔁 MODE SELECTION
# ==========================
mode = st.radio("Choose Mode", ["Manual Input", "AI Input"])

# ==========================
# 📥 INPUT SECTION
# ==========================
st.subheader("📥 Input Details")

col1, col2, col3, col4 = st.columns(4)

with col1:
    days = st.number_input("Days", min_value=0, value=0)

with col2:
    hours = st.number_input("Hours per day", min_value=0, value=0)

with col3:
    minutes = st.number_input("Extra Minutes", min_value=0, value=0)

with col4:
    from datetime import date
    start_date = st.date_input("📅 Start Date", value=date.today())

# ==========================
# 🟦 MANUAL MODE
# ==========================
if mode == "Manual Input":
    st.text_input("Subjects (comma separated)", key="subjects_input")
    st.text_input("Priorities (high/medium/low)", key="priority_input")

# ==========================
# 🧠 AI MODE
# ==========================
elif mode == "AI Input":

    nl_input = st.text_area(
        "Describe your study plan",
        placeholder="I have 4 hours. TOC is important, DBMS is optional"
    )

    if st.button("✨ Parse with AI"):
        s, p = extract_subjects_and_priority(nl_input)

        if not s:
            st.warning("⚠️ Could not detect subjects.")
        else:
            st.success("✅ Parsed Successfully")
            st.write("Subjects:", s)
            st.write("Priorities:", p)

            st.session_state["subjects_input"] = ",".join(s)
            st.session_state["priority_input"] = ",".join(p.values())

# ==========================
# 🚀 GENERATE PLAN
# ==========================
if st.button("🚀 Generate Plan", use_container_width=True):

    subjects_value = st.session_state.get("subjects_input", "")
    priority_value = st.session_state.get("priority_input", "")

    subjects = [s.strip().upper() for s in subjects_value.split(",") if s.strip()]
    priorities_list = [p.strip().lower() for p in priority_value.split(",") if p.strip()]

    if len(subjects) == 0 or len(priorities_list) == 0:
        st.error("⚠️ Please provide valid subjects and priorities")
        st.stop()

    if len(priorities_list) != len(subjects):
        st.warning("⚠️ Priority mismatch → defaulting to medium")
        priorities_list = ["medium"] * len(subjects)

    priorities = dict(zip(subjects, priorities_list))

    st.session_state["subjects"] = subjects
    st.session_state["priorities"] = priorities

    total_hours = (days * (hours + minutes / 60)) if days > 0 else (hours + minutes / 60)

    result = generate_schedule(total_hours, subjects, priorities, days, hours)
    st.session_state["result"] = result

    st.success("✅ Plan Generated!")

# ==========================
# 📊 OUTPUT
# ==========================
if "result" in st.session_state:

    result = st.session_state["result"]

    st.subheader("📊 Metrics")
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #22c55e, #4ade80);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 22px;
        font-weight: bold;
    ">
    🚀 Efficiency Score: {result['score']}%
    </div>
    """, unsafe_allow_html=True)
# ==========================
# 📊 GRAPH (UPGRADED)
# ==========================
    st.subheader("📊 Study Distribution (%)")

    df = pd.DataFrame(
        list(result["distribution"].items()),
        columns=["Subject", "Percent"]
    )

    # 🔥 PRIORITY COLORS
    color_map = {
        "high": "#ff4b4b",
        "medium": "#ffa500",
        "low": "#4caf50"
    }

    # 🔥 MAP PRIORITY BASED ON STUDY TIME
    max_val = max(result["study_plan"].values())
    min_val = min(result["study_plan"].values())

    df["Priority"] = df["Subject"].map(result["study_plan"]).apply(
        lambda x: "high" if x == max_val
        else "low" if x == min_val
        else "medium"
    )

    chart = alt.Chart(df).mark_bar(
        cornerRadiusTopLeft=6,
        cornerRadiusTopRight=6,
        cornerRadius=4
    ).encode(
        x=alt.X("Subject", sort="-y"),
        y=alt.Y("Percent", title="Study %"),
        color=alt.Color(
            "Priority",
            scale=alt.Scale(
                domain=list(color_map.keys()),
                range=list(color_map.values())
            )
        )
    ).properties(height=350)

    st.altair_chart(chart, use_container_width=True)
    # ==========================
    # 🧠 AI EXPLANATION (WOW)
    # ==========================
    st.subheader("🤖 Why this plan works")

    top_subject = max(result["study_plan"], key=result["study_plan"].get)
    least_subject = min(result["study_plan"], key=result["study_plan"].get)

    st.success(f"""
    • **{top_subject}** gets highest focus (high priority)  
    • **{least_subject}** gets balanced time  
    • High-energy hours → difficult subjects  
    • Breaks prevent burnout  

    👉 Optimized for **maximum efficiency**
    """)

    # ==========================
    # ⚠️ SMART ALERT
    # ==========================
    if result["score"] < 60:
        st.warning("⚠️ Plan may be inefficient")
    elif result["score"] > 85:
        st.success("🔥 Excellent plan!")

    # ==========================
    # 📅 TIMETABLE
    # ==========================
    st.subheader("📅 Timetable")

    df_slots = pd.DataFrame(result["time_slots"])

    st.dataframe(
        df_slots.sort_values(by=["day", "start"]),
        use_container_width=True
    )

    # ==========================
    # 📄 PDF DOWNLOAD
    # ==========================
    st.subheader("📄 Download Timetable")

    if st.button("📥 Generate PDF"):

        pdf_file = generate_pdf(df_slots)

        with open(pdf_file, "rb") as f:
            st.download_button(
            label="⬇️ Download PDF",
            data=f,
            file_name="study_plan.pdf",
            mime="application/pdf"
        )

    # ==========================
    # 📊 TIMELINE VIEW (WOW)
    # ==========================
    st.subheader("📊 Timeline View")

    import pandas as pd

    # 🔥 USE USER SELECTED DATE
    base_date = pd.to_datetime(start_date)

    # Extract day number (Day 1 → 1)
    df_slots["day_num"] = df_slots["day"].str.extract(r'(\d+)').astype(int)

    # Combine date + time
    df_slots["start_dt"] = (
        base_date
        + pd.to_timedelta(df_slots["day_num"] - 1, unit="D")
        + pd.to_timedelta(df_slots["start"] + ":00")
    )

    df_slots["end_dt"] = (
        base_date
        + pd.to_timedelta(df_slots["day_num"] - 1, unit="D")
        + pd.to_timedelta(df_slots["end"] + ":00")
    )

    timeline = alt.Chart(df_slots).mark_bar().encode(
        x="start_dt",
        x2="end_dt",
        y="day",
        color="subject",
        tooltip=["day", "subject", "start", "end"]  # 🔥 better hover
    )

    st.altair_chart(timeline, use_container_width=True)
    # ==========================
    # 🎯 PROGRESS TRACKER
    # ==========================
    st.subheader("🎯 Track Progress")

    if "progress" not in st.session_state:
        st.session_state["progress"] = {}

    for i, row in df_slots.iterrows():
        key = f"{row['day']}_{i}"

        completed = st.checkbox(
            f"{row['day']} | {row['subject']} ({row['start']} - {row['end']})",
            key=key
        )

        st.session_state["progress"][key] = completed

    if all(st.session_state["progress"].values()) and len(st.session_state["progress"]) > 0:
        st.success("🎉 You completed your full plan!")

    # ==========================
    # 🔄 RESCHEDULE
    # ==========================
    missed = st.number_input("Missed Day?", min_value=0, value=0)

    if st.button("🔄 Reschedule"):

        if missed > 0:
            updated_slots = reschedule_plan(
                st.session_state["result"]["time_slots"],
                missed
            )

            st.session_state["result"]["time_slots"] = updated_slots

            st.success("🔄 Rescheduled!")

            df_updated = pd.DataFrame(updated_slots)

            st.dataframe(
                df_updated.sort_values(by=["day", "start"]),
                use_container_width=True
            )

            st.rerun()

    

    # ==========================
    # 📅 GOOGLE CALENDAR
    # ==========================
    st.info("📌 Requires internet & Google login")
    if st.button("📅 Add to Calendar"):
        with st.spinner("📡 Connecting to Google Calendar..."):

            try:
                create_events(result["time_slots"])
                st.success("✅ Timetable successfully added to Google Calendar!")

            except Exception as e:
                st.error("⚠️ Failed to connect to Google Calendar.")
                st.caption("Check internet / OAuth setup")
    
    # ==========================
    # 📅 OFFLINE CALENDAR DOWNLOAD
    # ==========================
    if st.button("📥 Download Calendar (.ics)"):

        ics_file = generate_ics(result["time_slots"], start_date)

        with open(ics_file, "rb") as f:
            st.download_button(
                label="⬇️ Download .ics File",
                data=f,
                file_name="study_plan.ics",
                mime="text/calendar"
            )

    # ==========================
    # 💬 AI CHAT
    # ==========================
    st.subheader("💬 AI Assistant")
    st.caption("💡 Try asking: How to improve focus?")

    if "chat" not in st.session_state:
        st.session_state["chat"] = []

    msg = st.chat_input("Ask something...")

    if msg:
        st.session_state["chat"].append(("user", msg))
        res = chat_with_ai(msg, result)
        st.session_state["chat"].append(("ai", res))

    for role, text in st.session_state["chat"]:
        st.chat_message(role).write(text)

    # ==========================
    # 💬 MOTIVATION
    # ==========================
    st.subheader("💬 Motivation")
    st.success(generate_motivation(
        st.session_state.get("subjects", []),
        st.session_state.get("priorities", {})
    ))

    # ==========================
    # ✅ COMPLETION
    # ==========================
    if st.button("✅ Mark Completed"):
        st.success("🎉 Congratulations! Keep going!")