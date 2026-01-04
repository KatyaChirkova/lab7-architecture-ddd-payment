from typing import Dict, Optional
from application.interfaces import OrderRepository
from domain.entities import Order

class InMemoryOrderRepository(OrderRepository):
    """Реализация репозитория в оперативной памяти"""
    
    def __init__(self):
        self._storage: Dict[int, Order] = {}
        self._next_id = 1

    def get_by_id(self, order_id: int) -> Optional[Order]:
        return self._storage.get(order_id)

    def save(self, order: Order) -> None:
        if order.id is None:
            order.id = self._next_id
            self._next_id += 1
        self._storage[order.id] = order

    # Дополнительные методы для тестирования
    def add_order(self, order: Order) -> None:
        """Вспомогательный метод для добавления заказа"""
        self.save(order)
