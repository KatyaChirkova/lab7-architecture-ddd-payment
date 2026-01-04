print("=== Проверка тестовой логики ===")

from domain.entities import Order, OrderStatus
from domain.value_objects import Money
from infrastructure.repositories import InMemoryOrderRepository
from infrastructure.payment_gateways import FakePaymentGateway
from application.use_cases import PayOrderUseCase

# 1. Создаем заказ как в conftest.py
order = Order(id=1, customer_id=100)
order.add_line("Laptop", 1, Money(50000_00))
order.add_line("Mouse", 2, Money(1500_00))
print(f"1. Заказ создан: id={order.id}, статус={order.status}, строк={len(order.lines)}")

# 2. Создаем use case
repo = InMemoryOrderRepository()
gateway = FakePaymentGateway()
use_case = PayOrderUseCase(repo, gateway)

# 3. Сохраняем заказ
repo.save(order)
print(f"2. Заказ сохранен в репозитории")

# 4. Пытаемся оплатить
print(f"3. Пытаемся оплатить...")
success, message = use_case.execute(order_id=1)
print(f"   Результат: success={success}, message='{message}'")
print(f"   Статус заказа: {order.status}")

# 5. Проверяем лог платежей
print(f"4. Лог платежного шлюза: {gateway.charges_log}")

print("=== Проверка завершена ===")
