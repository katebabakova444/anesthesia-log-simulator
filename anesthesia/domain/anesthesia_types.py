from anesthesia.domain.asa import get_asa_multiplier
from anesthesia.domain.patient import Patient
class AnesthesiaType:
    def __init__(self, patient: Patient):
        self.patient = patient

class CombinedAnesthesia(AnesthesiaType):
    def generate_protocol(self):
        weight = self.patient.weight
        asa_class = self.patient.asa_class
        multiplier = get_asa_multiplier(asa_class)

        propofol_dose = round(weight * 2 * multiplier)
        fentanyl_dose = round(weight * 1.5 * multiplier)
        sevoflurane_range = "2-3% inspiring concentration"

        protocol = (
            f"Anesthesia Protocol: Combined IV + Inhalitional\n\n"
            f"ASA Class: {asa_class}\n"
            f"Induction:\n"
            f"Propofol {propofol_dose} mg IV\n"
            f"Fentanyl {fentanyl_dose} mcg IV\n"
            f"Sevoflurane {sevoflurane_range}\n"
            f"Maintenance:\n"
            f"Monitor: SpO2, EtCO2, BP, HR\n"
            f"Note: Dosages may require adjustment based on comorbidities and clinical status.\n"
        )

        doses = {
            "propofol": f"{propofol_dose} mg",
            "fentanyl": f"{fentanyl_dose} mcg",
            "sevoflurane": sevoflurane_range
        }
        return protocol, doses

class RegionalAnesthesia(AnesthesiaType):
    def __init__(self, patient: Patient, block_type: str):
        super().__init__(patient)
        self.block_type = block_type.lower()

    def generate_protocol(self):
        weight = self.patient.weight
        asa_class = self.patient.asa_class
        multiplier = get_asa_multiplier(asa_class)

        if self.block_type == "spinal":
            dose = min(15, round(weight * 0.2 * multiplier))
            concentration = "0.5% hyperbaric"
            max_dose = 20
            note = "Single-shot spinal block. Monitor for hypotension."
            title = "Spinal"
        elif self.block_type == "epidural":
            dose = round(min(weight * 2.5 * multiplier, 175))
            concentration = "0.25% or 0.5%"
            max_dose = 175
            note = "Titrate incremantally. Monitor dermatomal spread."
            title = "Epidural"
        else:
            raise ValueError("Error: Invalid block type.")

        protocol = (
            f"Anesthesia Protocol: {title}\n"
            f"ASA Class: {asa_class}\n"
            f"Dose(Bupivacaine): {dose} mg\n"
            f"Concentration: {concentration}\n"
            f"Monitoring: BP, HR, sensory/motor level\n"
            f"Note: {note}\n"
            f"Max safe dose: {max_dose} mg"
        )
        doses = {
            "bupivacaine": f"{dose} mg",
            "concentration": concentration,
            "max_safe_dose": f"{max_dose} mg",
        }
        return protocol, doses