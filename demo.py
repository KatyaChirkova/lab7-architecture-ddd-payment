#!/usr/bin/env python3
"""Демонстрация работы системы оплаты заказа"""

from domain.entities import Order
from domain.value_objects import Money
from infrastructure.repositories import InMemoryOrderRepository
from infrastructure.payment_gateways import FakePaymentGateway
from application.use_cases import PayOrderUseCase

def main():
    """Основная функция демонстрации"""
    print("=== Демонстрация системы оплаты заказа ===\n")
    
    # 1. Инициализируем зависимости
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway()
    use_case = PayOrderUseCase(repo, gateway)
    
    # 2. Создаем заказ
    order = Order(id=1, customer_id=123)
    order.add_line("Python Book", 2, Money(1500_00))
    order.add_line("Coffee Mug", 1, Money(800_00))
    
    # 3. Сохраняем заказ
    repo.save(order)
    print(f"Создан заказ #{order.id}")
    print(f"Клиент: {order.customer_id}")
    print(f"Сумма: {order.total_amount}")
    print(f"Статус: {order.status.value}")
    
    print("\n" + "="*50 + "\n")
    
    # 4. Пытаемся оплатить
    print("Попытка оплаты заказа...")
    success, message = use_case.execute(order_id=1)
    print(f"Результат: {message}")
    print(f"Статус после оплаты: {order.status.value}")
    
    print("\n" + "="*50 + "\n")
    
    # 5. Пытаемся оплатить повторно
    print("Попытка повторной оплаты...")
    success, message = use_case.execute(order_id=1)
    print(f"Результат: {message}")
    
    print("\n=== Демонстрация завершена ===")

if __name__ == "__main__":
    main()
