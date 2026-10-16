"""Manage a small in-memory set of hospital patient admission records."""

import hashlib
import json
import secrets
from pathlib import Path

PATIENT_RECORDS: dict[str, dict[str, str | bool | float]] = {
    "P101": {
        "name": "John Doe",
        "ward": "ICU",
        "is_admitted": True,
        "bill": 2400.0,
    },
    "P102": {
        "name": "Jane Smith",
        "ward": "General",
        "is_admitted": False,
        "bill": 450.0,
    },
    "P103": {
        "name": "Robert Brown",
        "ward": "Private",
        "is_admitted": True,
        "bill": 1200.0,
    },
}


def admit_patient(
    patient_id: str,
    name: str,
    ward: str,
    intake_log: list[str] | None = None,
) -> bool:
    """Admit a new patient and optionally record the action in a log."""
    if patient_id in PATIENT_RECORDS:
        return False

    if intake_log is None:
        intake_log = []

    PATIENT_RECORDS[patient_id] = {
        "name": name,
        "ward": ward,
        "is_admitted": True,
        "bill": 0.0,
    }
    intake_log.append(f"Admitted patient {patient_id} into ward {ward}")
    return True


def discharge_patient(patient_id: str) -> bool:
    """Discharge a patient, returning False when the ID is not registered."""
    patient = PATIENT_RECORDS.get(patient_id)
    if patient is None:
        return False

    patient["is_admitted"] = False
    return True


def verify_admission_status(patient_id: str) -> bool:
    """Return whether the specified patient is currently admitted."""
    patient = PATIENT_RECORDS.get(patient_id)
    return patient is not None and patient["is_admitted"] is True


def calculate_treatment_cost(
    patient_id: str, multiplier: float = 1.12
) -> float:
    """Calculate a patient's bill using a numeric treatment-cost multiplier."""
    patient = PATIENT_RECORDS.get(patient_id)
    if patient is None:
        raise KeyError(f"Unknown patient ID: {patient_id}")
    if multiplier < 0:
        raise ValueError("The treatment-cost multiplier cannot be negative.")

    return float(patient["bill"]) * multiplier


def generate_patient_hash(patient_id: str) -> str:
    """Return a SHA-256 digest for a patient ID."""
    return hashlib.sha256(patient_id.encode("utf-8")).hexdigest()


def generate_ward_token() -> int:
    """Generate a four-digit token using a security-oriented random source."""
    return secrets.randbelow(9000) + 1000


def export_patient_ledger(filename: str = "patient_records.json") -> None:
    """Write patient records as JSON without invoking a shell command."""
    output_path = Path(filename)
    with output_path.open("w", encoding="utf-8") as ledger_file:
        json.dump(PATIENT_RECORDS, ledger_file, indent=2, sort_keys=True)
    print(f"Patient ledger exported to: {output_path}")


def get_ward_summary(
    records: dict[str, dict[str, str | bool | float]],
) -> int:
    """Return the number of currently admitted patients in the records."""
    return sum(
        1 for patient in records.values() if patient["is_admitted"] is True
    )


def main() -> None:
    """Demonstrate the patient-management functions."""
    admit_patient("P104", "Alice Walker", "General")
    discharge_patient("P101")
    print("Is P103 admitted:", verify_admission_status("P103"))
    print("Cost calculated:", calculate_treatment_cost("P103", 1.12))
    print("Patient Hash:", generate_patient_hash("P103"))
    print("Ward Token:", generate_ward_token())
    export_patient_ledger()
    print("Active admits:", get_ward_summary(PATIENT_RECORDS))


if __name__ == "__main__":
    main()
