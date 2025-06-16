# 💉 Anesthesia Log Simulator

A Python console application that calculates recommended anesthesia dosages based on patient data. Built with a focus on input validation, modular logic, and file handling. This project reflects my transition from a clinical anesthesiologist to a backend-focused software developer.

---

## ⚙️ Features
- Collects patient data via CLI (name, age, weight)
- User chooses anesthesia type: Combined IV + Inhalational or Regional (Spinal/Epidural)
- Calculates drug dosages based on type and weight
- Recommends appropriate anesthesia protocol with clinical notes
- Logs session data to a .csv file with timestamp
- OOP-based design (inheritance, polymorphism, separation of concerns)
- Input validation with edge-case handling
- Fully unit tested (validation, calculations, logging)

---

## 🧭 Planned Enhancements
- Integrate ASA physical status classification to adjust recommended drug dosages based on patient comorbidity level.
- Implement logic to dynamically modify protocols according to ASA class (e.g. ASA III–IV → reduce induction agents).
- Add optional CLI prompts for ASA input and condition-based warnings in the output.

## 🧰 Technologies Used

- Python 3.12+
- Standard Library only (`datetime`, `unittest`, etc.)
- No external dependencies

---

## 📁 File Structure
📁 anesthesia_log_simulator/
├── main.py              # CLI interface and main app logic
├── patient.py           # Patient data class
├── storage.py           # Data logging to file
├── anesthesia_types.py  # Protocol recommendation
├── utils.py             # Input validators
├── test_utils.py        # Unit tests
└── README.md            # You’re reading it

---

## ▶️ How to Run

1. Make sure you have Python 3 installed.
2. Clone the repository:
- ```bash
git clone https://github.com/katebabakova444/anesthesia_log_simulator.git
cd anesthesia_log_simulator

---
## Example output
Enter patient age: 45  
Enter patient weight (kg): 80  
Select anesthesia type:
1. Regional Anesthesia
2. Combined IV+Inhalational Anesthesia
- Enter number: 2

Recommended protocol:
Anesthesia Protocol: Combined IV + Inhalitional

**Induction**:
- **Propofol** 136 mg IV
- **Fentanyl** 102 mcg IV
- **Sevoflurane** 2-3% inspiring concentration

**Maintenance**:
- Monitor: SpO2, EtCO2, BP, HR
- **Note**: Dosages may require adjustment based on comorbidities and clinical status.

---

**Doses**:
- Propofol: 136 mg
- Fentanyl: 102 mcg
- Sevoflurane: 2-3% inspiring concentration

Logged to anesthesia_log.csv


---

## 🧪 Testing

To run unit tests:
python -m unittest test_utils.py

---

## 👤 Author

Kateryna Babakova
Self-taught Python Developer | Background in Anesthesiology
GitHub (https://github.com/katebabakova444)

---

## 📌 Notes

This app was created as a way to combine my medical background with new technical skills in backend development.
All logic is handled using Python classes and functions. Data is stored in human-readable format in a .txt file for easy access and auditing.