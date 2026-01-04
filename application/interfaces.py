from abc import ABC, abstractmethod
from typing import Optional
from domain.entities import Order
from domain.value_objects import Money

class OrderRepository(ABC):
    """Интерфейс репозитория для работы с заказами"""
    
    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[Order]:
        """Найти заказ по ID"""
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        """Сохранить заказ"""
        pass

class PaymentGateway(ABC):
    """Интерфейс платежного шлюза"""
    
    @abstractmethod
    def charge(self, order_id: int, amount: Money) -> bool:
        """
        Выполнить платеж.
        Возвращает True если платеж прошел успешно, False в случае ошибки.
        """
        pass
