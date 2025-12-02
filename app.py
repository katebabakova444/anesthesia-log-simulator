from flask import Flask, request, jsonify
from anesthesia_types import CombinedAnesthesia, RegionalAnesthesia
from storage import save_to_db, load_logs, load_filtered_logs
from utils import validate_patient_data, prepare_log_entry
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

    if anesthesia_type_name == "combined":
        anesthesia_type = CombinedAnesthesia(patient_data)
    elif anesthesia_type_name == "regional":
        anesthesia_type = RegionalAnesthesia(patient_data, block_type=data.get("block_type"))
    else:
        return jsonify({"error": "Unknown anesthesia type"}), 400
    try:
        protocol_text, doses = anesthesia_type.generate_protocol()

        save_to_db(
            name=patient_data["name"],
            age=patient_data["age"],
            weight=patient_data["weight"],
            asa_class=patient_data["asa_class"],
            anesthesia_type=anesthesia_type_name,
            block_type=block_type,
            protocol=protocol_text,
            doses=doses
        )
        return jsonify({
            "message": "Entry created",
            "protocol": protocol_text,
            "doses": doses
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to generate protocol: {str(e)}"}), 400


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
def delete_log(log_id):
    conn = sqlite3.connect("anesthesia.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM logs WHERE id = ?", (log_id,))
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    if deleted_rows == 0:
        return jsonify({"error": "Log not found"}), 404
    return jsonify({"message": f"Log with id {log_id} deleted"}), 200

if __name__== '__main__':
    app.run(debug=True)
