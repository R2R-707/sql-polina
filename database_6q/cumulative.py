import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Подключение к базе данных
db_path = 'database.db'
if not os.path.exists(db_path):
    print(f"Ошибка: файл {db_path} не найден!")
    exit(1)

conn = sqlite3.connect(db_path)

# SQL запрос для когортного анализа (накопительный итог)
print("Выполнение SQL запроса для накопительного анализа...")
query = """
WITH user_cohorts AS (
    -- Определяем когорту для каждого пользователя (месяц регистрации)
    SELECT 
        id as user_id,
        STRFTIME('%Y-%m', registration_date) as cohort_month
    FROM Users
),
user_orders AS (
    -- Все заказы с информацией о когорте
    SELECT 
        uc.cohort_month,
        o.id as order_id,
        -- Номер месяца от регистрации (0, 1, 2, ...)
        (STRFTIME('%Y', o.order_date) - STRFTIME('%Y', uc.cohort_month || '-01')) * 12 +
        (STRFTIME('%m', o.order_date) - STRFTIME('%m', uc.cohort_month || '-01')) as month_from_reg
    FROM user_cohorts uc
    JOIN Orders o ON uc.user_id = o.user_id
    WHERE o.order_date IS NOT NULL
)
-- Считаем накопительные заказы для каждой когорты
SELECT 
    cohort_month,
    month_from_reg,
    COUNT(order_id) as orders_in_month,
    SUM(COUNT(order_id)) OVER (PARTITION BY cohort_month ORDER BY month_from_reg) as cumulative_orders
FROM user_orders
GROUP BY cohort_month, month_from_reg
ORDER BY cohort_month, month_from_reg
"""

# Выполняем запрос
df = pd.read_sql_query(query, conn)
conn.close()

print("\n📊 ДАННЫЕ НАКОПЛЕНИЯ (Первые 10 строк):")
print(df.head(10))

# графически отобразим динамику накопления заказов по когортам
print("\nГенерация графика накопительного итога...")
plt.figure(figsize=(14, 8))

# Разные цвета и маркеры для разных когорт
cohorts = sorted(df['cohort_month'].unique())
colors = plt.cm.tab10(np.linspace(0, 1, len(cohorts)))
markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h']

for i, cohort in enumerate(cohorts):
    cohort_data = df[df['cohort_month'] == cohort]
    plt.plot(cohort_data['month_from_reg'], cohort_data['cumulative_orders'], 
             marker=markers[i % len(markers)], label=f'Когорта {cohort}', 
             color=colors[i], linewidth=2)

plt.xlabel('Месяцев после регистрации')
plt.ylabel('Суммарное количество заказов (накопление)')
plt.title('Накопительный итог заказов по когортам (LTV-ориентированный анализ)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

output_file = 'cumulative_orders.png'
plt.savefig(output_file, dpi=130)
print(f"График накопительного итога сохранен в файл: {output_file}")
