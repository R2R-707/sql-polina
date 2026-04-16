import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Проверка наличия seaborn (он лучше для тепловых карт)
try:
    import seaborn as sns
    has_seaborn = True
except ImportError:
    has_seaborn = False

# Подключаемся к базе данных
db_path = 'database.db'
if not os.path.exists(db_path):
    print(f"Ошибка: файл {db_path} не найден!")
    exit(1)

conn = sqlite3.connect(db_path)

# SQL запрос для когортного анализа ( retention )
print("Выполнение SQL запроса для когортного анализа...")
query = """
WITH user_cohorts AS (
    -- Когорты по месяцу регистрации
    SELECT 
        id as user_id,
        STRFTIME('%Y-%m', registration_date) AS cohort_month
    FROM Users
),
user_orders AS (
    -- Заказы с номером месяца от регистрации
    SELECT 
        u.user_id,
        u.cohort_month,
        (STRFTIME('%Y', o.order_date) - STRFTIME('%Y', u.cohort_month || '-01')) * 12 +
        (STRFTIME('%m', o.order_date) - STRFTIME('%m', u.cohort_month || '-01')) AS month_number
    FROM user_cohorts u
    JOIN Orders o ON u.user_id = o.user_id
),
cohort_size AS (
    -- Размер каждой когорты
    SELECT 
        cohort_month,
        COUNT(DISTINCT user_id) AS users_in_cohort
    FROM user_cohorts
    GROUP BY cohort_month
)
-- Результирующая таблица
SELECT 
    uo.cohort_month,
    cs.users_in_cohort,
    uo.month_number,
    COUNT(DISTINCT uo.user_id) AS active_users,
    ROUND(COUNT(DISTINCT uo.user_id) * 100.0 / cs.users_in_cohort, 1) AS retention_rate
FROM user_orders uo
JOIN cohort_size cs ON uo.cohort_month = cs.cohort_month
GROUP BY uo.cohort_month, uo.month_number
ORDER BY uo.cohort_month, uo.month_number
"""

df = pd.read_sql_query(query, conn)

print("\n📊 ДАННЫЕ УДЕРЖАНИЯ (Первые 10 строк):")
print(df.head(10))

# Создаем сводную таблицу (pivot table)
retention_pivot = df.pivot(index='cohort_month', columns='month_number', values='retention_rate')

# Визуализация тепловой карты
print("\nГенерация тепловой карты...")
plt.figure(figsize=(14, 10))
plt.title('Когортный анализ: Удержание пользователей (%)', fontsize=16)

if has_seaborn:
    sns.heatmap(retention_pivot, annot=True, fmt='.1f', cmap='YlGnBu', cbar_kws={'label': 'Retention (%)'})
else:
    # Запасной вариант на чистом matplotlib, если seaborn не установился
    plt.imshow(retention_pivot, cmap='YlGnBu', aspect='auto')
    for i in range(len(retention_pivot.index)):
        for j in range(len(retention_pivot.columns)):
            val = retention_pivot.iloc[i, j]
            if not np.isnan(val):
                plt.text(j, i, f'{val:.1f}', ha='center', va='center')
    plt.colorbar(label='Retention (%)')
    plt.yticks(range(len(retention_pivot.index)), retention_pivot.index)
    plt.xticks(range(len(retention_pivot.columns)), retention_pivot.columns)

plt.ylabel('Месяц регистрации (когорта)')
plt.xlabel('Месяцев после регистрации')
plt.tight_layout()

output_file = 'retention_heatmap.png'
plt.savefig(output_file, dpi=150)
print(f"Тепловая карта сохранена в файл: {output_file}")

conn.close()
