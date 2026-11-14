"""
SkillSherpa Unit & Integration Tests
Validates scoring functions, data files, multi-agent event dispatch, and persona loading.
"""

import unittest
from datetime import datetime, timedelta
import scoring
import data_loader
from agents import orchestrator

class TestSkillSherpa(unittest.TestCase):

    def test_scoring_job_readiness(self):
        role_skills = {
            "HTML/CSS": {"weight": 1.0, "target_level": 2},
            "JavaScript": {"weight": 2.0, "target_level": 4}
        }
        # Nothing verified
        self.assertEqual(scoring.compute_job_readiness({}, role_skills), 0)

        # Partially verified
        verified = {
            "HTML/CSS": {"level": 2, "verified_date": datetime.now().strftime("%Y-%m-%d")}
        }
        # HTML/CSS: (2/2) * 1.0 = 1.0; total = 3.0; (1.0/3.0)*100 = 33%
        score = scoring.compute_job_readiness(verified, role_skills)
        self.assertEqual(score, 33)

        # Fully verified
        verified["JavaScript"] = {"level": 4, "verified_date": datetime.now().strftime("%Y-%m-%d")}
        score = scoring.compute_job_readiness(verified, role_skills)
        self.assertEqual(score, 100)

    def test_calibration_score(self):
        self_ratings = {"HTML/CSS": 3, "JavaScript": 2}
        verified = {
            "HTML/CSS": {"level": 3, "verified_date": "2026-10-15"},
            "JavaScript": {"level": 2, "verified_date": "2026-10-15"}
        }
        # Gaps: 0 and 0 -> calibration = 100
        calib, gap, count = scoring.compute_calibration_score(self_ratings, verified)
        self.assertEqual(calib, 100)
        self.assertEqual(gap, 0.0)
        self.assertEqual(count, 2)

        # Overconfident
        self_ratings_over = {"HTML/CSS": 5}
        verified_over = {"HTML/CSS": {"level": 1}}
        # Gap = 4 -> 100 - (4 * 20) = 20
        calib_over, gap_over, _ = scoring.compute_calibration_score(self_ratings_over, verified_over)
        self.assertEqual(calib_over, 20)

    def test_skill_expiry(self):
        today = datetime.now()
        fresh_date = (today - timedelta(days=10)).strftime("%Y-%m-%d")
        status, color, rem = scoring.get_skill_expiry_status(fresh_date, simulated_days_offset=0)
        self.assertEqual(status, "valid")
        self.assertEqual(color, "green")

        # Simulated 100 days later -> elapsed = 110 days -> expired!
        status_sim, color_sim, _ = scoring.get_skill_expiry_status(fresh_date, simulated_days_offset=100)
        self.assertEqual(status_sim, "expired")
        self.assertEqual(color_sim, "red")

    def test_agents_event_orchestration(self):
        # 1. Onboarding Event
        payload_onboard = {
            "name": "Arun Test",
            "board": "State Board",
            "branch": "IT",
            "current_comfort": "Beginner HTML",
            "stress_level": "High Anxiety",
            "weekly_hours": 10,
            "target_role": "Full Stack Developer",
            "verified_skills": {}
        }
        res_onboard = orchestrator.handle_event("onboarding_done", payload_onboard)
        self.assertIn("profile", res_onboard)
        self.assertEqual(res_onboard["profile"]["learner_type"], "Foundation")
        self.assertIn("trail", res_onboard)

        # 2. Quiz Failed Event (<50%)
        test_user = {
            "name": "Arun Test",
            "learner_type": "Foundation",
            "target_role": "Full Stack Developer",
            "verified_skills": {},
            "failed_attempts": [],
            "tanglish_mode": True
        }
        res_fail = orchestrator.handle_event("quiz_completed", {
            "skill": "JavaScript",
            "target_level": 3,
            "mcq_score": 40,
            "viva_answer": "I don't know much yet.",
            "time_taken": 35,
            "user_data": test_user
        })
        self.assertEqual(res_fail["action"], "replan")
        self.assertFalse(res_fail["grade"]["passed"])
        self.assertEqual(len(test_user["failed_attempts"]), 1)

        # 3. Quiz Passed Event (>=70%)
        res_pass = orchestrator.handle_event("quiz_completed", {
            "skill": "HTML/CSS",
            "target_level": 2,
            "mcq_score": 90,
            "viva_answer": "I built a responsive mountain portal handling mobile viewports and accessible semantic tags.",
            "time_taken": 50,
            "project_url": "https://github.com/arun/portal",
            "user_data": test_user
        })
        self.assertEqual(res_pass["action"], "verified")
        self.assertTrue(res_pass["grade"]["passed"])
        self.assertIn("HTML/CSS", test_user["verified_skills"])

    def test_personas_and_data(self):
        roles = data_loader.get_roles()
        self.assertIn("Full Stack Developer", roles)
        self.assertIn("Bioinformatics Analyst", roles)

        personas = data_loader.get_personas()
        self.assertIn("arun", personas)
        self.assertIn("meena", personas)
        self.assertIn("karthik", personas)

        opps = data_loader.get_opportunities()
        self.assertGreaterEqual(len(opps), 25)

        jargon = data_loader.get_jargon()
        self.assertIn("hackathon", jargon)
        self.assertIn("tanglish", jargon["hackathon"])

        cohort = data_loader.get_cohort()
        self.assertEqual(len(cohort), 60)

if __name__ == "__main__":
    unittest.main()

