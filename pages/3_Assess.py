"""
SkillSherpa: Assessor & AI Code Viva Verification
Generates randomized MCQs + AI Code Viva defense with anti-copy checks and live adaptive re-planning.
"""

import streamlit as st
import time
import re
from datetime import datetime
from ui import inject_theme, render_sidebar, render_agent_collaboration_panel, render_page_header, render_goal_diff_alert
from data_loader import init_session_state, get_roles, append_agent_log
from agents import orchestrator

inject_theme()
init_session_state()
render_sidebar()
render_goal_diff_alert()

user = st.session_state.user
target_role = user["target_role"]
roles = get_roles()
role_skills = roles.get(target_role, {}).get("skills", {})

render_page_header(
    title="🎯 Skill Verification & AI Code Viva",
    subtitle="Prove authentic competence through conceptual challenges, project evidence, and code defense.",
    badge_text="Anti-Copy Rubric Active"
)

# -------------------------------------------------------------
# SKILL SELECTOR
# -------------------------------------------------------------
unverified_skills = [s for s in role_skills if s not in user["verified_skills"]]
all_role_skills = list(role_skills.keys())

default_skill = st.session_state.get("selected_assessment_skill")
if not default_skill or default_skill not in all_role_skills:
    default_skill = unverified_skills[0] if unverified_skills else all_role_skills[0]

current_skill_idx = all_role_skills.index(default_skill)

selected_skill = st.selectbox(
    "Select Skill for Verification:",
    options=all_role_skills,
    index=current_skill_idx,
    key="assess_skill_select"
)

target_level = role_skills.get(selected_skill, {}).get("target_level", 2)

# Check if resources were marked watched (Mastery Gate)
watched_list = user.get("watched_resources", [])
is_prep_done = (selected_skill in watched_list) or (selected_skill in user["verified_skills"])

if not is_prep_done:
    st.warning(
        f"⚠️ **Mastery Gate Advisory:** You have not marked the trail resources for **{selected_skill}** as reviewed. "
        f"You can still proceed to test your knowledge directly (Fast-track placement mode)!"
    )

# -------------------------------------------------------------
# LOAD OR GENERATE ASSESSMENT
# -------------------------------------------------------------
if "current_assessment" not in st.session_state or st.session_state.get("assessment_skill") != selected_skill:
    assessment_data = orchestrator.assessor.generate_assessment(selected_skill)
    st.session_state.current_assessment = assessment_data
    st.session_state.assessment_skill = selected_skill
    st.session_state.assessment_start_time = time.time()

assessment = st.session_state.current_assessment
questions = assessment.get("questions", [])
viva_challenge = assessment.get("viva_challenge", {})

