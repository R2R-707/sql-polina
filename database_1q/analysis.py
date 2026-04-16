import sqlite3
import os

# Путь к базе данных
db_path = 'database.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def run_query(title, query):
    print(f"\n✅ {title}")
    cursor.execute(query)
    
    # Получаем названия столбцов
    columns = [description[0] for description in cursor.description]
    header = " | ".join(columns)
    print(header)
    print("-" * len(header))
    
    # Получаем данные
    rows = cursor.fetchall()
    for row in rows:
        print(" | ".join(map(str, row)))

# ЗАПРОС 1: Список всех профессий и средняя зарплата в каждой
run_query("Средняя зарплата по профессиям", """
    SELECT profession, ROUND(AVG(salary), 2) as avg_salary, COUNT(*) as people_count
    FROM Users 
    GROUP BY profession 
    ORDER BY avg_salary DESC
""")

# ЗАПРОС 2: Общая сумма выручки по категориям (условно разделим товары по цене)
run_query("Выручка от дорогих товаров (> 20 000)", """
    SELECT SUM(p.price) 
    FROM Orders o 
    JOIN Products p ON o.product_id = p.id 
    WHERE p.price > 20000
""")

# ЗАПРОС 3: Сколько заказов сделал каждый город
run_query("Активность городов (количество заказов)", """
    SELECT u.city, COUNT(o.id) as orders_count
    FROM Orders o
    JOIN Users u ON o.user_id = u.id
    GROUP BY u.city
    ORDER BY orders_count DESC
""")

# ЗАПРОС 4: Пользователи, которые зарегистрировались в 2025 году и уже что-то купили
run_query("Пользователи-новички с заказами", """
    SELECT DISTINCT u.first_name, u.last_name, u.registration_date
    FROM Users u
    JOIN Orders o ON u.id = o.user_id
    WHERE u.registration_date LIKE '2025%'
    LIMIT 10
""")

# ЗАПРОС 5: Самый дорогой заказ (информация о пользователе и товаре)
run_query("Самый дорогой проданный товар", """
    SELECT u.first_name, u.last_name, p.name, p.price
    FROM Orders o
    JOIN Users u ON o.user_id = u.id
    JOIN Products p ON o.product_id = p.id
    ORDER BY p.price DESC
    LIMIT 1
""")

conn.close()
