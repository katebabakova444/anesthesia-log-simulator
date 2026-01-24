from flask import Flask, request, jsonify
from anesthesia.anesthesia_service import AnesthesiaService
from anesthesia.repository import LogRepository
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "anesthesia.db")
repo = LogRepository(DB_PATH)
service = AnesthesiaService(repo)

@app.route("/")
def healthcheck():
    return jsonify({
        "service": "Anesthesia Log Simulator",
        "status": "running",
        "docs": "See README on GitHub for available endpoints"
    }), 200

@app.route('/anesthesia', methods=['POST'])
def generate_anesthesia():
    data = request.get_json() or {}
    result, status = service.process_request(data)
    return jsonify(result), status

@app.route("/logs", methods=["GET"])
def get_logs():
    logs = repo.load_all()
    return jsonify(logs), 200

@app.route("/logs/filter", methods=["GET"])
def get_filter_logs():
    filters = request.args.to_dict()
    logs = repo.filter(filters)
    return jsonify(logs), 200

@app.route("/logs/<int:log_id>", methods=["DELETE"])
def remove_log(log_id):
    deleted = repo.delete(log_id)
    if not deleted:
        return jsonify({"error": "Log not found"}), 404

    return jsonify({"message": f"Log with id {log_id} deleted"}), 200

if __name__== '__main__':
    app.run(debug=True)
