from __future__ import annotations

import re


class AgentIntakeParser:
    """
    Lightweight transcript parser (MVP).

    In production, you would replace/augment this with:
    - robust NER / LLM extraction with guardrails
    - confidence scores + human review UI
    - multilingual support
    """

    PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s-]?)?(?:\d[\s-]?){9,12}\d")
    AGE_RE = re.compile(r"\b(\d{1,3})\s*(?:years?|yrs?)\b", re.IGNORECASE)
    NAME_RE = re.compile(r"\bname\s*(?:is|:)\s*([a-zA-Z][a-zA-Z\s.'-]{1,60})", re.IGNORECASE)
    LOC_RE = re.compile(r"\b(?:address|location|pickup)\s*(?:is|:)\s*([a-zA-Z0-9][a-zA-Z0-9\s,.'#/-]{3,120})", re.IGNORECASE)
    SYM_RE = re.compile(r"\b(?:symptoms?|complaint|problem)\s*(?:are|is|:)\s*([a-zA-Z0-9][^.\n]{3,200})", re.IGNORECASE)

    @classmethod
    def extract(cls, text: str) -> dict:
        out: dict = {"raw": text}

        phone = cls.PHONE_RE.search(text)
        if phone:
            out["patient_phone"] = re.sub(r"\s+", "", phone.group(0))

        age = cls.AGE_RE.search(text)
        if age:
            try:
                out["patient_age"] = int(age.group(1))
            except ValueError:
                pass

        name = cls.NAME_RE.search(text)
        if name:
            out["patient_name"] = name.group(1).strip()

        loc = cls.LOC_RE.search(text)
        if loc:
            out["pickup_location"] = loc.group(1).strip()

        sym = cls.SYM_RE.search(text)
        if sym:
            out["symptoms"] = sym.group(1).strip()

        # You can add more patterns: allergies, vitals, blood group, etc.
        return out

