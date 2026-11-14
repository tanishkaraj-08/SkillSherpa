"""
SkillSherpa: The Trust Layer for Skills
Main Home & Zero-Assumption Onboarding Page
"""

import streamlit as st
import plotly.graph_objects as go
from ui import inject_theme, render_sidebar, render_agent_collaboration_panel, render_goal_diff_alert
from data_loader import init_session_state, get_roles, get_personas, load_persona, append_agent_log
from agents import orchestrator
from scoring import compute_calibration_score, compute_job_readiness

st.set_page_state = "wide"
st.set_page_config(
    page_title="SkillSherpa | Trust Layer for Skills",
    page_icon="🧗‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_theme()
init_session_state()
render_sidebar()
render_goal_diff_alert()

user = st.session_state.user

# -------------------------------------------------------------
# HERO BANNER
# -------------------------------------------------------------
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #0F172A 0%, #112A45 50%, #0D3B4C 100%); 
                border: 1px solid #14B8A6; border-radius: 16px; padding: 28px; margin-bottom: 24px; box-shadow: 0 8px 24px rgba(0,0,0,0.4);">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
            <div style="max-width: 680px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span style="background: #14B8A6; color: #042F2E; font-size: 0.75rem; font-weight: 700; padding: 3px 10px; border-radius: 9999px;">
                        AGENTIC AI LEARNING & VERIFICATION
                    </span>
                    <span style="background: #1E293B; color: #94A3B8; font-size: 0.75rem; padding: 3px 10px; border-radius: 9999px; border: 1px solid #334155;">
                        MOUNTAIN CLIMB THEME
                    </span>
                </div>
                <h1 style="color: #F8FAFC; margin: 4px 0 10px 0; font-size: 2.6rem; font-weight: 900; letter-spacing: -0.5px;">
                    🧗‍♂️ SkillSherpa
                </h1>
                <p style="font-size: 1.25rem; color: #38BDF8; font-weight: 600; margin-bottom: 8px;">
                    "Certificates prove you watched. We prove you can do."
                </p>
                <p style="color: #CBD5E1; font-size: 0.98rem; line-height: 1.5; margin: 0;">
                    Your AI Sherpa guides you from <strong>Base Camp (current ability)</strong> to your <strong>Career Summit</strong>. 
                    Every skill is unlocked through tangible project evidence, code viva defense, and automated anti-copy rigor — not passive video playlists.
                </p>
            </div>
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid #334155; border-radius: 12px; padding: 14px 18px; min-width: 250px;">
                <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 4px;">🚀 1-CLICK DEMO PERSONAS</div>
                <div style="display: flex; flex-direction: column; gap: 6px;">
                    <button onclick="document.querySelector('[data-testid=stSidebar] button:first-child')?.click()" 
                            style="display:none;"></button>
                    <span style="font-size: 0.85rem; color: #E2E8F0;">• <strong>Arun:</strong> State Board, Tamil medium beginner</span>
                    <span style="font-size: 0.85rem; color: #E2E8F0;">• <strong>Meena:</strong> Biotech student ➔ Bioinformatics</span>
                    <span style="font-size: 0.85rem; color: #E2E8F0;">• <strong>Karthik:</strong> C/Python coder, burned out</span>
                </div>
                <div style="font-size: 0.75rem; color: #38BDF8; margin-top: 8px;">👉 Select any persona from the sidebar anytime!</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------------------
# QUICK METRICS ROW (Current Active Learner)
# -------------------------------------------------------------
roles = get_roles()
target_role_info = roles.get(user["target_role"], {})
readiness = compute_job_readiness(user["verified_skills"], target_role_info.get("skills", {}), user.get("simulated_days", 0))
calib_score, avg_gap, v_count = compute_calibration_score(user["self_ratings"], user["verified_skills"])

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        f"""
        <div class="sherpa-card" style="text-align: center;">
            <div style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase;">Learner Profile</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: #F8FAFC; margin-top: 4px;">{user['avatar']} {user['name']}</div>
            <div style="font-size: 0.8rem; color: #38BDF8;">Type: <strong>{user['learner_type']}</strong></div>
        </div>
        """,
        unsafe_allow_html=True
    )
