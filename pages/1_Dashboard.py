"""
SkillSherpa: Learner Summit Dashboard
Visualizes Job Readiness Gauge, Radar Chart, Skill Gap Bars, Weekly Quest, and Badges.
"""

import streamlit as st
import plotly.graph_objects as go
from ui import inject_theme, render_sidebar, render_agent_collaboration_panel, render_page_header, render_goal_diff_alert
from data_loader import init_session_state, get_roles, get_resources
from scoring import compute_job_readiness, compute_gap_severity, get_skill_expiry_status
from agents import orchestrator

inject_theme()
init_session_state()
render_sidebar()
render_goal_diff_alert()

user = st.session_state.user
roles = get_roles()
target_role = user["target_role"]
role_info = roles.get(target_role, {})
role_skills = role_info.get("skills", {})
simulated_days = user.get("simulated_days", 0)

# Evaluate gap analysis
gap_res = orchestrator.gap_analyst.run(user, target_role)
readiness_score = gap_res["readiness_score"]
gaps = gap_res["gaps"]

render_page_header(
    title=f"🏔️ Summit Dashboard: {target_role}",
    subtitle=f"Evidence-based readiness tracking for {user['avatar']} {user['name']} ({user['learner_type']} Profile)",
    badge_text=f"{readiness_score}% Job Ready"
)

# -------------------------------------------------------------
# TOP ROW: GAUGE + RADAR CHART
# -------------------------------------------------------------
col_gauge, col_radar = st.columns([1, 1.4])

