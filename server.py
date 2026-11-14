"""
SkillSherpa Backend API Server (FastAPI + Uvicorn)
Connects the 7-agent swarm to a production-grade REST API and serves the modern frontend.
"""

import os
import time
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

import scoring
import data_loader
from agents import orchestrator
from llm import get_llm_status

app = FastAPI(
    title="SkillSherpa API",
    description="The Trust Layer for Skills: Agentic Learning, Skill Verification, and Evidence Auditing API",
    version="1.0.0"
)

# Enable CORS for local and cross-origin frontend integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# PYDANTIC SCHEMAS
# -------------------------------------------------------------
class OnboardingRequest(BaseModel):
    name: str
    board: str
    branch: str
    current_comfort: str
    weekly_hours: int = 10
    stress_level: str = "Medium"
    target_role: str = "Full Stack Developer"
    self_ratings: Dict[str, int] = {}

class AssessSubmissionRequest(BaseModel):
    skill: str
    target_level: int = 2
    mcq_score: int
    viva_answer: str
    time_taken_seconds: int = 45
    project_url: str
    persona_id: Optional[str] = "arun"

class MentorChatRequest(BaseModel):
    message: str
    tanglish: bool = False
    persona_id: Optional[str] = "arun"

class ResumeRequest(BaseModel):
    name: str
    target_role: str
    verified_skills: Dict[str, Any]
    self_ratings: Dict[str, int]
    board: str
    branch: str
    learner_type: str

# -------------------------------------------------------------
# API ROUTES
# -------------------------------------------------------------

@app.get("/api/health")
def health_check():
    status_txt, icon, is_live = get_llm_status()
    return {
        "status": "healthy",
        "service": "SkillSherpa API",
        "llm_mode": status_txt,
        "is_live_ai": is_live,
        "active_agents": ["Profiler", "GapAnalyst", "Curator", "Assessor", "Mentor", "Opportunity", "Orchestrator"]
    }

@app.get("/api/personas")
def get_all_personas():
    """Returns the 3 preloaded demo personas."""
    return data_loader.get_personas()

@app.get("/api/personas/{persona_id}")
def get_persona(persona_id: str):
    personas = data_loader.get_personas()
    if persona_id not in personas:
        raise HTTPException(status_code=404, detail=f"Persona '{persona_id}' not found.")
    return personas[persona_id]

@app.get("/api/roles")
def get_roles():
    """Lists all Summit career roles with weights and prerequisite graphs."""
    return data_loader.get_roles()

@app.post("/api/onboarding")
def submit_onboarding(req: OnboardingRequest):
    """Processes zero-assumption onboarding via ProfilerAgent and GapAnalystAgent."""
    payload = {
        "name": req.name,
        "board": req.board,
        "branch": req.branch,
        "current_comfort": req.current_comfort,
        "weekly_hours": req.weekly_hours,
        "stress_level": req.stress_level,
        "target_role": req.target_role,
        "self_ratings": req.self_ratings,
        "verified_skills": {}
    }
    result = orchestrator.handle_event("onboarding_done", payload)
    return result

@app.get("/api/gaps")
def compute_gaps(persona_id: str = "arun", role: Optional[str] = None, sim_days: int = 0):
    """Evaluates readiness score and skill gaps for a user profile."""
    personas = data_loader.get_personas()
    user = personas.get(persona_id, personas["arun"])
    target_role = role or user.get("target_role", "Full Stack Developer")
    user_copy = dict(user)
    user_copy["simulated_days"] = sim_days

    gap_data = orchestrator.gap_analyst.run(user_copy, target_role)
    calib_score, avg_gap, v_count = scoring.compute_calibration_score(
        user.get("self_ratings", {}), user.get("verified_skills", {})
    )

    return {
        "readiness_score": gap_data["readiness_score"],
        "calibration_score": calib_score,
        "avg_gap": avg_gap,
        "verified_count": v_count,
        "gaps": gap_data["gaps"],
        "target_role": target_role
    }

@app.get("/api/roadmap")
def get_roadmap(persona_id: str = "arun", role: Optional[str] = None):
    """Assembles the prerequisite-safe mountain trail with resources and mini projects."""
    personas = data_loader.get_personas()
    user = personas.get(persona_id, personas["arun"])
    target_role = role or user.get("target_role", "Full Stack Developer")

    trail = orchestrator.curator.run(
        target_role=target_role,
        verified_skills=user.get("verified_skills", {}),
        learner_type=user.get("learner_type", "Foundation")
    )
    return {"trail": trail, "target_role": target_role}

@app.get("/api/assess/challenge/{skill_name}")
def get_assessment_challenge(skill_name: str):
    """Generates fresh MCQs and AI code viva challenge for a given skill."""
    challenge = orchestrator.assessor.generate_assessment(skill_name)
    return challenge

