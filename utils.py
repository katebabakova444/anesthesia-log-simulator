import json

def validate_age(age):
    return 0 < age < 120
def validate_weight(weight):
    return 0 < weight < 300

def get_asa_multiplier(asa_class):
    asa_map = {
        "I": 1.0,
        "II": 0.9,
        "III": 0.8,
        "IV": 0.7,
        "V": 0.6
    }
    return asa_map.get(asa_class.upper(), 1.0)

def validate_patient_data(data):
    required_fields = ["name", "age", "weight", "asa_class"]
    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"
    name = data.get("name")
    age = data.get("age")
    weight = data.get("weight")
    asa_class = data.get("asa_class", "").upper()
    if not isinstance(name, str) or not name.strip():
        return False, "Invalid name"
    if not isinstance(age, int) or not (0 < age < 120):
        return False, "Invalid age: must be integer between 0 and 120"
    if not isinstance(weight, (int, float)) or weight <= 0:
        return False, "Invalid weight: must be integer or float number > 0."
    if asa_class not in ["I", "II", "III", "IV", "V"]:
        return False, "Invalid ASA class: must be I, II, III, IV or V."

    return True, {
        "name": name,
        "age": age,
        "weight": weight,
        "asa_class": asa_class
    }

def prepare_log_entry(patient_data, anesthesia_type, doses, block_type=None):
    from anesthesia_types import CombinedAnesthesia, RegionalAnesthesia
    if anesthesia_type not in ["combined", "regional"]:
        raise ValueError("Invalid anesthesia type")
    if anesthesia_type == "regional":

        try:
           dosage = float(dosage)
           if dosage < 0:
               raise ValueError
        except(TypeError, ValueError):
            raise ValueError("Invalid dosage value")

    if anesthesia_type == "combined":
        anesthesia = CombinedAnesthesia(patient_data)
    elif anesthesia_type == "regional":
        anesthesia = RegionalAnesthesia(patient_data, block_type)
    else:
        raise ValueError("Invalid anesthesia type")

    protocol, doses = anesthesia.generate_protocol()

    if anesthesia_type == "combined":
        filtered_doses = {k: doses[k] for k in ["propofol", "fentanyl", "sevoflurane"] if k in doses}

    elif anesthesia_type == "regional":
        filtered_doses = {k: doses[k] for k in ["drug", "dosage", "technique"] if k in doses}
    else:
         filtered_doses = {}
    row = {
        "name": patient_data["name"],
        "age": patient_data["age"],
        "weight": patient_data["weight"],
        "asa_class": patient_data["asa_class"],
        "anesthesia_type": anesthesia_type,
        **filtered_doses
    }