with col_gauge:
    st.markdown('<div class="sherpa-card" style="height: 100%;">', unsafe_allow_html=True)
    st.markdown("### 🎯 Job Readiness Gauge")
    st.caption("Weighted contribution of verified project proofs against industry baseline.")

    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=readiness_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        delta={'reference': 50, 'increasing': {'color': "#10B981"}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "#94A3B8"},
            'bar': {'color': "#14B8A6", 'thickness': 0.25},
            'bgcolor': "#0F172A",
            'borderwidth': 1,
            'bordercolor': "#334155",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.25)'},
                {'range': [40, 75], 'color': 'rgba(245, 158, 11, 0.25)'},
                {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.25)'}
            ],
            'threshold': {
                'line': {'color': "#38BDF8", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))
    gauge_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC"),
        height=260,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(gauge_fig, use_container_width=True)

    status_note = (
        "🚀 Interview Ready! Your verified proofs qualify you for competitive roles." 
        if readiness_score >= 75 else 
        "🧗 Solid progress! 2-3 more verified project proofs will unlock prime internships."
    )
    st.markdown(f"<p style='color: #38BDF8; font-size: 0.85rem; text-align: center;'>{status_note}</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_radar:
    st.markdown('<div class="sherpa-card" style="height: 100%;">', unsafe_allow_html=True)
    st.markdown("### 🕸️ Competency Radar: Verified vs Target")
    st.caption("Visualizes current verified evidence against Summit baseline expectations.")

    skill_names = list(role_skills.keys())
    target_levels = [role_skills[s].get("target_level", 3) for s in skill_names]
    
    verified_levels = []
    for s in skill_names:
        v_info = user["verified_skills"].get(s)
        if v_info:
            status, _, _ = get_skill_expiry_status(v_info.get("verified_date", ""), simulated_days)
            verified_levels.append(v_info.get("level", 0) if status != "expired" else 0)
        else:
            verified_levels.append(0)

    # Close the radar loop
    radar_skills = skill_names + [skill_names[0]]
    radar_targets = target_levels + [target_levels[0]]
    radar_verified = verified_levels + [verified_levels[0]]

    radar_fig = go.Figure()
    radar_fig.add_trace(go.Scatterpolar(
        r=radar_targets,
        theta=radar_skills,
        fill='toself',
        fillcolor='rgba(56, 189, 248, 0.15)',
        line=dict(color='#38BDF8', dash='dash'),
        name='Target Level'
    ))
    radar_fig.add_trace(go.Scatterpolar(
        r=radar_verified,
        theta=radar_skills,
        fill='toself',
        fillcolor='rgba(20, 184, 166, 0.4)',
        line=dict(color='#14B8A6', width=2),
        name='Verified Level'
    ))
    radar_fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5], tickfont=dict(color="#64748B"), gridcolor="#334155"),
            angularaxis=dict(tickfont=dict(color="#CBD5E1", size=10), gridcolor="#334155")
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC"),
        height=260,
        margin=dict(l=30, r=30, t=20, b=20),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(radar_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# -------------------------------------------------------------
# MIDDLE ROW: SKILL GAP BREAKDOWN & WEEKLY QUEST
# -------------------------------------------------------------
col_gaps, col_side = st.columns([1.6, 1])

with col_gaps:
    st.markdown("### 📊 Skill Gap Severity Breakdown")
    st.caption("Generated by GapAnalystAgent based on verified artifacts & assessments.")

    for g in gaps:
        badge_cls = "badge-green" if g["delta"] == 0 else ("badge-amber" if g["delta"] == 1 else "badge-red")
        expiry_info = ""
        if g.get("expiry_status") == "expired":
            expiry_info = '<span class="badge-red" style="margin-left: 8px;">🔴 EXPIRED (>90d)</span>'
        elif g.get("expiry_status") == "warning":
            expiry_info = '<span class="badge-amber" style="margin-left: 8px;">🟡 EXPIRES SOON</span>'

        st.markdown(
            f"""
            <div style="background: #1E293B; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px; border-left: 4px solid {g['color']};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: #F8FAFC; font-size: 1rem;">{g['skill']}</strong>
                        <span style="color: #94A3B8; font-size: 0.8rem; margin-left: 8px;">Weight: {g['weight']}x</span>
                        {expiry_info}
                    </div>
                    <div>
                        <span class="{badge_cls}">{g['severity']}</span>
                        <span style="color: #38BDF8; font-weight: 700; margin-left: 10px;">Lvl {g['verified_level']}/{g['target_level']}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander(f"🔍 Why this? (GapAnalystAgent Reasoning for {g['skill']})"):
            st.markdown(
                f"**Agent Reasoning:** {g['skill']} carries a weighted importance of **{g['weight']}x** for the **{target_role}** summit. "
                f"Closing this gap of {g['delta']} level(s) increases your overall Job Readiness by approximately **{int(round((g['weight']/sum(s['weight'] for s in role_skills.values())) * 100))}%**."
            )

with col_side:
    st.markdown("### 🏕️ Active Weekly Quest")
    
    # Pick next unverified skill
    active_quest_skill = None
    for g in gaps:
        if g["delta"] > 0:
            active_quest_skill = g["skill"]
            break
    if not active_quest_skill:
        active_quest_skill = gaps[0]["skill"]

    all_res = get_resources()
    quest_data = all_res.get(active_quest_skill, {})
    quest_text = quest_data.get("weekly_quest", f"Build and host an interactive demo with {active_quest_skill}.")

    st.markdown(
        f"""
        <div class="sherpa-card-highlight">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span class="badge-blue">Current Objective</span>
                <span style="font-size: 0.8rem; color: #14B8A6;">Camp Focus</span>
            </div>
            <h4 style="color: #F8FAFC; margin: 4px 0 8px 0;">{active_quest_skill}</h4>
            <p style="color: #CBD5E1; font-size: 0.9rem; line-height: 1.5;">{quest_text}</p>
            <div style="margin-top: 14px; background: rgba(0,0,0,0.25); padding: 8px 12px; border-radius: 6px; font-size: 0.8rem; color: #94A3B8;">
                Deliverable: Submit repository link to AssessorAgent for code viva verification.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Badges & Pressure-Free Mode
    st.markdown("### 🏅 Verified Badges")
    calib_score, _, _ = compute_calibration_score(user["self_ratings"], user["verified_skills"])
    badges = list(user.get("badges", []))
    if calib_score >= 80 and "Honest Learner" not in badges:
        badges.append("Honest Learner")

    badge_html_list = []
    for b in badges:
        badge_html_list.append(f'<span class="badge-green" style="margin: 3px;">🌟 {b}</span>')
    
    st.markdown(f'<div style="margin-bottom: 12px;">{" ".join(badge_html_list)}</div>', unsafe_allow_html=True)

    if user.get("pressure_free_mode", False):
        st.info("🧘 **Pressure-Free Mode Active:** No streak loss, no countdown penalties. Progress is permanent once verified.")
    else:
        st.markdown(f"🔥 **Verified Consistency Streak:** `{user.get('streak_days', 4)} Days`")

st.markdown("<br/>", unsafe_allow_html=True)
render_agent_collaboration_panel()

