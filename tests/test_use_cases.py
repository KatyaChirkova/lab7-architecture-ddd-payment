import pytest
from domain.entities import Order, OrderStatus
from domain.value_objects import Money
from domain.exceptions import EmptyOrderException, OrderAlreadyPaidException

def test_successful_payment(pay_order_use_case, order_repository, sample_order):
    """Тест успешной оплаты корректного заказа"""
    # Arrange
    order_repository.add_order(sample_order)
    
    # Act
    success, message = pay_order_use_case.execute(order_id=1)
    
    # Assert
    assert success is True
    assert "successfully paid" in message
    assert sample_order.status == OrderStatus.PAID

def test_payment_empty_order_fails(pay_order_use_case, order_repository):
    """Тест ошибки при оплате пустого заказа"""
    # Arrange
    order = Order(id=1, customer_id=100)
    order_repository.add_order(order)
    
    # Act
    success, message = pay_order_use_case.execute(order_id=1)
    
    # Assert
    assert success is False
    assert "empty" in message.lower() or "cannot pay" in message.lower()
    assert order.status == OrderStatus.PENDING

def test_double_payment_fails(pay_order_use_case, order_repository, sample_order):
    """Тест ошибки при повторной оплате"""
    # Arrange
    order_repository.add_order(sample_order)
    
    # Первая оплата
    success1, _ = pay_order_use_case.execute(order_id=1)
    assert success1 is True
    
    # Act: Вторая попытка
    success2, message = pay_order_use_case.execute(order_id=1)
    
    # Assert
    assert success2 is False
    assert "already paid" in message.lower()

def test_cannot_modify_after_payment():
    """Тест невозможности изменения заказа после оплаты"""
    # Arrange
    order = Order(id=1, customer_id=100)
    order.add_line("Item", 1, Money(1000_00))
    order.pay()
    
    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        order.add_line("Another Item", 1, Money(500_00))
    
    assert "modify" in str(exc_info.value).lower() or "paid" in str(exc_info.value).lower()

def test_correct_total_calculation():
    """Тест корректного расчёта итоговой суммы"""
    # Arrange
    order = Order(id=1, customer_id=100)
    
    # Добавляем несколько строк
    order.add_line("Product A", 2, Money(100_00))
    order.add_line("Product B", 3, Money(50_00))
    order.add_line("Product A", 1, Money(100_00))
    
    # Act
    total = order.total_amount
    
    # Assert
    assert total.amount == 450_00
    assert len(order.lines) == 2

def test_payment_gateway_failure():
    """Тест обработки отказа платежного шлюза"""
    # Arrange
    from infrastructure.payment_gateways import FakePaymentGateway
    from infrastructure.repositories import InMemoryOrderRepository
    from application.use_cases import PayOrderUseCase
    
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway(fail_mode=True)
    use_case = PayOrderUseCase(repo, gateway)
    
    order = Order(id=1, customer_id=100)
    order.add_line("Product", 1, Money(1000_00))
    repo.add_order(order)
    
    # Act
    success, message = use_case.execute(order_id=1)
    
    # Assert
    assert success is False
    assert "declined" in message or "gateway" in message
    assert order.status == OrderStatus.PENDING
