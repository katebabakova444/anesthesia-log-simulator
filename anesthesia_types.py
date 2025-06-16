from abc import ABC, abstractmethod
class AnesthesiaType(ABC):
    def __init__(self, patient_data):
        self.patient_data = patient_data

    @abstractmethod
    def generate_protocol(self):
        pass

class CombinedAnesthesia(AnesthesiaType):
    def generate_protocol(self):
        weight = self.patient_data.get('weight', 70)  # default if not entered
        propofol_dose = round(weight * 2)
        fentanyl_dose = round(weight * 1.5)
        sevoflurane_range = "2-3% inspiring concentration"

        protocol = (
            f"Anesthesia Protocol: Combined IV + Inhalitional\n\n"
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
    def __init__(self, patient_data, block_type='epidural'):
        super().__init__(patient_data)
        self.block_type = block_type.lower()

    def generate_protocol(self):
        weight = self.patient_data.get('weight', 70)
        if self.block_type == "spinal":
            dose = min(15, round(weight * 0.2))
            concentration = "0.5% hyperbaric"
            max_dose = 20
            note = "Single-shot spinal block. Monitor for hypotension."
        elif self.block_type == "epidural":
            dose = round(min(weight * 2.5, 175))
            concentration = "0.25% or 0.5%"
            max_dose = 175
            note = "Titrate incremantally. Monitor dermatomal spread."
        else:
            return f"Error: Invalid block type."
        technique = "Single-shot spinal block" if self.block_type == "spinal" else "Incremental epidural"
        protocol = (
            f"Anesthesia Protocol: {self.block_type.capitalize()}\n"
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
            "technique": technique
        }
        return protocol, doses