from PyQt5.QtWidgets import QMessageBox


def show_empty_error():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("ПОЛЕ ВВОДА НЕ ДОЛЖНЫ БЫТЬ ПУСТЫМИ")
    # возбуждаем исключение
    exit = msg.exec_()

def show_connect_error():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText("ОШИБКА ПОДКЛЮЕНИЯ К СЕРВЕРУ!\nПОПРОБУЙСТЕ СНОВА!")
    exit = msg.exec_()