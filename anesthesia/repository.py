import json
from anesthesia.models import Session, AnesthesiaLog, Patient
from typing import List, Dict

class SQLAlchemyLogRepository:

    def save_patient(self, entry: Dict):
        session = Session()
        try:
            patient = Patient(
                name=entry["name"],
                age=entry["age"],
                weight=entry["weight"]
            )
            session.add(patient)
            session.commit()
            return patient.to_dict()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def save_anesthesia_log(self, patient_id: int, entry: Dict):
        session = Session()
        try:
            log = AnesthesiaLog(
                patient_id=patient_id,
                asa_class=entry["asa_class"],
                anesthesia_type=entry["anesthesia_type"],
                block_type=entry.get("block_type"),
                protocol=entry.get("protocol"),
                doses=json.dumps(entry.get("doses", {}))
            )
            session.add(log)
            session.commit()
            return log.to_dict()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_patient(self, patient_id: int):
        session = Session()
        try:
            patient = session.query(Patient).filter_by(id=patient_id).first()

            if not patient:
                return None
            return patient.to_dict()
        finally:
            session.close()

    def get_patient_logs(self, patient_id: int):
        session = Session()
        try:
            logs = session.query(AnesthesiaLog).filter_by(patient_id=patient_id).all()
            return [log.to_dict() for log in logs]
        finally:
            session.close()

    def load_all(self):
        session = Session()
        try:
            logs = session.query(AnesthesiaLog).all()
            return [log.to_dict() for log in logs]
        finally:
            session.close()
    def filter(self, filters: Dict):
        session = Session()
        try:
            query = session.query(AnesthesiaLog)
            allowed_fields = {
                "asa_class": AnesthesiaLog.asa_class,
                "anesthesia_type": AnesthesiaLog.anesthesia_type,
                "block_type": AnesthesiaLog.block_type,
                "patient_id": AnesthesiaLog.patient_id,
            }
            for key, value in filters.items():
                if key in allowed_fields:
                    query = query.filter(allowed_fields[key] == value)
            logs = query.all()
            return [log.to_dict() for log in logs]
        finally:
            session.close()
    def delete(self, log_id: int):
        session = Session()
        try:
            log = session.query(AnesthesiaLog).filter_by(id=log_id).first()
            if not log:
                return False
            session.delete(log)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

