## Prompt Wars

# 🧠 Smart Study Planner Assistant

An AI-powered intelligent assistant that dynamically generates personalized study schedules based on time availability, subject priority, and user intent — with real-time Google Calendar integration.
> 🚀 Built as a smart, decision-driven assistant for Prompt Wars — combining AI reasoning, scheduling optimization, and real-world automation.

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

## ❗ Problem Statement

Students often:
- Do not know how to divide limited time efficiently  
- Fail to prioritize subjects based on importance  
- Cannot adapt schedules when time constraints change  
- Lack structured and actionable study plans  

---

## 💡 Solution Overview

The **Smart Study Planner Assistant** solves this by:

- Dynamically allocating time based on subject priority  
- Supporting both manual input and natural language (AI Mode)  
- Generating optimized time-slot schedules  
- Providing efficiency scoring and improvement suggestions  
- Automatically converting schedules into real-time Google Calendar events  

---

## 🚀 Core Features

- ✅ **Priority-Based Scheduling** (High / Medium / Low)  
- ✅ **AI Mode (Natural Language Input Parsing)**  
- ✅ **Dynamic Time Allocation Algorithm**  
- ✅ **Break & Revision Optimization**  
- ✅ **Time-Slot Generation (Structured Study Flow)**  
- ✅ **Plan Efficiency Scoring System**  
- ✅ **AI-Based Study Suggestions**  
- ✅ **Google Calendar API Integration (Real-time Automation)**  

---

## 🤖 AI Mode (Natural Language Understanding)

The assistant supports natural language input for seamless interaction.

### Example:
**Input:**

I need to learn DSA, FSD, COA which are equally important


### Output:
- Extracts subjects automatically  
- Assigns equal priority  
- Generates optimized schedule  

This makes the system intuitive and user-friendly.

---

## 🧠 Intelligent Decision-Making Logic

The assistant uses layered decision-making:

- 🔹 **NLP Parsing** → Extracts subjects & priorities  
- 🔹 **Weighted Allocation Algorithm** → Distributes time proportionally  
- 🔹 **Adaptive Scheduling** → Adjusts based on available time  
- 🔹 **Efficiency Scoring** → Evaluates quality of study plan  
- 🔹 **AI Suggestions** → Improves learning outcomes  

> This ensures **context-aware dynamic planning**, not static scheduling.

---

## ⚙️ System Workflow

### 1. Input
- Time (Days / Hours / Minutes)
- Subjects
- Priority OR natural language input

### 2. Processing
- Converts time into total minutes  
- Applies weighted distribution  
- Generates structured time slots  
- Computes efficiency score  

### 3. Output
- Optimized study plan  
- Time-slot schedule  
- Break & revision allocation  
- AI suggestions  
- (Optional) Calendar events  

---

## 📅 Google Calendar Integration

This project integrates with **Google Calendar API** to:

- Automatically create study sessions as calendar events  
- Schedule tasks sequentially with accurate timing  
- Trigger notifications exactly at session start time  

### 🔐 Setup Instructions:
1. Go to Google Cloud Console  
2. Enable **Google Calendar API**  
3. Create OAuth credentials  
4. Download and rename file to `my_credentials.json`  
5. Place it in the project root  
6. Run the application and authenticate  

⚠️ **Note:**  
Credentials are not included in the repository for security reasons.

---

## 🏗️ Project Structure

```plaintext
project-root/
│
├── app.py                      # Main application logic
├── scheduler.py               # Scheduling algorithm
├── calendar_integration.py    # Google Calendar integration
├── prompt_parser.py           # NLP processing
├── utils.py                   # Helper functions
├── sample_input.json
├── requirements.txt
└── README.md
```


---

## ▶️ How to Run

### 1. Install dependencies:
```bash
pip install -r requirements.txt
```

### Run the application:
python app.py

### Choose mode:
1 → Manual Mode
2 → AI Mode


## 📊 Sample Output

📅 OPTIMIZED STUDY PLAN:

TOC → 90 mins  
FSD → 90 mins  

⏸ Break Time: 15 mins  
🔁 Revision Time: 18 mins  

⏰ TIME-SLOT PLAN:

09:00 - 09:50 → TOC  
10:00 - 10:40 → TOC  
10:40 - 11:30 → FSD  
11:40 - 12:20 → FSD  

🧠 Plan Efficiency Score: 66%  
⚠️ Needs Improvement  

💡 Suggestions:
• Add more revision for better retention  
• Follow 50-10 focus cycles  


## 🔐 Security Considerations
Credentials (my_credentials.json, token.json) are excluded using .gitignore
No sensitive data is stored in the repository
OAuth authentication ensures secure access

## ⚡ Performance & Efficiency
Lightweight implementation (<1MB repository)
No heavy frameworks or dependencies
Optimized scheduling algorithm
Fast execution with minimal resource usage


## 🧪 Testing & Validation
Tested for:
Manual input scenarios
AI-based natural language input
Edge cases (low time, equal priority)
Google Calendar integration

## 🌍 Real-World Impact
This project helps students:
Improve productivity
Make better time decisions
Reduce planning stress
Follow structured learning

## 💡 Why This Project Stands Out
Combines AI + scheduling + automation
Supports both structured & natural input
Implements decision-based logic
Integrates real Google services
Provides actionable insights, not just output
Clean, modular, and scalable design

## 🚀 Future Enhancements
Web interface (Flask / React)
Performance tracking dashboard
Adaptive learning based on past behavior
Google Sheets integration for analytics

🏁 Conclusion

The Smart Study Planner Assistant demonstrates how AI-driven decision-making combined with real-world integrations can create impactful productivity tools.

It is scalable, practical, and designed for real users — not just a prototype.

