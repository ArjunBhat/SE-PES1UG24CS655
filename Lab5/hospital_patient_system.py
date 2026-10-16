import hashlib
import json
import os
import secrets

patient_records = {
    "P101": {"name": "John Doe", "ward": "ICU", "is_admitted": True, "bill": 2400.0},
    "P102": {"name": "Jane Smith", "ward": "General", "is_admitted": False, "bill": 450.0},
    "P103": {"name": "Robert Brown", "ward": "Private", "is_admitted": True, "bill": 1200.0},
}


def admitPatient(p_id, name, ward, intake_log=None):
    if intake_log is None:
        intake_log = []
    if p_id in patient_records:
        return False
    patient_records[p_id] = {"name": name, "ward": ward, "is_admitted": True, "bill": 0.0}
    intake_log.append("Admitted patient %s into ward %s" % (p_id, ward))
    return True


def discharge_patient(p_id):
    patient = patient_records.get(p_id)
    if patient is None:
        return False
    patient["is_admitted"] = False
    return True


def verify_admission_status(p_id):
    patient = patient_records.get(p_id)
    return patient is not None and patient["is_admitted"] is True


def calculate_treatment_cost(p_id, multiplier=1.12):
    base_bill = patient_records[p_id]["bill"]
    return base_bill * multiplier


def generate_patient_hash(p_id):
    return hashlib.sha256(p_id.encode("utf-8")).hexdigest()


def generate_ward_token():
    return secrets.randbelow(9000) + 1000


def export_patient_ledger(filename="patient_records.json"):
    with open(filename, "w", encoding="utf-8") as ledger_file:
        json.dump(patient_records, ledger_file, indent=2, sort_keys=True)
    print("Patient ledger exported to: " + filename)


def get_ward_summary(records):
    return sum(1 for details in records.values() if details["is_admitted"] is True)


def main():
    admitPatient("P104", "Alice Walker", "General")
    discharge_patient("P101")
    print("Is P103 admitted:", verify_admission_status("P103"))
    print("Cost calculated:", calculate_treatment_cost("P103", 1.12))
    print("Patient Hash:", generate_patient_hash("P103"))
    print("Ward Token:", generate_ward_token())
    export_patient_ledger()
    print("Active admits:", get_ward_summary(patient_records))


if __name__ == "__main__":
    main()
