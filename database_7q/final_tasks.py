import sqlite3
import os

# Подключение к базе данных в текущей директории
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("🚀 ЗАПУСК ИТОГОВЫХ ЗАДАЧ (ЛАБОРАТОРНАЯ №7)\n")

# --- ЗАДАЧА 1: Подсчет по полу и окончаниям фамилий ---
print("-" * 50)
print("ЗАДАЧА 1: Статистика по полу и фамилиям")
cursor.execute("SELECT gender, COUNT(*) FROM Users WHERE gender IS NOT NULL GROUP BY gender")
for row in cursor.fetchall():
    print(f" Пол {row[0]}: {row[1]} чел.")

cursor.execute("SELECT COUNT(*) FROM Users WHERE last_name LIKE '%ов'")
count_ov = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM Users WHERE last_name LIKE '%ова'")
count_ova = cursor.fetchone()[0]
print(f" Фамилии, заканчивающиеся на 'ов': {count_ov}")
print(f" Фамилии, заканчивающиеся на 'ова': {count_ova}")

# --- ЗАДАЧА 2: Города с буквой 'а' ---
print("\n" + "-" * 50)
print("ЗАДАЧА 2: Города, содержащие букву 'а'")
cursor.execute("SELECT DISTINCT city FROM Users WHERE city LIKE '%а%'")
cities = cursor.fetchall()
print(f" Найдено городов: {len(cities)}")
print(f" Примеры: {', '.join([c[0] for c in cities[:10]])}")

# --- ЗАДАЧА 3: Смена регистра первого символа профессии ---
print("\n" + "-" * 50)
print("ЗАДАЧА 3: Инверсия регистра первой буквы профессии")
cursor.execute("SELECT id, profession FROM Users WHERE profession IS NOT NULL LIMIT 5")
professions = cursor.fetchall()
for pid, prof in professions:
    if prof:
        # Инвертируем регистр первой буквы
        new_prof = prof[0].swapcase() + prof[1:]
        print(f" {prof} -> {new_prof}")
        cursor.execute("UPDATE Users SET profession = ? WHERE id = ?", (new_prof, pid))

# --- ЗАДАЧА 4: Смена фамилий пользователей ---
print("\n" + "-" * 50)
print("ЗАДАЧА 4: Смена фамилий у нескольких пользователей")
updates = [
    (1, "Волков"),
    (3, "Лебедева"),
    (5, "Тихонов")
]
for uid, new_last in updates:
    cursor.execute("UPDATE Users SET last_name = ? WHERE id = ?", (new_last, uid))
    print(f" Пользователю ID {uid} назначена новая фамилия: {new_last}")

# --- ЗАДАЧА 5: Продукты по окончаниям ---
print("\n" + "-" * 50)
print("ЗАДАЧА 5: Продукты по типам окончаний (гласная/согласная)")
vowels = "аеёиоуыэюя"
cursor.execute("SELECT name FROM Products")
products = [p[0] for p in cursor.fetchall()]

on_vowel = [p for p in products if p and p[-1].lower() in vowels]
on_consonant = [p for p in products if p and p[-1].lower() not in vowels and p[-1].isalpha()]

print(f" На гласную ({len(on_vowel)} шт.): {', '.join(on_vowel[:7])}...")
print(f" На согласную ({len(on_consonant)} шт.): {', '.join(on_consonant[:7])}...")

# --- ЗАДАЧА 6: Формат Фамилия И. ---
print("\n" + "-" * 50)
print("ЗАДАЧА 6: Вывод в формате 'Фамилия И.'")
cursor.execute("SELECT last_name, first_name FROM Users LIMIT 15")
for last, first in cursor.fetchall():
    print(f" {last} {first[0]}.")

conn.commit()
conn.close()
print("\n" + "=" * 50)
print("✅ ВСЕ ЗАДАНИЯ УСПЕШНО ВЫПОЛНЕНЫ И СОХРАНЕНЫ В БД")
