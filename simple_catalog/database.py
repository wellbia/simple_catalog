import pymysql


class Database:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.conn = pymysql.connect(
            host=host, user=user, password=password, database=database
        )

    def select_one(self, query: str, args: tuple = None) -> tuple:
        with self.conn.cursor() as cursor:
            cursor.execute(query, args)
            result = cursor.fetchone()
        self.conn.commit()
        return result

    def select_all(self, query: str, args: tuple = None) -> tuple:
        with self.conn.cursor() as cursor:
            cursor.execute(query, args)
            result = cursor.fetchall()
        self.conn.commit()
        return result

    def execute(self, query: str, args: tuple = None):
        with self.conn.cursor() as cursor:
            cursor.execute(query, args)
        self.conn.commit()
