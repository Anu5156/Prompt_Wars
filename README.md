![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Status](https://img.shields.io/badge/Status-Active-green)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)

# 🧠 Adaptive AI Study Planning System

> 🚀 A hybrid AI system that generates, critiques, and optimizes personalized study plans using a multi-agent pipeline.

---

## ⚡ Overview

This project is an **AI-driven study planning system** that goes beyond traditional schedulers by combining:

- 📊 Rule-based time allocation  
- 🤖 LLM-powered reasoning  
- 🔁 Multi-agent feedback loops  

👉 The result: **optimized, adaptive, and continuously refined study plans**

---

## 🎯 Problem

Students struggle with:
- Poor time management  
- Lack of prioritization  
- Static and ineffective study schedules  

---

## 💡 Solution

This system generates **dynamic, priority-based study plans** using:

- Natural language input (AI parsing)
- Weighted scheduling algorithms
- AI critique + optimization loops

👉 Not just a planner — a **decision-making system**

---

## 🧠 Core Innovation

### 🔹 Multi-Agent AI Pipeline

User Input
↓
AI Parser (LLM extraction)
↓
Rule-Based Scheduler
↓
AI Critic Agent
↓
AI Optimizer Agent
↓
AI Evaluator Agent
↓
Final Optimized Plan

---

### ✨ What Makes It Unique

- Multi-agent prompt engineering (Planner → Critic → Optimizer → Evaluator)
- Hybrid AI system (deterministic + LLM reasoning)
- Iterative plan refinement using feedback loops
- Context-aware scheduling (not static timetables)

---

## 🧠 Key Technical Challenges & Solutions

- **Ambiguous user input**  
  → Solved using LLM-based subject & priority extraction  

- **Balancing AI vs algorithmic control**  
  → Hybrid system ensures stability + intelligence  

- **Multi-agent coordination**  
  → Designed structured pipeline for Critic → Optimizer flow  

- **Maintaining schedule consistency after AI changes**  
  → Post-optimization validation ensures feasibility  

---

## 🚀 Features

- ✅ Priority-Based Scheduling (High / Medium / Low)  
- ✅ Natural Language Input (AI Mode)  
- ✅ Dynamic Time Allocation Algorithm  
- ✅ AI Critique & Optimization  
- ✅ Efficiency Scoring System  
- ✅ Structured Timetable Generation  
- ✅ Google Calendar Integration  
- ✅ PDF + CSV Export  
- ✅ Study Analytics Visualization  
- ✅ Progress Tracking  

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **Scheduling Engine:** Custom Weighted Algorithm  
- **AI Layer:** LLM-based multi-agent system  
- **Visualization:** Pandas + Altair  
- **Integration:** Google Calendar API  

---

## 🔄 How It Works

1. User provides:
   - Subjects + priorities OR natural language input  

2. AI Parser:
   - Extracts structured data using LLM  

3. Scheduler:
   - Allocates time using weighted distribution  

4. AI Layer:
   - Critic detects inefficiencies  
   - Optimizer improves plan  
   - Evaluator scores effectiveness  

5. Output:
   - Study plan  
   - Timetable  
   - Efficiency score  
   - Calendar events  
   - Analytics  

---

## 📊 Example Output

- Optimized study timetable  
- AI-generated improvement suggestions  
- Efficiency score (plan quality metric)  
- Exportable formats (PDF, CSV, Calendar)

---

## 🌐 Live Demo

🔗 https://promptwars-r86ripmbuk27tyamz5jx62.streamlit.app/

---

## 🎥 Demo Video

[![Watch Demo](https://img.shields.io/badge/▶️%20Watch%20Demo-Click%20Here-blue)](https://www.youtube.com/watch?v=rLS3vJWCYyY)

---

## 📸 Screenshots

### 🔹 Input Interface
![Input](assets/screenshots/input.png)

### 🔹 Study Plan Output
![Plan](assets/screenshots/plan.png)

### 🔹 Timetable View
![Table](assets/screenshots/table.png)

### 🔹 AI Mode
![AI Mode](assets/screenshots/ai_mode.png)

### 🔹 Study Analytics
![Study Analytics](assets/screenshots/study_analytics.png)

---

## 🏗️ Project Structure

project-root/
│
├── app_streamlit.py           # Main UI (Streamlit app)
├── scheduler.py               # Core scheduling engine
├── calendar_integration.py    # Google Calendar integration
├── prompt_parser.py           # NLP processing
├── utils.py                   # Helper functions
├── requirements.txt           # Dependencies
│
├── tests/
│ └── test_scheduler.py        # Unit tests
│
└── assets/
└── screenshots/
         |
         |__ input.png          # Input Interface
         |__ plan.png           # Study Plan Output
         |__ table.png          # Timetable View
         |__ ai_mode.png        # AI Mode
         

