import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# 1. Создание таблицы Message
print("Создание таблицы Message...")
cursor.execute('''
CREATE TABLE IF NOT EXISTS Message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    message_text TEXT NOT NULL
)
''')

# 2. Добавление столбца status (с проверкой на существование)
try:
    print("Добавление столбца status...")
    cursor.execute('''
    ALTER TABLE Message
    ADD COLUMN status TEXT DEFAULT 'active'
    ''')
except sqlite3.OperationalError:
    print("Столбец status уже существует.")

# 3. Добавление столбца rating (с проверкой на существование)
try:
    print("Добавление столбца rating...")
    cursor.execute('''
    ALTER TABLE Message
    ADD COLUMN rating INTEGER DEFAULT 5
    ''')
except sqlite3.OperationalError:
    print("Столбец rating уже существует.")

# 4. Получение продуктов
print("Получение данных из Products...")
cursor.execute("SELECT id, name FROM Products")
products = cursor.fetchall()
print("Доступные продукты:", products)

# 5. Подготовка данных для вставки
message_data = [
    (1, "Отличный, рекомендую к покупке!", 'active', 5),
    (2, "Хорошее качество, быстрая доставка.", 'inactive', 4),
    (3, "Средненький, ожидал лучшего качества.", 'moderated', 3),
    (4, "Отличное соотношение цены и качества. Очень доволен!", 'moderated', 4),
    (5, "Неплохой, но есть небольшие недостатки.", 'active', 4)
]

# 6. Вставка данных
print("Вставка сообщений...")
cursor.executemany('''
INSERT INTO Message (product_id, message_text, status, rating)
VALUES (?, ?, ?, ?)
''', message_data)

# 7. SQL запрос SELECT с JOIN
print("\nРезультаты начального запроса (JOIN Message + Products):")
cursor.execute('''
SELECT
    m.id,
    p.name AS product_name,
    m.message_text,
    m.rating,
    m.status
FROM Message m
JOIN Products p ON m.product_id = p.id
ORDER BY m.rating DESC
''')

rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Продукт: {row[1]}, Отзыв: {row[2]}, Рейтинг: {row[3]}, Статус: {row[4]}")

# 8. SQL запрос UPDATE
print("\nОбновление данных (UPDATE)...")
cursor.execute("UPDATE Message SET status = 'approved' WHERE rating >= 4")
print(f"Обновлено строк: {cursor.rowcount}")

# 9. SQL запрос DELETE
print("\nУдаление данных (DELETE)...")
cursor.execute("DELETE FROM Message WHERE status = 'inactive'")
print(f"Удалено строк: {cursor.rowcount}")

# 10. Проверка после изменений
print("\nСостояние таблицы после UPDATE и DELETE:")
cursor.execute('''
SELECT m.id, p.name, m.status, m.rating 
FROM Message m 
JOIN Products p ON m.product_id = p.id
''')
for row in cursor.fetchall():
    print(row)

# 11. DROP TABLE (раскомментируйте, если нужно удалить таблицу в конце)
# print("\nУдаление таблицы (DROP)...")
# cursor.execute("DROP TABLE Message")

conn.commit()
conn.close()
print("\nРабота завершена.")
