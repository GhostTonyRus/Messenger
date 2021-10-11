"""
В файле написан код для деплой на удалённый сервер. Файл принимает входящие соединения и сообщения, а потом отправляет
их обратно клиенту.
"""
import sqlite3
import socket
import sys
import multiprocessing
from datetime import datetime

# server_addr = ("127.0.0.1", 11111)
server_addr = ("192.168.0.12", 11111)


class Server:

    def __init__(self, family, connect_type):
        self.family = family
        self.type = connect_type
        self.server = socket.socket(self.family, self.type)
        self.clients = {}
        self.msg_datetime = datetime.now()
        self.custom_msg_datetime = self.msg_datetime.strftime('%Y-%m-%d %H:%M:%S')

    # начинаем разделение
    def start_multiprocessing(self, func, connection, client_addr):
        # self.connections[connection] = client_addr
        # self.connections.append(connection)
        print(f"Пользователь {client_addr} присоединился к серверу")
        # разбиваем получение и отправку сообщений от клиента на ядра процессора
        multiprocess = multiprocessing.Process(target=func, args=(connection, client_addr))
        multiprocess.daemon = True
        multiprocess.start()
        return multiprocess

    # биндим сервер на адрес локальной сети
    def bind_server(self, server_addr):
        self.server.bind(server_addr)
        print("Подлючение к ip {} port {}".format(*server_addr))

    # ожидаем подключения от пользователей
    def get_users_connection(self, connection, client_addr):
        while True:
            try:
                # получаем данные от пользователя
                data = connection.recv(2048)
                # если нет данных
                if not data:
                    print(f"Сообщение от пользователя отсутствуют: {client_addr}")
                    connection.close()
                    break
                # если пользователь отключился
                elif "exit" in data.decode("utf-8"):
                    print(f"Пользователь {client_addr} отключился от сервера")
                    connection.close()
                    break
                # если пришли данные от пользователя
                else:
                    print(f"Сообщение от пользователя {client_addr}: {data.decode('utf-8')}")
                    print("Отправляем данные обратно пользователю")
                    self.save_message_in_db(client_addr, data.decode("utf-8"))
                    self.send_messages(connection, data)
                    continue
            except socket.error as error:
                self.connection.close()
                break

    # запускаем пользователей в поток на сервере
    def start_server(self, num_of_users):
        self.server.listen(int(num_of_users))
        print("Ожидание подлкючения пользователей: ")
        while True:
            # принимаем подключение и адрес подключившихся пользователей
            self.connection, self.client_addr = self.server.accept()
            self.clients[self.client_addr] = self.connection
            # добавление пользователей в поток
            self.start_multiprocessing(func=self.get_users_connection, connection=self.connection,
                                       client_addr=self.client_addr)
            continue

    # отправляем сообщения
    def send_messages(self, connection, data):
        connection.sendall(data)

    # сохраняем полученные сообщения от клиентов в базу данных
    def save_message_in_db(self, user, data):
        with sqlite3.connect("messages.db") as sq:
            cur = sq.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user TEXT,
                        message TEXT,
                        datetime TEXT
                        )""")
            cur.execute(f"""
            INSERT INTO messages 
                (id, user, message, datetime)
                VALUES 
                (NULL, "{user}", "{data}", "{self.custom_msg_datetime}")
            """)
            messages = cur.execute("""
                SELECT user, message, datetime FROM messages ORDER BY id DESC LIMIT 1
                """)
            for msg in messages.fetchall():
                print(f"{msg[0]}>>> {msg[1]}: {msg[2]}")


    def main(self, server_addres, number_of_clients):
        self.bind_server(server_addres)
        self.start_server(number_of_clients)


if __name__ == '__main__':
    server = Server(socket.AF_INET, socket.SOCK_STREAM)
    server.main(server_addr, 3)


