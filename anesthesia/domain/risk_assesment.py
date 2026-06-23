from anesthesia.domain.patient import Patient

class RiskAssessment:
    @staticmethod
    def generate(patient, anesthesia_type, block_type=None):
        warnings = []
        recommendations = []
        risk_score = 0

        if patient.asa_class in ("IV", "V"):
            risk_score += 3
            warnings.append("High ASA class indicates elevated perioperative risk.")
            recommendations.append("Recommend senior anesthesia review and enhanced monitoring plan.")
        elif patient.asa_class == "III":
            risk_score += 2
            warnings.append("ASA III indicates significant systemic disease.")
            recommendations.append("Review comorbidities and prepare escalation plan before anesthesia.")

        if patient.age >= 75:
            risk_score += 2
            warnings.append("Advanced age may increase anesthesia-related complications.")
            recommendations.append("Consider age-adjusted dosing and closer postoperative monitoring.")
        elif patient.age >= 65:
            risk_score += 1
            warnings.append("Older age may require more conservative dosing.")
            recommendations.append("Use cautious titration and monitor hemodynamic response.")

        if patient.weight < 40:
            risk_score += 1
            warnings.append("Low body weight may increase sensitivity to anesthetic medications.")
            recommendations.append("Verify weight-based dose calculations carefully.")
        elif patient.weight > 120:
            risk_score += 1
            warnings.append("High body weight may complicate airway, dosing, and positioning.")
            recommendations.append("Confirm airway plan, positioning, and dose strategy.")

        if anesthesia_type == "combined" and patient.asa_class in ("III", "IV", "V"):
            risk_score += 1
            warnings.append("Combined anesthesia in higher-risk patients requires careful monitoring.")
            recommendations.append("Document monitoring plan and recovery criteria clearly.")

        if not warnings:
            warnings.append("No major rule-based risk flags detected from provided inputs.")
            recommendations.append("Proceed with standard pre-anesthesia safety checklist.")

        if risk_score >= 5:
            risk_level = "high"
        elif risk_score >= 2:
            risk_level = "moderate"
        else:
            risk_level = "low"

        return {
            "risk_level": risk_level,
            "risk_score": risk_score,
            "warnings": warnings,
            "recommendations": recommendations,
            "disclaimer": "Educational rule-based summary only; not medical advice or clinical decision support."
        }

patient = Patient("Test Patient", 76, 85, "III")
print(RiskAssessment.generate(patient, "combined"))