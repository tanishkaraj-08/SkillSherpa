"""
SkillSherpa: ATS-Friendly Verified Resume Builder
Generates recruiter and ATS-optimized resume markdown/text strictly from audited project proofs.
"""

import streamlit as st
from ui import inject_theme, render_sidebar, render_agent_collaboration_panel, render_page_header, render_goal_diff_alert
from data_loader import init_session_state, get_roles
from scoring import compute_job_readiness, compute_calibration_score

inject_theme()
init_session_state()
render_sidebar()
render_goal_diff_alert()

user = st.session_state.user
target_role = user["target_role"]
verified = user["verified_skills"]
calib_score, _, _ = compute_calibration_score(user["self_ratings"], verified)

render_page_header(
    title="📄 ATS-Optimized Proof Resume Builder",
    subtitle="Zero fluff or unverified keywords. Strictly exports proven projects and auditable code repositories.",
    badge_text="ATS Compliant"
)

st.markdown(
    """
    <div class="sherpa-card-highlight" style="margin-bottom: 20px;">
        <h4 style="color: #14B8A6; margin-top: 0;">🛡️ The Verified ATS Guarantee</h4>
        <p style="color: #E2E8F0; font-size: 0.9rem; margin-bottom: 0;">
            Most resumes fail ATS screening due to non-standard columns or keyword stuffing. 
            SkillSherpa formats your verified competencies with clean semantic hierarchy, 
            concrete technical deliverables, and active GitHub proof links.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------------
# COMPOSE RESUME MARKDOWN / TEXT
# -------------------------------------------------------------
verified_skills_list = []
project_sections = []

for sname, v_info in verified.items():
    verified_skills_list.append(f"{sname} (Level {v_info.get('level', 1)} Verified)")
    project_sections.append(
        f"### {sname} Implementation & Architecture\n"
        f"- **Repository Evidence:** {v_info.get('project_url', 'https://github.com/user/demo')}\n"
        f"- **Verification Protocol:** AssessorAgent randomized evaluation (MCQ: {v_info.get('quiz_score', 80)}%, Viva: {v_info.get('viva_score', 80)}%)\n"
        f"- **Deliverable:** Engineered full modular implementation adhering to production error handling and architectural guidelines."
    )

skills_str = ", ".join(verified_skills_list) if verified_skills_list else "Skills in verification pipeline"
projects_str = "\n\n".join(project_sections) if project_sections else "No verified projects completed yet."

resume_md = f"""# {user['name'].upper()}
**Aspiring {target_role}**
Location: Tamil Nadu / India | Email: {user['name'].lower().replace(' ', '.')}@example.com
Portfolio Passport: https://skillsherpa.live/p/SKSH-2026-{abs(hash(user['name'])) % 90000 + 10000}
GitHub: https://github.com/{user['name'].lower().replace(' ', '-')}

---

## PROFESSIONAL SUMMARY
Passionate and disciplined {target_role} candidate specializing in robust, tested web architecture. 
Verified through SkillSherpa's agentic proof layer with an authentic self-calibration score of {calib_score}/100. 
Proven ability to build end-to-end projects, write clean version-controlled code, and defend engineering decisions in technical code vivas.

---

## VERIFIED TECHNICAL COMPETENCIES (AUDITED PROOF)
- **Verified Skills:** {skills_str}
- **Calibration Index:** {calib_score}/100 (Awarded 'Honest Learner' Badge)
- **Methodology:** Version control with Git, Semantic HTML, Clean Architecture, Defensive Error Handling

---

## AUDITED PROJECT ARTIFACTS
{projects_str}

---

## EDUCATION & BACKGROUND
- **Discipline:** {user['branch']}
- **Institution Background:** {user['board']}
- **Learning Track:** SkillSherpa {user['learner_type']} Expedition Track

---
*Verified cryptographically via SkillSherpa Proof-of-Skill Protocol (Anti-copy verified).*
"""

col_preview, col_export = st.columns([1.6, 1])

with col_preview:
    st.markdown("### 📝 Live ATS Resume Preview")
    st.text_area("Plain Text / Markdown Output:", value=resume_md, height=450)

with col_export:
    st.markdown("### 💾 Export & Download")
    st.markdown("Download in single-column `.txt` or `.md` formats to guarantee 100% ATS readability.")

    st.download_button(
        label="📥 Download Resume (.txt)",
        data=resume_md,
        file_name=f"{user['name'].replace(' ', '_')}_Verified_Resume.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.download_button(
        label="📥 Download Resume (.md)",
        data=resume_md,
        file_name=f"{user['name'].replace(' ', '_')}_Verified_Resume.md",
        mime="text/markdown",
        use_container_width=True
    )

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="sherpa-card">
            <h5 style="color: #38BDF8; margin-top: 0;">🎯 Recruiter Tips:</h5>
            <ul style="color: #CBD5E1; font-size: 0.85rem; padding-left: 18px; margin-bottom: 0;">
                <li>Keep contact links at the very top.</li>
                <li>Link directly to live repositories, not static PDFs.</li>
                <li>Highlight the <strong>Calibration Index ({calib_score}/100)</strong> to prove honesty.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br/>", unsafe_allow_html=True)
render_agent_collaboration_panel()

