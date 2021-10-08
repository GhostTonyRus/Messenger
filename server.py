import socket
import sys
import multiprocessing


server_addr = ("127.0.0.1", 11111)


class Server:
    """
    Сервер работает на локальном сети
    """

    def __init__(self, family, connect_type):
        self.family = family
        self.type = connect_type
        self.server = socket.socket(self.family, self.type)
        self.connections = {}

    def start_threads(self, func, connection, client_addr):
        self.connections[connection] = client_addr
        print(f"Пользователь {client_addr} присоединился")
        # t = threading.Thread(target=func, args=(connection, client_addr))
        # t.start()
        # t.join()
        m = multiprocessing.Process(target=func, args=(connection, client_addr))
        m.start()
        return m

    # биндим сервер на адрес локальной сети
    def bind_server(self, server_addr):
        self.server.bind(server_addr)
        print("Подлючение к ip {} port {}".format(*server_addr))

    # ожидаем подключения от пользователей
    def get_users_connection(self, connection, client_addr):
        # print(f"Пользователь {client_addr} присоединился")
        while True:
            try:
                # получаем данные от пользователя
                data = connection.recv(2048)
                if not data:
                    print(f"Данные от пользователя отсутствуют: {client_addr}")
                    connection.close()
                    break
                else:
                    print(f"Данные от пользователя: {data.decode('utf-8')}")
                    print("Отправляем данные обратно клиенту")
                    connection.sendall(data)
                    continue
            except socket.error as error:
                self.connection.close()
                break

    # запускаем пользователей в поток на сервере
    def start_server(self, num_of_users):
        self.server.listen(int(num_of_users))
        print("Ожидание подлкючения пользователей: ")
        while True:
            # print("Ожидание подлкючения пользователей: ")
            self.connection, self.client_addr = self.server.accept()
            # добавление пользователей в поток
            self.start_threads(func=self.get_users_connection, connection=self.connection, client_addr=self.client_addr)
            continue
            # t = threading.Thread(target=self.get_users_connection, args=(self.connection, self.client_addr))
            # t.start()
            # t.join()
            # continue


if __name__ == '__main__':
    server = Server(socket.AF_INET, socket.SOCK_STREAM)
    server.bind_server(server_addr)
    server.start_server(3)
