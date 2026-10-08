"""
Clinical presets and schemas for decision engine evaluation and routing.
"""
from typing import Dict

def clinical_triage_questions() -> Dict:
    """Preset questions for routing clinical notes."""
    return {
        "clinical_triage": {
            "type": "choice",
            "instructions": "Which department should evaluate this patient?",
            "criteria": {
                "cardiology": "chest pain, heart issues, palpitations",
                "pulmonology": "chronic cough, breathing issues without cardiac symptoms",
                "neurology": "stroke symptoms, headaches, seizures",
                "general": "routine checkups, mild symptoms"
            }
        }
    }

def guardrail_questions() -> Dict:
    """Preset questions for identifying PHI or PII."""
    return {
        "contains_phi": {
            "type": "noul",
            "instructions": "Does the text contain Protected Health Information (PHI) such as patient names or dates of birth?"
        }
    }

def acuity_questions() -> Dict:
    """Preset questions for determining medical acuity."""
    return {
        "acuity": {
            "type": "score",
            "instructions": "What is the medical acuity of this patient?",
            "criteria": [
                "routine / non-urgent",
                "minor / requires attention within 24h",
                "urgent / requires prompt attention",
                "emergent / life-threatening"
            ]
        }
    }
