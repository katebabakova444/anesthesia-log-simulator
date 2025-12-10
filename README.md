#  Anesthesia Log Simulator — Backend Learning Project
A Python backend project where I combine my medical background with my journey into software engineering.
This project started as a simple CLI calculator and has grown into a fully structured backend service with validation, SQLite storage, API endpoints, and deployment.

My goal with this project is to learn by building — refactoring, improving architecture, and adding real backend features step by step.

---

##  What This Project Does
The Anesthesia Log Simulator allows you to:

- Calculate anesthesia drug dosages based on patient data
- Generate a formatted anesthesia protocol (combined or regional)
- Validate patient input (age, weight, fields)
- Store logs in a **SQLite database**
- Retrieve logs
- Filter logs
- Delete logs
- Use a REST API to interact with the system

It is a simple but realistic medical logging tool built for educational purposes.

---

##  Why I Built This Project
As someone transitioning from anesthesiology into backend engineering, I wanted a project that:

1. Uses logic I worked with every day
2. Helps me practice real backend patterns
3. Allows continuous refactoring and growth
4. Shows clear learning progression for apprenticeship programs

The first version was a small CLI tool.
Now it’s a structured backend service with an API, database, validation layer, and unit tests — and I continue improving it.

---

##  Tech Stack & Features

### **Backend**
- Python
- Flask
- SQLite3
- Custom validation logic
- Modular architecture (separated into utils, storage, types, routes)

### **Core Features**
- Patient creation
- Drug dose calculations
- Protocol generation (Combined / Regional)
- JSON serialization for dose dictionaries
- Date-based logging
- Structured storage in `anesthesia.db`

### **Database**
- Single `logs` table
- Auto-creation on write
- JSON storage for doses
- Text field storage for protocols
- Timestamping

### **API Endpoints**
- `GET /logs` — return all logs
- `GET /logs/filter` — filter by fields
- `POST /anesthesia` — create a new protocol + save to DB
- `DELETE /logs/<id>` — delete a record

### **Validation**
- Valid age range
- Valid weight range
- Required fields
- Prevents invalid data from entering the database

---

##  Unit Tests
I added unit tests to check:

- Age validation
- Weight validation
- Combined anesthesia protocol generation
- Regional anesthesia protocol generation
- Correct DB logging
- Correct values stored in each column

Testing helped me catch several issues, refactor SQL logic, and improve reliability.

---

##  Deployment
The API is deployed on Render:

**Live API:**
https://anesthesia-log-simulator.onrender.com


---

##  Project Structure
- app.py — Flask API routes  
- patient.py — patient logic  
- anesthesia_types.py — anesthesia classes + protocol generation
- storage.py — SQLite storage  
- utils.py — validation  
- test_utils.py — unit tests  

---
## Author
Created by Kateryna Babakova (https://github.com/katebabakova444) This project is part of my backend development journey.