import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from collections import defaultdict
import os

# Подключение к базе данных
db_path = 'database.db'
if not os.path.exists(db_path):
    print(f"Ошибка: файл {db_path} не найден!")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Получаем данные о заказах в разрезе дат и пола пользователей
print("Загрузка данных временных рядов...")
cursor.execute('''
SELECT date(o.order_date) as order_date, u.gender, COUNT(*) as order_count
FROM Orders o
JOIN Users u ON o.user_id = u.id
GROUP BY date(o.order_date), u.gender
ORDER BY date(o.order_date)
''')
data = cursor.fetchall()

if not data:
    print("Данные для анализа отсутствуют!")
    exit(1)

# 2. Группируем данные по датам
print("Обработка данных...")
dates = sorted(set([row[0] for row in data]))
female = {date: 0 for date in dates}
male = {date: 0 for date in dates}

for date, gender, count in data:
    if gender == 'Female':
        female[date] = count
    else:
        # Считаем Male и Other вместе или только Male как в листинге
        male[date] = count

# 3. Подготовка данных для расчета трендов
x = list(range(len(dates)))
y_female = [female[date] for date in dates]
y_male = [male[date] for date in dates]

# 4. Расчет трендов (линейная регрессия 1-й степени)
print("Расчет линий тренда...")
trend_female = np.polyfit(x, y_female, 1)
trend_male = np.polyfit(x, y_male, 1)
line_female = np.poly1d(trend_female)(x)
line_male = np.poly1d(trend_male)(x)

# 5. Построение графика
print("Генерация графика трендов...")
date_objects = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
plt.figure(figsize=(12, 6))

# Отрисовка фактических данных
plt.plot(date_objects, y_female, '-', color='pink', label='Женщины (факт)', linewidth=1, alpha=0.5)
plt.plot(date_objects, y_male, '-', color='lightblue', label='Мужчины (факт)', linewidth=1, alpha=0.5)

# Отрисовка линий тренда
plt.plot(date_objects, line_female, '--', color='red', 
         label=f'Тренд женщин (наклон: {trend_female[0]:.3f})', linewidth=2)
plt.plot(date_objects, line_male, '--', color='blue', 
         label=f'Тренд мужчин (наклон: {trend_male[0]:.3f})', linewidth=2)

plt.xlabel('Дата')
plt.ylabel('Количество заказов')
plt.title('Анализ временных рядов: Тренды заказов по полу пользователей')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.xticks(rotation=45)
plt.tight_layout()

# Сохранение результата
output_file = 'order_trends.png'
plt.savefig(output_file, dpi=130)
print(f"График трендов сохранен в файл: {output_file}")

# Вывод коэффициентов в консоль
print(f"\n📈 КОЭФФИЦИЕНТЫ ТРЕНДА")
print(f"-----------------------------------")
print(f"Наклон тренда (женщины): {trend_female[0]:.4f}")
print(f"Наклон тренда (мужчины): {trend_male[0]:.4f}")
print(f"-----------------------------------")

conn.close()
