# Anesthesia Log Simulator

A Python console + API application that calculates recommended anesthesia dosages based on patient data. Built with a focus on input validation, modular logic, and file handling. This project reflects my transition from a clinical anesthesiologist to a backend-focused software developer.

---

## Features

- Collects patient data via CLI (name, age, weight, ASA class)
- User chooses anesthesia type: Combined IV + Inhalational or Regional (Spinal/Epidural)
- Calculates drug dosages based on type and weight
- Adjusts dosages dynamically based on ASA class
- Recommends appropriate anesthesia protocol with clinical notes
- Logs session data to a `.csv` file with timestamp
- REST API endpoint for JSON input/output using Flask
- OOP-based design (inheritance, polymorphism, separation of concerns)
- Input validation with edge-case handling
- Fully unit tested (validation, calculations, logging)

---

## Planned Enhancements

Planned Improvements
- Add dosage warnings for pediatric and geriatric edge cases
- Add HTML form interface for direct web input
- Host public version on Render or Railway
- Add SQL backend for persistent case storage

---

## Technologies Used

- Python 3.12+
- Standard Library only (`datetime`, `csv`, `unittest`, etc.)
- Flask (for REST API)

---


##  File Structure
📁 anesthesia_log_simulator/
├── main.py              # CLI interface and main app logic
├── app.py               # Flask API endpoint
├── patient.py           # Patient data class
├── storage.py           # Data logging to file
├── anesthesia_types.py  # Protocol recommendation
├── utils.py             # Input validators and ASA logic
├── test_utils.py        # Unit tests
├── requirements.txt
└── README.md            

---

##  How to Run (CLI)

1. Make sure you have Python 3 installed.
2. Clone the repository:
```bash
git clone https://github.com/katebabakova444/anesthesia_log_simulator.git
cd anesthesia_log_simulator
```
---
## Example output
Enter patient name: John Doe
Enter patient age: 45  
Enter patient weight (kg): 80  
Enter ASA class (I-V): [default: I]: II

Select anesthesia type:
1. Regional Anesthesia
2. Combined IV+Inhalational Anesthesia
- Enter number: 2

Recommended protocol:
Anesthesia Protocol: Combined IV + Inhalitional

ASA Class: II

**Induction**:
- **Propofol** 160 mg IV
- **Fentanyl** 120 mcg IV
- **Sevoflurane** 2-3% inspiring concentration

**Maintenance**:
- Monitor: SpO2, EtCO2, BP, HR
- **Note**: Dosages may require adjustment based on comorbidities and clinical status.

---

**Doses**:
- Propofol: 160 mg
- Fentanyl: 120 mcg
- Sevoflurane: 2-3% inspiring concentration

Logged to anesthesia_log.csv


---

## How to Run(API)
1. Install Flask
``` bash
pip install flask
```
2. Run the app
``` bash
python app.py
```
3. The API will be available at:
http://127.0.0.1:5000/anesthesia

POST /anesthesia

JSON Input Example:


```json
{
  "name": "Kateryna Babakova",
  "age": 30,
  "weight": 60,
  "asa_class": "II",
  "anesthesia_type": "combined"
}
```

JSON Response:

```json
{
  "asa_class": "II",
  "doses": {
    "fentanyl": "81 mcg",
    "propofol": "108 mg",
    "sevoflurane": "2-3% inspiring concentration"
  },
  "protocol": "Anesthesia Protocol: Combined IV + Inhalitional\n\nASA Class: II\nInduction: Propofol 108 mg IV, Fentanyl 81 mcg IV, Sevoflurane 2-3% inspiring concentration\nMaintenance: Monitor SpO2, EtCO2, BP, HR\nNote: Dosages may require adjustment based on comorbidities and clinical status."
}
```


##  Testing

To run unit tests:
python -m unittest test_utils.py

---

##  Author

Kateryna Babakova
Self-taught Python Developer | Background in Anesthesiology
GitHub (https://github.com/katebabakova444)

---

##  Notes

This app was created as a way to combine my medical background with new technical skills in backend development.
All logic is handled using Python classes and functions. Data is stored in human-readable format in a .csv file for easy access and auditing.
It was designed to showcase problem-solving, code structure, and the ability to evolve an idea from a CLI to a scalable API.