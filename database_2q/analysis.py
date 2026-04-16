import sqlite3
import os

# Подключение к базе данных (находимся в папке database_2q)
db_path = 'database.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def run_query(title, query):
    print(f"\n📊 {title}")
    cursor.execute(query)
    
    # Получаем названия столбцов
    if cursor.description:
        columns = [description[0] for description in cursor.description]
        header = " | ".join(columns)
        print(header)
        print("-" * len(header))
        
        # Получаем данные
        rows = cursor.fetchall()
        for row in rows:
            print(" | ".join(map(str, row)))
    else:
        print("Запрос выполнен успешно (без вывода данных).")

# ЗАПРОС 1: Средний рейтинг товаров на основе отзывов
run_query("Средний рейтинг товаров по отзывам", """
    SELECT p.name, ROUND(AVG(m.rating), 1) as avg_rating, COUNT(m.id) as reviews_count
    FROM Products p
    JOIN Message m ON p.id = m.product_id
    GROUP BY p.name
    ORDER BY avg_rating DESC
""")

# ЗАПРОС 2: Статистика отзывов по статусам
run_query("Статистика отзывов по статусам", """
    SELECT status, COUNT(*) as count
    FROM Message
    GROUP BY status
""")

# ЗАПРОС 3: Самые популярные города среди покупателей
run_query("Топ 5 городов по количеству покупок", """
    SELECT u.city, COUNT(o.id) as orders_count
    FROM Orders o
    JOIN Users u ON o.user_id = u.id
    GROUP BY u.city
    ORDER BY orders_count DESC
    LIMIT 5
""")

# ЗАПРОС 4: Общая стоимость всех заказов
run_query("Общая выручка магазина", """
    SELECT SUM(p.price) as total_revenue
    FROM Orders o
    JOIN Products p ON o.product_id = p.id
""")

# ЗАПРОС 5: Продукты без отзывов
run_query("Продукты, на которые еще нет отзывов", """
    SELECT p.name
    FROM Products p
    LEFT JOIN Message m ON p.id = m.product_id
    WHERE m.id IS NULL
    LIMIT 10
""")

conn.close()
print("\nАнализ завершен.")
