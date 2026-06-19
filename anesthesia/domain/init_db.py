from anesthesia.models import Base, engine
Base.metadata.create_all(engine)
print("Database tables created")