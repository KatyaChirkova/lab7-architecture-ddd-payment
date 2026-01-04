# Лабораторная работа 7 - Создание структуры проекта
Write-Host "Создаем структуру для лабораторной работы..." -ForegroundColor Green

# 1. Создаем папки
$folders = @("domain", "application", "infrastructure", "tests")
foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Name $folder -Force
        Write-Host "Создана папка: $folder" -ForegroundColor Cyan
    }
}

# 2. Функция для создания файлов с содержимым
function Create-File {
    param($path, $content)
    Set-Content -Path $path -Value $content -Encoding UTF8
    Write-Host "Создан файл: $path" -ForegroundColor Yellow
}

# 3. Создаем файлы DOMAIN слоя
Create-File "domain\__init__.py" "# Domain layer package"
Create-File "domain\entities.py" "# Domain entities: Order, OrderLine"
Create-File "domain\value_objects.py" "# Value objects: Money"
Create-File "domain\exceptions.py" "# Domain exceptions"

# 4. Создаем файлы APPLICATION слоя
Create-File "application\__init__.py" "# Application layer package"
Create-File "application\use_cases.py" "# Use cases: PayOrderUseCase"
Create-File "application\interfaces.py" "# Interfaces: OrderRepository, PaymentGateway"

# 5. Создаем файлы INFRASTRUCTURE слоя
Create-File "infrastructure\__init__.py" "# Infrastructure layer package"
Create-File "infrastructure\repositories.py" "# Repository implementations"
Create-File "infrastructure\payment_gateways.py" "# Payment gateway implementations"

# 6. Создаем файлы TESTS
Create-File "tests\__init__.py" "# Tests package"
Create-File "tests\conftest.py" "# Test fixtures"
Create-File "tests\test_use_cases.py" "# Use cases tests"

# 7. Создаем вспомогательные файлы
Create-File "README.md" @"
# Лабораторная работа 7: Архитектура, слои и DDD-lite

## Система оплаты заказа

### Структура проекта:
- \`domain/\` - доменная модель и бизнес-правила
- \`application/\` - use-case слой  
- \`infrastructure/\` - реализации интерфейсов
- \`tests/\` - тесты use-case без базы данных

### Запуск тестов:
\`\`\`bash
pytest tests/
\`\`\`

### Требования:
\`\`\`bash
pip install pytest
\`\`\`
"@

Create-File "requirements.txt" "pytest"

Create-File "demo.py" @"
#!/usr/bin/env python3
"""Демонстрация работы системы оплаты"""

print("Payment System Lab")
print("Структура проекта создана!")
"@

Create-File ".gitignore" @"
# Python
__pycache__/
*.py[cod]
*.pyc
.python-version

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
htmlcov/
.pytest_cache/
"@

Write-Host "`nСтруктура проекта успешно создана!" -ForegroundColor Green
Write-Host "Файлы готовы к заполнению кодом." -ForegroundColor Green
