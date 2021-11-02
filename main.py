import sys
from PyQt5 import QtWidgets
from interface import MyWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    application = MyWindow()
    application.show()
    sys.exit(app.exec_())

