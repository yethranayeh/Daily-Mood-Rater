import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolTip
from PyQt5.QtGui import QIcon
from interface import Ui_MainWindow

class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

def app_window():
    app = QApplication(sys.argv)
    win = Application()
    win.show()
    sys.exit(app.exec_())

app_window()
