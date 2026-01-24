def get_asa_multiplier(asa_class):
    asa_map = {
        "I": 1.0,
        "II": 0.9,
        "III": 0.8,
        "IV": 0.7,
        "V": 0.6
    }
    return asa_map.get(asa_class.upper(), 1.0)