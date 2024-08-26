import sqlite3

class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    # Create table
    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            fullname TEXT NOT NULL,
            telegram_id TEXT UNIQUE NOT NULL,
            language TEXT NOT NULL DEFAULT 'uz',
            illegal INTEGER DEFAULT 0
        );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, fullname: str, telegram_id: str = None, language: str = 'uz'):
        sql = """
        INSERT INTO Users(id, fullname, telegram_id, language) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, fullname, telegram_id, language), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_fullname(self, fullname, telegram_id):
        sql = """
        UPDATE Users SET fullname=? WHERE telegram_id=?
        """
        return self.execute(sql, parameters=(fullname, telegram_id), commit=True)

    def illegal_add(self, telegram_id):
        sql = """
        UPDATE Users SET illegal = illegal + 1 WHERE telegram_id=?
        """
        return self.execute(sql, parameters=(telegram_id,), commit=True)

    def update_illegal_zero(self, telegram_id):
        sql = """
            UPDATE Users
            SET illegal = 0
            WHERE telegram_id = ?
        """
        return self.execute(sql, parameters=(telegram_id,), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)
