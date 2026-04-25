import re
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CPFValueObject:
    value: str

    def __post_init__(self):
        digits = re.sub(r"\D", "", self.value)
        if len(digits) != 11:
            raise ValueError(f"CPF inválido: {self.value!r}")
        object.__setattr__(self, "value", digits)


@dataclass(frozen=True)
class EmailValueObject:
    value: str

    def __post_init__(self):
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, self.value):
            raise ValueError(f"E-mail inválido: {self.value!r}")


@dataclass(frozen=True)
class MoneyValueObject:
    amount: Decimal

    def __post_init__(self):
        if self.amount < Decimal("0"):
            raise ValueError("Valor monetário não pode ser negativo.")
