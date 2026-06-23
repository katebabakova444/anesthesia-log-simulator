from anesthesia.domain.patient import Patient
from anesthesia.domain.risk_assesment import RiskAssessment


def test_low_risk_patient():
    patient = Patient(
        name="Test",
        age=30,
        weight=70,
        asa_class="I"
    )
    result = RiskAssessment.generate(patient, anesthesia_type="combined")

    assert result["risk_level"] == "low"
    assert result["risk_score"] == 0

def test_high_asa_patient():
    patient = Patient(
        name="Test",
        age=60,
        weight=80,
        asa_class="IV"
    )
    result = RiskAssessment.generate(patient, anesthesia_type="combined")

    assert result["risk_level"] in ["moderate", "high"]
    assert any("ASA" in warning for warning in result["warnings"])

def test_elderly_patient_risk():
    patient = Patient(
        name="Test",
        age=78,
        weight=65,
        asa_class="II"
    )

    result = RiskAssessment.generate(patient, anesthesia_type="combined")
    assert result["risk_score"] >= 2
    assert any("age" in warning.lower() for warning in result["warnings"])