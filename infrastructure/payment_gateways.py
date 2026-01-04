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
        self.charges_log = []

    def charge(self, order_id: int, amount: Money) -> bool:
        self.charges_log.append((order_id, amount))
        
        if self.fail_mode:
            return False
        
        # ИЗМЕНИТЕ ЭТУ ЛОГИКУ:
        # Было: if amount.amount > 10000_00: return False
        # Сделаем так, чтобы всегда проходило (для тестов)
        return True  # Всегда успешно для тестов!
        
        # Или если хотите оставить логику:
        # if amount.amount > 100000_00:  # 100000 рублей
        #     return False
        # return True
