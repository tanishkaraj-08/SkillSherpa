"""
SkillSherpa: Start Here (Zero-Assumption Beginner On-Ramp)
Demystifies tech culture, explains 5 core concepts in simple Tanglish+English, and offers a calm 7-day mini plan.
"""

import streamlit as st
from ui import inject_theme, render_sidebar, render_agent_collaboration_panel, render_page_header, render_goal_diff_alert
from data_loader import init_session_state, get_jargon

inject_theme()
init_session_state()
render_sidebar()
render_goal_diff_alert()

user = st.session_state.user

render_page_header(
    title="🌱 Start Here: Zero-Assumption Welcome",
    subtitle="No confusing acronyms, no gatekeeping. Everything you need to take your first steps with confidence.",
    badge_text="Beginner Haven"
)

st.markdown(
    """
    <div class="sherpa-card-highlight" style="margin-bottom: 24px;">
        <h3 style="color: #14B8A6; margin-top: 0;">👋 Welcome to the Mountain Base Camp!</h3>
        <p style="color: #E2E8F0; font-size: 1rem; line-height: 1.6;">
            If you come from a <strong>State Board</strong>, non-English medium, or non-Computer Science background, 
            you might feel like everyone else knows a secret language. <strong>They don't.</strong> Tech is just a set of tools, 
            and language is just communication. Your logic and determination are what truly matter.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------------
# 5 ESSENTIAL CARDS (Demystifying Tech Culture)
# -------------------------------------------------------------
st.markdown("### 🧩 The 5 Core Concepts You Need to Know")
st.caption("Explained simply in English and Tanglish.")

jargon_data = get_jargon()

five_terms = ["hackathon", "github", "open source", "internship", "portfolio"]

for term_key in five_terms:
    entry = jargon_data.get(term_key, {})
    if entry:
        st.markdown(
            f"""
            <div class="sherpa-card" style="margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <h4 style="color: #38BDF8; margin: 0;">💡 {entry['term']}</h4>
                    <span class="badge-blue">{entry['category']}</span>
                </div>
                <div style="color: #F8FAFC; font-size: 0.95rem; margin-bottom: 6px;">
                    <strong>In Plain English:</strong> {entry['english']}
                </div>
                <div style="color: #34D399; font-size: 0.88rem; background: rgba(6, 78, 59, 0.4); padding: 8px 12px; border-radius: 6px; margin-bottom: 6px; border-left: 3px solid #10B981;">
                    🗣️ <strong>Tanglish:</strong> {entry['tanglish']}
                </div>
                <div style="color: #94A3B8; font-size: 0.82rem;">
                    🎯 <strong>Sherpa Tip:</strong> {entry['tip']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<br/>", unsafe_allow_html=True)

# -------------------------------------------------------------
# YOUR FIRST 7 DAYS MINI PLAN
# -------------------------------------------------------------
st.markdown("### 📅 Your First 7 Days Mini Plan (Zero Pressure)")
st.caption("A gentle, low-stress itinerary designed to build momentum without overwhelm.")

plan_days = [
    {"day": "Day 1", "focus": "Base Camp Setup", "task": "Create a free GitHub account and customize your profile username.", "time": "20 mins"},
    {"day": "Day 2", "focus": "First Tag Written", "task": "Write your first 10 lines of HTML in a free browser editor (Codepen / Replit).", "time": "30 mins"},
    {"day": "Day 3", "focus": "Look at Real Code", "task": "Browse 1 open-source documentation page and notice how headings and links are formatted.", "time": "25 mins"},
    {"day": "Day 4", "focus": "Sherpa Check-In", "task": "Chat with the AI Sherpa Mentor in Tanglish and ask any questions on what felt confusing.", "time": "15 mins"},
    {"day": "Day 5", "focus": "Build a Profile Card", "task": "Assemble a simple card with your photo, name, and 3 personal interests using HTML.", "time": "45 mins"},
    {"day": "Day 6", "focus": "First Git Commit", "task": "Upload your profile card project to GitHub and copy the repository link.", "time": "30 mins"},
    {"day": "Day 7", "focus": "First Passport Stamp", "task": "Take the HTML/CSS verification in Assess to earn your very first verified level badge!", "time": "20 mins"}
]

for d in plan_days:
    st.markdown(
        f"""
        <div style="background: #1E293B; border-left: 4px solid #14B8A6; border-radius: 6px; padding: 10px 16px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <strong style="color: #38BDF8;">{d['day']}: {d['focus']}</strong><br/>
                <span style="color: #CBD5E1; font-size: 0.88rem;">{d['task']}</span>
            </div>
            <div style="color: #94A3B8; font-size: 0.8rem; font-weight: 600;">
                ⏱️ {d['time']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br/>", unsafe_allow_html=True)
render_agent_collaboration_panel()

