from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()
Base = declarative_base()
class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    asa_class = Column(String)
    anesthesia_type = Column(String)
    block_type = Column(String)
    protocol = Column(String)
    doses = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)




