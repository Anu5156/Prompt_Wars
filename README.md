![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Status](https://img.shields.io/badge/Status-Active-green)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)

# 🧠 Adaptive AI Study Planning System

> 🚀 A multi-agent AI system that generates, critiques, and optimizes study plans in real time.

## ⚡ Quick Preview

- 🎯 AI-driven adaptive planning system
- 📊 Smart time allocation based on priority  
- 📅 Google Calendar integration  
- 📄 PDF + CSV export  
- 🤖 AI assistant + analytics 

🚀 Designed to improve productivity and reduce planning stress
---
## 🧠 What Makes It Intelligent?

Unlike traditional tools:
- It doesn’t just generate a plan  
- It **analyzes, critiques, and improves it using AI**

👉 Every output goes through an **AI reasoning loop**

---

## 🏆 Key Innovation

Unlike traditional planners, this system:

- Uses **multi-agent prompt engineering**
- Applies **AI critique + optimization loops**
- Generates **self-improving study plans**
- Combines **deterministic algorithms + LLM intelligence**

> Designed as a hybrid AI system, not just a scheduler

---

## 🧠 Prompt Architecture (Core Innovation)

This system uses a **multi-agent prompt engineering approach**:

### 🔹 AI Pipeline

User Input  
↓  
AI Parser (LLM-based extraction)  
↓  
Rule-based Scheduler  
↓  
AI Critic Agent (analyzes plan quality)  
↓  
AI Optimizer Agent (improves schedule)  
↓  
AI Evaluation Agent (scores efficiency)  
↓  
Final Output  

> This pipeline ensures every plan is not just generated, but **critically evaluated and improved by AI**

---

## 🎯 Problem Statement Alignment

### 📌 Problem
Students often struggle to manage study time effectively due to lack of planning and prioritization.

### 💡 Solution
This app intelligently distributes study time based on subject importance and availability.

### 🧠 Approach
- Multi-agent prompt engineering (Planner → Critic → Optimizer)  
- Hybrid system (LLM reasoning + deterministic scheduling)  
- Self-improving feedback loop  
- Context-aware adaptive scheduling  

### 🚀 Impact
- Better time management
- Improved focus on key subjects
- Structured and efficient study routines

--- 
## 💡 Solution

This application intelligently distributes study time based on subject priority and availability,
generating optimized study plans, timetables, and actionable insights.

🚀 Built with Streamlit + Google Calendar API + Intelligent Scheduling Logic  

An AI-powered intelligent assistant that dynamically generates personalized study schedules based on time availability, subject priority, and user intent — with real-time Google Calendar integration.

---
## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **Scheduling Engine:** Custom Algorithm  
- **Visualization:** Pandas + Altair  
- **AI/NLP:** LLM-based prompt engineering (multi-agent system)
- **Integration:** Google Calendar API  

--- 


## 🎯 Challenge Vertical
**Productivity / Education**

---

## 👤 Target Persona
Engineering students preparing for exams, assignments, and projects who struggle with:
- Time management  
- Subject prioritization  
- Adapting study plans dynamically  

---

## 🔄 How It Works

1. User provides:
   - Subjects + priorities OR natural language input  

2. AI Parser:
   - Extracts subjects & priority using LLM  

3. Scheduling Engine:
   - Allocates time using weighted algorithm  

4. AI Intelligence Layer:
   - Critic analyzes weaknesses  
   - Optimizer improves plan  
   - Evaluator scores efficiency  

5. Output:
   - Study plan  
   - Timetable  
   - AI insights  
   - Export options (PDF, CSV, Calendar)

---
## 🚀 Core Features

- ✅ Priority-Based Scheduling (High / Medium / Low)  
- ✅ AI Mode (Natural Language Input Parsing)  
- ✅ Dynamic Time Allocation Algorithm  
- ✅ Break & Revision Optimization  
- ✅ Time-Slot Generation (Structured Study Flow)  
- ✅ Plan Efficiency Scoring System  
- ✅ AI-Based Study Suggestions  
- ✅ Google Calendar API Integration  
- ✅ PDF Export of Timetable  
- ✅ CSV Export  
- ✅ Progress Tracking  
- ✅ Clean Streamlit UI  

---

## ⭐ Key Highlights

- Real-time adaptive scheduling  
- Intelligent priority-based allocation  
- AI-assisted insights  
- Multi-format export  
- Clean and accessible UI  

---

## 🧠 Intelligent Decision-Making Logic

The assistant uses layered decision-making:

- 🔹 NLP Parsing → Extracts subjects & priorities  
- 🔹 Weighted Allocation Algorithm → Distributes time proportionally  
- 🔹 Adaptive Scheduling → Adjusts based on available time  
- 🔹 Efficiency Scoring → Evaluates quality of study plan  
- 🔹 AI Suggestions → Improves learning outcomes  

> This ensures **context-aware dynamic planning**, not static scheduling.

---

## ⚙️ System Workflow

1. User enters time, subjects, priorities  
2. System calculates weighted distribution  
3. Generates optimized study plan  
4. Creates interleaved timetable  
5. Outputs:
   - Study plan  
   - Timetable  
   - Efficiency score  
   - Calendar events  
   - Study Analytics  

---

## 🌐 Live Demo

🔗 https://promptwars-r86ripmbuk27tyamz5jx62.streamlit.app/

---

## 🎥 Demo Video

▶️ Watch full working demo:

[![Watch Demo](https://img.shields.io/badge/▶️%20Watch%20Demo-Click%20Here-blue)][(https://www.youtube.com/watch?v=rLS3vJWCYyY)]

---

## 🎬 Demo Highlights

The demo showcases:
- AI-based subject parsing (AI mode)
- Smart schedule generation
- Multi-agent AI optimization (Planner → Critic → Optimizer)
- Study analytics visualization
- Timetable generation
- PDF + CSV export
- Google Calendar integration

---
## 📸 Screenshots

### 🔹 Input Interface
![Input](assets/screenshots/input.png)

### 🔹 Study Plan Output
![Plan](assets/screenshots/plan.png)

### 🔹 Timetable View
![Table](assets/screenshots/table.png)

---

## 🏗️ Project Structure

```plaintext
project-root/
│
├── app_streamlit.py           # Main UI (Streamlit app)
├── scheduler.py               # Core scheduling engine
├── calendar_integration.py    # Google Calendar integration
├── prompt_parser.py           # NLP processing
├── utils.py                   # Helper functions
├── requirements.txt           # Dependencies
├── README.md
│
├── tests/                     # 🧪 Testing folder
│   └── test_scheduler.py      # Unit tests for scheduler
│
└── assets/
    └── screenshots/
        ├── input.png
        ├── plan.png
        ├── table.png
```
## ⚙️ Setup Instructions

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 2️⃣.Run the application
```bash
streamlit run app_streamlit.py
```

## Google Calendar Setup

1.Go to Google Cloud Console
2.Enable Google Calendar API
3.Create OAuth credentials
4.Download and rename file to my_credentials.json
5.Place it in the project root
6.Run the application and authenticate

⚠️ Credentials are not included in the repository for security reasons

---

 ## 📅 Google Calendar Integration
This project integrates with Google Calendar API to:

Automatically create study sessions as calendar events
Schedule tasks sequentially with accurate timing
Trigger notifications at session start time

---

## 🔐 Security Considerations
Credentials (my_credentials.json, token.json) are excluded via .gitignore
No sensitive data is stored in the repository
OAuth authentication ensures secure access

---

## ⚡ Performance & Efficiency
Lightweight implementation (<1MB repository)
No heavy frameworks
Optimized scheduling algorithm
Fast execution

---

## 🧪 Testing
Unit tests implemented using pytest
Covers scheduling logic and edge cases
All tests passing successfully (6/6)

---

## ♿ Accessibility

- Clear input labels and instructions
- Structured layout for readability
- User-friendly interface design
- Error handling and validation messages
- Simple and intuitive navigation

---

## ⚡ Performance
- Lightweight (<1MB)
- Fast execution
- Optimized scheduling

---

## ⚠️ Limitations
- AI responses depend on API availability and latency
- Requires API key configuration for full functionality
- No persistent storage (session-based)

---

## 🌍 Real-World Impact
This project helps students:

- Improve productivity
- Make better time decisions
- Reduce planning stress
- Follow structured learning

---

## 🚀 Advanced Features

- Priority-based color-coded calendar events
- Intelligent study balance detection
- Real-time analytics insights
- Progress tracking system
- Multi-format export (PDF + CSV)
- Smart feedback based on efficiency score

---
## 💡 Why This Project Stands Out

- Implements a **multi-agent AI pipeline** (Planner → Critic → Optimizer → Evaluator)  
- Uses **LLM-driven reasoning instead of static logic**  
- Applies **self-improving feedback loops** for better outputs  
- Bridges **algorithmic scheduling with AI intelligence**  
- Integrates real-world systems (Google Calendar) for practical usability  

> This is not just a planner — it is an **adaptive AI decision-making system**

---

## 🚀 Future Enhancements
Performance tracking dashboard
Adaptive learning system
Analytics integration
Google Sheets integration

---

## 🏁 Conclusion

The Smart Study Planner System demonstrates how AI-driven decision-making combined with real-world integrations can create impactful productivity tools.

It is scalable, practical, and designed for real users — not just a prototype.
