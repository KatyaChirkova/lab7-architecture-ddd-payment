import pytest
from infrastructure.repositories import InMemoryOrderRepository
from infrastructure.payment_gateways import FakePaymentGateway
from application.use_cases import PayOrderUseCase
from domain.entities import Order, OrderStatus
from domain.value_objects import Money

@pytest.fixture
def order_repository():
    """Фикстура репозитория"""
    return InMemoryOrderRepository()

@pytest.fixture
def payment_gateway():
    """Фикстура платежного шлюза"""
    return FakePaymentGateway()

@pytest.fixture
def pay_order_use_case(order_repository, payment_gateway):
    """Фикстура use case"""
    return PayOrderUseCase(order_repository, payment_gateway)

@pytest.fixture
def sample_order():
    """Фикстура тестового заказа"""
    order = Order(id=1, customer_id=100)
    order.add_line("Laptop", 1, Money(50000_00))
    order.add_line("Mouse", 2, Money(1500_00))
    return order
