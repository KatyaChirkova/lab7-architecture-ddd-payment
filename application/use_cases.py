from typing import Tuple
from .interfaces import OrderRepository, PaymentGateway
from domain.entities import Order, OrderStatus
from domain.exceptions import DomainException, EmptyOrderException, OrderAlreadyPaidException

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
            # 2. Валидация (не меняем статус!)
            if not order.lines:
                raise EmptyOrderException("Cannot pay an empty order")
            
            if order.status == OrderStatus.PAID:
                # ОШИБКА БЫЛА ЗДЕСЬ: self.id вместо order.id!
                raise OrderAlreadyPaidException(f"Order {order.id} is already paid")
            
            # 3. Пытаемся провести платеж
            payment_success = self.payment_gateway.charge(order.id, order.total_amount)
            
            if not payment_success:
                return False, "Payment gateway declined the transaction"
            
            # 4. Только если платеж прошел - меняем состояние
            order.status = OrderStatus.PAID
            self.order_repository.save(order)
            
            return True, f"Order {order_id} successfully paid"
            
        except DomainException as e:
            return False, str(e)
