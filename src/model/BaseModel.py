import mysql.connector
from config.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


class BaseModel:
    def __init__(self, table):
        self.table = table
        self.conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def findAll(self, panda=False):
        self.cursor.execute(f"SELECT * FROM {self.table}")
        if panda:
            import pandas as pd

            data = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            df = pd.DataFrame(data, columns=columns)
            self.close()
            return df
        return self.cursor.fetchall()

    def find(self, id):
        self.cursor.execute(f"SELECT * FROM {self.table} WHERE id = %s", (id,))
        return self.cursor.fetchone()

    def first(self):
        self.cursor.execute(f"SELECT * FROM {self.table} LIMIT 1")
        return self.cursor.fetchone()

    def where(self, conditions: dict):
        keys = list(conditions.keys())
        values = list(conditions.values())
        where_clause = " AND ".join([f"{k} = %s" for k in keys])
        query = f"SELECT * FROM {self.table} WHERE {where_clause}"
        self.cursor.execute(query, tuple(values))
        return self.cursor.fetchall()

    def select(self, fields: list, where: dict = None):
        field_clause = ", ".join(fields)
        query = f"SELECT {field_clause} FROM {self.table}"
        values = ()
        if where:
            where_clause = " AND ".join([f"{k} = %s" for k in where])
            query += f" WHERE {where_clause}"
            values = tuple(where.values())
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def insert(self, data: dict):
        keys = ", ".join(data.keys())
        values = tuple(data.values())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {self.table} ({keys}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()
        return self.cursor.lastrowid

    def update(self, data: dict, where: dict):
        set_clause = ", ".join([f"{k} = %s" for k in data])
        where_clause = " AND ".join([f"{k} = %s" for k in where])
        query = f"UPDATE {self.table} SET {set_clause} WHERE {where_clause}"
        values = tuple(data.values()) + tuple(where.values())
        self.cursor.execute(query, values)
        self.conn.commit()
        return self.cursor.rowcount

    def delete(self, where: dict):
        where_clause = " AND ".join([f"{k} = %s" for k in where])
        query = f"DELETE FROM {self.table} WHERE {where_clause}"
        self.cursor.execute(query, tuple(where.values()))
        self.conn.commit()
        return self.cursor.rowcount

    def close(self):
        self.cursor.close()
        self.conn.close()
