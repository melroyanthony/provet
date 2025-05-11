"""Unit tests for data_models.py module.

Tests for the data model classes and their functionality.
"""

import pytest

from provet.core.data_models import (
    ClinicalNote,
    ConsultationData,
    Patient,
)


class TestPatient:
    """Test class for the Patient data model."""

    @pytest.mark.parametrize(
        "name, species, breed, gender, neutered, date_of_birth, weight, microchip",
        [
            (
                "Max",
                "Dog",
                "Golden Retriever",
                "Male",
                True,
                "2018-05-10",
                "32 kg",
                "123456789012345",
            ),
            (
                "Luna",
                "Cat",
                "Maine Coon",
                "Female",
                False,
                "2020-01-15",
                "4.5 kg",
                None,
            ),
            ("Buddy", "Dog", "Mixed", "Male", True, "2019-03-22", "25 kg", None),
        ],
    )
    def test_patient_init(
        self, name, species, breed, gender, neutered, date_of_birth, weight, microchip
    ):
        """Test Patient initialization with different parameter values.

        Given: Patient attributes
        When: A Patient object is created
        Then: The object should have the correct attributes.
        """
        patient = Patient(
            name=name,
            species=species,
            breed=breed,
            gender=gender,
            neutered=neutered,
            date_of_birth=date_of_birth,
            weight=weight,
            microchip=microchip,
        )

        assert patient.name == name
        assert patient.species == species
        assert patient.breed == breed
        assert patient.gender == gender
        assert patient.neutered == neutered
        assert patient.date_of_birth == date_of_birth
        assert patient.weight == weight
        assert patient.microchip == microchip


class TestClinicalNote:
    """Test class for the ClinicalNote data model."""

    @pytest.mark.parametrize(
        "note, note_type, expected_type",
        [
            ("Test note", None, "general"),
            ("Assessment note", "assessment", "assessment"),
            ("Diagnosis", "diagnosis", "diagnosis"),
        ],
    )
    def test_clinical_note_init(self, note, note_type, expected_type):
        """Test ClinicalNote initialization with different parameter values.

        Given: Clinical note attributes
        When: A ClinicalNote object is created
        Then: The object should have the correct attributes with default type if not specified.
        """
        kwargs = {"note": note}
        if note_type:
            kwargs["type"] = note_type

        clinical_note = ClinicalNote(**kwargs)

        assert clinical_note.note == note
        assert clinical_note.type == expected_type


class TestConsultationData:
    """Test class for the ConsultationData data model."""

    def test_from_dict(self, sample_consultation_data):
        """Test creation of ConsultationData from a dictionary.

        Given: A dictionary containing consultation data
        When: ConsultationData.from_dict is called
        Then: It should return a properly populated ConsultationData object.
        """
        data = ConsultationData.from_dict(sample_consultation_data)

        # Check patient data
        assert data.patient.name == "Max"
        assert data.patient.species == "Dog (Canine - Domestic)"
        assert data.patient.breed == "Golden Retriever"
        assert data.patient.gender == "Male"
        assert data.patient.neutered is True
        assert data.patient.date_of_birth == "2018-05-10"
        assert data.patient.weight == "32 kg"
        assert data.patient.microchip == "123456789012345"

        # Check consultation data
        assert data.consultation.date == "2023-07-15"
        assert data.consultation.time == "10:30"
        assert data.consultation.reason == "Vomiting and lethargy"
        assert data.consultation.type == "Outpatient"

        # Check clinical notes
        assert len(data.consultation.clinical_notes) == 2
        assert (
            data.consultation.clinical_notes[0].note
            == "Patient presented with vomiting and lethargy for the past 24 hours."
        )
        assert data.consultation.clinical_notes[0].type == "general"

        # Check procedures
        assert len(data.consultation.treatment_items.procedures) == 2
        assert (
            data.consultation.treatment_items.procedures[0].name
            == "Physical examination"
        )

        # Check medicines
        assert len(data.consultation.treatment_items.medicines) == 1
        assert data.consultation.treatment_items.medicines[0].name == "Cerenia"

        # Check prescriptions
        assert len(data.consultation.treatment_items.prescriptions) == 1
        assert (
            data.consultation.treatment_items.prescriptions[0].name == "Metronidazole"
        )
        assert data.consultation.treatment_items.prescriptions[0].duration == "5 days"

        # Check diagnostics
        assert len(data.consultation.diagnostics) == 1
        assert data.consultation.diagnostics[0].name == "Complete Blood Count"
        assert data.consultation.diagnostics[0].result == "Within normal limits"

    def test_from_dict_minimal(self):
        """Test creation of ConsultationData from a minimal dictionary.

        Given: A dictionary with minimal required consultation data
        When: ConsultationData.from_dict is called
        Then: It should return a ConsultationData object with default values for missing fields.
        """
        minimal_data = {
            "patient": {
                "name": "Rex",
                "species": "Dog",
                "breed": "Labrador",
                "gender": "Male",
                "neutered": False,
                "date_of_birth": "2017-01-01",
                "weight": "30 kg",
            },
            "consultation": {
                "date": "2023-08-01",
                "time": "09:00",
                "reason": "Annual checkup",
                "type": "Wellness",
            },
        }

        data = ConsultationData.from_dict(minimal_data)

        # Check patient data
        assert data.patient.name == "Rex"
        assert data.patient.microchip is None

        # Check empty lists
        assert len(data.consultation.clinical_notes) == 0
        assert len(data.consultation.treatment_items.procedures) == 0
        assert len(data.consultation.treatment_items.medicines) == 0
        assert len(data.consultation.treatment_items.prescriptions) == 0
        assert len(data.consultation.diagnostics) == 0

    def test_to_template_context(self, consultation_data_object):
        """Test conversion of ConsultationData to template context.

        Given: A ConsultationData object
        When: to_template_context is called
        Then: It should return a dictionary with the appropriate keys.
        """
        context = consultation_data_object.to_template_context()

        assert "patient" in context
        assert "consultation" in context
        assert "clinical_notes" in context
        assert "procedures" in context
        assert "medicines" in context
        assert "prescriptions" in context
        assert "diagnostics" in context

        assert context["patient"] == consultation_data_object.patient
        assert context["consultation"] == consultation_data_object.consultation
        assert (
            context["clinical_notes"]
            == consultation_data_object.consultation.clinical_notes
        )
        assert (
            context["procedures"]
            == consultation_data_object.consultation.treatment_items.procedures
        )
