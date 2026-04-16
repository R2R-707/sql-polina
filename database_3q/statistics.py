import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
import os

# Подключение к базе данных
db_path = 'database.db'
if not os.path.exists(db_path):
    print(f"Ошибка: файл {db_path} не найден!")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Получаем возрасты пользователей
print("Загрузка данных о возрасте пользователей...")
cursor.execute("SELECT age FROM Users WHERE age IS NOT NULL")
ages = [row[0] for row in cursor.fetchall()]

if not ages:
    print("Таблица Users пуста или не содержит данных о возрасте!")
    exit(1)

# 2. Математическое ожидание (среднее)
mean = sum(ages) / len(ages)

# 3. Дисперсия
variance = sum((x - mean) ** 2 for x in ages) / len(ages)

# 4. Стандартное отклонение
std_dev = sqrt(variance)

# Вывод статистики в консоль
print(f"\n📈 СТАТИСТИКА ВОЗРАСТА")
print(f"-----------------------------------")
print(f"Математическое ожидание (средний возраст): {mean:.2f}")
print(f"Дисперсия: {variance:.2f}")
print(f"Стандартное отклонение: {std_dev:.2f}")
print(f"Минимальный возраст: {min(ages)}")
print(f"Максимальный возраст: {max(ages)}")
print(f"-----------------------------------")

# 5. Построение гистограммы
print("Генерация гистограммы...")
plt.figure(figsize=(10, 6))
# Делаем распределение более наглядным с помощью bins
plt.hist(ages, bins=15, edgecolor='black', alpha=0.7, color='green', label='Количество пользователей')
plt.xlabel('Возраст (лет)')
plt.ylabel('Частота (количество человек)')
plt.title('Гистограмма распределения возраста пользователей')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.3)

# Сохраняем график вместо отображения (plt.show() заменен на savefig)
output_file = 'age_distribution.png'
plt.savefig(output_file, dpi=150)
print(f"График сохранен в файл: {output_file}")

conn.close()
