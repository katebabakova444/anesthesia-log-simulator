from flask import Flask, request, jsonify
from anesthesia.anesthesia_types import CombinedAnesthesia, RegionalAnesthesia
from anesthesia.storage import save_to_db, load_logs, load_filtered_logs, delete_logs, DB_NAME
from anesthesia.utils import validate_patient_data
import sqlite3

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

    anesthesia_type_name = data.get("anesthesia_type")
    block_type = data.get("block_type")

    if anesthesia_type_name not in ("combined", "regional"):
        return jsonify({"error": "Invalid anesthesia_type"}), 400

    if anesthesia_type_name == "regional" and not block_type:
        return jsonify({"error": "block_type is required for regional anesthesia"}), 400

    try:
        if anesthesia_type_name == "combined":
            anesthesia_type = CombinedAnesthesia(patient_data)
        else:
            anesthesia_type = RegionalAnesthesia(patient_data, block_type)

        protocol_text, doses = anesthesia_type.generate_protocol()

        save_to_db(
            name=patient_data["name"],
            age=patient_data["age"],
            weight=patient_data["weight"],
            asa_class=patient_data["asa_class"],
            anesthesia_type=anesthesia_type_name,
            block_type=block_type,
            protocol=protocol_text,
            doses=doses,
            DB_NAME=DB_NAME
        )
        return jsonify({
        "message": "Entry created",
        "protocol": protocol_text,
        "doses": doses
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except sqlite3.Error:
        return jsonify({"error": "Database error"}), 500

@app.route("/logs", methods=["GET"])
def get_logs():
    logs = load_logs()
    return jsonify(logs), 200

@app.route("/logs/filter", methods=["GET"])
def get_filter_logs():
    filters = request.args.to_dict()
    logs = load_filtered_logs(filters)
    return jsonify(logs), 200

@app.route("/logs/<int:log_id>", methods=["DELETE"])
def remove_log(log_id):
    deleted = delete_logs(log_id)
    if not deleted:
        return jsonify({"error": "Log not found"}), 404

    return jsonify({"message": f"Log with id {log_id} deleted"}), 200

if __name__== '__main__':
    app.run(debug=True)
