from application.interfaces import PaymentGateway
from domain.value_objects import Money

class FakePaymentGateway(PaymentGateway):
    """
    Фейковый платежный шлюз для тестирования.
    """
    
    def __init__(self, fail_mode: bool = False):
        """
        :param fail_mode: Если True, все платежи будут отклоняться
        """
        self.fail_mode = fail_mode
        self.charges_log = []  # Лог для проверки в тестах

    def charge(self, order_id: int, amount: Money) -> bool:
        self.charges_log.append((order_id, amount))
        
        if self.fail_mode:
            return False
        
        # Фейковая логика: отклоняем платежи больше 10000 рублей
        if amount.amount > 10000_00:
            return False
        
        return True
