import unittest
import json
from anesthesia.domain.anesthesia_types import CombinedAnesthesia, RegionalAnesthesia
from anesthesia.domain.asa import get_asa_multiplier
from anesthesia.repository import SQLAlchemyLogRepository
from anesthesia.domain.validators import PatientValidator
from anesthesia.domain.patient import Patient



class TestUtils(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            "name": "John",
            "age": 30,
            "weight": 70,
            "asa_class": "II",
            "anesthesia_type": "combined"
        }
    def test_missing_required_field(self):
        data = self.valid_data.copy()
        data.pop("age")

        is_valid, msg = PatientValidator.validate(data)

        self.assertFalse(is_valid)
        self.assertEqual(msg, "age is required")

    def test_invalid_age_negative(self):
        data = self.valid_data.copy()
        data["age"] = -1

        is_valid, msg = PatientValidator.validate(data)
        self.assertFalse(is_valid)
        self.assertEqual(msg, "age must be integer between 0 and 120")

    def test_invalid_age_too_high(self):
        data = self.valid_data.copy()
        data["age"] = 150

        is_valid, msg = PatientValidator.validate(data)
        self.assertFalse(is_valid)
        self.assertEqual(msg, "age must be integer between 0 and 120")

    def test_invalid_age_not_int(self):
        data = self.valid_data.copy()
        data["age"] = "abc"

        is_valid, msg = PatientValidator.validate(data)
        self.assertFalse(is_valid)

    def test_valid_age(self):
        is_valid, validated = PatientValidator.validate(self.valid_data)
        self.assertTrue(is_valid)
        self.assertEqual(validated["age"], 30)

    def test_invalid_weight_zero(self):
        data = self.valid_data.copy()
        data["weight"] = 0

        is_valid, msg = PatientValidator.validate(data)
        self.assertFalse(is_valid)
        self.assertEqual(msg, "weight must be a positive number up to 300")

    def test_invalid_weight_too_high(self):
        data = self.valid_data.copy()
        data["weight"] = 400

        is_valid, msg = PatientValidator.validate(data)
        self.assertFalse(is_valid)
        self.assertEqual(msg, "weight must be a positive number up to 300")

    def test_invalid_weight_type(self):
        data = self.valid_data.copy()
        data["weight"] = "abc"

        is_valid, msg = PatientValidator.validate(data)
        self.assertFalse(is_valid)

    def test_valid_weight_float_conversion(self):
        data = self.valid_data.copy()
        data["weight"] = 70.5

        is_valid, validated = PatientValidator.validate(data)
        self.assertTrue(is_valid)
        self.assertEqual(validated["weight"], float(70.5))

    def test_invalid_asa_class(self):
        data = self.valid_data.copy()
        data["asa_class"] = "X"

        is_valid, msg = PatientValidator.validate(data)

        self.assertFalse(is_valid)
        self.assertEqual(msg, "asa_class must be one of I, II, III, IV, V")

    def test_valid_asa_class(self):
        is_valid, validated = PatientValidator.validate(self.valid_data)
        self.assertTrue(is_valid)
        self.assertEqual(validated["asa_class"], "II")

    def test_validated_data_structure(self):
        is_valid, validated = PatientValidator.validate(self.valid_data)

        self.assertTrue(is_valid)
        self.assertEqual(validated["name"], "John")
        self.assertEqual(validated["age"], 30)
        self.assertEqual(validated["weight"], 70.0)  # converted to float
        self.assertEqual(validated["asa_class"], "II")


class TestCombinedAnesthesia(unittest.TestCase):
    def setUp(self):
        raw = {
            "name": "Test",
            "age": 35,
            "weight": 70,
            "asa_class": "II",
            "anesthesia_type": "combined",
        }
        ok, validated = PatientValidator.validate(raw)
        self.assertTrue(ok, msg=str(validated))

        self.patient = Patient(**validated)
        self.combined = CombinedAnesthesia(self.patient)

    def test_generate_combined_protocol_contains_expected_text(self):
        protocol_text, doses = self.combined.generate_protocol()
        self.assertIn("Propofol", protocol_text)
        self.assertIn("Fentanyl", protocol_text)
        self.assertIn("Sevoflurane", protocol_text)

    def test_combined_anesthesia_calculates_correct_doses(self):
        protocol, doses = self.combined.generate_protocol()
        expected_propofol = round(70 * 2* get_asa_multiplier("II"))
        expected_fentanyl = round(70 * 1.5 * get_asa_multiplier("II"))

        self.assertIn(f"{expected_propofol} mg", protocol)
        self.assertIn(f"{expected_fentanyl} mcg", protocol)

class TestRegionalAnesthesia(unittest.TestCase):
    def setUp(self):
        raw = {
            "name": "Test",
            "age": 40,
            "weight": 70,
            "asa_class": "II",
            "anesthesia_type": "regional",
            "block_type": "spinal",
        }
        ok, validated = PatientValidator.validate(raw)
        self.assertTrue(ok, msg=str(validated))
        self.patient = Patient(**validated)

    def test_generate_spinal_protocol_contains_expected_text(self):
        regional = RegionalAnesthesia(self.patient, block_type="spinal")
        protocol_text, doses = regional.generate_protocol()

        self.assertIn("Spinal", protocol_text)
        self.assertIn("Bupivacaine", protocol_text)

    def test_generate_epidural_protocol_contains_expected_text(self):
        regional = RegionalAnesthesia(self.patient, block_type="epidural")
        protocol_text, doses = regional.generate_protocol()
        self.assertIn("Epidural", protocol_text)
        self.assertIn("Bupivacaine", protocol_text)

class TestStorage(unittest.TestCase):
    def test_log_patient_data(self):
        repo = SQLAlchemyLogRepository()

        entry = {
           "name": "Test",
           "age": 34,
           "weight": 70,
           "asa_class": "II",
           "anesthesia_type": "test_type",
           "block_type": "test",
           "protocol": "test",
           "doses": {"dose": "120 mg"},
        }

        patient = repo.save_patient({
            "name": entry["name"],
            "age": entry["age"],
            "weight": entry["weight"],
        })
        log = repo.save_anesthesia_log(patient["id"], {
            "asa_class": entry["asa_class"],
            "anesthesia_type": entry["anesthesia_type"],
            "block_type": entry["block_type"],
            "protocol": entry["protocol"],
            "doses": entry["doses"],
        })
        found_patient = repo.get_patient(patient["id"])
        patient_logs = repo.get_patient_logs(patient["id"])



        self.assertIsNotNone(found_patient)
        self.assertEqual(found_patient["name"], entry["name"])
        self.assertEqual(found_patient["age"], entry["age"])
        self.assertEqual(float(found_patient["weight"]), entry["weight"])
        self.assertEqual(len(patient_logs), 1)
        saved_log = patient_logs[0]
        self.assertEqual(saved_log["patient_id"], patient["id"])
        self.assertEqual(saved_log["asa_class"], entry["asa_class"])
        self.assertEqual(saved_log["anesthesia_type"], entry["anesthesia_type"])
        self.assertEqual(saved_log["block_type"], entry["block_type"])
        self.assertEqual(saved_log["protocol"], entry["protocol"])
        self.assertEqual(saved_log["doses"], json.dumps(entry["doses"]))

