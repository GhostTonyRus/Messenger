import datetime
import time
from datetime import datetime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDesktopWidget
from config import SERVER_ADDRESS
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QPoint, QTimer, QThread, QDateTime
from error_messages import show_empty_error, show_connect_error, show_authorization_error, show_success_registration
from db_logic import DataBase
from UI.main_ui import Ui_MainWindow
from UI.settings_window_ui import Ui_ChildWindow
from client import Client

client = Client()


# окно с настройками
class SettingsWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SettingsWindow, self).__init__()
        self.ui = Ui_ChildWindow()
        self.ui.setupUi(self)

        # настройка кнопок
        self.ui.btn_connect_to_server.clicked.connect(lambda: self.make_connect_to_server())

    # перетаскивание окна
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


class MyThread(QThread):
    my_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(MyThread, self).__init__()

    # запуск потока
    def run(self):
        time.sleep(10)
        while True:
            incoming_msg = client.receive_msg()
            if incoming_msg:
                self.my_signal.emit(incoming_msg)
            elif incoming_msg == None or incoming_msg == "":
                break


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.db = DataBase()
        self.__version = "v.0.5 alpha"

        # настройка времени
        # self.msg_datetime = datetime.now().strftime("%H:%M:%S %Y-%m-%d")
        # self.custom_msg_datetime = self.msg_datetime.strftime("%H:%M:%S %Y-%m-%d")

        # настройка окна по умолчанию
        self.ui.stackedWidget.setCurrentWidget(self.ui.authorization_page)

        # настройка поля ввода пароля
        self.ui.le_input_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.le_register_password.setEchoMode(QtWidgets.QLineEdit.Password)

        # настройка кнопок
        self.ui.btn_registration.clicked.connect(lambda: self.show_registration_page())  # показать окно регистрации
        self.ui.btn_register.clicked.connect(lambda: self.register_user()) # зарегистрирвоать пользователя
        self.ui.btn_enter.clicked.connect(self.enter_to_messenger)  # авторизация и вход на сервер
        self.ui.btn_exit_from_messenger.clicked.connect(
            self.close)  # кнопка завершения работы программы (на страницу авторизации)
        self.ui.btn_exit_to_auth_page.clicked.connect(lambda: self.show_authorization_page())  # выход
        self.ui.btn_exit_from_server.clicked.connect(lambda: self.disconnect_from_server())  # выход с сервера
        self.ui.btn_settings.clicked.connect(lambda: self.settings_page())  # окно настроек
        self.ui.btn_send_msg.clicked.connect(lambda: self.send_msg())  # отправляем письмо
        self.ui.btn_minimize_window.clicked.connect(lambda: self.showMinimized())  # кнопка сворачивания программв
        self.ui.btn_close_app.clicked.connect(self.close)  # кнопка завершения работы программы

        # версия программы
        self.ui.lbl_version.setText(self.__version)

        # настройка кнопок
        self.ui.btn_enter.setAutoDefault(True)  # нажатие <Enter>
        self.ui.le_input_password.returnPressed.connect(self.ui.btn_enter.click)  # нажатие <Enter>

        # запуск сингала для принятия сообщений
        self.my_thread = MyThread()
        self.my_thread.my_signal.connect(self.receive_msg)
        self.my_thread.start()
        if not self.db.create_database():
            self.db.create_database()

        # настройка время
        self.timer = QTimer()
        self.timer.timeout.connect(self.start_Timer)
        self.show_Time()
        self.start_Timer()

        # настройка рамки окна
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_AttributeCount)

        # настройка иконки
        icon = QPixmap("C:\PycharmProjects\CHAT\img\logo.png")
        icon.size()
        self.ui.lbl_icon.setPixmap(icon)
        self.setWindowIcon(QtGui.QIcon("C:\PycharmProjects\CHAT\img\logo.png"))

    # показ странциы регистрации
    def show_registration_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.registration_page)

    # окно выхода с сервера
    def disconnect_from_server(self):
        time.sleep(1)
        # client.disconnect_from_server()
        self.ui.stackedWidget.setCurrentWidget(self.ui.authorization_page)

    # показ окна авторизации
    def show_authorization_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.authorization_page)

    # показ окна сообщений
    def show_main_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.main_page)

    # окно настроек
    def settings_page(self):
        self.window = SettingsWindow()
        self.window.show()

    # регистрация пользователя
    def register_user(self):
        __login = self.ui.le_register_username.text()
        __password = self.ui.le_register_password.text()
        self.db.insert_data(__login, __password)
        time.sleep(1)
        show_success_registration()
        self.show_authorization_page()

    # авторизация в мессенджер и присоединение к серверу
    def enter_to_messenger(self):
        __login = self.ui.le_input_username.text()  # получаем логин из поля ввода
        __password = self.ui.le_input_password.text()  # получаем пароль из поля ввода
        validate = self.db.check_data(__login, __password)  # проверка введённого пароля и логина
        if validate:
            time.sleep(1)
            # подлключение к серверу
            if client.connect_to_server(SERVER_ADDRESS):
                # открывается страница с чатом
                self.show_main_page()
            else:
                # ошибка подключения к серверу
                show_connect_error()
                self.show_authorization_page()
            # hello_msg = client.receive_msg()  # приветственное сообщение
            self.ui.lw_messages.addItem(
                f"{__login}\t{datetime.now().strftime('%H:%M:%S %Y-%m-%d')}\n>>> Вы присоединились к серверу\n")  # отображем сообщение из формы в список
            self.start_Timer()  # показываем время
        if not validate:
            show_authorization_error()  # ошибка авторизации
            self.show_authorization_page()

    # отправляем и получаем сообщения
    def send_msg(self):
        __login = self.ui.le_input_username.text()  # получаем логин, как имя отправителя
        msg = self.ui.te_input_msg.toPlainText()  # получаем сообщение из поля ввода
        if len(msg) == 0:
            show_empty_error()  # сообщение об ошибке (пустое сообщение)
        elif msg:
            client.send_msg(__login, msg, datetime.now().strftime("%H:%M:%S %Y-%m-%d"))  # отправка сообщения
            self.ui.te_input_msg.clear()  # очищаем поля ввода

    # получаем сообщения от сервера
    def receive_msg(self, value):
        self.ui.lw_messages.addItem(f"{value}")  # отображаем входящие сообщения

    # показываем время в реальном времени
    def show_Time(self):
        time = QDateTime.currentDateTime()
        self.timeDisplay = time.toString("hh:mm:ss yyyy-MM-dd dddd")
        self.ui.lbl_frame.setText(self.timeDisplay)  # устанавливаем в лейбл время

    # начать показывать время
    def start_Timer(self):
        self.timer.start(1000)
        self.show_Time()

    # перетаскивание окна
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
