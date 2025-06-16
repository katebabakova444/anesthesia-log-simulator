from patient import Patient
from storage import save_log
from utils import validate_age, validate_weight
from anesthesia_types import CombinedAnesthesia, RegionalAnesthesia

def choose_anesthesia_type(patient_data):
    print("Select anesthesia type:")
    print("1. Regional Anesthesia")
    print("2. Combined IV+Inhalational Anesthesia")
    choice = input("Enter number: ")
    if choice == "1":
        print("\nSelect regional block type:")
        print("1. Spinal")
        print("2. Epidural")
        block_choice = input("Enter number: ")
        block_type = "spinal" if block_choice == "1" else "epidural"
        return RegionalAnesthesia(patient_data, block_type)
    elif choice == "2":
        return CombinedAnesthesia(patient_data)
    else:
        print("Invalid input. Defaulting to Combined.")
        return CombinedAnesthesia(patient_data)

def main():
    name = input("Enter patient name: ")
    age = int(input("Enter patient age: "))
    while not validate_age(age):
        age = int(input("Invalid age. Enter again: "))
    weight = float(input("Enter patient weight (kg): "))
    while not validate_weight(weight):
        weight = float(input("Invalid weight. Enter again: "))
    patient_data = {"name": name, "age": age, "weight": weight}

    anesthesia = choose_anesthesia_type(patient_data)
    protocol, doses = anesthesia.generate_protocol()
    print(f"\nRecommended protocol:\n{protocol}")

    print("\nDoses:")
    for drug, amount in doses.items():
        print(f"{drug.capitalize()}: {amount}")

    log_kwargs = dict(
        name=name,
        age=age,
        weight=weight,
        anesthesia_type=anesthesia.__class__.__name__.replace("Anesthesia", "").lower(),
    )
    if isinstance(anesthesia, CombinedAnesthesia):
        log_kwargs.update(
            drug="propofol, sevoflurane",
            dosage=doses.get("propofol", ""),
            maintenance=doses.get("sevoflurane", ""),
            technique=""
        )
    else:
        log_kwargs.update(
            drug="bupivacaine",
            dosage=doses.get("bupivacaine", ""),
            maintenance="",
            technique=anesthesia.block_type.capitalize() + " block"
        )

    save_log(**log_kwargs)
    print("\nLogged to anesthesia_log.csv")

if __name__ == "__main__":
    main()