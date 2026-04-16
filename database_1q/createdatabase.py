import sqlite3
import os

# Создаем папку database, если ее нет
if not os.path.exists('database'):
    os.makedirs('database')

# Переходим в папку database, чтобы файл создался там, 
# либо просто указываем путь. В листинге указано просто 'database.db'.
# Если запустить скрипт ИЗ папки database, файл ляжет рядом.
db_path = os.path.join('database', 'database.db')

# Подключение к базе данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Создание таблицы Users (Пользователи)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age INTEGER,
    gender TEXT CHECK(gender IN ('Male', 'Female', 'Other')),
    profession TEXT,
    salary REAL,
    city TEXT,
    registration_date DATE DEFAULT CURRENT_DATE
)
''')

# 2. Создание таблицы Products (Продукты)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER DEFAULT 0,
    expiration_date DATE
)
''')

# 3. Создание таблицы Orders (Заказы)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(id) ON DELETE CASCADE
)
''')

# Подтверждаем изменения
conn.commit()

# Закрываем соединение
conn.close()

print(f"База данных и таблицы успешно созданы в файле {db_path}")
