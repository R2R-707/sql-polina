import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter
import os

# Подключение к базе данных
db_path = 'database.db'
if not os.path.exists(db_path):
    print(f"Ошибка: файл {db_path} не найден!")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Получаем все даты заказов (извлекаем только дату из TIMESTAMP)
print("Загрузка данных о заказах...")
# В SQLite функция date() возвращает строку в формате ИИИИ-ММ-ДД
cursor.execute("SELECT date(order_date) as order_day FROM Orders WHERE order_date IS NOT NULL")
order_days = [row[0] for row in cursor.fetchall()]

if not order_days:
    print("В таблице Orders нет данных о заказах!")
    exit(1)

# 2. Подсчитываем количество заказов в каждый день
daily_counts = Counter(order_days)

# 3. Сортируем даты и получаем соответствующие количества
# Сортировка строковых дат (ИИИИ-ММ-ДД) будет корректной
dates = sorted(daily_counts.keys())
counts = [daily_counts[date] for date in dates]

# Вывод краткой статистики
print(f"\n📊 СТАТИСТИКА ЗАКАЗОВ ВО ВРЕМЕНИ")
print(f"-----------------------------------")
print(f"Период данных: с {min(dates)} по {max(dates)}")
print(f"Всего дней с заказами: {len(dates)}")
print(f"Среднее количество заказов в день: {sum(counts) / len(counts):.2f}")
print(f"Пик заказов в один день: {max(counts)}")
print(f"-----------------------------------")

# 4. Построение графика динамики
print("Генерация графика динамики заказов...")
plt.figure(figsize=(12, 6))
# Используем plt.plot для создания линейного графика
plt.plot(dates, counts, marker='o', linestyle='-', color='blue', linewidth=2, label='Количество заказов')

plt.xlabel('Дата заказа')
plt.ylabel('Количество заказов (шт.)')
plt.title('Динамика количества заказов во времени')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()

# Сохраняем график вместо отображения (plt.show() заменен на savefig)
output_file = 'order_dynamics.png'
plt.savefig(output_file, dpi=120)
print(f"График динамики сохранен в файл: {output_file}")

conn.close()
