import sqlite3

class Model():
    ALLOWED_TABLES = {"estates_raw", "estates_final"}
    DB_NAME = "city24.db"

    def __init__(self):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        # TODO Add floor column
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
                link TEXT,
                is_sold INTEGER DEFAULT 0,
                date_sold TEXT DEFAULT NULL
            )
        """)

        conn.commit()

        # TODO Add floor column
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
                link TEXT,
                is_sold INTEGER DEFAULT 0,
                date_sold TEXT DEFAULT NULL
            )
        """)

        conn.commit()

        conn.close()
    
    def validate_table_name(self, table_name: str) -> None:
        if (table_name not in self.ALLOWED_TABLES):
            raise ValueError("Invalid table name:" + table_name)

    def disconnect(self, conn: sqlite3.Connection) -> None:
        conn.commit()
        conn.close()

    def get_column_names(self) -> list:
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM estates_final LIMIT 0")
        columns = [desc[0] for desc in cursor.description]

        self.disconnect(conn)

        return columns

    # WIP
    # def execute(self, sql: str) -> list:
    #     conn = sqlite3.connect(self.DB_NAME)
    #     cursor = conn.cursor()

    #     cursor.execute(f"""{sql}""")

    #     data = cursor.fetchall()

    #     self.disconnect(conn)

    #     return data

    def insert_multiple(self, data: list, table_name: str) -> None:
        self.validate_table_name(table_name)

        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        for estate in data:
            try:
                cursor.execute(f"""
                    INSERT INTO {table_name} (id, address, price, price_per_unit, property_size, room_count, date_published, link, is_sold, date_sold)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, estate)
            except sqlite3.IntegrityError as error:
                pass
        
        self.disconnect(conn)
    
    def insert(self, data: tuple, where: str) -> None:
        self.validate_table_name(where)
        
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        try:
            cursor.execute(f"""
                INSERT INTO {where} (id, address, price, price_per_unit, property_size, room_count, date_published, link)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
        except sqlite3.IntegrityError as error:
            print(data, error, where)
        
        self.disconnect(conn)
    
    def get_all(self, table_name: str) -> list:
        self.validate_table_name(table_name)

        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT * FROM {table_name}
        """)

        data = cursor.fetchall()

        self.disconnect(conn)

        return data

    # WIP
    # def update(self, table_name: str) -> None:
    #     conn = sqlite3.connect(self.DB_NAME)
    #     cursor = conn.cursor()


    # Repo
    def update_sold_status(self, estates_raw: str, estates_final: str) -> None:
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT *
            FROM {estates_final} AS f
            WHERE NOT EXISTS (
                SELECT *
                FROM {estates_raw} AS r
                WHERE r.id = f.id
            )
            AND f.is_sold = 0
        """)

        not_sold_data = cursor.fetchall()

        for estate in not_sold_data:
            estate_id = estate[0]
            cursor.execute(f"""
                UPDATE {estates_final}
                SET is_sold = 1, date_sold = date()
                WHERE id = ?
            """, (estate_id, ))
            conn.commit()

        cursor.execute(f"""
            SELECT *
            FROM {estates_final} AS f
            WHERE EXISTS (
                SELECT *
                FROM {estates_raw} AS r
                WHERE r.id = f.id
            )
            AND f.is_sold = 1
        """)

        sold_data = cursor.fetchall()

        for estate in sold_data:
            estate_id = estate[0]
            cursor.execute(f"""
                UPDATE {estates_final}
                SET is_sold = 0, date_sold = NULL
                WHERE id = ?
            """, (estate_id, ))
            conn.commit()

        conn.close()
    
    # Repo
    def update_estates(self, estates_raw: str, estates_final: str) -> None:
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f"""
            UPDATE {estates_final} AS f
            SET (address, price, price_per_unit, property_size, room_count, link) = (
                SELECT r.address, r.price, r.price_per_unit, r.property_size, r.room_count, r.link
                FROM {estates_raw} AS r
                WHERE r.id = f.id
            )
            WHERE EXISTS (
                SELECT *
                FROM {estates_raw} AS r
                WHERE r.id = f.id
            )
        """)

        self.disconnect(conn)
    
    def delete_all(self, table_name: str) -> None:
        self.validate_table_name(table_name)

        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f"""
            DELETE FROM {table_name}
        """)

        self.disconnect(conn)