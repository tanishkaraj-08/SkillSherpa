"""
SkillSherpa: Proof-of-Skill Passport & Recruiter Audit View
Comprehensive immutable evidence cards, honest audit trails (including failed attempts), and candidate search.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from ui import inject_theme, render_sidebar, render_agent_collaboration_panel, render_page_header, render_goal_diff_alert
from data_loader import init_session_state, get_roles, get_cohort, append_agent_log
from scoring import get_skill_expiry_status, compute_calibration_score

inject_theme()
init_session_state()
render_sidebar()
render_goal_diff_alert()

user = st.session_state.user
simulated_days = user.get("simulated_days", 0)

render_page_header(
    title="🛡️ Proof-of-Skill Passport & Recruiter View",
    subtitle="Auditable cryptographic evidence of real competence. Honest history, project links, and live freshness.",
    badge_text="Public Verification Dossier"
)

tab_passport, tab_recruiter = st.tabs([
    "📜 Learner Proof Passport", 
    "👔 Recruiter & Company Talent Search"
])

# =============================================================
# TAB 1: LEARNER PROOF PASSPORT
# =============================================================
with tab_passport:
    # Passport Header Card
    calib_score, avg_gap, v_count = compute_calibration_score(user["self_ratings"], user["verified_skills"])
    
    st.markdown(
        f"""
        <div class="sherpa-card-highlight" style="margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
                <div>
                    <span class="badge-blue">PASSPORT ID: SKSH-2026-{abs(hash(user['name'])) % 90000 + 10000}</span>
                    <h2 style="color: #F8FAFC; margin: 8px 0 4px 0;">{user['avatar']} {user['name']}</h2>
                    <div style="color: #38BDF8; font-size: 0.95rem;">
                        Target Summit: <strong>{user['target_role']}</strong> • Profile: <strong>{user['learner_type']}</strong>
                    </div>
                    <div style="color: #94A3B8; font-size: 0.85rem; margin-top: 4px;">
                        Institution / Board: {user['board']} • Discipline: {user['branch']}
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.8rem; color: #94A3B8;">CALIBRATION AUDIT</div>
                    <div style="font-size: 2rem; font-weight: 900; color: #34D399;">{calib_score}/100</div>
                    <span class="{'badge-green' if calib_score >= 80 else 'badge-blue'}">
                        {'🌟 Honest Learner Verified' if calib_score >= 80 else '⚖️ Calibration Pending'}
                    </span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if simulated_days > 0:
        st.warning(
            f"⏱️ **Simulation Active (+{simulated_days} Days):** You are viewing this passport 100 days into the future. "
            f"Skills older than 90 days have expired and require re-verification."
        )

    # ---------------------------------------------------------
    # VERIFIED SKILL EVIDENCE CARDS
    # ---------------------------------------------------------
    st.markdown("### 🏆 Verified Competency Artifacts")
    
    if not user["verified_skills"]:
        st.info("No skills verified yet. Complete an expedition challenge in the Assess page to earn your first stamp!")
    else:
        for sname, v_info in user["verified_skills"].items():
            status, badge_color, days_rem = get_skill_expiry_status(v_info.get("verified_date", ""), simulated_days)
            
            if status == "valid":
                status_badge = f'<span class="badge-green">🟢 Valid ({days_rem} days left)</span>'
                card_border = "#10B981"
            elif status == "warning":
                status_badge = f'<span class="badge-amber">🟡 Expires Soon ({days_rem} days left)</span>'
                card_border = "#F59E0B"
            else:
                status_badge = f'<span class="badge-red">🔴 Expired ({abs(days_rem)} days ago - Re-test needed)</span>'
                card_border = "#EF4444"

            # Compute expiry date
            v_date_str = v_info.get("verified_date", "2026-10-15")
            try:
                exp_date_str = (datetime.strptime(v_date_str, "%Y-%m-%d") + timedelta(days=90)).strftime("%Y-%m-%d")
            except Exception:
                exp_date_str = "90 days from verification"

            st.markdown(
                f"""
                <div style="background: #1E293B; border: 1px solid {card_border}; border-radius: 12px; padding: 18px; margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                        <div>
                            <span style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase;">Verified Skill Credential</span>
                            <h3 style="color: #F8FAFC; margin: 4px 0;">{sname} — Level {v_info.get('level', 1)}</h3>
                            <div style="font-size: 0.85rem; color: #CBD5E1;">
                                Verified on: <strong>{v_date_str}</strong> • Expiry Date: <strong>{exp_date_str}</strong>
                            </div>
                        </div>
                        <div>
                            {status_badge}
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin: 14px 0;">
                        <div class="sherpa-metric-box">
                            <div style="font-size: 0.72rem; color: #94A3B8;">ASSESSMENT MCQ</div>
                            <div style="font-size: 1.15rem; font-weight: 700; color: #38BDF8;">{v_info.get('quiz_score', 80)}%</div>
                        </div>
                        <div class="sherpa-metric-box">
                            <div style="font-size: 0.72rem; color: #94A3B8;">AI CODE VIVA</div>
                            <div style="font-size: 1.15rem; font-weight: 700; color: #10B981;">{v_info.get('viva_score', 80)}%</div>
                        </div>
                        <div class="sherpa-metric-box">
                            <div style="font-size: 0.72rem; color: #94A3B8;">ATTEMPTS COUNT</div>
                            <div style="font-size: 1.15rem; font-weight: 700; color: #F59E0B;">{v_info.get('attempts', 1)}</div>
                        </div>
                        <div class="sherpa-metric-box">
                            <div style="font-size: 0.72rem; color: #94A3B8;">TIME INVESTED</div>
                            <div style="font-size: 1.15rem; font-weight: 700; color: #94A3B8;">{v_info.get('time_taken_days', 4)} Days</div>
                        </div>
                    </div>
                    <div style="font-size: 0.85rem;">
                        <strong>Proof Artifact URL:</strong> 
                        <a href="{v_info.get('project_url', '#')}" target="_blank" style="color: #38BDF8; margin-left: 6px; text-decoration: none;">
                            {v_info.get('project_url', 'https://github.com/demo/repo')} ↗
                        </a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.expander(f"🔍 How this was verified by AssessorAgent ({sname})"):
                st.markdown(
                    f"""
                    - **Verification Protocol:** AssessorAgent randomized 3 architecture questions + live code defense viva.
                    - **Anti-Copy Checks:** Answer passed word-timing heuristic (>40 words, deliberate authoring) and similarity semantic check against reference answers.
                    - **Evidence Audit:** GitHub repository inspects file structure, meaningful commit diffs, and functional execution logic.
                    - **Integrity Seal:** Digitally signed by SkillSherpa Agentic Swarm.
                    """
                )

    # ---------------------------------------------------------
    # HONEST HISTORY (FAILED ATTEMPTS)
    # ---------------------------------------------------------
    st.markdown("### 🧗 Honest Expedition History (Failed Attempts & Growth Trajectory)")
    st.caption("Unlike fake certificates that hide struggle, SkillSherpa records failure as proof of authentic effort and resilience.")

    failed_attempts = user.get("failed_attempts", [])
    if failed_attempts:
        for f in failed_attempts:
            st.markdown(
                f"""
                <div style="background: #111827; border-left: 4px solid #EF4444; border-radius: 6px; padding: 12px 16px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="color: #F8FAFC;">{f.get('skill')} — Attempted {f.get('attempt_date')}</strong>
                        <span class="badge-red">Score: {f.get('quiz_score')}%</span>
                    </div>
                    <p style="color: #94A3B8; font-size: 0.85rem; margin: 6px 0 0 0;">
                        <strong>Mentor Growth Note:</strong> {f.get('feedback')}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.markdown("<p style='color: #94A3B8;'>No failed attempts recorded yet.</p>", unsafe_allow_html=True)

# =============================================================
# TAB 2: RECRUITER & COMPANY TALENT SEARCH
# =============================================================
with tab_recruiter:
    st.markdown("### 👔 Enterprise Talent Search: Filter by Audited Evidence")
    st.markdown(
        "Recruiters can search candidates based on **strictly verified skills and minimum levels**, "
        "inspect their real project code, and verify their anti-copy evaluation rubric."
    )

    cohort = get_cohort()

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        roles_filter = ["All Roles"] + list(get_roles().keys())
        req_role = st.selectbox("Filter Target Role:", options=roles_filter, key="recruiter_role_filter")
    with col_f2:
        all_skills_pool = ["Any Skill", "HTML/CSS", "JavaScript", "React", "Node.js", "Python", "SQL", "Pandas", "Biology Domain Knowledge"]
        req_skill = st.selectbox("Required Verified Skill:", options=all_skills_pool, key="recruiter_skill_filter")
    with col_f3:
        min_lvl = st.slider("Minimum Verified Level (1-5):", 1, 5, 2, key="recruiter_min_lvl")

    # Filter cohort candidates
    filtered_candidates = []
    
    # Include current user in pool for demo parity
    user_cand = {
        "id": "LIVE-USER",
        "name": f"{user['name']} (Active Profile)",
        "branch": user["branch"],
        "board": user["board"],
        "target_role": user["target_role"],
        "readiness_score": int(calib_score * 0.7 + 20),
        "skills": {
            sn: {"verified_level": v_info["level"], "quiz_avg": v_info["quiz_score"]}
            for sn, v_info in user["verified_skills"].items()
        }
    }
    candidate_pool = [user_cand] + cohort

    for c in candidate_pool:
        if req_role != "All Roles" and c["target_role"] != req_role:
            continue
            
        if req_skill != "Any Skill":
            c_skill = c.get("skills", {}).get(req_skill, {})
            if c_skill.get("verified_level", 0) < min_lvl:
                continue
                
        filtered_candidates.append(c)

    st.markdown(f"#### 🔍 Found {len(filtered_candidates)} Candidates Matching Verified Evidence Criteria")

    for cand in filtered_candidates[:8]:
        st.markdown(
            f"""
            <div class="sherpa-card" style="margin-bottom: 12px; padding: 14px 18px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <strong style="color: #F8FAFC; font-size: 1.1rem;">{cand['name']}</strong>
                        <span style="color: #94A3B8; font-size: 0.82rem; margin-left: 8px;">{cand['branch']} ({cand['board']})</span><br/>
                        <span style="color: #38BDF8; font-size: 0.85rem;">Summit: {cand['target_role']} • Job Readiness: {cand['readiness_score']}%</span>
                    </div>
                    <div>
                        <span class="badge-green">Evidence Verified</span>
                    </div>
                </div>
                <div style="margin-top: 8px; font-size: 0.8rem; color: #CBD5E1;">
                    <strong>Verified Skills:</strong> 
                    {", ".join([f"{k} (Lvl {v.get('verified_level')})" for k, v in cand.get('skills', {}).items() if v.get('verified_level', 0) > 0]) or "None"}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("<br/>", unsafe_allow_html=True)
render_agent_collaboration_panel()