st.markdown(
    f"""
    <div class="sherpa-card-highlight" style="margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3 style="color: #F8FAFC; margin: 0;">Expedition Challenge: {selected_skill}</h3>
            <span class="badge-blue">Target: Level {target_level} Mastery</span>
        </div>
        <p style="color: #CBD5E1; font-size: 0.9rem; margin-top: 6px;">
            Complete the 3 conceptual edge-case queries, link your working GitHub project repository, and defend your architecture in the AI Viva.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------------
# ASSESSMENT FORM
# -------------------------------------------------------------
with st.form("assessment_submission_form"):
    st.markdown("#### Part 1: Conceptual Edge-Case Queries (MCQ)")
    user_answers = {}

    for q in questions:
        q_id = q.get("id", 1)
        st.markdown(f"**Q{q_id}. {q.get('question')}**")
        options = q.get("options", ["Option A", "Option B", "Option C", "Option D"])
        choice = st.radio(
            label=f"Options for Q{q_id}:",
            options=options,
            key=f"mcq_{selected_skill}_{q_id}",
            label_visibility="collapsed"
        )
        user_answers[q_id] = options.index(choice) if choice in options else 0
        st.markdown("<br/>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Part 2: Hands-On Project Evidence (GitHub Proof)")
    st.caption("Recruiters and institutions require an auditable repository link to verify hands-on execution.")
    
    project_url = st.text_input(
        "GitHub Repository URL:",
        value=f"https://github.com/{user['name'].lower().replace(' ', '-')}/{selected_skill.lower().replace(' ', '-').replace('/', '-')}-demo",
        placeholder="https://github.com/username/project-repo"
    )

    st.markdown("---")
    st.markdown("#### Part 3: AI Code Viva (Explain Your Implementation)")
    viva_q = viva_challenge.get("question", f"Explain the architectural decisions and tricky edge cases you solved while working on {selected_skill}.")
    st.markdown(f"**Sherpa Viva Prompt:** *\"{viva_q}\"*")
    
    viva_answer = st.text_area(
        "Your Defense (In your own words):",
        height=140,
        placeholder="Explain how you handled data errors, state lifecycle, or performance trade-offs. Authentic struggle and honest reflection are graded higher than generic definitions!"
    )

    # Optional simulated quick-fail / quick-pass buttons for demo speed
    col_submit, col_demo_fail, col_demo_pass = st.columns([1.5, 1, 1])
    
    with col_submit:
        submitted = st.form_submit_button("🛡️ Submit Evidence to AssessorAgent", use_container_width=True)
    with col_demo_fail:
        demo_fail = st.form_submit_button("💥 [Demo] Simulate Fail (<50%)", use_container_width=True)
    with col_demo_pass:
        demo_pass = st.form_submit_button("🌟 [Demo] Simulate Pass (>=85%)", use_container_width=True)

# -------------------------------------------------------------
# EVALUATION & ADAPTIVE ORCHESTRATION
# -------------------------------------------------------------
if submitted or demo_fail or demo_pass:
    elapsed_seconds = int(time.time() - st.session_state.get("assessment_start_time", time.time() - 30))
    if elapsed_seconds <= 0:
        elapsed_seconds = 25

    # Check project URL format
    url_pattern = r"^https?://github\.com/[\w\-_]+/[\w\-_]+.*"
    if not re.match(url_pattern, project_url.strip()) and not demo_fail:
        st.error("⚠️ Invalid Repository URL. Proof requires a valid GitHub link format: `https://github.com/owner/repository`")
        st.stop()

    if demo_fail:
        mcq_pct = 40
        viva_ans_eval = "I just used default settings and copied a template."
        elapsed = 40
    elif demo_pass:
        mcq_pct = 95
        viva_ans_eval = (
            "I structured the application with clean separation of concerns. "
            "To handle asynchronous API errors and state race conditions, I created an abort controller and fallback mock state. "
            "The hardest bug was an infinite re-render loop caused by missing dependency array references, which I resolved by memoizing handlers."
        )
        elapsed = 60
    else:
        # Score MCQs
        correct_count = 0
        for q in questions:
            q_id = q.get("id", 1)
            correct_idx = q.get("correct_index", 0)
            if user_answers.get(q_id) == correct_idx:
                correct_count += 1
        mcq_pct = int(round((correct_count / max(1, len(questions))) * 100))
        viva_ans_eval = viva_answer
        elapsed = elapsed_seconds

    # Dispatch to Orchestrator event: quiz_completed
    with st.spinner("🤖 Orchestrator coordinating Assessor, Mentor, and Curator..."):
        eval_result = orchestrator.handle_event("quiz_completed", {
            "skill": selected_skill,
            "target_level": target_level,
            "mcq_score": mcq_pct,
            "viva_answer": viva_ans_eval,
            "time_taken": elapsed,
            "project_url": project_url,
            "user_data": user
        })

    grade = eval_result.get("grade", {})
    action = eval_result.get("action", "")

    st.markdown("---")
    st.markdown("### 📋 Verification Outcome & Anti-Copy Report")

    # Anti-Copy Flag Banner
    if grade.get("anti_copy_flag"):
        st.error(
            "⚠️ **Anti-Copy Detection Triggered:** The submission was flagged by our timing or similarity heuristics. "
            "SkillSherpa proves authentic competence — please explain in your genuine firsthand words without copy-pasting. "
            "This flag has been logged to the Proof Passport history."
        )

    # Outcome Layout
    col_score, col_feedback = st.columns([1, 2])

    with col_score:
        score_val = grade.get("overall_score", 0)
        score_color = "#10B981" if grade.get("passed") else "#EF4444"
        st.markdown(
            f"""
            <div class="sherpa-card" style="text-align: center;">
                <div style="font-size: 0.8rem; color: #94A3B8;">COMPREHENSIVE SCORE</div>
                <div style="font-size: 3rem; font-weight: 900; color: {score_color};">{score_val}%</div>
                <div style="font-size: 0.85rem; color: #CBD5E1;">
                    MCQ: {grade.get('mcq_score')}% • Viva: {grade.get('viva_score')}%
                </div>
                <div style="margin-top: 10px;">
                    <span class="{'badge-green' if grade.get('passed') else 'badge-red'}">
                        {'🟢 EVIDENCE VERIFIED' if grade.get('passed') else '🔴 RE-TRAIL REQUIRED'}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_feedback:
        st.markdown(
            f"""
            <div class="sherpa-card">
                <h4 style="color: #38BDF8; margin-top: 0;">🧭 Sherpa Mentor Feedback</h4>
                <p style="color: #F8FAFC; font-size: 0.95rem; line-height: 1.6;">
                    {eval_result.get('mentor_message')}
                </p>
                <div style="margin-top: 12px; font-size: 0.8rem; color: #94A3B8;">
                    <strong>Viva Rubric Breakdown:</strong><br/>
                    • Technical Correctness: {grade.get('rubric', {}).get('correctness', 80)}%<br/>
                    • Depth & Trade-offs: {grade.get('rubric', {}).get('depth', 75)}%<br/>
                    • Authentic Originality: {grade.get('rubric', {}).get('originality', 85)}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    if grade.get("passed"):
        st.balloons()
        st.success(
            f"🎉 **Congratulations!** Your mastery in **{selected_skill}** is officially verified and stamped onto your **Proof-of-Skill Passport**! "
            f"Newly unlocked opportunities are now visible in the Opportunities tab."
        )
    else:
        st.info(
            "🧗 **Adaptive Trail Updated:** No stress! CuratorAgent has automatically inserted foundational revision checkpoints "
            "and simplified practice exercises into your Mountain Trail. Your Job Readiness score is protected and was not penalized."
        )

st.markdown("<br/>", unsafe_allow_html=True)
render_agent_collaboration_panel()

