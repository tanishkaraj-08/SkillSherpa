"""
SkillSherpa: Opportunity Engine
Matches ONLY verified skills to internships, jobs, hackathons, and open-source bounties.
"""

import streamlit as st
from ui import inject_theme, render_sidebar, render_agent_collaboration_panel, render_page_header, render_goal_diff_alert
from data_loader import init_session_state, get_roles, append_agent_log
from agents import orchestrator

inject_theme()
init_session_state()
render_sidebar()
render_goal_diff_alert()

user = st.session_state.user
simulated_days = user.get("simulated_days", 0)

render_page_header(
    title="💼 Verified Skill Opportunities",
    subtitle="Zero unverified claims. Every opportunity below maps strictly to auditable code proof.",
    badge_text="Audited Matches"
)

# Run OpportunityAgent
opp_data = orchestrator.opportunity.run(user["verified_skills"], simulated_days)
matched = opp_data.get("matched", [])
unlockable = opp_data.get("unlockable", [])
beginner = opp_data.get("beginner_friendly", [])

# Top summary metric banner
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        f"""
        <div class="sherpa-card" style="text-align: center;">
            <div style="font-size: 0.8rem; color: #94A3B8;">QUALIFIED MATCHES</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #10B981;">{len(matched)}</div>
            <div style="font-size: 0.78rem; color: #CBD5E1;">Ready to apply right now</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with c2:
    st.markdown(
        f"""
        <div class="sherpa-card" style="text-align: center;">
            <div style="font-size: 0.8rem; color: #94A3B8;">UNLOCKABLE SOON</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #F59E0B;">{len(unlockable)}</div>
            <div style="font-size: 0.78rem; color: #CBD5E1;">1 skill level away</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with c3:
    st.markdown(
        f"""
        <div class="sherpa-card" style="text-align: center;">
            <div style="font-size: 0.8rem; color: #94A3B8;">BEGINNER ON-RAMPS</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #38BDF8;">{len(beginner)}</div>
            <div style="font-size: 0.78rem; color: #CBD5E1;">Safe starting points</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br/>", unsafe_allow_html=True)

# -------------------------------------------------------------
# TABS: MATCHED | UNLOCKABLE | BEGINNER-FRIENDLY
# -------------------------------------------------------------
tab_match, tab_unlock, tab_begin = st.tabs([
    f"✅ Verified Matches ({len(matched)})",
    f"🔓 Unlockable Soon ({len(unlockable)})",
    f"🌱 Beginner On-Ramps ({len(beginner)})"
])

def render_opp_card(opp, is_unlock=False):
    type_badges = {
        "Internship": "badge-blue",
        "Job": "badge-green",
        "Hackathon": "badge-amber",
        "Open Source": "badge-blue",
        "Scholarship": "badge-green",
        "Free Certification": "badge-blue"
    }
    badge_cls = type_badges.get(opp.get("type"), "badge-blue")

    unlock_hint_html = ""
    if is_unlock and "unlock_hint" in opp:
        unlock_hint_html = (
            f'<div style="background: #78350F; color: #FCD34D; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; margin-top: 8px;">'
            f'💡 <strong>Unlock Requirement:</strong> {opp["unlock_hint"]}'
            f'</div>'
        )

    # Required skills pill list
    skills_html = []
    for sname, lvl in opp.get("required_skills", {}).items():
        user_lvl = user["verified_skills"].get(sname, {}).get("level", 0)
        has_skill = user_lvl >= lvl
        color_dot = "🟢" if has_skill else "⚪"
        skills_html.append(f'<span style="background: #0F172A; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; border: 1px solid #334155;">{color_dot} {sname} (Lvl {lvl})</span>')

    st.markdown(
        f"""
        <div class="sherpa-card" style="margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                <div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span class="{badge_cls}">{opp.get('type', 'Role')}</span>
                        <span style="font-size: 0.85rem; color: #94A3B8;">📍 {opp.get('location')}</span>
                    </div>
                    <h3 style="color: #F8FAFC; margin: 6px 0 4px 0; font-size: 1.25rem;">{opp.get('title')}</h3>
                    <div style="font-size: 0.9rem; color: #38BDF8; font-weight: 600;">{opp.get('organization')} • {opp.get('stipend_or_perk')}</div>
                </div>
                <div>
                    <a href="{opp.get('apply_url', '#')}" target="_blank" 
                       style="background: #14B8A6; color: #042F2E; padding: 8px 16px; border-radius: 6px; font-weight: 700; text-decoration: none; font-size: 0.85rem; display: inline-block;">
                       {'View Opportunity ↗' if not is_unlock else 'See Target ↗'}
                    </a>
                </div>
            </div>
            <p style="color: #CBD5E1; font-size: 0.9rem; margin: 10px 0 8px 0; line-height: 1.5;">{opp.get('description')}</p>
            <div style="margin-top: 10px; display: flex; gap: 6px; flex-wrap: wrap;">
                {' '.join(skills_html)}
            </div>
            {unlock_hint_html}
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander(f"🔍 Why this? (OpportunityAgent Reasoning for {opp.get('title')})"):
        st.markdown(f"**Agent Reasoning:** {opp.get('why_this', 'Matches verified skillset requirements.')}")

with tab_match:
    if matched:
        for opp in matched:
            render_opp_card(opp, is_unlock=False)
    else:
        st.info("🧗 **Keep Climbing:** You have not fully cleared the verified requirements for any role yet. Complete your current Camp in the Roadmap to unlock your first opportunities!")

with tab_unlock:
    if unlockable:
        for opp in unlockable:
            render_opp_card(opp, is_unlock=True)
    else:
        st.write("No near-term unlockable opportunities at this time.")

with tab_begin:
    st.markdown("##### 🚀 Curated Entry Points for First-Time Hackers & Open-Source Contributors")
    for opp in beginner:
        render_opp_card(opp, is_unlock=False)

st.markdown("<br/>", unsafe_allow_html=True)
render_agent_collaboration_panel()

