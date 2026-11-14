"""
SkillSherpa: Mountain Trail Roadmap
Step-by-step prerequisite-aware trail with camps, mastery gates, free resources, and mini-projects.
"""

import streamlit as st
from ui import inject_theme, render_sidebar, render_agent_collaboration_panel, render_page_header, render_goal_diff_alert
from data_loader import init_session_state, get_roles, get_resources, append_agent_log
from agents import orchestrator

inject_theme()
init_session_state()
render_sidebar()
render_goal_diff_alert()

user = st.session_state.user
target_role = user["target_role"]

render_page_header(
    title=f"🗺️ Mountain Trail: {target_role}",
    subtitle="A prerequisite-guided expedition. Step by step from Base Camp to the Summit.",
    badge_text="Mastery Gate Enforced"
)

# Run CuratorAgent to assemble trail
trail = orchestrator.curator.run(
    target_role=target_role,
    verified_skills=user["verified_skills"],
    learner_type=user["learner_type"]
)

st.markdown(
    """
    <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid #334155; border-radius: 10px; padding: 12px 18px; margin-bottom: 20px;">
        <span style="color: #38BDF8; font-weight: 700;">🛡️ The Mastery Gate Rule:</span> 
        Watching a video marks a resource as prepared, but <em>never</em> marks a skill complete. 
        Advancing to the next Camp strictly requires a passing <strong>Assessor Quiz + Code Viva</strong> and a valid <strong>GitHub Project URL</strong>.
    </div>
    """,
    unsafe_allow_html=True
)

watched_list = set(user.get("watched_resources", []))

for idx, camp in enumerate(trail):
    skill_name = camp["skill"]
    status = camp["status"] # Mastered, Unlocked, Locked
    is_adapted = camp.get("adapted", False)
    
    # Border color based on status
    if status == "Mastered":
        card_border = "#10B981"
        badge_html = '<span class="badge-green">🟢 Mastered & Verified</span>'
    elif status == "Unlocked":
        card_border = "#38BDF8"
        badge_html = '<span class="badge-blue">⛺ Current Active Camp</span>'
    else:
        card_border = "#475569"
        badge_html = f'<span class="badge-amber">{camp["badge"]}</span>'

    adapted_banner = ""
    if is_adapted:
        adapted_banner = (
            '<div style="background: #78350F; color: #FCD34D; padding: 6px 12px; border-radius: 6px; font-size: 0.8rem; margin-bottom: 10px;">'
            '⚡ <strong>Adaptive Revision Inserted by MentorAgent:</strong> Added prerequisite drills to reinforce fundamentals without pressure.'
            '</div>'
        )

    st.markdown(
        f"""
        <div style="background: #1E293B; border: 1px solid {card_border}; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
            {adapted_banner}
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                <div>
                    <span style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">{camp['camp']} • {camp['category']}</span>
                    <h3 style="color: #F8FAFC; margin: 4px 0 6px 0; font-size: 1.4rem;">{skill_name}</h3>
                    <p style="color: #CBD5E1; font-size: 0.95rem; margin-bottom: 8px;">{camp['description']}</p>
                </div>
                <div>
                    {badge_html}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Camp Details Columns (Resources & Mini Project)
    col_res, col_proj = st.columns([1.2, 1])

    with col_res:
        st.markdown("##### 📚 Free Curated Trail Resources")
        for res_idx, r in enumerate(camp.get("resources", [])):
            icon = "🎬" if r["type"] == "video" else ("📖" if r["type"] == "tutorial" else "💻")
            res_key = f"{skill_name}_{res_idx}"
            is_watched = res_key in watched_list or skill_name in watched_list

            st.markdown(
                f"""
                <div style="background: #0F172A; border: 1px solid #334155; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; font-size: 0.88rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{icon} {r['title']}</strong><br/>
                            <span style="color: #94A3B8; font-size: 0.78rem;">{r['platform']} • {r['hours']} hrs • {r['difficulty']}</span>
                        </div>
                        <div>
                            <a href="{r['url']}" target="_blank" style="color: #38BDF8; font-size: 0.82rem; text-decoration: none; font-weight: 600;">Open Link ↗</a>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Watch toggle
        if status != "Mastered":
            watched = st.checkbox(
                f"Mark resources for {skill_name} reviewed (Unlocks Assessment)",
                value=(skill_name in watched_list),
                key=f"watch_{skill_name}"
            )
            if watched and skill_name not in watched_list:
                user["watched_resources"].append(skill_name)
                append_agent_log("CuratorAgent", "🗺️", "AssessorAgent", f"Learner reviewed resources for '{skill_name}'. Assessment gate unlocked.")
                st.rerun()

    with col_proj:
        mini_p = camp.get("mini_project", {})
        st.markdown("##### 🛠️ Hands-on Mini Project (Proof Artifact)")
        st.markdown(
            f"""
            <div style="background: #0F172A; border: 1px solid #14B8A6; border-radius: 8px; padding: 12px 14px; font-size: 0.88rem;">
                <strong style="color: #14B8A6;">{mini_p.get('title', 'Practical Challenge')}</strong>
                <p style="color: #CBD5E1; font-size: 0.85rem; margin: 6px 0 8px 0;">{mini_p.get('prompt', 'Build a real app.')}</p>
                <div style="color: #94A3B8; font-size: 0.78rem;"><strong>Deliverable:</strong> {mini_p.get('deliverable', 'GitHub repo URL')}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if status == "Unlocked":
            st.markdown("<br/>", unsafe_allow_html=True)
            if st.button(f"🎯 Proceed to Verify {skill_name} in Assess Page ➔", key=f"btn_verify_{skill_name}", use_container_width=True):
                st.session_state.selected_assessment_skill = skill_name
                st.switch_page("pages/3_Assess.py")
        elif status == "Mastered":
            v_data = user["verified_skills"].get(skill_name, {})
            st.markdown(
                f"""
                <div style="margin-top: 10px; font-size: 0.8rem; color: #10B981;">
                    ✓ Verified at Level {v_data.get('level', 1)} | Score: {v_data.get('quiz_score', 80)}%<br/>
                    <a href="{v_data.get('project_url', '#')}" target="_blank" style="color: #38BDF8;">View Verified Repository ↗</a>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.caption(f"🔒 Complete previous prerequisite camps to unlock {skill_name}.")

    # "Why this?" Expander
    with st.expander(f"🔍 Why this? (Explainable AI reasoning for {skill_name})"):
        st.markdown(
            f"**CuratorAgent Rationale:** {camp['why_this']} "
            f"Prerequisites: `{', '.join(camp['prerequisites']) if camp['prerequisites'] else 'None'}`. "
            f"Tailored for `{user['learner_type']}` pace."
        )

    st.markdown("<hr style='border-color: #334155; margin: 16px 0;'/>", unsafe_allow_html=True)

render_agent_collaboration_panel()