@app.post("/api/assess/submit")
def submit_assessment(sub: AssessSubmissionRequest):
    """Evaluates assessment submission with anti-copy timing and rubric grading."""
    personas = data_loader.get_personas()
    user = personas.get(sub.persona_id, personas["arun"])

    eval_result = orchestrator.handle_event("quiz_completed", {
        "skill": sub.skill,
        "target_level": sub.target_level,
        "mcq_score": sub.mcq_score,
        "viva_answer": sub.viva_answer,
        "time_taken": sub.time_taken_seconds,
        "project_url": sub.project_url,
        "user_data": user
    })

    return eval_result

@app.post("/api/mentor/chat")
def mentor_chat(chat_req: MentorChatRequest):
    """Converses with the AI Sherpa Mentor with Tanglish and tone adaptation."""
    personas = data_loader.get_personas()
    user = personas.get(chat_req.persona_id, personas["arun"])

    profile_summary = (
        f"Name: {user['name']}, Board: {user['board']}, Branch: {user['branch']}, "
        f"Learner Type: {user['learner_type']}, Target: {user['target_role']}, "
        f"Verified: {list(user.get('verified_skills', {}).keys())}"
    )

    reply = orchestrator.mentor.get_chat_response(
        user_msg=chat_req.message,
        profile_summary=profile_summary,
        tanglish=chat_req.tanglish
    )

    return {"reply": reply, "persona": user["name"], "tanglish": chat_req.tanglish}

@app.get("/api/opportunities")
def get_opportunities(persona_id: str = "arun", sim_days: int = 0):
    """Surfaces strictly verified opportunity matches and near-term unlocks."""
    personas = data_loader.get_personas()
    user = personas.get(persona_id, personas["arun"])

    opps = orchestrator.opportunity.run(user.get("verified_skills", {}), sim_days)
    return opps

@app.get("/api/cohort")
def get_cohort():
    """Returns the 60-student cohort dataset for institution dean analytics."""
    return data_loader.get_cohort()

@app.get("/api/jargon")
def get_jargon():
    """Returns technical jargon entries explained in simple English and Tanglish."""
    return data_loader.get_jargon()

@app.post("/api/resume")
def generate_resume(req: ResumeRequest):
    """Composes an ATS-optimized single-column resume text strictly from verified proofs."""
    calib_score, _, _ = scoring.compute_calibration_score(req.self_ratings, req.verified_skills)

    skills_lines = [f"{sn} (Level {v.get('level', 1)} Verified)" for sn, v in req.verified_skills.items()]
    skills_str = ", ".join(skills_lines) if skills_lines else "Skills in verification pipeline"

    project_sections = []
    for sn, v in req.verified_skills.items():
        project_sections.append(
            f"### {sn} Implementation & Architecture\n"
            f"- Repository Evidence: {v.get('project_url', 'https://github.com/user/demo')}\n"
            f"- Audit: MCQ {v.get('quiz_score', 80)}% | AI Viva {v.get('viva_score', 80)}%\n"
            f"- Deliverable: Tested, modular implementation with defensive error handling."
        )
    projects_str = "\n\n".join(project_sections) if project_sections else "No verified projects."

    resume_text = f"""# {req.name.upper()}
Aspiring {req.target_role}
Verified Proof Portfolio: https://skillsherpa.live/p/SKSH-2026-VERIFIED
GitHub: https://github.com/{req.name.lower().replace(' ', '-')}

---

## PROFESSIONAL SUMMARY
Passionate and disciplined {req.target_role} verified through SkillSherpa's agentic proof layer.
Self-Calibration Score: {calib_score}/100 ('Honest Learner' Badge). 
Demonstrated ability to write version-controlled code, build end-to-end architectures, and defend designs in AI code vivas.

---

## VERIFIED COMPETENCIES
- Skills: {skills_str}
- Calibration: {calib_score}/100 (High Self-Knowledge)
- Focus: Semantic architecture, defensive error handling, Git version control

---

## AUDITED PROJECT ARTIFACTS
{projects_str}

---

## EDUCATION
- Discipline: {req.branch}
- Background: {req.board}
- Track: SkillSherpa {req.learner_type} Expedition
"""
    return {"resume_markdown": resume_text}

# -------------------------------------------------------------
# STATIC FILE SERVING FOR FRONTEND
# -------------------------------------------------------------
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    def serve_frontend():
        return FileResponse(os.path.join(frontend_dir, "index.html"))

if __name__ == "__main__":
    import uvicorn
    print("\n🧗‍♂️ SkillSherpa Full-Stack Server Starting...")
    print("👉 Website URL: http://localhost:8000")
    print("👉 API Documentation (Swagger UI): http://localhost:8000/docs\n")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
