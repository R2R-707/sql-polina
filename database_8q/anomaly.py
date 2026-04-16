import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# Подключение к базе данных
db_path = 'database.db'
if not os.path.exists(db_path):
    print(f"Ошибка: файл {db_path} не найден!")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Загрузка данных о зарплатах
print("Загрузка данных пользователей...")
cursor.execute("SELECT id, first_name, last_name, profession, salary FROM Users WHERE salary IS NOT NULL")
users = cursor.fetchall()

salaries = [user[4] for user in users]

if not salaries:
    print("Данные о зарплатах отсутствуют!")
    exit(1)

# 2. Расчет межквартильного размаха (IQR) для поиска аномалий
Q1 = np.percentile(salaries, 25)
Q3 = np.percentile(salaries, 75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# 3. Выявление аномалий
low_anomalies = [user for user in users if user[4] < lower_bound]
high_anomalies = [user for user in users if user[4] > upper_bound]

# Вывод результатов в консоль
print(f"\n📊 СТАТИСТИКА ЗАРПЛАТ")
print(f"-----------------------------------")
print(f"Q1 (25%): {Q1:,.0f} руб.")
print(f"Q3 (75%): {Q3:,.0f} руб.")
print(f"IQR: {IQR:,.0f} руб.")
print(f"Нижний порог аномалий: {lower_bound:,.0f} руб.")
print(f"Верхний порог аномалий: {upper_bound:,.0f} руб.")
print(f"-----------------------------------")
print(f"Выявлено аномально низких: {len(low_anomalies)}")
print(f"Выявлено аномально высоких: {len(high_anomalies)}")

if high_anomalies:
    print("\n⚠️ СПИСОК ВЫСОКООПЛАЧИВАЕМЫХ АНОМАЛИЙ:")
    for a in high_anomalies[:5]:
        print(f"  ID {a[0]}: {a[1]} {a[2]} ({a[3]}) - {a[4]:,.0f} руб.")

# 4. Визуализация гистограммы с выделением аномальных зон
print("\nГенерация гистограммы аномалий...")
plt.figure(figsize=(12, 7))
n, bins, patches = plt.hist(salaries, bins=25, alpha=0.7, color='skyblue', edgecolor='black')

# Подсвечиваем аномальные области (те, что за пределами границ)
for i in range(len(patches)):
    if bins[i] < lower_bound or bins[i] > upper_bound:
        patches[i].set_facecolor('red')
        patches[i].set_alpha(0.5)

# Добавляем вертикальные линии для границ
plt.axvline(lower_bound, color='red', linestyle='--', linewidth=2, label=f'Нижняя граница ({lower_bound:,.0f})')
plt.axvline(upper_bound, color='red', linestyle='--', linewidth=2, label=f'Верхняя граница ({upper_bound:,.0f})')
plt.axvline(Q1, color='orange', linestyle=':', linewidth=2, label=f'Q1 ({Q1:,.0f})')
plt.axvline(Q3, color='orange', linestyle=':', linewidth=2, label=f'Q3 ({Q3:,.0f})')
plt.axvline(np.median(salaries), color='green', linestyle='-', linewidth=2, label=f'Медиана ({np.median(salaries):,.0f})')

plt.xlabel('Зарплата (руб.)')
plt.ylabel('Количество сотрудников')
plt.title('Распределение зарплат и выявление выбросов (аномалий)')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()

output_file = 'salary_anomalies.png'
plt.savefig(output_file, dpi=130)
print(f"График сохранен в файл: {output_file}")

conn.close()
