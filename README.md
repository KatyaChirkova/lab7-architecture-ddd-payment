# Лабораторная работа 7: Архитектура, слои и DDD-lite

## Система оплаты заказа

### Структура проекта:
- \domain/\ - доменная модель и бизнес-правила
- \pplication/\ - use-case слой  
- \infrastructure/\ - реализации интерфейсов
- \	ests/\ - тесты use-case без базы данных

### Запуск тестов:
\\\ash
pytest tests/
\\\

### Требования:
\\\ash
pip install pytest
\\\
"@

Create-File "requirements.txt" "pytest"

Create-File "demo.py" @"
#!/usr/bin/env python3
"""Демонстрация работы системы оплаты"""

print("Payment System Lab")
print("Структура проекта создана!")
