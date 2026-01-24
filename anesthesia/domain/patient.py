from dataclasses import dataclass

@dataclass
class Patient:
    name: str
    age: int
    weight: float
    asa_class: str

    @staticmethod
    def from_dict(data: dict):
        return Patient(
            name=data["name"],
            age=data["age"],
            weight=float(data["weight"]),
            asa_class=data["asa_class"]
        )