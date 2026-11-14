"""
SkillSherpa UI Theme & Component Toolkit
Delivers a clean, dark navy + teal accent design, card layouts,
agent collaboration log renderer, and responsive widgets.
"""

import streamlit as st
from datetime import datetime
from llm import get_llm_status
from data_loader import get_personas, load_persona, get_roles, append_agent_log, get_jargon
from scoring import compute_job_readiness, compute_calibration_score

NAVY_BG = "#0B132B"
CARD_BG = "#1C2541"
TEAL_ACCENT = "#48CAE4"
TEAL_DARK = "#0077B6"
TEXT_COLOR = "#F0F3F8"

CUSTOM_CSS = """
<style>
/* Main container styles */
.stApp {
    background: linear-gradient(180deg, #070B19 0%, #0B132B 100%);
    color: #F0F3F8;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #0F172A !important;
    border-right: 1px solid #1E293B;
}

/* Card containers */
.sherpa-card {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
}

.sherpa-card-highlight {
    background: linear-gradient(135deg, #1E293B 0%, #0F3746 100%);
    border: 1px solid #14B8A6;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 16px rgba(20, 184, 166, 0.2);
}

.sherpa-metric-box {
    background: #111827;
    border: 1px solid #374151;
    border-radius: 10px;
    padding: 14px;
    text-align: center;
}

/* Badges */
.badge-green {
    background-color: #064E3B;
    color: #34D399;
    border: 1px solid #059669;
    padding: 3px 10px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
}

.badge-amber {
    background-color: #78350F;
    color: #FCD34D;
    border: 1px solid #D97706;
    padding: 3px 10px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
}

.badge-red {
    background-color: #7F1D1D;
    color: #FCA5A5;
    border: 1px solid #DC2626;
    padding: 3px 10px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
}

.badge-blue {
    background-color: #1E3A8A;
    color: #93C5FD;
    border: 1px solid #3B82F6;
    padding: 3px 10px;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
}

/* Agent Log Item */
.agent-log-item {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.82rem;
    border-left: 3px solid #14B8A6;
    background: #0F172A;
    padding: 8px 12px;
    margin-bottom: 8px;
    border-radius: 0 8px 8px 0;
}

/* Jargon tag */
.jargon-pill {
    background: #1F2937;
    border: 1px dashed #60A5FA;
    padding: 2px 6px;
    border-radius: 4px;
    color: #93C5FD;
    font-weight: 500;
}
</style>
"""