with c2:
    st.markdown(
        f"""
        <div class="sherpa-card" style="text-align: center;">
            <div style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase;">Summit Target</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: #14B8A6; margin-top: 4px;">🏔️ {user['target_role']}</div>
            <div style="font-size: 0.8rem; color: #94A3B8;">{len(target_role_info.get('skills', {}))} Required Skills</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with c3:
    st.markdown(
        f"""
        <div class="sherpa-card" style="text-align: center;">
            <div style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase;">Job Readiness</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #38BDF8; margin-top: 2px;">{readiness}%</div>
            <div style="font-size: 0.8rem; color: #94A3B8;">Weighted Evidence Proof</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with c4:
    badge_label = "🌟 Honest Learner" if calib_score >= 80 else "⚖️ In Calibration"
    st.markdown(
        f"""
        <div class="sherpa-card" style="text-align: center;">
            <div style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase;">Calibration Score</div>
            <div style="font-size: 1.8rem; font-weight: 900; color: #34D399; margin-top: 2px;">{calib_score}/100</div>
            <div style="font-size: 0.8rem; color: #34D399;">{badge_label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br/>", unsafe_allow_html=True)

# -------------------------------------------------------------
# TABS: 1. ZERO-ASSUMPTION ONBOARDING | 2. LEARNER TYPE CARD | 3. CONFIDENCE VS REALITY
# -------------------------------------------------------------
tab_onboard, tab_profiler, tab_calibration = st.tabs([
    "📝 Zero-Assumption Onboarding", 
    "🧭 AI Profiler & Learner Type",
    "⚖️ Confidence vs Reality Meter"
])

with tab_onboard:
    st.markdown("### 🧗 Step 1: Tell Your Sherpa Where You Are Starting")
    st.markdown(
        "No complex jargon, no gatekeeping. Answer 6 simple questions and let our **ProfilerAgent** tailor the mountain trail."
    )

    with st.form("onboarding_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            name_input = st.text_input("1. What is your name or preferred nickname?", value=user["name"])
            board_input = st.selectbox(
                "2. What was your high school / diploma board?",
                options=["State Board (Vernacular/English)", "CBSE", "ICSE", "Other / Open Schooling"],
                index=0 if "State" in user["board"] else 1
            )
            branch_input = st.selectbox(
                "3. College discipline or background:",
                options=[
                    "Information Technology / Computer Science",
                    "Biotechnology / Life Sciences",
                    "Electronics & Communication",
                    "Mechanical / Civil Engineering",
                    "Commerce / Arts / Self-Taught"
                ],
                index=1 if "Bio" in user["branch"] else 0
            )

        with col_b:
            comfort_input = st.text_input(
                "4. What is your current comfort with computers / coding?",
                value=user["current_comfort"]
            )
            hours_input = st.slider("5. How many hours can you comfortably invest each week?", 3, 40, user["weekly_hours"])
            stress_input = st.select_slider(
                "6. How stressed or anxious do you feel about learning to code?",
                options=["Very Calm & Curious", "Slightly Nervous", "Moderate Pressure", "High Anxiety / Burned Out"],
                value="High Anxiety / Burned Out" if "High" in user["stress_level"] else "Slightly Nervous"
            )

        st.markdown("#### 🎯 Baseline Self-Rating (1: Beginner | 5: Production Ready)")
        st.caption("Be totally honest — calibration is valued higher than fake perfection!")
        
        # Self-rating sliders for target role skills
        role_skills_dict = target_role_info.get("skills", {})
        new_self_ratings = {}
        skill_cols = st.columns(min(len(role_skills_dict), 4))
        
        for idx, (sname, sinfo) in enumerate(role_skills_dict.items()):
            col_target = skill_cols[idx % min(len(role_skills_dict), 4)]
            with col_target:
                current_val = user["self_ratings"].get(sname, 1)
                new_self_ratings[sname] = st.slider(f"{sname}:", 1, 5, current_val, key=f"self_rate_{sname}")

        submit_onboard = st.form_submit_button("🚀 Submit to ProfilerAgent & Launch Expedition", use_container_width=True)

        if submit_onboard:
            user["name"] = name_input
            user["board"] = board_input
            user["branch"] = branch_input
            user["current_comfort"] = comfort_input
            user["weekly_hours"] = hours_input
            user["stress_level"] = stress_input
            user["self_ratings"] = new_self_ratings
            
            # Execute Orchestrator event
            res = orchestrator.handle_event("onboarding_done", {
                "name": name_input,
                "board": board_input,
                "branch": branch_input,
                "current_comfort": comfort_input,
                "weekly_hours": hours_input,
                "stress_level": stress_input,
                "target_role": user["target_role"],
                "self_ratings": new_self_ratings,
                "verified_skills": user["verified_skills"]
            })
            
            user["learner_type"] = res.get("profile", {}).get("learner_type", "Foundation")
            user["pressure_free_mode"] = res.get("profile", {}).get("suggested_pressure_free", True)
            user["tanglish_mode"] = res.get("profile", {}).get("suggested_tanglish", False)
            
            st.success(f"✅ Onboarding complete! ProfilerAgent classified your profile as '{user['learner_type']}'.")
            st.rerun()

with tab_profiler:
    st.markdown("### 🔍 ProfilerAgent Diagnosis")
    l_type = user["learner_type"]
    
    type_cards = {
        "Foundation": {
            "title": "🏕️ Foundation Learner (Step-by-Step Vernacular Path)",
            "desc": "Prioritizes plain-English & Tanglish explanations, zero technical gatekeeping, and confidence-building small projects before theory.",
            "color": "#14B8A6",
            "perks": ["Jargon auto-translation enabled", "Pressure-Free Mode active", "Bite-sized weekly quests"]
        },
        "Bridge": {
            "title": "🧬 Bridge Path (Domain to Code Convergence)",
            "desc": "Explicitly leverages prior non-CS knowledge (e.g. Molecular Biology, Genetics) as an asset rather than a deficit. Fast-tracks computational domain tools.",
            "color": "#8B5CF6",
            "perks": ["Domain-first project templates", "Skip generic toy apps", "Niche industry matchmaker"]
        },
        "Pressure-relief": {
            "title": "⚡ Pressure-Relief Learner (Calm Agency & Autonomy)",
            "desc": "Engineered for learners burned out by competitive LeetCode and toxic streaks. Eliminates all countdown timers, guilt-inducing streak losses, and leaderboards.",
            "color": "#38BDF8",
            "perks": ["Zero streak penalties", "Autonomy-driven project choice", "Async code defense viva"]
        },
        "Fast-track": {
            "title": "🚀 Fast-Track Learner (Placement Test Skip-Ahead)",
            "desc": "Bypasses standard prerequisite reading via instant placement viva challenges. Ideal for experienced developers adding new stack proficiencies.",
            "color": "#10B981",
            "perks": ["Direct challenge bypass", "Advanced architectural vivas", "Immediate recruiter passport visibility"]
        }
    }
    
    current_card = type_cards.get(l_type, type_cards["Foundation"])
    
    st.markdown(
        f"""
        <div class="sherpa-card-highlight">
            <h3 style="color: {current_card['color']}; margin-top: 0;">{current_card['title']}</h3>
            <p style="font-size: 1.05rem; color: #E2E8F0; line-height: 1.6;">{current_card['desc']}</p>
            <div style="margin-top: 16px;">
                <strong style="color: #F8FAFC;">Active Accommodations:</strong>
                <ul style="color: #94A3B8; margin-top: 6px;">
                    {''.join([f"<li>{p}</li>" for p in current_card['perks']])}
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("#### 🧭 Live Inter-Agent Handoff")
    st.info(
        f"**ProfilerAgent ➔ GapAnalystAgent**: Profiling data analyzed for **{user['name']}**. "
        f"Goal: **{user['target_role']}**. Adaptive mode: **{l_type}**."
    )

with tab_calibration:
    st.markdown("### ⚖️ Confidence vs Reality Meter")
    st.markdown(
        """
        > **"Calibration = knowing yourself."**  
        > Traditional platforms encourage learners to click 5-star ratings or cheat on multiple-choice quizzes. 
        > SkillSherpa measures how accurately your self-perception matches verified project evidence. 
        > High calibration builds authentic self-knowledge that recruiters trust implicitly.
        """
    )
    
    calib_val, gap_val, v_count = compute_calibration_score(user["self_ratings"], user["verified_skills"])
    
    col_meter, col_chart = st.columns([1, 2])
    
    with col_meter:
        st.markdown(
            f"""
            <div class="sherpa-card" style="text-align: center; height: 100%;">
                <h4 style="color: #94A3B8; margin-bottom: 4px;">CALIBRATION SCORE</h4>
                <div style="font-size: 3.2rem; font-weight: 900; color: #34D399;">{calib_val}/100</div>
                <div style="font-size: 0.95rem; color: #E2E8F0; margin-top: 8px;">
                    Avg Perception Gap: <strong>{gap_val} levels</strong>
                </div>
                <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 6px;">
                    Verified Evidence Points: <strong>{v_count}</strong>
                </div>
                <div style="margin-top: 16px;">
                    <span class="{'badge-green' if calib_val >= 80 else 'badge-blue'}">
                        {'🌟 Awarded Honest Learner Badge' if calib_val >= 80 else '🧗 Building Calibration Data'}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_chart:
        # Side-by-side bar chart: Self Rating vs Verified Level
        skills_to_plot = list(user["self_ratings"].keys())
        self_vals = [user["self_ratings"].get(s, 1) for s in skills_to_plot]
        verified_vals = [user["verified_skills"].get(s, {}).get("level", 0) for s in skills_to_plot]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=skills_to_plot,
            y=self_vals,
            name="Self-Assessed Confidence",
            marker_color="#38BDF8"
        ))
        fig.add_trace(go.Bar(
            x=skills_to_plot,
            y=verified_vals,
            name="Verified Proof Level",
            marker_color="#10B981"
        ))
        fig.update_layout(
            barmode="group",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F0F3F8"),
            yaxis=dict(title="Skill Level (1-5)", range=[0, 5.5], gridcolor="#334155"),
            xaxis=dict(gridcolor="rgba(0,0,0,0)"),
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown("<br/>", unsafe_allow_html=True)
render_agent_collaboration_panel()

