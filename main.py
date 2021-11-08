import sys
from PyQt5 import QtWidgets
from interface import MyWindow

if __name__ == '__main__':
    def my_excepthook(type, value, tback):
        QtWidgets.QMessageBox.critical(application, "Critical Error", str(value),
                                       QtWidgets.QMessageBox.Cancel)
        sys.__excepthook__(type, value, tback)

    sys.excepthook = my_excepthook
    app = QtWidgets.QApplication(sys.argv)
    application = MyWindow()
    application.show()
    sys.exit(app.exec_())


# pyuic5 UI/main_ui.ui -o main_ui.py
# pyuic5 UI/settings_window.ui - o settings_window.py
# pyinstaller -w -F --onefile --icon=C:\PycharmProjects\Chat\img\logo_img.ico --noconsole main.py
# pyinstaller main.spec