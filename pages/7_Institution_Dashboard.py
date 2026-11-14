"""
SkillSherpa: Institution & Campus Placement Analytics Dashboard
Visualizes cohort skill heatmaps, missing skill gaps, board equity breakdowns, and at-risk interventions.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ui import inject_theme, render_sidebar, render_agent_collaboration_panel, render_page_header, render_goal_diff_alert
from data_loader import init_session_state, get_cohort, get_roles

inject_theme()
init_session_state()
render_sidebar()
render_goal_diff_alert()

render_page_header(
    title="🏫 Institution & Campus Placement Intelligence",
    subtitle="Audit cohort readiness across 60 students. Spot systemic curricular gaps before placement season.",
    badge_text="Campus Dean Portal"
)

cohort = get_cohort()
df = pd.DataFrame(cohort)

# -------------------------------------------------------------
# TOP METRICS
# -------------------------------------------------------------
avg_readiness = int(df["readiness_score"].mean())
at_risk_count = int(df["at_risk"].sum())
state_board_count = int((df["board"] == "State Board").sum())
verified_skill_events = sum(
    sum(1 for s in row["skills"].values() if s.get("verified_level", 0) > 0)
    for row in cohort
)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(
        f"""
        <div class="sherpa-card" style="text-align: center;">
            <div style="font-size: 0.8rem; color: #94A3B8;">COHORT SIZE</div>
            <div style="font-size: 2rem; font-weight: 800; color: #F8FAFC;">{len(df)}</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Across 6 Branches</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with m2:
    st.markdown(
        f"""
        <div class="sherpa-card" style="text-align: center;">
            <div style="font-size: 0.8rem; color: #94A3B8;">AVG JOB READINESS</div>
            <div style="font-size: 2rem; font-weight: 800; color: #38BDF8;">{avg_readiness}%</div>
            <div style="font-size: 0.75rem; color: #10B981;">+14% vs last semester</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with m3:
    st.markdown(
        f"""
        <div class="sherpa-card" style="text-align: center;">
            <div style="font-size: 0.8rem; color: #94A3B8;">AT-RISK LEARNERS</div>
            <div style="font-size: 2rem; font-weight: 800; color: #EF4444;">{at_risk_count}</div>
            <div style="font-size: 0.75rem; color: #EF4444;">Need Foundation Support</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with m4:
    st.markdown(
        f"""
        <div class="sherpa-card" style="text-align: center;">
            <div style="font-size: 0.8rem; color: #94A3B8;">VERIFIED PROOFS</div>
            <div style="font-size: 2rem; font-weight: 800; color: #10B981;">{verified_skill_events}</div>
            <div style="font-size: 0.75rem; color: #10B981;">Audited Code Artifacts</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br/>", unsafe_allow_html=True)

# -------------------------------------------------------------
# ROW 1: SKILLS X STUDENTS HEATMAP
# -------------------------------------------------------------
st.markdown("### 🗺️ Cohort Competency Heatmap (Skills × Students Sample)")
st.caption("Visualizes verified proficiency levels (0 = Unverified, 1-4 = Verified Mastery)")

sample_students = cohort[:25]
student_names = [s["name"] for s in sample_students]

# Collect all unique skills in sample
all_skills = set()
for s in sample_students:
    all_skills.update(s.get("skills", {}).keys())
all_skills = sorted(list(all_skills))

matrix = []
for s in sample_students:
    row = []
    for sk in all_skills:
        val = s.get("skills", {}).get(sk, {}).get("verified_level", 0)
        row.append(val)
    matrix.append(row)

heatmap_fig = go.Figure(data=go.Heatmap(
    z=matrix,
    x=all_skills,
    y=student_names,
    colorscale=[
        [0.0, "#0F172A"],
        [0.25, "#1E3A8A"],
        [0.5, "#0D9488"],
        [0.75, "#14B8A6"],
        [1.0, "#34D399"]
    ],
    colorbar=dict(title="Level", tickvals=[0, 1, 2, 3, 4], ticktext=["None", "Lvl 1", "Lvl 2", "Lvl 3", "Lvl 4"]),
    hoverongaps=False
))
heatmap_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#F8FAFC"),
    height=450,
    margin=dict(l=80, r=20, t=20, b=80),
    xaxis=dict(tickangle=-30)
)
st.plotly_chart(heatmap_fig, use_container_width=True)

st.markdown("<br/>", unsafe_allow_html=True)

# -------------------------------------------------------------
# ROW 2: TOP 5 MISSING SKILLS & EQUITY BREAKDOWNS
# -------------------------------------------------------------
col_missing, col_equity = st.columns([1.2, 1])

with col_missing:
    st.markdown("### ⚠️ Top 5 Curricular Deficits (Missing Skills)")
    st.caption("Highest proportion of unverified skills across the student body.")

    # Calculate deficit per skill
    skill_counts = {}
    skill_missing = {}
    for c in cohort:
        for sk, sinfo in c.get("skills", {}).items():
            skill_counts[sk] = skill_counts.get(sk, 0) + 1
            if sinfo.get("verified_level", 0) == 0:
                skill_missing[sk] = skill_missing.get(sk, 0) + 1

    missing_rates = []
    for sk in skill_counts:
        rate = int((skill_missing[sk] / skill_counts[sk]) * 100)
        missing_rates.append({"skill": sk, "missing_pct": rate})
    
    missing_df = pd.DataFrame(missing_rates).sort_values("missing_pct", ascending=False).head(5)

    bar_fig = px.bar(
        missing_df,
        x="missing_pct",
        y="skill",
        orientation="h",
        color="missing_pct",
        color_continuous_scale=["#F59E0B", "#EF4444"],
        text="missing_pct"
    )
    bar_fig.update_traces(texttemplate='%{text}% Missing', textposition='inside')
    bar_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC"),
        height=260,
        margin=dict(l=20, r=20, t=10, b=20),
        xaxis=dict(title="Percentage of Students Lacking Proof", range=[0, 100], gridcolor="#334155"),
        yaxis=dict(title="", autorange="reversed"),
        coloraxis_showscale=False
    )
    st.plotly_chart(bar_fig, use_container_width=True)

with col_equity:
    st.markdown("### 🏛️ Readiness by School Board")
    st.caption("Evaluating vernacular vs CBSE transition parity.")

    board_df = df.groupby("board")["readiness_score"].mean().reset_index()
    board_df["readiness_score"] = board_df["readiness_score"].round().astype(int)

    board_fig = px.bar(
        board_df,
        x="board",
        y="readiness_score",
        color="board",
        color_discrete_sequence=["#14B8A6", "#38BDF8", "#8B5CF6"],
        text="readiness_score"
    )
    board_fig.update_traces(texttemplate='%{text}% Avg', textposition='outside')
    board_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC"),
        height=260,
        margin=dict(l=20, r=20, t=10, b=20),
        yaxis=dict(range=[0, 100], gridcolor="#334155", title="Avg Job Readiness"),
        xaxis=dict(title=""),
        showlegend=False
    )
    st.plotly_chart(board_fig, use_container_width=True)

st.markdown("<br/>", unsafe_allow_html=True)

# -------------------------------------------------------------
# ROW 3: AT-RISK LEARNERS & CSV DOWNLOAD
# -------------------------------------------------------------
st.markdown("### 🚨 At-Risk Learner Intervention Roster")
st.caption("Students needing targeted Sherpa vernacular workshops and zero-pressure pacing.")

at_risk_learners = df[df["at_risk"]][["id", "name", "branch", "board", "target_role", "readiness_score"]]

st.dataframe(
    at_risk_learners,
    use_container_width=True,
    hide_index=True
)

# CSV Export
csv_data = df.to_csv(index=False)
st.download_button(
    label="📥 Download Full Institution Audit Report (CSV)",
    data=csv_data,
    file_name=f"SkillSherpa_Cohort_Audit_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
    use_container_width=True
)

st.markdown("<br/>", unsafe_allow_html=True)
render_agent_collaboration_panel()

