import pytest
from infrastructure.repositories import InMemoryOrderRepository
from infrastructure.payment_gateways import FakePaymentGateway
from application.use_cases import PayOrderUseCase
from domain.entities import Order, OrderStatus
from domain.value_objects import Money

@pytest.fixture
def order_repository():
    return InMemoryOrderRepository()

@pytest.fixture
def payment_gateway():
    return FakePaymentGateway()

@pytest.fixture
def pay_order_use_case(order_repository, payment_gateway):
    return PayOrderUseCase(order_repository, payment_gateway)

@pytest.fixture
def sample_order():
    order = Order(id=1, customer_id=100)
    # ИЗМЕНИТЕ СУММЫ чтобы было меньше 10000 рублей!
    order.add_line("Laptop", 1, Money(5000_00))   # 5000 рублей вместо 50000
    order.add_line("Mouse", 2, Money(500_00))     # 500 рублей вместо 1500
    # Итого: 5000 + 1000 = 6000 рублей < 10000 рублей
    return order
