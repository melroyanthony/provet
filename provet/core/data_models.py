"""Data models for the Provet application.

This module defines structured data models for consultation information,
facilitating type checking and data validation.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Patient:
    """Patient information model.

    Attributes:
        name: The patient's name.
        species: The species of the patient (e.g., "Dog (Canine - Domestic)").
        breed: The breed of the patient.
        gender: The gender of the patient.
        neutered: Whether the patient is neutered/spayed.
        date_of_birth: The patient's date of birth.
        weight: The patient's weight with unit.
        microchip: The patient's microchip number, if available.
    """

    name: str
    species: str
    breed: str
    gender: str
    neutered: bool
    date_of_birth: str
    weight: str
    microchip: str | None = None


@dataclass
class ClinicalNote:
    """Clinical note model.

    Attributes:
        note: The content of the clinical note.
        type: The type of note (e.g., "general", "assessment").
    """

    note: str
    type: str = "general"


@dataclass
class Procedure:
    """Medical procedure model.

    Attributes:
        name: The name of the procedure.
        date: The date the procedure was performed.
        time: The time the procedure was performed.
        code: The procedure code.
        quantity: The quantity of the procedure performed.
        total_price: The total price of the procedure in smallest currency unit.
        currency: The currency code for the price.
    """

    name: str
    date: str | None = None
    time: str | None = None
    code: str | None = None
    quantity: int = 1
    total_price: int | None = None
    currency: str | None = None


@dataclass
class Medicine:
    """Medicine model.

    Attributes:
        name: The name of the medicine.
        dosage: The dosage information.
        instructions: Instructions for administering the medicine.
    """

    name: str
    dosage: str | None = None
    instructions: str | None = None


@dataclass
class Prescription:
    """Prescription model.

    Attributes:
        name: The name of the prescribed medication.
        dosage: The dosage information.
        instructions: Instructions for using the prescription.
        duration: The duration for which the prescription should be taken.
    """

    name: str
    dosage: str | None = None
    instructions: str | None = None
    duration: str | None = None


@dataclass
class Diagnostic:
    """Diagnostic test model.

    Attributes:
        name: The name of the diagnostic test.
        result: The result of the diagnostic test.
        notes: Additional notes about the diagnostic test.
    """

    name: str
    result: str | None = None
    notes: str | None = None


@dataclass
class TreatmentItems:
    """Treatment items model.

    Attributes:
        procedures: List of procedures performed.
        medicines: List of medicines administered.
        prescriptions: List of prescriptions issued.
        foods: List of recommended foods.
        supplies: List of supplies provided.
    """

    procedures: list[Procedure] = field(default_factory=list)
    medicines: list[Medicine] = field(default_factory=list)
    prescriptions: list[Prescription] = field(default_factory=list)
    foods: list[dict[str, Any]] = field(default_factory=list)
    supplies: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class Consultation:
    """Consultation model.

    Attributes:
        date: The date of the consultation.
        time: The time of the consultation.
        reason: The reason for the consultation.
        type: The type of consultation (e.g., "Outpatient").
        clinical_notes: List of clinical notes.
        treatment_items: Treatment items provided during the consultation.
        diagnostics: List of diagnostic tests performed.
    """

    date: str
    time: str
    reason: str
    type: str
    clinical_notes: list[ClinicalNote] = field(default_factory=list)
    treatment_items: TreatmentItems = field(default_factory=TreatmentItems)
    diagnostics: list[Diagnostic] = field(default_factory=list)


@dataclass
class ConsultationData:
    """Complete consultation data model.

    Attributes:
        patient: Patient information.
        consultation: Consultation details.
    """

    patient: Patient
    consultation: Consultation

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConsultationData":
        """Create a ConsultationData object from a dictionary.

        Args:
            data: Dictionary containing consultation data.

        Returns:
            ConsultationData object populated with the data.
        """
        patient_data = data.get("patient", {})
        patient = Patient(
            name=patient_data.get("name", ""),
            species=patient_data.get("species", ""),
            breed=patient_data.get("breed", ""),
            gender=patient_data.get("gender", ""),
            neutered=patient_data.get("neutered", False),
            date_of_birth=patient_data.get("date_of_birth", ""),
            weight=patient_data.get("weight", ""),
            microchip=patient_data.get("microchip"),
        )

        consultation_data = data.get("consultation", {})

        # Process clinical notes
        clinical_notes = []
        for note_data in consultation_data.get("clinical_notes", []):
            clinical_notes.append(
                ClinicalNote(
                    note=note_data.get("note", ""),
                    type=note_data.get("type", "general"),
                )
            )

        # Process treatment items
        treatment_items_data = consultation_data.get("treatment_items", {})

        # Process procedures
        procedures = []
        for proc_data in treatment_items_data.get("procedures", []):
            procedures.append(
                Procedure(
                    name=proc_data.get("name", ""),
                    date=proc_data.get("date"),
                    time=proc_data.get("time"),
                    code=proc_data.get("code"),
                    quantity=proc_data.get("quantity", 1),
                    total_price=proc_data.get("total_price"),
                    currency=proc_data.get("currency"),
                )
            )

        # Process medicines
        medicines = []
        for med_data in treatment_items_data.get("medicines", []):
            medicines.append(
                Medicine(
                    name=med_data.get("name", ""),
                    dosage=med_data.get("dosage"),
                    instructions=med_data.get("instructions"),
                )
            )

        # Process prescriptions
        prescriptions = []
        for rx_data in treatment_items_data.get("prescriptions", []):
            prescriptions.append(
                Prescription(
                    name=rx_data.get("name", ""),
                    dosage=rx_data.get("dosage"),
                    instructions=rx_data.get("instructions"),
                    duration=rx_data.get("duration"),
                )
            )

        treatment_items = TreatmentItems(
            procedures=procedures,
            medicines=medicines,
            prescriptions=prescriptions,
            foods=treatment_items_data.get("foods", []),
            supplies=treatment_items_data.get("supplies", []),
        )

        # Process diagnostics
        diagnostics = []
        for diag_data in consultation_data.get("diagnostics", []):
            diagnostics.append(
                Diagnostic(
                    name=diag_data.get("name", ""),
                    result=diag_data.get("result"),
                    notes=diag_data.get("notes"),
                )
            )

        consultation = Consultation(
            date=consultation_data.get("date", ""),
            time=consultation_data.get("time", ""),
            reason=consultation_data.get("reason", ""),
            type=consultation_data.get("type", ""),
            clinical_notes=clinical_notes,
            treatment_items=treatment_items,
            diagnostics=diagnostics,
        )

        return cls(patient=patient, consultation=consultation)

    def to_template_context(self) -> dict[str, Any]:
        """Convert the consultation data to a template context dictionary.

        Returns:
            Dictionary containing template context data.
        """
        return {
            "patient": self.patient,
            "consultation": self.consultation,
            "clinical_notes": self.consultation.clinical_notes,
            "procedures": self.consultation.treatment_items.procedures,
            "medicines": self.consultation.treatment_items.medicines,
            "prescriptions": self.consultation.treatment_items.prescriptions,
            "diagnostics": self.consultation.diagnostics,
        }
