from typing import Tuple
from .interfaces import OrderRepository, PaymentGateway
from domain.entities import Order
from domain.exceptions import DomainException

class PayOrderUseCase:
    """Use Case: Оплата заказа"""
    
    def __init__(
        self,
        order_repository: OrderRepository,
        payment_gateway: PaymentGateway
    ):
        self.order_repository = order_repository
        self.payment_gateway = payment_gateway

    def execute(self, order_id: int) -> Tuple[bool, str]:
        """
        Основной метод Use Case.
        Возвращает кортеж (успех_операции, сообщение).
        """
        # 1. Загружаем заказ
        order = self.order_repository.get_by_id(order_id)
        if not order:
            return False, f"Order {order_id} not found"
        
        try:
            # 2. Выполняем доменную операцию (проверка инвариантов)
            order.pay()
            
            # 3. Вызываем внешний платежный сервис
            payment_success = self.payment_gateway.charge(order.id, order.total_amount)
            
            if not payment_success:
                return False, "Payment gateway declined the transaction"
            
            # 4. Сохраняем обновленный заказ
            self.order_repository.save(order)
            
            return True, f"Order {order_id} successfully paid"
            
        except DomainException as e:
            return False, str(e)
