class PatientValidator:
    REQUIRED_FIELDS = ["name", "age", "weight", "asa_class", "anesthesia_type"]

    @staticmethod
    def validate(data: dict):
        for field in PatientValidator.REQUIRED_FIELDS:
            if field not in data:
                return False, f"{field} is required"

        age = data["age"]
        if not isinstance(age, int) or age < 0 or age > 120:
            return False, "age must be integer between 0 and 120"

        weight = data["weight"]
        if not isinstance(weight, (int, float)) or weight <= 0 or weight > 300:
            return False, "weight must be a positive number up to 300"

        asa = data["asa_class"]
        if asa not in ("I", "II", "III", "IV", "V"):
            return False, "asa_class must be one of I, II, III, IV, V"

        validated = {
            "name": data["name"],
            "age": age,
            "weight": float(weight),
            "asa_class": asa

        }
        return True, validated

