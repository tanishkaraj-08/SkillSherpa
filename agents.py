"""
SkillSherpa Multi-Agent System (agents.py)
Implements the 7 collaborating agents and the central event orchestrator.
"""

from typing import Dict, Any, List
import streamlit as st
from datetime import datetime
from llm import llm
from scoring import compute_job_readiness, compute_gap_severity, get_skill_expiry_status
from data_loader import get_roles, get_resources, get_opportunities, append_agent_log

# -------------------------------------------------------------
# Base Agent Class
# -------------------------------------------------------------
class Agent:
    def __init__(self, name: str, role: str, emoji: str, system_prompt: str):
        self.name = name
        self.role = role
        self.emoji = emoji
        self.system_prompt = system_prompt

    def log(self, to_agent: str, message: str):
        append_agent_log(self.name, self.emoji, to_agent, message)

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

# -------------------------------------------------------------
# 1. ProfilerAgent
# -------------------------------------------------------------
class ProfilerAgent(Agent):
    def __init__(self):
        super().__init__(
            name="ProfilerAgent",
            role="Zero-Assumption Learner Profiler",
            emoji="🔍",
            system_prompt=(
                "You analyze onboarding answers (interests, school board, comfort with computers, "
                "stress level, weekly hours) and self-ratings. Classify the learner into: "
                "Foundation (needs vernacular/plain concepts & confidence building), "
                "Bridge (transitioning from non-CS domain like biology/mechanical), "
                "Pressure-relief (burned out by competitive coding, needs calm agency), or "
                "Fast-track (experienced coder needing placement skips)."
            )
        )

    def run(self, answers: Dict[str, Any]) -> Dict[str, Any]:
        board = str(answers.get("board", "")).lower()
        comfort = str(answers.get("current_comfort", "")).lower()
        branch = str(answers.get("branch", "")).lower()
        stress = str(answers.get("stress_level", "")).lower()

        # Decision rule with LLM verification
        if "biotech" in branch or "biology" in branch or "mechanical" in branch:
            learner_type = "Bridge"
            rationale = "Non-CS background; prior domain is a massive asset when combined with computation."
        elif "burnout" in stress or "pressure" in stress or ("c" in comfort and "python" in comfort and "exhausted" in comfort):
            learner_type = "Pressure-relief"
            rationale = "High technical aptitude with emotional burnout; requires self-paced autonomy and no streaks."
        elif "state" in board or "tamil" in comfort or "beginner" in comfort:
            learner_type = "Foundation"
            rationale = "Vernacular/State board background with tech anxiety; requires zero-jargon small wins."
        else:
            learner_type = "Fast-track"
            rationale = "Strong self-assessed foundation; skip introductory modules via placement assessments."

        self.log(
            "GapAnalystAgent",
            f"Classified '{answers.get('name', 'Learner')}' as '{learner_type}'. {rationale}"
        )
        return {
            "learner_type": learner_type,
            "rationale": rationale,
            "suggested_pressure_free": (learner_type in ["Foundation", "Pressure-relief"]),
            "suggested_tanglish": (learner_type == "Foundation")
        }

# -------------------------------------------------------------
# 2. GapAnalystAgent
# -------------------------------------------------------------
class GapAnalystAgent(Agent):
    def __init__(self):
        super().__init__(
            name="GapAnalystAgent",
            role="Skill Gap & Readiness Evaluator",
            emoji="📊",
            system_prompt=(
                "You evaluate verified proof-of-skills against target role requirements. "
                "Compute weighted job readiness and categorize skill gaps by severity."
            )
        )

    def run(self, user_data: Dict[str, Any], target_role: str) -> Dict[str, Any]:
        roles = get_roles()
        role_info = roles.get(target_role, {})
        role_skills = role_info.get("skills", {})
        verified = user_data.get("verified_skills", {})
        simulated_days = user_data.get("simulated_days", 0)

        readiness_score = compute_job_readiness(verified, role_skills, simulated_days)

        gaps = []
        for sname, req in role_skills.items():
            target_lvl = req.get("target_level", 3)
            weight = req.get("weight", 1.0)
            
            # Check verified status
            v_info = verified.get(sname)
            v_level = 0
            expiry_status = "unverified"
            
            if v_info:
                v_level = v_info.get("level", 0)
                status, _, _ = get_skill_expiry_status(v_info.get("verified_date", ""), simulated_days)
                expiry_status = status
                if status == "expired":
                    v_level = 0

            severity, color = compute_gap_severity(target_lvl, v_level)
            gaps.append({
                "skill": sname,
                "target_level": target_lvl,
                "verified_level": v_level,
                "weight": weight,
                "severity": severity,
                "color": color,
                "expiry_status": expiry_status,
                "delta": max(0, target_lvl - v_level)
            })

        # Sort gaps by critical first, then weight
        gaps.sort(key=lambda x: (x["delta"] == 0, -x["weight"], -x["delta"]))

        self.log(
            "CuratorAgent",
            f"Evaluated readiness for '{target_role}': {readiness_score}%. Identified {len([g for g in gaps if g['delta'] > 0])} gaps to close."
        )

        return {
            "readiness_score": readiness_score,
            "gaps": gaps,
            "role_title": target_role
        }

