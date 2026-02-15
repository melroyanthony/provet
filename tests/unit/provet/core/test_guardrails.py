"""Unit tests for guardrails.py module.

Tests for the PHIRedactor class covering redaction and restoration of PHI tokens.
"""

import pytest

from provet.core.guardrails import PHIRedactor


class TestPHIRedactor:
    """Test class for PHIRedactor."""

    def test_redact_microchip(self):
        """Given: Text containing a 15-digit microchip number
        When: redact() is called
        Then: The microchip number should be replaced with a placeholder.
        """
        redactor = PHIRedactor(enabled=True)
        text = "Patient microchip: 123456789012345"
        redacted, mapping = redactor.redact(text)

        assert "123456789012345" not in redacted
        assert "[REDACTED_MICROCHIP_0]" in redacted
        assert mapping["[REDACTED_MICROCHIP_0]"] == "123456789012345"

    def test_redact_date_of_birth(self):
        """Given: Text containing a date in YYYY-MM-DD format
        When: redact() is called
        Then: The date should be replaced with a placeholder.
        """
        redactor = PHIRedactor(enabled=True)
        text = "Date of birth: 2018-05-10"
        redacted, mapping = redactor.redact(text)

        assert "2018-05-10" not in redacted
        assert "[REDACTED_DOB_0]" in redacted

    def test_redact_email(self):
        """Given: Text containing an email address
        When: redact() is called
        Then: The email should be replaced with a placeholder.
        """
        redactor = PHIRedactor(enabled=True)
        text = "Owner contact: owner@example.com"
        redacted, mapping = redactor.redact(text)

        assert "owner@example.com" not in redacted
        assert "[REDACTED_EMAIL_0]" in redacted

    def test_redact_multiple_phi(self):
        """Given: Text with multiple PHI types
        When: redact() is called
        Then: All PHI tokens should be redacted with unique placeholders.
        """
        redactor = PHIRedactor(enabled=True)
        text = "Microchip: 123456789012345, DOB: 2020-01-15, Email: vet@clinic.com"
        redacted, mapping = redactor.redact(text)

        assert "123456789012345" not in redacted
        assert "2020-01-15" not in redacted
        assert "vet@clinic.com" not in redacted
        assert len(mapping) == 3

    def test_restore_roundtrip(self):
        """Given: Text that has been redacted
        When: restore() is called with the mapping
        Then: The original text should be fully restored.
        """
        redactor = PHIRedactor(enabled=True)
        original = "Microchip: 123456789012345, DOB: 2018-05-10"
        redacted, mapping = redactor.redact(original)
        restored = redactor.restore(redacted, mapping)

        assert restored == original

    def test_disabled_redactor_passthrough(self):
        """Given: A disabled PHIRedactor
        When: redact() is called
        Then: Text should pass through unchanged with empty mapping.
        """
        redactor = PHIRedactor(enabled=False)
        text = "Microchip: 123456789012345"
        redacted, mapping = redactor.redact(text)

        assert redacted == text
        assert mapping == {}

    def test_restore_with_empty_mapping(self):
        """Given: Text and an empty mapping
        When: restore() is called
        Then: Text should be returned unchanged.
        """
        redactor = PHIRedactor(enabled=True)
        text = "No PHI here"
        result = redactor.restore(text, {})

        assert result == text

    def test_no_phi_in_text(self):
        """Given: Text with no PHI
        When: redact() is called
        Then: Text should be returned unchanged.
        """
        redactor = PHIRedactor(enabled=True)
        text = "The patient was seen for a routine checkup."
        redacted, mapping = redactor.redact(text)

        assert redacted == text
        assert mapping == {}
