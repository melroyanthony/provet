"""PHI redaction guardrails for veterinary discharge notes.

Redacts Protected Health Information (PHI) before sending prompts to external
LLM providers, then restores original values in the generated output. This
ensures sensitive patient/owner data never leaves the application boundary.
"""

import re


class PHIRedactor:
    """Redacts and restores PHI tokens in text.

    Supported PHI categories:
        - Microchip numbers (10-15 digit sequences)
        - Dates of birth (YYYY-MM-DD)
        - Phone numbers (common formats)
        - Email addresses

    Attributes:
        enabled: Whether redaction is active.
    """

    # Patterns ordered from most specific to least specific
    PATTERNS: list[tuple[str, str, re.Pattern]] = [
        ("MICROCHIP", "microchip", re.compile(r"\b\d{10,15}\b")),
        ("DOB", "date", re.compile(r"\b\d{4}-\d{2}-\d{2}\b")),
        ("PHONE", "phone", re.compile(r"\+?\d[\d\s\-]{7,14}\d")),
        ("EMAIL", "email", re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")),
    ]

    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled

    def redact(self, text: str) -> tuple[str, dict[str, str]]:
        """Replace PHI tokens with placeholders and return the mapping.

        Args:
            text: Input text potentially containing PHI.

        Returns:
            Tuple of (redacted text, {placeholder: original_value} mapping).
        """
        if not self.enabled:
            return text, {}

        mapping: dict[str, str] = {}
        counters: dict[str, int] = {}

        for category, _label, pattern in self.PATTERNS:
            for match in pattern.finditer(text):
                original = match.group()
                if original in mapping.values():
                    continue
                count = counters.get(category, 0)
                placeholder = f"[REDACTED_{category}_{count}]"
                counters[category] = count + 1
                mapping[placeholder] = original

        redacted = text
        for placeholder, original in mapping.items():
            redacted = redacted.replace(original, placeholder)

        return redacted, mapping

    def restore(self, text: str, mapping: dict[str, str]) -> str:
        """Restore original PHI values from placeholders.

        Args:
            text: Text containing redaction placeholders.
            mapping: Placeholder-to-original mapping from redact().

        Returns:
            Text with original PHI values restored.
        """
        restored = text
        for placeholder, original in mapping.items():
            restored = restored.replace(placeholder, original)
        return restored
