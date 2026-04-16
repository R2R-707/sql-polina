import sqlite3
import matplotlib.pyplot as plt
import os

# Подключение к базе данных
db_path = 'database.db'
if not os.path.exists(db_path):
    print(f"Ошибка: файл {db_path} не найден!")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Получаем данные о поле пользователей
print("Загрузка данных о поле пользователей...")
cursor.execute("SELECT gender, COUNT(*) as count FROM Users WHERE gender IS NOT NULL GROUP BY gender")
gender_data = cursor.fetchall()

if not gender_data:
    print("В таблице Users нет данных о поле пользователей!")
    exit(1)

# Формируем списки для графика
labels = [row[0] for row in gender_data]
sizes = [row[1] for row in gender_data]
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99'] # Цветовая палитра

# Вывод статистики в консоль
print(f"\n👥 СООТНОШЕНИЕ ПОЛА")
print(f"-----------------------------------")
for label, count in zip(labels, sizes):
    print(f"{label}: {count}")
print(f"-----------------------------------")

# 2. Построение круговой диаграммы
print("Генерация круговой диаграммы...")
plt.figure(figsize=(8, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors[:len(labels)], shadow=True)

plt.title('Соотношение количества мужчин и женщин среди пользователей')
plt.axis('equal') # Равные пропорции для круга

# Сохраняем график
output_file = 'gender_ratio.png'
plt.savefig(output_file, dpi=120)
print(f"График сохранен в файл: {output_file}")

conn.close()
