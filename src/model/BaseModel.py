import mysql.connector
from config.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from model.ResultWrapper import ResultWrapper


class BaseModel:
    def __init__(self, table):
        self.table = table
        self.conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def findAll(self):
        self.cursor.execute(f"SELECT * FROM {self.table}")
        data = self.cursor.fetchall()
        return ResultWrapper(data, self.cursor.description, self)

    def find(self, id):
        self.cursor.execute(f"SELECT * FROM {self.table} WHERE id = %s", (id,))
        return self.cursor.fetchone()

    def where(self, **kwargs):
        conditions = " AND ".join([f"{k}=%s" for k in kwargs])
        values = tuple(kwargs.values())
        query = f"SELECT * FROM {self.table} WHERE {conditions}"
        self.cursor.execute(query, values)
        data = self.cursor.fetchall()
        return ResultWrapper(data, self.cursor.description, self)

    def insert(self, data: dict):
        keys = ", ".join(data.keys())
        values = tuple(data.values())
        placeholders = ", ".join(["%s"] * len(data))
        query = f"INSERT INTO {self.table} ({keys}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()
        return self.cursor.lastrowid

    def select(self, *fields):
        columns = ", ".join(fields)
        query = f"SELECT {columns} FROM {self.table}"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        description = self.cursor.description
        return ResultWrapper(data, description, self)

    def truncate_table(self):
        query = f"TRUNCATE TABLE {self.table}"
        self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
