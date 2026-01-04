class DomainException(Exception):
    """Базовое исключение для доменных ошибок"""
    pass

class OrderAlreadyPaidException(DomainException):
    """Заказ уже оплачен"""
    pass

class EmptyOrderException(DomainException):
    """Попытка оплатить пустой заказ"""
    pass

class OrderModificationException(DomainException):
    """Попытка изменить оплаченный заказ"""
    pass
