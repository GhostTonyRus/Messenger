"""
Файл с кодом для присоединения к серверу. Можно отпарвить сообщение и получить его обратно от сервера.
"""

import socket
import sys
from messages import main

# server_addr = ("127.0.0.1", 11111)
server_addr = ("192.168.0.12", 11111)


# класс клиент
class Client:

    def __init__(self, family, connect_type):
        self.family = family
        self.connect_type = connect_type
        self.client = socket.socket(self.family, self.connect_type)

    # подлкючение к серверу
    def connect_to_server(self):
        try:
            self.client.connect(server_addr)
            print("Выполнено подлюкчение к серверу")
        except socket.error as ex:
            print(f"Ошибка подключения: {ex}")

    # получаем данные от пользователя и отправляем их
    def get_and_send_data(self):
        while True:
            msg = input("Введите текст сообщение:\n")
            if msg == "exit":
                self.client.sendall(str.encode("exit"))
                self.disconnect_from_server()
                break
            else:
                users_data = msg.encode()
                # отправляем данные
                self.client.sendall(users_data)
                # получаем данные от сервера
                self.recv_data()
                continue
        self.client.close()

    # получаем сообщение от сервера
    def recv_data(self):
        try:
            data = self.client.recv(2048)
            print(f"Сообщение от сервера: {data.decode()}")
        except socket.error as error:
            self.client.close()

    # отсоединение от сервера
    def disconnect_from_server(self):
        self.client.close()

    def main(self):
        self.connect_to_server()
        self.get_and_send_data()


if __name__ == '__main__':
    client = Client(socket.AF_INET, socket.SOCK_STREAM)
    client.main()
