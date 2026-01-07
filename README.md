# Anesthesia Log Simulator  
**Backend Engineering Project (Python / Flask / SQLite)**

Anesthesia Log Simulator is a backend-focused Python project that combines my medical background in anesthesiology with my transition into software engineering.

The project started as a simple CLI dosage calculator and evolved into a structured backend application with a REST API, persistent storage, and automated tests.  
Its primary goal is to demonstrate how I learn backend engineering by building, refactoring, testing, and improving real-world logic step by step.

---

## Project Goals

- Apply backend engineering principles to a real, domain-specific problem
- Practice clean architecture and separation of concerns
- Build a REST API with validation and persistence
- Design and test backend logic using unit and integration tests
- Show measurable growth between project iterations

---

## What This Project Does

The Anesthesia Log Simulator allows you to:

- Calculate anesthesia drug dosages based on patient data
- Generate structured anesthesia protocols:
  - Regional (epidural/spinal)
  - Combined anesthesia
- Validate clinical input (age, weight, ASA class)
- Demonstrates stateful backend behavior with persistent storage
- Retrieve saved anesthesia logs via API
- Handle API errors and invalid input

---

##  Why I Built This Project
As someone transitioning from anesthesiology into backend engineering, I wanted a project that:

1. Uses logic I worked with every day
2. Helps me practice real backend patterns
3. Allows continuous refactoring and growth
4. Shows clear learning progression for apprenticeship programs

The first version was a small CLI tool.
Now it’s a structured backend service with an API, database, validation layer, and test coverage — and I continue improving it.

---

## Architecture Overview
``` text
anesthesia_log_simulator/
├── anesthesia/
│    ├── app.py                # Flask application entry point (API routes)
│    ├── patient.py            # Patient domain model
│    ├── anesthesia_types.py   # Anesthesia protocol definitions and dosage rules
│    ├── storage.py            # Persistence layer
│    └── utils.py              # Shared helper functions and validation     
│ 
│
├── tests/
│   ├── conftest.py           # Pytest shared fixtures
│   ├── test_api.py           # API endpoint tests
│   ├── test_api_logs.py      # Logging and persistence tests
│   ├── test_api_errors.py    # Error handling & validation tests
│   └── test_utils.py         # Unit tests for core logic
│
├── requirements.txt      # Project dependencies
├── Procfile              # Deployment configuration (Render)
└── README.md             # Project documentation
```

---

##  Tech Stack & Features

### **Backend**
- Python
- Flask
- SQLite3
- pytest
- unittest


### **Core Features**
- Create anesthesia log entries from validated patient input
- Protocol generation (Combined / Regional)
- Persist logs in SQLite with timestamps
- Retrieve and filter logs via API
- Predictable error responses for invalid input

### **API Endpoints**
- `GET /logs` — return all logs
- `GET /logs/filter` — filter logs by query params
- `POST /anesthesia` — validate input, generate protocol, persist to DB
- `DELETE /logs/<id>` — delete a log record by id

### **Validation**
- Valid age range
- Valid weight range
- Required fields must be present
- Prevents invalid data from entering the database

### **Testing**

**Unit tests(unittest) cover:**
- Input validation (age, weight)
- Dose calculations
- Protocol text generation
- Storage layer behavior

**Integration tests(pytest) cover API-level behavior:**
- Request/respond validation
- Error handling
- Database side effects

## Running tests
```bush
python -m pytest
```
---
## Run API locally
```bush
python -m anesthesia.app
```

##  Deployment
The API is deployed on Render as a production-style backend service:

**Live API:**
https://anesthesia-log-simulator.onrender.com

---
## Author
Created by Kateryna Babakova (https://github.com/katebabakova444) This project is part of my backend development journey.