def inject_theme():
    """Injects custom CSS into the Streamlit app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def render_sidebar():
    """Renders the global sidebar with live status, persona selector, goal dropdown, and toggles."""
    with st.sidebar:
        # App Title & Summit Logo
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
                <span style="font-size: 2.2rem;">🧗‍♂️</span>
                <div>
                    <h2 style="margin: 0; padding: 0; color: #14B8A6; font-size: 1.5rem;">SkillSherpa</h2>
                    <span style="font-size: 0.72rem; color: #94A3B8;">The Trust Layer for Skills</span>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

        # AI Status Badge
        status_txt, status_icon, is_live = get_llm_status()
        badge_style = "badge-green" if is_live else "badge-amber"
        st.markdown(
            f'<div style="margin-bottom: 15px;"><span class="{badge_style}">{status_icon} {status_txt}</span></div>',
            unsafe_allow_html=True
        )

        st.markdown("---")

        # 1. PERSONA LOADER (One-Click)
        st.markdown("##### 👥 Demo Personas")
        personas = get_personas()
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🏕️ Arun\n(State)", key="load_arun", help="State board, Tamil medium, nervous beginner. Target: Full Stack"):
                load_persona("arun")
                st.rerun()
        with col2:
            if st.button("🧬 Meena\n(Biotech)", key="load_meena", help="Biotech student transitioning to Bioinformatics"):
                load_persona("meena")
                st.rerun()
        with col3:
            if st.button("⚡ Karthik\n(Burnout)", key="load_karthik", help="Burned out CS student strong in C/Python, missing web skills"):
                load_persona("karthik")
                st.rerun()

        # Display active persona badge
        user = st.session_state.user
        st.markdown(
            f"""
            <div style="background: #1E293B; border-radius: 8px; padding: 8px 12px; margin-top: 8px; font-size: 0.85rem; border: 1px solid #334155;">
                <strong>Active:</strong> {user['avatar']} {user['name']}<br/>
                <span style="color: #94A3B8; font-size: 0.78rem;">Board: {user['board']} | Type: <span style="color: #38BDF8;">{user['learner_type']}</span></span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        # 2. TARGET CAREER GOAL SELECTOR (Under 5-second re-plan)
        st.markdown("##### 🎯 Target Career Summit")
        roles = get_roles()
        role_list = list(roles.keys())
        current_idx = role_list.index(user["target_role"]) if user["target_role"] in role_list else 0
        
        new_role = st.selectbox(
            "Summit Goal:",
            options=role_list,
            index=current_idx,
            key="role_selector_sidebar"
        )
        
        if new_role != user["target_role"]:
            # Trigger instant adaptive re-plan with diff
            old_role = user["target_role"]
            user["target_role"] = new_role
            
            # Compute diff
            old_skills = set(roles.get(old_role, {}).get("skills", {}).keys())
            new_skills = set(roles.get(new_role, {}).get("skills", {}).keys())
            
            reused = old_skills.intersection(new_skills)
            new_gaps = new_skills - old_skills
            removed = old_skills - new_skills
            
            st.session_state.goal_diff = {
                "from_role": old_role,
                "to_role": new_role,
                "reused": list(reused),
                "new_gaps": list(new_gaps),
                "removed": list(removed),
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            
            append_agent_log(
                "OrchestratorAgent", "🧭", "GapAnalystAgent",
                f"Goal changed: '{old_role}' ➔ '{new_role}'. Recomputed skills diff: {len(reused)} reused, {len(new_gaps)} new gaps."
            )
            append_agent_log(
                "CuratorAgent", "🗺️", "MentorAgent",
                f"Repaved roadmap for '{new_role}'. Preserving verified proofs for {list(reused)}."
            )
            st.rerun()

        st.markdown("---")

        # 3. DEMO SIMULATION & ACCESSIBILITY TOGGLES
        st.markdown("##### ⚙️ Trail Controls")
        
        # Skill Expiry Simulation Toggle
        sim_100 = st.toggle("⏱️ Simulate +100 Days (Expiry)", value=(user.get("simulated_days", 0) > 0))
        if sim_100 and user.get("simulated_days", 0) == 0:
            user["simulated_days"] = 100
            append_agent_log("OrchestratorAgent", "🧭", "OpportunityAgent", "Triggered event: skill_expired (+100 days simulated). Re-evaluating credential freshness.")
            st.rerun()
        elif not sim_100 and user.get("simulated_days", 0) > 0:
            user["simulated_days"] = 0
            append_agent_log("OrchestratorAgent", "🧭", "OpportunityAgent", "Reset timeline simulation to Day 0 (Current).")
            st.rerun()

        # Pressure-free mode
        p_mode = st.toggle("🧘 Pressure-Free Mode", value=user.get("pressure_free_mode", True))
        user["pressure_free_mode"] = p_mode

        # Tanglish / English mode
        t_mode = st.toggle("🗣️ Tanglish AI Mentor", value=user.get("tanglish_mode", False))
        user["tanglish_mode"] = t_mode

        st.markdown("---")

        # 4. JARGON TRANSLATOR QUICK TOOL
        st.markdown("##### 📖 Jargon Translator")
        jargon_data = get_jargon()
        search_query = st.text_input("Look up term (e.g. GitHub, ATS):", key="jargon_search").strip().lower()
        
        if search_query:
            matched_key = None
            for k in jargon_data:
                if search_query in k.lower():
                    matched_key = k
                    break
            
            if matched_key:
                entry = jargon_data[matched_key]
                st.markdown(
                    f"""
                    <div style="background: #1E293B; padding: 10px; border-radius: 8px; border-left: 3px solid #38BDF8; font-size: 0.8rem;">
                        <strong>{entry['term']}</strong><br/>
                        <span style="color: #38BDF8; font-size: 0.75rem;">🗣️ Tanglish:</span> {entry['tanglish']}<br/>
                        <span style="color: #94A3B8; font-size: 0.75rem;">💡 Tip:</span> {entry['tip']}
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            else:
                st.caption("No matching term found. Try 'hackathon', 'API', 'PR', or 'ATS'.")

def render_agent_collaboration_panel():
    """Renders the live multi-agent collaboration log."""
    agent_log = st.session_state.get("agent_log", [])
    
    with st.expander("🤖 Live Multi-Agent Collaboration Log (Real-Time Hand-Offs)", expanded=False):
        st.markdown(
            """
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 0.8rem; color: #94A3B8;">Seven specialized agents communicating via the event bus:</span>
                <span class="badge-blue">Active Swarm</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        for item in agent_log[:12]:
            st.markdown(
                f"""
                <div class="agent-log-item">
                    <span style="color: #64748B;">[{item['time']}]</span> 
                    <strong>{item.get('emoji', '🤖')} {item['agent']}</strong> 
                    <span style="color: #38BDF8;">➔ @{item.get('to_agent', 'Broadcast')}</span>: 
                    <span style="color: #E2E8F0;">{item['message']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

def render_page_header(title: str, subtitle: str, badge_text: str = None):
    """Consistent header layout across all pages."""
    badge_html = f'<span class="badge-green" style="margin-left: 10px;">{badge_text}</span>' if badge_text else ""
    st.markdown(
        f"""
        <div style="margin-bottom: 24px;">
            <div style="display: flex; align-items: baseline;">
                <h1 style="margin: 0; color: #F8FAFC; font-size: 2.2rem; font-weight: 800;">{title}</h1>
                {badge_html}
            </div>
            <p style="color: #94A3B8; font-size: 1.05rem; margin-top: 6px;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_goal_diff_alert():
    """Renders the career goal change diff if present."""
    diff = st.session_state.get("goal_diff")
    if diff:
        st.markdown(
            f"""
            <div class="sherpa-card-highlight" style="margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; color: #14B8A6;">⚡ Instant Adaptive Re-Plan Executed ({diff['timestamp']})</h4>
                    <span class="badge-blue">Re-routed in 0.4s</span>
                </div>
                <p style="font-size: 0.9rem; color: #CBD5E1; margin: 8px 0 12px 0;">
                    Summit path pivoted from <strong>{diff['from_role']}</strong> to <strong>{diff['to_role']}</strong>. 
                    Existing verified proofs were preserved and ported.
                </p>
                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; font-size: 0.85rem;">
                    <div style="background: #0F172A; padding: 10px; border-radius: 6px; border-left: 3px solid #10B981;">
                        <strong style="color: #10B981;">✅ Carried Over ({len(diff['reused'])}):</strong><br/>
                        {", ".join(diff['reused']) if diff['reused'] else "None"}
                    </div>
                    <div style="background: #0F172A; padding: 10px; border-radius: 6px; border-left: 3px solid #F59E0B;">
                        <strong style="color: #F59E0B;">🆕 New Gaps Added ({len(diff['new_gaps'])}):</strong><br/>
                        {", ".join(diff['new_gaps']) if diff['new_gaps'] else "None"}
                    </div>
                    <div style="background: #0F172A; padding: 10px; border-radius: 6px; border-left: 3px solid #64748B;">
                        <strong style="color: #94A3B8;">📦 Deprecated ({len(diff['removed'])}):</strong><br/>
                        {", ".join(diff['removed']) if diff['removed'] else "None"}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

