import sqlite3
from error_messages import show_empty_error
import os

users_db = "users.db"
my_dir = "C:\\CHAT\\"
db = os.path.join(my_dir, users_db)


class DataBase:
    def check_db_path(self):
        """есть ли файл базы данных в каталоге"""
        path = os.listdir("C:\\")
        if my_dir in path:
            return True
        else:
            return False

    def create_database(self):
        """создаём базу данных"""
        try:
            with sqlite3.connect(db) as con:
                cur = con.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user TEXT UNIQUE,
                            password TEXT
                )""")
        except FileExistsError as error:
            raise error
        except sqlite3.OperationalError as err:
            os.mkdir(my_dir)

    def insert_data(self, login, password):
        """вставляем данные"""
        if len(login) == 0 or len(password) == 0:
            show_empty_error()
        else:
            try:
                with sqlite3.connect(db) as con:
                    cur = con.cursor()
                    cur.execute(f"""
                    INSERT INTO users (id, user, password)
                    VALUES
                    (NULL, "{login}", "{password}")
                    """)
            except FileExistsError as error:
                raise error

    def check_data(self, login, password):
        """проверяем введённые данные"""
        users = {}
        try:
            with sqlite3.connect(db) as con:
                cur = con.cursor()
                cur.execute(f"""
                SELECT user, password FROM users WHERE user = "{login}" AND password = "{password}"
                """)
                data = cur.fetchall()
                if data:
                    for i in data:
                        users[i[0]] = i[1]
                        for user_login, user_password in users.items():
                            if user_login == login and user_password == password:
                                return True
                elif len(login) == 0 or len(password) == 0:
                    show_empty_error()
        except FileExistsError as error:
            raise error

