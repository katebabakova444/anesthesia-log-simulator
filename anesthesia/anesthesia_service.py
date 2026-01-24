from anesthesia.domain.patient import Patient
from anesthesia.domain.validators import PatientValidator
from anesthesia.domain.anesthesia_types import CombinedAnesthesia, RegionalAnesthesia

class AnesthesiaService:
    def __init__(self, repository):
        self.repository = repository

    def process_request(self, data):
        valid, result = PatientValidator.validate(data)
        if not valid:
            return{"error": result}, 400
        patient = Patient.from_dict(result)
        anesthesia_type_name = data.get("anesthesia_type")
        block_type = data.get("block_type")

        if anesthesia_type_name not in ("combined", "regional"):
            return {"error": "Invalid anesthesia_type"}, 400

        if anesthesia_type_name == "regional" and not block_type:
            return {"error":"block_type is required for regional anesthesia"}, 422

        if anesthesia_type_name == "combined":
            anesthesia_type = CombinedAnesthesia(patient)
        else:
            anesthesia_type = RegionalAnesthesia(patient, block_type)

        try:
            protocol_text, doses = anesthesia_type.generate_protocol()
        except Exception:
            return {"error": "Internal anesthesia processing error"}, 500

        try:
            entry = {
                "name": patient.name,
                "age": patient.age,
                "weight": patient.weight,
                "asa_class": patient.asa_class,
                "anesthesia_type": anesthesia_type_name,
                "block_type": block_type,
                "protocol": protocol_text,
                "doses": doses,
            }
            self.repository.save(entry)

        except Exception:
            return {"error": "Internal database error"}, 500

        return {
            "message": "Entry created",
            "protocol": protocol_text,
            "doses": doses
        }, 200