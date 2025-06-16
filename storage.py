import csv
import os
import datetime


filename = "anesthesia_log.csv"
FIELDNAMES = ["timestamp", "name", "age", "weight", "anesthesia_type", "drug", "dosage", "maintenance", "technique"]

def save_log(filename="anesthesia_log.csv", **kwargs):
    is_new = not os.path.exists(filename)
    with open(filename, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if is_new:
            writer.writeheader()
        row = {"timestamp": datetime.datetime.now().isoformat()}
        for field in FIELDNAMES:
            if field != "timestamp":
                row[field] = kwargs.get(field, "")
        writer.writerow(row)