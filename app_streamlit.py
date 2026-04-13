import streamlit as st
from scheduler import generate_schedule

st.set_page_config(page_title="Smart Study Planner", page_icon="🧠")

st.title("🧠 Smart Study Planner Assistant")

st.write("Generate your personalized study plan instantly 🚀")

# 🧾 INPUTS
subjects_input = st.text_input(
    "Enter subjects (comma separated)",
    placeholder="TOC,DBMS,FSD"
)

hours = st.number_input(
    "Total Study Hours",
    min_value=1,
    max_value=24,
    value=4
)

priority_input = st.text_input(
    "Enter priorities (comma separated: high/medium/low)",
    placeholder="high,medium,low"
)

# 🚀 BUTTON
if st.button("Generate Study Plan"):

    if not subjects_input or not priority_input:
        st.error("⚠️ Please enter both subjects and priorities")
    else:
        subjects = [s.strip().upper() for s in subjects_input.split(",")]
        priorities_list = [p.strip().lower() for p in priority_input.split(",")]

        # ⚠️ Validation
        if len(subjects) != len(priorities_list):
            st.error("⚠️ Number of subjects and priorities must match")
        else:
            priorities = {
                subjects[i]: priorities_list[i]
                for i in range(len(subjects))
            }

            # 📊 Generate plan
            result = generate_schedule(
                total_hours=hours,
                subjects=subjects,
                priorities=priorities,
                days=0,
                hours_per_day=None
            )

            # 📅 OUTPUT
            st.subheader("📅 Study Plan")
            for sub, mins in result["study_plan"].items():
                st.write(f"**{sub} → {mins} mins**")

            st.write(f"⏸ Break Time: {result['break_time']} mins")
            st.write(f"🔁 Revision Time: {result['revision_time']} mins")

            st.subheader("🧠 Efficiency Score")
            st.write(f"{result['score']}%")

            # ⏰ TIME SLOTS
            st.subheader("⏰ Time Slots")
            for slot in result["time_slots"]:
                if "day" in slot:
                    st.write(f"Day {slot['day']} | {slot['start']} - {slot['end']} → {slot['subject']}")
                else:
                    st.write(f"{slot['start']} - {slot['end']} → {slot['subject']}")