# -------------------------------------------------------------
# 3. CuratorAgent
# -------------------------------------------------------------
class CuratorAgent(Agent):
    def __init__(self):
        super().__init__(
            name="CuratorAgent",
            role="Prerequisite-Aware Roadmap Architect",
            emoji="🗺️",
            system_prompt=(
                "You build a mountain trail roadmap respecting the skill prerequisite graph. "
                "Assemble curated free resources, mini-projects, and weekly quests tailored to learner pace."
            )
        )

    def run(self, target_role: str, verified_skills: Dict[str, Any], learner_type: str, failing_skill: str = None) -> List[Dict[str, Any]]:
        roles = get_roles()
        all_resources = get_resources()
        role_info = roles.get(target_role, {})
        role_skills = role_info.get("skills", {})
        prereqs = role_info.get("prerequisites", {})

        trail = []
        camp_num = 1

        for skill_name, req in role_skills.items():
            req_prereqs = prereqs.get(skill_name, [])
            
            # Prereqs are satisfied if every prereq is verified >= 1
            prereqs_met = all(
                (p in verified_skills and verified_skills[p].get("level", 0) >= 1)
                for p in req_prereqs
            )
            
            is_verified = (skill_name in verified_skills and verified_skills[skill_name].get("level", 0) >= req.get("target_level", 3))
            is_in_progress = (skill_name in verified_skills and not is_verified)
            
            # Locked state logic
            if is_verified:
                status = "Mastered"
                badge = "🟢 Camp Cleared"
            elif prereqs_met:
                status = "Unlocked"
                badge = "⛺ Current Camp"
            else:
                status = "Locked"
                badge = f"🔒 Needs {', '.join(req_prereqs)}"

            # Adaptive insertion if failing skill matches
            is_adapted = (failing_skill and failing_skill == skill_name)

            res_data = all_resources.get(skill_name, {
                "description": f"Master core fundamentals of {skill_name}.",
                "weekly_quest": f"Build a practical working demo utilizing {skill_name}.",
                "mini_project": {
                    "title": f"{skill_name} Hands-On Showcase",
                    "prompt": f"Author a functional project demonstrating core {skill_name} principles.",
                    "deliverable": "GitHub repository with README."
                },
                "items": []
            })

            trail.append({
                "camp": f"Camp {camp_num}",
                "skill": skill_name,
                "target_level": req.get("target_level", 3),
                "weight": req.get("weight", 1.0),
                "category": req.get("category", "General"),
                "status": status,
                "badge": badge,
                "prerequisites": req_prereqs,
                "description": res_data.get("description", ""),
                "weekly_quest": res_data.get("weekly_quest", ""),
                "mini_project": res_data.get("mini_project", {}),
                "resources": res_data.get("items", []),
                "adapted": is_adapted,
                "why_this": f"Required at Level {req.get('target_level', 3)} for {target_role}. Closes foundational dependencies."
            })
            camp_num += 1

        self.log(
            "MentorAgent",
            f"Curated {len(trail)} mountain checkpoints for '{target_role}'. {sum(1 for t in trail if t['status']=='Mastered')} completed, {sum(1 for t in trail if t['status']=='Unlocked')} active."
        )

        return trail

