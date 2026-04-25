import re
from dataclasses import dataclass


@dataclass(frozen=True)
class LicensePlate:
    """Accepts old format AAA-0000 and Mercosul format AAA0A00."""
    value: str

    def __post_init__(self):
        normalized = re.sub(r"[-\s]", "", self.value.upper())
        old = re.fullmatch(r"[A-Z]{3}\d{4}", normalized)
        mercosul = re.fullmatch(r"[A-Z]{3}\d[A-Z]\d{2}", normalized)
        if not old and not mercosul:
            raise ValueError(f"Placa inválida: {self.value!r}")
        object.__setattr__(self, "value", normalized)
