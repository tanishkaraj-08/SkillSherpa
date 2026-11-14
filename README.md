# 🧗‍♂️ SkillSherpa: The Trust Layer for Skills

> **"Certificates prove you watched. We prove you can do."**

SkillSherpa is an agentic AI learning and verification platform that transforms career upskilling into an auditable mountain expedition. From **Base Camp** (your verified foundation) to your **Summit** (your target role), a collaborative swarm of 7 specialized AI agents detects skill gaps, curates prerequisite-safe trails, enforces mastery gates through real code evidence and anti-copy AI viva defenses, adaptively recalculates trails upon failure, and provides recruiters and academic institutions with cryptographic, explainable proof of competency.

---

## 🏗️ Multi-Agent Architecture & Event Flow

```
                      +-----------------------------+
                      |     OrchestratorAgent       |
                      |   (Central Event Router)    |
                      +--------------+--------------+
                                     |
    +-----------------+--------------+--------------+-----------------+
    |                 |                             |                 |
    v                 v                             v                 v
[onboarding_done] [quiz_completed]            [goal_changed]    [skill_expired]
    |                 |                             |                 |
    |                 +--> (Score < 50%)            |                 +--> OpportunityAgent
    |                 |    AssessorAgent            |                      (Filters valid)
    |                 |          |                  |
    v                 |          v                  v
ProfilerAgent         |    MentorAgent        GapAnalystAgent
    |                 |          |                  |
    v                 |          v                  v
GapAnalystAgent       |    CuratorAgent       CuratorAgent
    |                 |    (Insert Revision)  (Instant <0.5s diff)
    v                 |
CuratorAgent          +--> (Score >= 70% + Viva)
                           AssessorAgent
                                 |
                                 v
                           Proof-Passport Stamp
                                 |
                                 v
                           OpportunityAgent
                           (Surfaces Newly Unlocked)
```

### The 7 Specialized Agents
1. **🔍 ProfilerAgent**: Zero-assumption intake engine analyzing educational board, anxiety levels, and pace to classify learners into *Foundation*, *Bridge*, *Pressure-Relief*, or *Fast-Track*.
2. **📊 GapAnalystAgent**: Compares verified proof levels vs target industry summit requirements to compute weighted Job Readiness (0-100%).
3. **🗺️ CuratorAgent**: Prerequisite-graph architect assembling free resources (freeCodeCamp, MDN, Kaggle, CS50), weekly quests, and mini-projects.
4. **🎯 AssessorAgent**: Dynamically generates fresh randomized conceptual questions and conducts the AI Code Viva Defense evaluated against a tripartite rubric (correctness, depth, originality) with timing and anti-copy heuristics.
5. **🧗‍♂️ MentorAgent**: Empathic sherpa adapting tone and vernacular language (Tanglish/English) to normalize failure and reduce coding anxiety.
6. **💼 OpportunityAgent**: Matches **strictly verified** evidence to 25+ real-world internships, hackathons, open-source bounties, and grants.
7. **🧭 OrchestratorAgent**: Event bus routing signals between agents with full audit trail logging to the live UI panel.

---

## ⚡ Fast Setup & Run

### Prerequisites
- Python 3.9+
- Recommended: Virtual environment (`venv`)

### 1. Installation
```bash
git clone <repo-url>
cd skillsherpa
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Optional: Live Gemini AI API Key
SkillSherpa contains an intelligent **deterministic mock engine** ensuring a **flawless demo even when offline or without an API key**. To enable live Google Gemini calls:
```bash
export GEMINI_API_KEY="your-gemini-api-key"
```

### 3. Launch App
```bash
streamlit run app.py
```
App will open automatically at `http://localhost:8501`.

---

## 🎬 5-Minute Flawless Hackathon Demo Script

Follow these steps for an end-to-end hackathon presentation:

| Step | Action | What to Point Out |
|---|---|---|
| **1. Zero-Assumption Onboarding** | In sidebar, click **"🏕️ Arun (State)"** | Highlight the tagline: *"Certificates prove you watched. We prove you can do."* Arun is a Tamil-medium State Board beginner. ProfilerAgent diagnoses him as **Foundation Profile** with Tanglish and Pressure-Free Mode active. Point out the **Start Here** page with simple Tanglish explanations of Hackathon, GitHub, and ATS. |
| **2. Confidence vs Reality** | Switch to the **Confidence vs Reality Meter** tab | Show the side-by-side comparison of self-ratings vs verified proof. Explain: *"Calibration = knowing yourself"*. Show the **Honest Learner** badge awarded when calibration ≥ 80%. |
| **3. Fail a Quiz & Adaptive Re-Plan** | Navigate to **Assess** page. Select JavaScript, and click **"💥 [Demo] Simulate Fail (<50%)"** | Watch the live **Agent Collaboration Log** fire: `AssessorAgent ➔ MentorAgent ➔ CuratorAgent`. Show the warm, non-shaming Mentor message in Tanglish (*"Calm-ah irunga, idhu romba normal..."*). Point out how the mountain roadmap inserted prerequisite revisions without docking readiness score. |
| **4. Pass a Quiz + AI Code Viva** | In **Assess**, select HTML/CSS, click **"🌟 [Demo] Simulate Pass (>=85%)"** | Balloons animate! Overall score 92%, Viva passed on originality rubric. Readiness score jumps. Go to **Opportunities** page: new junior roles and hackathons unlock with celebration badges! |
| **5. Instant Career Summit Pivot (<0.5s)** | In sidebar, change **Summit Goal** from *Full Stack Developer* to *Data Analyst* | Instant re-plan banner renders showing a **Skill Diff**: preserved skills carried over, new gaps calculated, deprecated items removed. |
| **6. Proof Passport & Recruiter Audit** | Open **Proof Passport & Recruiter View** | Per-skill evidence card showing quiz score, viva score, GitHub project URL, attempts, and honest history of failed attempts. Switch to **Recruiter Search** tab: filter candidates by verified skill and minimum level (e.g., SQL Level 2+). |
| **7. 100-Day Expiry Simulation** | In sidebar, toggle **"⏱️ Simulate +100 Days (Expiry)"** | Proof badge switches from **🟢 Valid** to **🔴 Expired (>90 days)**. Explain credential decay prevents stale certificates. |
| **8. Institution Analytics** | Open **Institution Dashboard** | 60-student cohort heatmap, top 5 missing skills bar chart, State Board vs CBSE equity breakdown, and 1-click CSV export for university deans. |

---

## 📊 Trust Layer Differentiators
- **Mastery Gate**: Watching resources only unlocks the assessment. Progressing to the next camp requires verified code and viva defense.
- **Explainable AI ("Why this?")**: Every resource, opportunity, and roadmap checkpoint contains an expander detailing the agent's exact algorithmic reasoning.
- **Anti-Copy Heuristic**: Evaluates timing velocity, similarity to reference solution, and code explanation depth.
- **Zero-Pressure Philosophy**: No streak loss, no countdown penalties, vernacular onboarding for first-generation engineers.

