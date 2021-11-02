import sys
import sqlite3
from PyQt5.QtWidgets import QMessageBox, QDesktopWidget
from PyQt5.QtCore import QPoint

users_db = "users.db"


# with sqlite3.connect(users_db) as con:
#     cur = con.cursor()
#     cur.execute("""CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 user TEXT UNIQUE,
#                 password TEXT
#     )""")

def show_empty_error():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("ПОЛЯ ВВОДА НЕ ДОЛЖНЫ БЫТЬ ПУСТЫМИ")
    # возбуждаем исключение
    exit = msg.exec_()

def show_value_error():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("НЕВЕРНЫЙ ЛОГИН ИЛИ ПАРОЛЬ")
    # возбуждаем исключение
    exit = msg.exec_()


class DataBase:

    def insert_data(self, login, password):
        if len(login) == 0 or len(password) == 0:
            show_empty_error()
        else:
            with sqlite3.connect(users_db) as con:
                cur = con.execute(f"""
                INSERT INTO users (id, user, password)
                VALUES
                (NULL, "{login}", "{password}")
                """)


    def check_data(self, login, password):
        users = {}
        with sqlite3.connect(users_db) as con:
            # cur = con.execute(f"""
            # SELECT user, password FROM users""")
            cur = con.execute(f"""
            SELECT user, password FROM users WHERE user = "{login}" AND password = "{password}"
            """)
            data = cur.fetchall()
            if data:
                for i in data:
                    users[i[0]] = i[1]
                    for user_login, user_password in users.items():
                        if user_login == login and user_password == password:
                            return True
            else:
                show_value_error()

    def get_data(self):
        pass

