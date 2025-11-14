from flask import Flask, request, jsonify
from anesthesia_types import CombinedAnesthesia, RegionalAnesthesia
from storage import save_to_db, load_logs, load_filtered_logs
from utils import validate_patient_data, prepare_log_entry

app = Flask(__name__)
@app.route('/anesthesia', methods=['POST'])
def generate_anesthesia():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    valid, result = validate_patient_data(data)
    if not valid:
        return jsonify({"error": result}), 400
    patient_data = result

    anesthesia_type = data.get("anesthesia_type")
    block_type = data.get("block_type", "spinal")
    dosage = data.get("dosage")
    try:
        row = prepare_log_entry(patient_data, anesthesia_type, dosage, block_type)
        return jsonify({"message": "Entry created"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/logs", methods=["GET"])
def get_logs():
    logs = load_logs()
    return jsonify(logs), 200

@app.route("/logs/filter", methods=["GET"])
def get_filter_logs():
    filters = request.args.to_dict()
    logs = load_filtered_logs(filters)
    return jsonify(logs), 200

if __name__== '__main__':
    app.run(debug=True)
