"""
В файле написан код для деплой на удалённый сервер. Файл принимает входящие соединения и сообщения, а потом отправляет
их обратно клиенту.
"""
import sqlite3
import socket
import sys
import threading
from datetime import datetime
from constants import IP, PORT

# server_addr = ("127.0.0.1", 11111)
server_addr = (IP, PORT)


class Server:

    def __init__(self, family, connect_type):
        self.__family = family
        self.__type = connect_type
        self.server = socket.socket(self.__family, self.__type)
        self.clients = []
        self.msg_datetime = datetime.now()
        self.custom_msg_datetime = self.msg_datetime.strftime('%Y-%m-%d %H:%M:%S')

    # присоединение пользователей у серверу
    def start_client_thread(self, func, connection, client_addr):
        notification = f"Пользователь {client_addr} присоединился к серверу"
        print(notification)
        thread = threading.Thread(target=func, args=(connection, client_addr,))
        thread.start()
        return thread

    # биндим сервер на адрес локальной сети
    def bind_server(self, server_addr):
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(server_addr)
        print("Подлючение к ip {} port {}".format(*server_addr))

    # запускаем пользователей в поток на сервере
    def start_server(self, num_of_users):
        self.server.listen(int(num_of_users))
        self.server.setblocking(False)
        print("Ожидание подлкючения пользователей: ")
        while True:
            # принимаем подключение и адрес подключившихся пользователей
            self.server.setblocking(True)  # сервер в режиме ожидания
            self.connection, self.client_addr = self.server.accept()
            self.clients.append(self.connection)
            # self.connection.send("Вы присоединились к серверу".encode("utf-8"))
            # добавление пользователей в поток
            self.start_client_thread(func=self.get_users_connection, connection=self.connection,
                                     client_addr=self.client_addr)
            continue

    # ожидаем подключения от пользователей
    def get_users_connection(self, connection, client_addr):
        while True:
            # получаем тип подключения из словаря
            try:
                # получаем данные от пользователя
                self.server.setblocking(True)
                data = connection.recv(4096)
                # если нет данных
                if len(data) == 0:
                    print(f"Сообщение от пользователя отсутствуют: {client_addr}")
                    self.close_connection(connection)
                    break
                # если пришли данные от пользователя
                elif data:
                    print(f"Сообщение от пользователя {client_addr}: {data.decode('utf-8')}")
                    print("Отправляем данные обратно пользователю")
                    # self.save_message_in_db(client_addr, data.decode("utf-8"))
                    self.send_messages(data)
                    continue
            except socket.error as error:
                self.close_connection(connection)
                break

    # отправляем сообщения
    def send_messages(self, data):
        for client in self.clients:
            msg = data.decode('utf-8')  # данные полученные от пользователя
            client.sendall(msg.encode("utf-8"))

    # отсоединение от сервера
    def close_connection(self, connection):
        print(f"Пользователь {connection} отключился")
        self.clients.remove(connection)
        connection.shutdown(socket.SHUT_RDWR)
        connection.close()

    # запуск сервера
    def main(self, server_address, number_of_clients):
        self.bind_server(server_address)
        self.start_server(number_of_clients)


if __name__ == '__main__':
    server = Server(socket.AF_INET, socket.SOCK_STREAM)
    # server.main(server_addr, 3)
    s_a = ("127.0.0.1", 2222)
    # server.main(s_a, 10)
    thread_main = threading.Thread(target=server.main, args=(s_a, 10, ))
    thread_main.start()
    thread_main.join()

    # # сохраняем полученные сообщения от клиентов в базу данных
    # def save_message_in_db(self, user, data):
    #     with sqlite3.connect("messages.db") as sq:
    #         cur = sq.cursor()
    #         cur.execute("""CREATE TABLE IF NOT EXISTS messages (
    #                     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                     user TEXT,
    #                     message TEXT,
    #                     datetime TEXT
    #                     )""")
    #         cur.execute(f"""
    #         INSERT INTO messages
    #             (id, user, message, datetime)
    #             VALUES
    #             (NULL, "{user}", "{data}", "{self.custom_msg_datetime}")
    #         """)
    #         messages = cur.execute("""
    #             SELECT user, message, datetime FROM messages ORDER BY id DESC LIMIT 1
    #             """)
    #         for msg in messages.fetchall():
    #             print(f"{msg[0]}>>> {msg[1]}: {msg[2]}")
