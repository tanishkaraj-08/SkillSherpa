"""
SkillSherpa Data Loader & State Management
Handles persistent JSON file access and Streamlit session_state lifecycle.
"""

import json
import os
import streamlit as st
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def load_json(filename: str) -> dict:
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json(filename: str, data: dict):
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_roles():
    return load_json("roles.json")

def get_resources():
    return load_json("resources.json")

def get_opportunities():
    return load_json("opportunities.json")

def get_jargon():
    return load_json("jargon.json")

def get_personas():
    return load_json("personas.json")

def get_cohort():
    return load_json("cohort.json")

def init_session_state():
    """Initializes all necessary session_state keys with sensible defaults."""
    personas = get_personas()
    default_persona = personas.get("arun", {})

    if "user" not in st.session_state:
        st.session_state.user = {
            "name": default_persona.get("name", "Arun Kumar"),
            "avatar": default_persona.get("avatar", "🏕️"),
            "board": default_persona.get("board", "State Board"),
            "branch": default_persona.get("branch", "Information Technology"),
            "target_role": default_persona.get("target_role", "Full Stack Developer"),
            "learner_type": default_persona.get("learner_type", "Foundation"),
            "weekly_hours": default_persona.get("weekly_hours", 10),
            "stress_level": default_persona.get("stress_level", "High"),
            "current_comfort": default_persona.get("current_comfort", "Beginner - HTML only"),
            "self_ratings": default_persona.get("self_ratings", {
                "HTML/CSS": 3, "Git & GitHub": 1, "JavaScript": 1, "React": 1, "Node.js": 1, "SQL": 1
            }),
            "verified_skills": default_persona.get("verified_skills", {
                "HTML/CSS": {
                    "level": 2,
                    "verified_date": "2026-10-15",
                    "quiz_score": 85,
                    "viva_score": 80,
                    "project_url": "https://github.com/arun-dev/state-board-notes-portal",
                    "attempts": 1,
                    "time_taken_days": 6
                }
            }),
            "failed_attempts": default_persona.get("failed_attempts", []),
            "watched_resources": ["HTML/CSS"],
            "badges": ["Mountain Pioneer", "First Evidence Logged"],
            "streak_days": 4,
            "pressure_free_mode": True,
            "tanglish_mode": True,
            "simulated_days": 0
        }

    if "agent_log" not in st.session_state:
        st.session_state.agent_log = [
            {
                "time": "10:14:02",
                "agent": "OrchestratorAgent",
                "emoji": "🧭",
                "to_agent": "ProfilerAgent",
                "message": "Initialized zero-assumption profile for Arun Kumar. Target: Full Stack Developer."
            },
            {
                "time": "10:14:03",
                "agent": "ProfilerAgent",
                "emoji": "🔍",
                "to_agent": "GapAnalystAgent",
                "message": "Learner type classified as 'Foundation' (State Board background, High anxiety). Recommend step-by-step small wins & Tanglish support."
            },
            {
                "time": "10:14:04",
                "agent": "GapAnalystAgent",
                "emoji": "📊",
                "to_agent": "CuratorAgent",
                "message": "Assessed skills: HTML/CSS verified at Level 2. Critical gaps in JavaScript, React, and Node.js. Job Readiness: 22%."
            },
            {
                "time": "10:14:05",
                "agent": "CuratorAgent",
                "emoji": "🗺️",
                "to_agent": "MentorAgent",
                "message": "Assembled tailored mountain roadmap: Camp 1 (JavaScript ES6 Async) -> Camp 2 (React Essentials) -> Camp 3 (Node.js REST)."
            }
        ]

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": "Vanakkam Arun! 🧗‍♂️ I am your Sherpa. We climb this mountain one step at a time — no pressure, pure verified mastery. How are you feeling today about starting JavaScript?"
            }
        ]

    if "goal_diff" not in st.session_state:
        st.session_state.goal_diff = None

def load_persona(persona_key: str):
    """Loads a specific pre-defined persona into session_state."""
    personas = get_personas()
    p = personas.get(persona_key)
    if not p:
        return
        
    st.session_state.user["name"] = p["name"]
    st.session_state.user["avatar"] = p["avatar"]
    st.session_state.user["board"] = p["board"]
    st.session_state.user["branch"] = p["branch"]
    st.session_state.user["target_role"] = p["target_role"]
    st.session_state.user["learner_type"] = p["learner_type"]
    st.session_state.user["weekly_hours"] = p["weekly_hours"]
    st.session_state.user["stress_level"] = p["stress_level"]
    st.session_state.user["current_comfort"] = p["current_comfort"]
    st.session_state.user["self_ratings"] = dict(p["self_ratings"])
    st.session_state.user["verified_skills"] = dict(p["verified_skills"])
    st.session_state.user["failed_attempts"] = list(p["failed_attempts"])
    st.session_state.user["pressure_free_mode"] = p.get("pressure_free_mode", False)
    st.session_state.user["tanglish_mode"] = (p["learner_type"] == "Foundation")
    st.session_state.user["watched_resources"] = list(p["verified_skills"].keys())
    st.session_state.user["simulated_days"] = 0
    st.session_state.goal_diff = None
    
    # Reset chat history for persona
    if p["learner_type"] == "Foundation":
        intro = f"Vanakkam {p['name'].split()[0]}! 🧗‍♂️ I am your Sherpa. We climb this mountain one step at a time — zero pressure, pure verified mastery. Bayapadama start pannunga!"
    elif p["learner_type"] == "Bridge":
        intro = f"Welcome {p['name'].split()[0]}! 🧬 Your biology background is a massive superpower. In bioinformatics, algorithms are easy to learn, but biology intuition is rare. Ready to bridge the gap?"
    else:
        intro = f"Hey {p['name'].split()[0]}! ⚡ No countdown timers, no competitive leaderboards. We focus 100% on building high-impact real-world systems you actually own."

    st.session_state.chat_history = [{"role": "assistant", "content": intro}]
    
    # Append to agent log
    append_agent_log(
        "OrchestratorAgent", "🧭", "AllAgents",
        f"Loaded Persona '{p['name']}' ({p['learner_type']} Profile). Re-running Gap Analysis and Trail Curator."
    )

def append_agent_log(agent: str, emoji: str, to_agent: str, message: str):
    """Appends an event to the global live agent collaboration log."""
    now_str = datetime.now().strftime("%H:%M:%S")
    if "agent_log" not in st.session_state:
        st.session_state.agent_log = []
    st.session_state.agent_log.insert(0, {
        "time": now_str,
        "agent": agent,
        "emoji": emoji,
        "to_agent": to_agent,
        "message": message
    })
    # Keep last 50 entries
    if len(st.session_state.agent_log) > 50:
        st.session_state.agent_log.pop()

