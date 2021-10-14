"""
Файл отображает сообщения полученные сервером.
"""
import sqlite3
import socket
import multiprocessing
import time
import threading

messages_db = "messages.db"
# server_addr = ("192.168.0.12", 11111)
#
# def connect_to_server():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.connect(server_addr)
#     while True:
#         connect_to_db(database=messages_db)


def connect_to_db(database):
    with sqlite3.connect(database) as db:
        cur = db.execute("SELECT user, message, datetime FROM messages ORDER BY id DESC LIMIT 1")
        data = cur.fetchall()
        for msg in data:
            return f"{msg[0]}>>> {msg[1]}: {msg[2]}"


def show_messages_from_db():
    print(connect_to_db(messages_db))



if __name__ == '__main__':
    show_messages_from_db()
