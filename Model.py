import sqlite3

class Model():
    ALLOWED_TABLES = {"estates_raw", "estates_final"}
    DB_NAME = "city24.db"

    def __init__(self):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estates_raw
            (
                id INTEGER PRIMARY KEY,
                address TEXT,
                price INTEGER,
                price_per_unit REAL,
                property_size REAL,
                room_count INTEGER,
                date_published TEXT,
                is_sold INTEGER DEFAULT 0
            )
        """)

        conn.commit()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estates_final
            (
                id INTEGER PRIMARY KEY,
                address TEXT,
                price INTEGER,
                price_per_unit REAL,
                property_size REAL,
                room_count INTEGER,
                date_published TEXT,
                is_sold INTEGER DEFAULT 0
            )
        """)

        conn.commit()

        conn.close()
    
    def validate_table_name(self: Model, table_name: str) -> None:
        if (table_name not in self.ALLOWED_TABLES):
            raise ValueError("Invalid table name:" + table_name)

    def insert_multiple(self: Model, data: list, table_name: str) -> None:
        self.validate_table_name(table_name)

        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        for estate in data:
            try:
                cursor.execute(f"""
                    INSERT INTO {table_name} (id, address, price, price_per_unit, property_size, room_count, date_published, is_sold)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, estate)
            except sqlite3.IntegrityError as error:
                print(data, error)
        
        conn.commit()
        conn.close()
    
    def insert(self: Model, data: tuple, table_name: str) -> None:
        self.validate_table_name(table_name)
        
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        try:
            cursor.execute(f"""
                INSERT INTO {table_name} (id, address, price, price_per_unit, property_size, room_count, date_published, is_sold)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
        except sqlite3.IntegrityError as error:
            print(data, error)
        
        conn.commit()
        conn.close()
    
    def get_all(self: Model, table_name: str) -> list:
        self.validate_table_name(table_name)

        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT * FROM {table_name}
        """)

        data = cursor.fetchall()

        conn.close()

        return data

    def update_sold_status(self: Model) -> None:
        estates_raw = "estates_raw"
        estates_final = "estates_final"

        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT * FROM {estates_final}
            EXCEPT
            SELECT * FROM {estates_raw}
        """)

        data = cursor.fetchall()

        for estate in data:
            estate_id = estate[0]
            cursor.execute(f"""
                UPDATE {estates_final}
                SET is_sold = 1
                WHERE id = ?
            """, (estate_id, ))
            conn.commit()

        conn.close()
    
    def delete_all(self: Model, table_name: str) -> None:
        self.validate_table_name(table_name)
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f"""
            DELETE FROM {table_name}
        """)

        conn.close()