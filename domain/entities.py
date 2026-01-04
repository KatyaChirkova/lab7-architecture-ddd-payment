from dataclasses import dataclass, field
from typing import List
from enum import Enum
from .value_objects import Money
from .exceptions import (
    OrderAlreadyPaidException,
    EmptyOrderException,
    OrderModificationException
)

class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"

@dataclass
class OrderLine:
    """Часть агрегата Order"""
    product_name: str
    quantity: int
    unit_price: Money

    @property
    def total(self) -> Money:
        return Money(self.unit_price.amount * self.quantity, self.unit_price.currency)

@dataclass
class Order:
    """Агрегат. Корневая сущность."""
    id: int
    customer_id: int
    status: OrderStatus = OrderStatus.PENDING
    lines: List[OrderLine] = field(default_factory=list)

    def add_line(self, product_name: str, quantity: int, unit_price: Money) -> None:
        if self.status == OrderStatus.PAID:
            raise OrderModificationException("Cannot modify paid order")
        
        for line in self.lines:
            if line.product_name == product_name and line.unit_price == unit_price:
                line.quantity += quantity
                return
        
        self.lines.append(OrderLine(product_name, quantity, unit_price))

    @property
    def total_amount(self) -> Money:
        if not self.lines:
            return Money(0)
        
        total = Money(0)
        for line in self.lines:
            total = total + line.total
        return total

    def pay(self) -> None:
        if not self.lines:
            raise EmptyOrderException("Cannot pay an empty order")
        
        if self.status == OrderStatus.PAID:
            raise OrderAlreadyPaidException(f"Order {self.id} is already paid")
        
        self.status = OrderStatus.PAID
