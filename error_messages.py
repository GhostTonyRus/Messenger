from PyQt5.QtWidgets import QMessageBox


def show_empty_error():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("ПОЛЕ ВВОДА НЕ ДОЛЖНЫ БЫТЬ ПУСТЫМИ!")
    # возбуждаем исключение
    exit = msg.exec_()

def show_connect_error():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("ОШИБКА ПОДКЛЮЕНИЯ К СЕРВЕРУ!\nПОПРОБУЙСТЕ СНОВА!")
    exit = msg.exec_()

def show_authorization_error():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("ЛОГИН ИЛИ ПАРОЛЬ ВВЕДЕНЫ НЕВЕРНО!")
    exit = msg.exec_()

def show_success_registration():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("ВЫ УСПЕШНО ЗАРЕГИСТРИРОВАЛИСЬ!")
    exit = msg.exec_()