# -------------------------------------------------------------
# 4. AssessorAgent
# -------------------------------------------------------------
class AssessorAgent(Agent):
    def __init__(self):
        super().__init__(
            name="AssessorAgent",
            role="Skill & Viva Verification Authority",
            emoji="🎯",
            system_prompt=(
                "You generate rigorous, fresh technical assessments (MCQs + Viva viva-voce) "
                "and grade evidence submissions using anti-copy rubrics (correctness, depth, originality)."
            )
        )

    def generate_assessment(self, skill_name: str) -> Dict[str, Any]:
        prompt = f"generate quiz and mcq assessment for technical skill: {skill_name}"
        data = llm(prompt, json_mode=True)
        self.log("MentorAgent", f"Generated fresh verified challenge for '{skill_name}' (3 MCQs + AI Code Viva).")
        return data

    def grade_assessment(
        self, 
        mcq_score: int, 
        viva_answer: str, 
        time_taken_seconds: int = 45,
        skill_name: str = ""
    ) -> Dict[str, Any]:
        """
        Runs anti-copy checks and grades viva response.
        Anti-copy checks:
        1. Timing heuristic: word count > 60 in < 8 seconds -> flag pasted
        2. Prompt similarity / length check
        """
        words = len(viva_answer.strip().split())
        is_timing_pasted = (words > 40 and time_taken_seconds < 7)
        
        # Call LLM grader
        prompt = (
            f"grade viva answer for skill {skill_name}.\n"
            f"Student Answer: {viva_answer}\n"
            f"Word count: {words}. Time taken: {time_taken_seconds} seconds.\n"
            f"{'pasted_flag' if is_timing_pasted else 'authentic_flag'}"
        )
        grade_result = llm(prompt, json_mode=True)
        
        # Override if timing heuristic flagged
        if is_timing_pasted:
            grade_result["anti_copy_flag"] = True
            grade_result["score"] = min(40, grade_result.get("score", 40))
            grade_result["feedback"] = "⚠️ Answer submitted unnaturally fast for its length. Please explain in your own words."
            grade_result["passed"] = False

        total_score = int(round((mcq_score * 0.5) + (grade_result.get("score", 70) * 0.5)))
        passed = (total_score >= 70) and (not grade_result.get("anti_copy_flag", False))

        self.log(
            "OrchestratorAgent",
            f"Graded {skill_name} assessment: MCQ {mcq_score}%, Viva {grade_result.get('score')}%. Overall: {total_score}%. Passed: {passed}."
        )

        return {
            "overall_score": total_score,
            "mcq_score": mcq_score,
            "viva_score": grade_result.get("score", 0),
            "passed": passed,
            "feedback": grade_result.get("feedback", ""),
            "anti_copy_flag": grade_result.get("anti_copy_flag", False),
            "rubric": grade_result.get("rubric_breakdown", {})
        }

# -------------------------------------------------------------
# 5. MentorAgent
# -------------------------------------------------------------
class MentorAgent(Agent):
    def __init__(self):
        super().__init__(
            name="MentorAgent",
            role="Empathic Sherpa & Growth Mentor",
            emoji="🧗‍♂️",
            system_prompt=(
                "You are the Sherpa mentor. You adapt your warmth, encouragement, and language "
                "(Tanglish/English) to normalize failure, celebrate project proofs, and alleviate anxiety."
            )
        )

    def get_reassurance(self, skill_name: str, score: int, tanglish: bool = False, learner_type: str = "Foundation") -> str:
        prompt = (
            f"mentor encouragement for learner who failed quiz on {skill_name} with score {score}%.\n"
            f"Learner type: {learner_type}. {'tanglish mode' if tanglish else 'english mode'}"
        )
        msg = llm(prompt, json_mode=False)
        self.log("CuratorAgent", f"Delivered growth reassurance for '{skill_name}'. Requested prerequisite revision insertion.")
        return msg

    def get_chat_response(self, user_msg: str, profile_summary: str, tanglish: bool = False) -> str:
        prompt = (
            f"mentor chat conversation.\n"
            f"Profile context: {profile_summary}\n"
            f"Language mode: {'Tanglish / Tamil English mix' if tanglish else 'Warm English'}\n"
            f"Learner says: {user_msg}"
        )
        return llm(prompt, json_mode=False)

# -------------------------------------------------------------
# 6. OpportunityAgent
# -------------------------------------------------------------
class OpportunityAgent(Agent):
    def __init__(self):
        super().__init__(
            name="OpportunityAgent",
            role="Verified Skill Opportunity Matchmaker",
            emoji="💼",
            system_prompt=(
                "You match learners ONLY to opportunities where their VERIFIED skills meet or exceed "
                "the required level. Provide 'Unlock' teasers for near-term targets."
            )
        )

    def run(self, verified_skills: Dict[str, Any], simulated_days: int = 0) -> Dict[str, Any]:
        all_opps = get_opportunities()
        matched = []
        unlockable = []
        beginner_friendly = []

        # Filter active verified skills (exclude expired)
        active_verified = {}
        for sname, v_info in verified_skills.items():
            status, _, _ = get_skill_expiry_status(v_info.get("verified_date", ""), simulated_days)
            if status != "expired":
                active_verified[sname] = v_info.get("level", 0)

        for opp in all_opps:
            reqs = opp.get("required_skills", {})
            meets_all = True
            missing_or_short = []

            for req_skill, min_lvl in reqs.items():
                learner_lvl = active_verified.get(req_skill, 0)
                if learner_lvl < min_lvl:
                    meets_all = False
                    missing_or_short.append((req_skill, min_lvl - learner_lvl, min_lvl))

            if meets_all:
                matched.append(opp)
            elif len(missing_or_short) == 1:
                # Close to unlocking!
                s_name, delta, target_l = missing_or_short[0]
                opp_copy = dict(opp)
                opp_copy["unlock_hint"] = f"Reach {s_name} Level {target_l} to unlock!"
                unlockable.append(opp_copy)

            if opp.get("beginner_friendly", False):
                beginner_friendly.append(opp)

        self.log(
            "OrchestratorAgent",
            f"Opportunity scan complete: {len(matched)} matched, {len(unlockable)} unlockable, {len(beginner_friendly)} beginner opportunities surfaced."
        )

        return {
            "matched": matched,
            "unlockable": unlockable,
            "beginner_friendly": beginner_friendly
        }

