# **Project Documentation: N.O.V.A. | MaxHP**

*(Nutrition Optimization & Vitality Agent)*

---

## **1. Executive Summary**

**Project Name:** N.O.V.A. (Telegram Handle: `@NovaMaxHP_bot`)
**Mission:** To serve as an adaptive, gamified AI health companion that increases the user's "Max HP" (longevity, performance, and resilience) through frictionless tracking, contextual workout generation, and empathetic, state-driven coaching.
**Target Audience:** A two-player party.

* **Player 1:** Focuses on combat sports (Muay Thai), explosive power, and structured strength conditioning.
* **Player 2:** A commercial pilot requiring extreme flexibility, travel-friendly routines, and recovery-focused sessions to combat an erratic schedule and jet lag.

## **2. Core Philosophy (The N.O.V.A. Directive)**

* **Increase Max HP (Longevity over Burnout):** The system prioritizes injury prevention, consistent recovery, and sustainable nutrition over extreme, rapid weight loss or overtraining.
* **The Gentle Coach:** N.O.V.A. does not punish missed days or imperfect diets. It acknowledges reality (e.g., flight fatigue, holidays) and recalculates the optimal next step to keep the "run" alive.
* **State-Driven, Not Calendar-Driven:** Workouts and diet nudges are generated based on a 14-day rolling history of what actually happened, not what was hypothetically scheduled.

---

## **3. System Architecture & Tech Stack**

* **User Interface:** Telegram Bot API (allows photo uploads, text chat, and highly accessible mobile use).
* **Brain / Orchestration:** LangGraph (manages conversational state, routes tasks between nutrition/workout nodes, and handles the 14-day memory).
* **Intelligence Engine:** Multimodal LLM (processes meal images for macro extraction, generates context-aware text responses and workout programming).
* **Database:** Google Sheets (One private workbook per user acting as the backend ledger and visualization dashboard).

---

## **4. Database Schema (Google Sheets)**

Each user possesses a private Google Sheets workbook containing three primary tabs.

### **Tab 1: Profile & Goals (The Control Center)**

Stores overarching targets and static physical data. N.O.V.A. reads this to understand current objectives.

| Attribute | Example Value | Last Updated |
| --- | --- | --- |
| Height | 174 cm | 2026-03-01 |
| Current Weight | 75 kg | 2026-03-08 |
| Goal Weight | 73 kg | 2026-03-01 |
| Daily Target Calories | 2600 kcal | 2026-03-01 |
| Primary Workout Focus | Explosive Power / Core | 2026-03-05 |
| Weekly Goal | Hit 150g protein consistently | 2026-03-08 |

### **Tab 2: Daily Tracker (HP & Stamina Log)**

Logs daily metrics. Blank rows indicate missed days (which N.O.V.A. interprets as rest, travel, or off-grid time).

| Date | Morning Weight | Calories | Protein (g) | Carbs (g) | Fats (g) | AI Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-03-07 | 75.2 | 2800 | 140 | 300 | 80 | High carb day. |
| 2026-03-08 | 75.0 | 1200 | 60 | 100 | 40 | Partial log. |

### **Tab 3: Workout History (Experience Points)**

Logs completed training to ensure progressive overload and track fatigue.

| Date | Workout Type | Key Lifts / Drills | RPE / Feel |
| --- | --- | --- | --- |
| 2026-03-06 | Strength | Squats 3x5, Pallof Press 3x10 | 8/10, strong core |
| 2026-03-07 | Muay Thai | Heavy bag 5 rounds, clinching | 9/10, high cardio |

---

## **5. LangGraph State & Memory Logic**

The LangGraph `AgentState` holds the active context for every interaction.

* **The 14-Day Memory Window:** Upon receiving a message, N.O.V.A. fetches the `Profile & Goals` tab and only the last 14 rows of the `Daily Tracker` and `Workout History`. This prevents token overload while providing exact context on recent fatigue, diet trends, and consistency.
* **Dynamic Goal Pushback (Reality Check):** If a user attempts to set an unrealistic goal (e.g., losing 5kg in two weeks), an Evaluation Node flags it. N.O.V.A. will warn the user about the loss of athletic performance/Max HP and suggest a sustainable timeline.

---

## **6. Key Features & Workflows**

### **A. Frictionless Nutrition Tracking**

* **Input:** User sends a photo of a meal.
* **Process:** Vision LLM estimates ingredients, portion sizes, and macros.
* **Output:** N.O.V.A. updates the Google Sheet with the new macro totals and replies with a quick status update (e.g., *"Logged! You have 60g of protein remaining for today to hit your MaxHP goal."*).

### **B. Context-Aware Workout Generation**

* **Input:** User requests a workout (e.g., *"I'm at the gym, what's today?"*).
* **Process:** N.O.V.A. checks the 14-day history. It identifies what muscle groups are fatigued, what the current `Primary Workout Focus` is, and the user's available equipment.
* **Output:** Generates a highly specific routine (Warm-up, Main Lifts/Conditioning, Cooldown) tailored exactly to the user's current physical state.

### **C. Proactive Coaching (The Gentle Nudges)**

* **The Morning Briefing:** Reviews yesterday's data. If sugar was high, it suggests complex carbs. If calories were dangerously low, it prompts nutrient-dense recovery foods (avocados, nuts).
* **The Weekly Review:** Conducted on Sundays. Analyzes the week's consistency, sets a low-pressure focus for the upcoming week, and updates the `Weekly Goal` field in the database.

---

## **7. Player Profiles (Initial Context)**

### **Player 1: The Striker Build**

* **Discipline:** Muay Thai & Strength Conditioning (Targeting 6 sessions/week).
* **Key Stats:** 75 kg, ~10-15% body fat. Supplementing 6g Creatine daily.
* **Training Priorities:** Core anti-rotation (Pallof press, woodchoppers), back strength, explosive power (jump squats), and injury prevention (rotator cuff, scapular stabilizers).

### **Player 2: The Aviator Build**

* **Discipline:** Adaptive maintenance and longevity.
* **Key Stats:** Commercial Pilot.
* **Training Priorities:** Counteracting cockpit posture, managing jet lag, hotel-friendly mobility routines, and zero-guilt schedule adjustments when grounded or fatigued from long-haul flights.