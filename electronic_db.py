import sqlite3
import random

class ElectronicDB:
    def __init__(self, db_name="electronic.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    price INTEGER NOT NULL
                )
            """)

    def insert_product(self, product_id, name, price):
        with self.conn:
            self.conn.execute(
                "INSERT INTO products (id, name, price) VALUES (?, ?, ?)",
                (product_id, name, price)
            )

    def update_product(self, product_id, name=None, price=None):
        with self.conn:
            if name and price is not None:
                self.conn.execute(
                    "UPDATE products SET name=?, price=? WHERE id=?",
                    (name, price, product_id)
                )
            elif name:
                self.conn.execute(
                    "UPDATE products SET name=? WHERE id=?",
                    (name, product_id)
                )
            elif price is not None:
                self.conn.execute(
                    "UPDATE products SET price=? WHERE id=?",
                    (price, product_id)
                )

    def delete_product(self, product_id):
        with self.conn:
            self.conn.execute(
                "DELETE FROM products WHERE id=?",
                (product_id,)
            )

    def select_products(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, price FROM products")
        return cursor.fetchall()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = ElectronicDB()
    # 샘플 데이터 100개 삽입
    for i in range(1, 101):
        name = f"전자제품_{i}"
        price = random.randint(10000, 1000000)
        db.insert_product(i, name, price)

    # 데이터 조회 예시
    products = db.select_products()
    for p in products[:5]:  # 처음 5개만 출력
        print(p)