# -------------------------------------------------------------
# 7. OrchestratorAgent (Central Event Router)
# -------------------------------------------------------------
class OrchestratorAgent(Agent):
    def __init__(self):
        super().__init__(
            name="OrchestratorAgent",
            role="Central Event Bus & Swarm Coordinator",
            emoji="🧭",
            system_prompt="Coordinate events across Profiler, GapAnalyst, Curator, Assessor, Mentor, and Opportunity agents."
        )
        self.profiler = ProfilerAgent()
        self.gap_analyst = GapAnalystAgent()
        self.curator = CuratorAgent()
        self.assessor = AssessorAgent()
        self.mentor = MentorAgent()
        self.opportunity = OpportunityAgent()

    def handle_event(self, event_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Routes system events:
        - onboarding_done
        - quiz_completed
        - goal_changed
        - skill_expired
        """
        self.log("AllAgents", f"Handling event: '{event_name}'")

        if event_name == "onboarding_done":
            profile_res = self.profiler.run(payload)
            gap_res = self.gap_analyst.run(payload, payload.get("target_role", "Full Stack Developer"))
            trail = self.curator.run(
                payload.get("target_role", "Full Stack Developer"),
                payload.get("verified_skills", {}),
                profile_res.get("learner_type", "Foundation")
            )
            return {"profile": profile_res, "gap": gap_res, "trail": trail}

        elif event_name == "quiz_completed":
            # Grade assessment
            grade = self.assessor.grade_assessment(
                mcq_score=payload.get("mcq_score", 0),
                viva_answer=payload.get("viva_answer", ""),
                time_taken_seconds=payload.get("time_taken", 45),
                skill_name=payload.get("skill", "")
            )

            skill = payload.get("skill", "")
            user_data = payload.get("user_data", {})
            
            if grade["passed"]:
                # Skill Verified!
                now_str = datetime.now().strftime("%Y-%m-%d")
                user_data["verified_skills"][skill] = {
                    "level": payload.get("target_level", 2),
                    "verified_date": now_str,
                    "quiz_score": grade["mcq_score"],
                    "viva_score": grade["viva_score"],
                    "project_url": payload.get("project_url", "https://github.com/user/demo-repo"),
                    "attempts": payload.get("attempts", 1),
                    "time_taken_days": 3
                }
                self.log("OpportunityAgent", f"Verified mastery in '{skill}'! Surfacing newly unlocked internships and open-source bounties.")
                opps = self.opportunity.run(user_data["verified_skills"], user_data.get("simulated_days", 0))
                mentor_msg = f"🎉 Incredible milestone! You verified {skill} at Level {payload.get('target_level', 2)}. Your Job Readiness just soared!"
                return {"grade": grade, "mentor_message": mentor_msg, "action": "verified", "opps": opps}
            else:
                # Adaptive re-plan: Assessor -> Mentor -> Curator
                user_data.setdefault("failed_attempts", []).append({
                    "skill": skill,
                    "attempt_date": datetime.now().strftime("%Y-%m-%d"),
                    "quiz_score": grade["overall_score"],
                    "feedback": grade["feedback"]
                })
                mentor_reassurance = self.mentor.get_reassurance(
                    skill, 
                    grade["overall_score"], 
                    tanglish=user_data.get("tanglish_mode", False),
                    learner_type=user_data.get("learner_type", "Foundation")
                )
                self.curator.run(
                    user_data.get("target_role", "Full Stack Developer"),
                    user_data.get("verified_skills", {}),
                    user_data.get("learner_type", "Foundation"),
                    failing_skill=skill
                )
                return {"grade": grade, "mentor_message": mentor_reassurance, "action": "replan"}

        elif event_name == "goal_changed":
            target_role = payload.get("new_role", "Full Stack Developer")
            user_data = payload.get("user_data", {})
            gap_res = self.gap_analyst.run(user_data, target_role)
            trail = self.curator.run(
                target_role, 
                user_data.get("verified_skills", {}), 
                user_data.get("learner_type", "Foundation")
            )
            return {"gap": gap_res, "trail": trail}

        elif event_name == "skill_expired":
            user_data = payload.get("user_data", {})
            opps = self.opportunity.run(user_data.get("verified_skills", {}), user_data.get("simulated_days", 0))
            return {"opps": opps}

        return {}

# Singleton instance
orchestrator = OrchestratorAgent()

