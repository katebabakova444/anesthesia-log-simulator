from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    logs = relationship("AnesthesiaLog", back_populates="patient")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
        }
class AnesthesiaLog(Base):
    __tablename__ = "anesthesia_logs"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    asa_class = Column(String, nullable=False)
    anesthesia_type = Column(String, nullable=False)
    block_type = Column(String)
    protocol = Column(String)
    doses = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="logs")

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "asa_class": self.asa_class,
            "anesthesia_type": self.anesthesia_type,
            "block_type": self.block_type,
            "protocol": self.protocol,
            "doses": self.doses,
            "created_at": str(self.created_at)
        }






