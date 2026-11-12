import os
import pymysql
from dotenv import load_dotenv

# 1. 读取你的 .env 配置
load_dotenv()

# 2. 连接 MySQL
try:
    conn = pymysql.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"), # 这里要确保你已经建好了 finance_db 这个库
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    print("✅ 成功连接到 MySQL 数据库！")

    # 3. 建表：公司财务表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS company_finance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        stock_code VARCHAR(10),
        company_name VARCHAR(50),
        report_date VARCHAR(20),
        total_revenue DECIMAL(15,2),  -- 单位：亿元
        net_profit DECIMAL(15,2)      -- 单位：亿元
    )
    """)
    print("✅ 数据表 company_finance 已就绪。")

    # 4. 插入真实财报数据（这里用比亚迪的真实数据，单位：亿元）
    # 先清空一下旧数据，防止重复插入
    cursor.execute("TRUNCATE TABLE company_finance")
    
    data = [
        ('002594', '比亚迪', '2023-12-31', 6023.15, 300.40),
        ('002594', '比亚迪', '2024-12-31', 7771.00, 402.54),
        ('002594', '比亚迪', '2025-12-31', 8039.64, 326.19), # 对应你刚才报告里的数据
        ('002594', '比亚迪', '2026-06-30', 3448.00, 123.30),
    ]
    
    insert_sql = "INSERT INTO company_finance (stock_code, company_name, report_date, total_revenue, net_profit) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(insert_sql, data)
    conn.commit()
    print(f"✅ 成功插入了 {cursor.rowcount} 条财务数据！")

except Exception as e:
    print(f"❌ 出错了：{e}")
finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()
    