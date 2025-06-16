import unittest
from utils import validate_age, validate_weight
from storage import save_log
from anesthesia_types import CombinedAnesthesia, RegionalAnesthesia
import os
import csv

class TestUtils(unittest.TestCase):
    def test_validate_age_valid(self):
        self.assertTrue(validate_age(38))

    def test_validate_age_invalid(self):
        self.assertFalse(validate_age(-1))
        self.assertFalse(validate_age(120))

    def test_validate_weight_valid(self):
        self.assertTrue(validate_weight(78))

    def test_validate_weight_invalid(self):
        self.assertFalse(validate_weight(0))
        self.assertFalse(validate_weight(300))

class TestCombinedAnesthesia(unittest.TestCase):
    def setUp(self):
        self.data = {"name": "Test", "age": 35, "weight": 70}
        self.combined = CombinedAnesthesia(self.data)

    def test_generate_combined_protocol_contains_expected_text(self):
        protocol_text, _ = self.combined.generate_protocol()
        self.assertIn("Propofol", protocol_text)
        self.assertIn("Fentanyl", protocol_text)
        self.assertIn("Sevoflurane", protocol_text)

    def test_combined_anesthesia_propofol_dose(self):
        _, doses = self.combined.generate_protocol()
        self.assertEqual(doses["propofol"], "140 mg")

class TestRegionalAnesthesia(unittest.TestCase):
    def setUp(self):
        self.data = {"name": "Test", "age": 40, "weight": 70}
        self.regional_spinal = RegionalAnesthesia(self.data, block_type="spinal")
        self.regional_epidural = RegionalAnesthesia(self.data, block_type="epidural")

    def test_generate_spinal_protocol_contains_expected_text(self):
        protocol_text, _ = self.regional_spinal.generate_protocol()
        self.assertIn("Spinal", protocol_text)
        self.assertIn("Bupivacaine", protocol_text)

    def test_generate_epidural_protocol_contains_expected_text(self):
        protocol_text, _ = self.regional_epidural.generate_protocol()
        self.assertIn("Epidural", protocol_text)
        self.assertIn("Bupivacaine", protocol_text)

class TestStorage(unittest.TestCase):
    def test_log_patient_data(self):
        test_filename = "test_anesthesia_log.csv"
        name = "Test"
        age = 34
        weight = 70
        dosage = "120 mg"
        protocol = "Test Protocol"
        drug = "TestDrug"
        anesthesia_type = "test_type"
        save_log(
            name=name,
            age=age,
            weight=weight,
            anesthesia_type=anesthesia_type,
            drug=drug,
            dosage=dosage,
            protocol=protocol,
            filename=test_filename,
        )

        with open(test_filename, newline="") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            self.assertGreater(len(rows), 0)
            last_entry = rows[-1]
            self.assertEqual(last_entry["name"], name)
            self.assertEqual(int(last_entry["age"]), age)
            self.assertEqual(float(last_entry["weight"]), weight)
            self.assertEqual(last_entry["anesthesia_type"], anesthesia_type)
            self.assertEqual(last_entry["drug"], drug)
            self.assertEqual(last_entry["dosage"], dosage)

        os.remove(test_filename)

