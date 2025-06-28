from flask import Flask, request, jsonify
from anesthesia_types import CombinedAnesthesia, RegionalAnesthesia
from storage import save_log

app = Flask(__name__)
@app.route('/anesthesia', methods=['POST'])
def generate_anesthesia():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    name = data.get("name")
    age = data.get("age")
    weight = data.get("weight", 70)
    asa_class = data.get("asa_class", "I")
    anesthesia_type = data.get("anesthesia_type")
    block_type = data.get("block_type", "spinal")
    dosage = data.get("dosage")
    patient_data = {
        "name": name,
        "age": age,
        "weight": weight,
        "asa_class": asa_class
    }
    if not name or not isinstance(name, str):
        return jsonify({"error": "Invalid or missing name"}), 400
    try:
        age = int(age)
        if age < 0 or age > 120:
            raise ValueError
    except:
        return jsonify({"error": "Invalid age"}), 400

    valid_asa = {"I", "II", "III", "IV", "V"}
    if asa_class not in valid_asa:
        return jsonify({"error": "ASA class must be one of: I, II, III, IV, V"}), 400
    if anesthesia_type not in ["combined", "regional"]:
        return jsonify({"error": "Invalid anesthesia type"}), 400
    if anesthesia_type == "regional":

        try:
           dosage = float(dosage)
           if dosage < 0:
               raise ValueError
        except(TypeError, ValueError):
            return jsonify({"error": "Invalid dosage value"}), 400
    return jsonify({"status": "OK", "data": data}), 200



    if anesthesia_type == "combined":
        anesthesia = CombinedAnesthesia(patient_data)
    elif anesthesia_type == "regional":
        anesthesia = RegionalAnesthesia(patient_data, block_type)
    else:
        return jsonify({"error": "Invalid anesthesia type"}), 400

    protocol, doses = anesthesia.generate_protocol()

    if anesthesia_type == "combined":
        filtered_doses = {k: doses[k] for k in ["propofol", "fentanyl", "sevoflurane"] if k in doses}

    elif anesthesia_type == "regional":
        filtered_doses = {k: doses[k] for k in ["drug", "dosage", "technique"] if k in doses}
    else:
         filtered_doses = {}


    row = {
        "name": name,
        "age": age,
        "weight": weight,
        "asa_class": asa_class,
        "anesthesia_type": anesthesia_type,
        **filtered_doses
    }
    save_log(**row)

    return jsonify({
        "protocol": protocol,
        "doses": filtered_doses,
        "asa_class": asa_class
    })

