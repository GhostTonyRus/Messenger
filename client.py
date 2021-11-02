"""
Файл с кодом для присоединения к серверу. Можно отпарвить сообщение и получить его обратно от сервера.
"""
import os
import socket
import sys
import time
from datetime import datetime
import signal
import threading
from tests.threadTest import ThreadWithReturnValue


# класс клиент
class Client:

    def __init__(self):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.__client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.msg_datetime = datetime.now().strftime("%H:%M:%S %Y-%m-%d")
        self.custom_msg_datetime = self.msg_datetime  # .strftime("%H:%M:%S %Y-%m-%d")

    # подлкючение к серверу
    def connect_to_server(self, server_address):
        try:
            self.__client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.__client.connect(server_address)
            print("Выполнено подключение к серверу")
        except socket.error as error:
            print(f"Ошибка подключения: {error} 31")
        finally:
            return True

    # отправляем сообщения на сервер
    def send_msg(self, nickname, message, custome_time):
        time.sleep(1)
        if len(message) == 0:
            pass
        elif message:
            # отправляем данные
            self.__client.sendall(str(f"{nickname}\t{custome_time}\n>>> {message}\n").encode())

    # получаем сообщение от сервера
    def receive_msg(self):
        time.sleep(3)
        while True:
            try:
                data = self.__client.recv(2048)
                print(data)
                # show_messages_from_db()
                if data:
                    return data.decode("utf-8")
                elif len(data) == 0:
                    self.disconnect_from_server()
                    break
            except socket.error as error:
                print(f"{error} ошибка из 54")
                self.disconnect_from_server()
                break
        self.disconnect_from_server()

    # отсоединение от сервера
    def disconnect_from_server(self):
        try:
            self.__client.shutdown(socket.SHUT_RDWR)
            print("Отключение от сервера, 64")
        except socket.error as error:
            print(error, "66")
            time.sleep(5)
        finally:
            self.__client.close()

    # # запуск получения сообщений в потоке
    # def thread_receive(self):
    #     thread_receive = ThreadWithReturnValue(target=self.receive_msg)
    #     thread_receive.start()
    #     rez = thread_receive.join()
    #
    # # запуск отправки сообщения в потоке
    # def thread_send_msg(self, message):
    #     thread_send_msg = threading.Thread(target=self.send_msg, args=(message,))
    #     thread_send_msg.start()
    #     rez = thread_send_msg.join()
    #     return rez
    #
    # def main(self, message):
    #     # запуск получения сообщений
    #     thread_receive = threading.Thread(target=self.receive_msg)
    #     thread_receive.start()
    #     # запуск отправки сообщения
    #     thread_send_msg = threading.Thread(target=self.send_msg, args=(message, ))
    #     thread_send_msg.start()

# if __name__ == '__main__':
#     client = Client()
#     client.connect_to_server("23.111.121.114", 12345)
#     client.main()
