"""
SkillSherpa Scoring Engine
Pure, unit-testable mathematical functions for computing:
1. Job Readiness Score (0-100 weighted)
2. Confidence vs Reality Calibration Score (0-100)
3. Skill Expiry Status (Green / Amber / Red)
"""

from datetime import datetime, timedelta
from typing import Dict, Any, Tuple

def compute_job_readiness(
    verified_skills: Dict[str, Dict[str, Any]], 
    role_skills: Dict[str, Dict[str, Any]],
    simulated_days_offset: int = 0
) -> int:
    """
    Computes a weighted Job Readiness Score (0 - 100).
    A verified skill contributes proportionately: min(1.0, verified_level / target_level) * weight.
    If a skill is expired (>90 days), its effective verified level drops to 0 until re-verified.
    
    Formula:
        (sum(earned_weight) / sum(total_weights)) * 100
    """
    if not role_skills:
        return 0
        
    total_weight = 0.0
    earned_weight = 0.0
    
    for skill_name, req in role_skills.items():
        weight = float(req.get("weight", 1.0))
        target_lvl = float(req.get("target_level", 3))
        total_weight += weight
        
        if skill_name in verified_skills:
            v_data = verified_skills[skill_name]
            v_level = float(v_data.get("level", 0))
            
            # Check expiry
            status, _, _ = get_skill_expiry_status(v_data.get("verified_date", ""), simulated_days_offset)
            if status == "expired":
                v_level = 0.0 # expired skills do not contribute to live job readiness
                
            fraction = min(1.0, v_level / target_lvl) if target_lvl > 0 else 0
            earned_weight += fraction * weight

    if total_weight <= 0:
        return 0
    return int(round((earned_weight / total_weight) * 100))

def compute_calibration_score(
    self_ratings: Dict[str, int], 
    verified_skills: Dict[str, Dict[str, Any]]
) -> Tuple[int, float, int]:
    """
    Computes the Confidence vs Reality Calibration Score.
    
    Formula:
        Calibration = max(0, min(100, int(100 - (avg_abs_gap * 20))))
        where avg_abs_gap = mean(|self_rating - verified_level|) across verified skills.
    
    Returns:
        (calibration_score (0-100), avg_abs_gap, verified_count)
    """
    evaluated_gaps = []
    
    for skill, v_data in verified_skills.items():
        if skill in self_ratings:
            self_val = float(self_ratings[skill])
            v_val = float(v_data.get("level", 0))
            evaluated_gaps.append(abs(self_val - v_val))
            
    if not evaluated_gaps:
        return 100, 0.0, 0 # Default neutral high when nothing verified yet
        
    avg_gap = sum(evaluated_gaps) / len(evaluated_gaps)
    calibration = int(round(max(0.0, min(100.0, 100.0 - (avg_gap * 20.0)))))
    return calibration, round(avg_gap, 2), len(evaluated_gaps)

def get_skill_expiry_status(
    verified_date_str: str, 
    simulated_days_offset: int = 0,
    validity_days: int = 90
) -> Tuple[str, str, int]:
    """
    Calculates whether a verified skill is active, nearing expiry, or expired.
    
    Status logic:
    - Days remaining <= 0: 'expired' (Red, 🔴)
    - Days remaining <= 15: 'warning' (Amber, 🟡)
    - Days remaining > 15: 'valid' (Green, 🟢)
    
    Returns:
        (status_code: 'valid'|'warning'|'expired', badge_color: 'green'|'amber'|'red', days_remaining: int)
    """
    if not verified_date_str:
        return "expired", "red", 0
        
    try:
        v_date = datetime.strptime(verified_date_str, "%Y-%m-%d")
    except ValueError:
        return "expired", "red", 0
        
    # Baseline comparison date = today plus any simulation offset
    current_virtual_date = datetime.now() + timedelta(days=simulated_days_offset)
    elapsed_days = (current_virtual_date - v_date).days
    days_remaining = validity_days - elapsed_days
    
    if days_remaining <= 0:
        return "expired", "red", days_remaining
    elif days_remaining <= 15:
        return "warning", "amber", days_remaining
    else:
        return "valid", "green", days_remaining

def compute_gap_severity(target_level: int, verified_level: int) -> Tuple[str, str]:
    """
    Returns gap severity label and color indicator:
    - target - verified == 0: 'Mastered' (🟢)
    - target - verified == 1: 'Moderate Gap' (🟡)
    - target - verified >= 2: 'Critical Gap' (🔴)
    """
    diff = max(0, target_level - verified_level)
    if diff == 0:
        return "Mastered", "#10B981"
    elif diff == 1:
        return "Moderate Gap", "#F59E0B"
    else:
        return "Critical Gap", "#EF4444"

