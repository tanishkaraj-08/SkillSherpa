"""
SkillSherpa: AI Sherpa Mentor Chat
Context-aware, empathic AI guide adapting to learner type, language (Tanglish/English), and recent performance.
"""

import streamlit as st
from ui import inject_theme, render_sidebar, render_agent_collaboration_panel, render_page_header, render_goal_diff_alert
from data_loader import init_session_state, get_roles, append_agent_log
from agents import orchestrator
from scoring import compute_job_readiness

inject_theme()
init_session_state()
render_sidebar()
render_goal_diff_alert()

user = st.session_state.user
target_role = user["target_role"]
roles = get_roles()
role_info = roles.get(target_role, {})
readiness = compute_job_readiness(user["verified_skills"], role_info.get("skills", {}), user.get("simulated_days", 0))

render_page_header(
    title=f"🧗‍♂️ AI Sherpa Mentor",
    subtitle=f"1-on-1 personalized guidance for {user['name']} • Goal: {target_role} • Mode: {user['learner_type']}",
    badge_text="Tanglish Enabled" if user.get("tanglish_mode") else "Warm English"
)

# Top Context Banner
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        f"""
        <div class="sherpa-card" style="padding: 12px; font-size: 0.85rem;">
            <strong>Learner Profile:</strong> {user['avatar']} {user['name']}<br/>
            <span style="color: #94A3B8;">Type: {user['learner_type']} | Board: {user['board']}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
with c2:
    st.markdown(
        f"""
        <div class="sherpa-card" style="padding: 12px; font-size: 0.85rem;">
            <strong>Summit Readiness:</strong> <span style="color: #38BDF8; font-weight: 700;">{readiness}%</span><br/>
            <span style="color: #94A3B8;">Verified Proofs: {len(user['verified_skills'])} skills</span>
        </div>
        """,
        unsafe_allow_html=True
    )
with c3:
    st.markdown(
        f"""
        <div class="sherpa-card" style="padding: 12px; font-size: 0.85rem;">
            <strong>Tone Setting:</strong> <span style="color: #10B981; font-weight: 700;">{'Tanglish Vernacular' if user.get('tanglish_mode') else 'Empathetic English'}</span><br/>
            <span style="color: #94A3B8;">Pressure: {'Free (No penalties)' if user.get('pressure_free_mode') else 'Active Pace'}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br/>", unsafe_allow_html=True)

# -------------------------------------------------------------
# QUICK SUGGESTED QUESTIONS
# -------------------------------------------------------------
st.markdown("##### 💡 Suggested Questions for Your Sherpa:")
q_cols = st.columns(3)

with q_cols[0]:
    if st.button("🧗 What should I focus on this week?", use_container_width=True):
        st.session_state.pending_user_prompt = "What specific trail milestone should I focus on this week to make progress without feeling overwhelmed?"
with q_cols[1]:
    if st.button("🤯 I feel stuck and confused by errors", use_container_width=True):
        st.session_state.pending_user_prompt = "I feel totally stuck and frustrated by coding errors. How do experienced developers overcome this?"
with q_cols[2]:
    if st.button("💼 Will companies hire me without CS degree?", use_container_width=True):
        st.session_state.pending_user_prompt = "Will recruiters really hire me if I come from a non-CS or State board background?"

# -------------------------------------------------------------
# CHAT LOG DISPLAY
# -------------------------------------------------------------
chat_container = st.container()

with chat_container:
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.chat_message("user", avatar="🧗").markdown(msg["content"])
        else:
            st.chat_message("assistant", avatar="🧭").markdown(msg["content"])

# -------------------------------------------------------------
# CHAT INPUT & RESPONSE
# -------------------------------------------------------------
user_input = st.chat_input("Ask your Sherpa anything (concepts, project bugs, career doubts, anxiety)...")

# Check if clicked from quick prompt buttons
if "pending_user_prompt" in st.session_state and st.session_state.pending_user_prompt:
    user_input = st.session_state.pending_user_prompt
    st.session_state.pending_user_prompt = None

if user_input:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with chat_container:
        st.chat_message("user", avatar="🧗").markdown(user_input)

    # Generate Mentor response
    profile_summary = (
        f"Name: {user['name']}, Board: {user['board']}, Branch: {user['branch']}, "
        f"Learner Type: {user['learner_type']}, Target: {target_role}, Readiness: {readiness}%, "
        f"Verified: {list(user['verified_skills'].keys())}, Failed attempts: {len(user.get('failed_attempts', []))}"
    )

    with st.spinner("🧗‍♂️ Sherpa is drafting advice..."):
        ai_reply = orchestrator.mentor.get_chat_response(
            user_msg=user_input,
            profile_summary=profile_summary,
            tanglish=user.get("tanglish_mode", False)
        )

    st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
    with chat_container:
        st.chat_message("assistant", avatar="🧭").markdown(ai_reply)

    append_agent_log(
        "MentorAgent", "🧗‍♂️", "Learner",
        f"Answered learner query with tailored {'Tanglish' if user.get('tanglish_mode') else 'English'} guidance."
    )
    st.rerun()

st.markdown("<br/>", unsafe_allow_html=True)
render_agent_collaboration_panel()

