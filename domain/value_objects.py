from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True, eq=True)
class Money:
    """Value Object для денежных сумм"""
    amount: int  # Храним в копейках для точности
    currency: str = "RUB"

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __repr__(self) -> str:
        return f"{self.amount / 100:.2f} {self.currency}"
