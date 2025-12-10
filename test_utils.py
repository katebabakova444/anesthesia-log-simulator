import unittest
from utils import validate_age, validate_weight
from storage import save_to_db
from anesthesia_types import CombinedAnesthesia, RegionalAnesthesia
import os
import csv
import sqlite3
import json

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
        db_filename = "test_anesthesia_log.db"
        if os.path.exists(db_filename):
            os.remove(db_filename)
        name = "Test"
        age = 34
        weight = 70
        asa_class = "II"
        anesthesia_type = "test_type"
        block_type = "test"
        protocol = "test"
        doses = "120 mg"

        save_to_db(
            name=name,
            age=age,
            weight=weight,
            asa_class=asa_class,
            anesthesia_type=anesthesia_type,
            block_type=block_type,
            protocol=protocol,
            doses=doses,
            filename=db_filename
        )

        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(row)
        self.assertEqual(row[1], name)
        self.assertEqual(row[2], age)
        self.assertEqual(float(row[3]), weight)
        self.assertEqual(row[4], asa_class)
        self.assertEqual(row[5], anesthesia_type)
        self.assertEqual(row[6], block_type)
        self.assertEqual(row[7], protocol)
        self.assertEqual(row[8], json.dumps(doses))

