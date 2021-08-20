import sys
# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolTip
# from PyQt5.QtGui import QIcon
from interface import Ui_MainWindow

class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #  TODO: Show current date on status bar
        # self.setStatusBar(QtWidgets.QStatusBar(self).setStatusTip("string"))
        self.ui.lbl_mood.setText(f"Rate Your Mood - {self.ui.slider_mood.sliderPosition()}")
        self.ui.textEdit_description.setToolTip("You can describe how you feel")

        # Functionality
        self.ui.slider_mood.sliderMoved.connect(self.label_update)
        # TODO: text edit will be disabled by default. so change it to setEnabled when connecting
        self.ui.checkBox_mood.stateChanged.connect(self.enable_text)

    def label_update(self):
        self.ui.lbl_mood.setText(f"Rate Your Mood - {self.ui.slider_mood.sliderPosition()}")

    def enable_text(self, value):
        if value == 2:
            self.ui.textEdit_description.setEnabled(True)
        else:
            self.ui.textEdit_description.clear()
            self.ui.textEdit_description.setDisabled(True)


def app_window():
    app = QApplication(sys.argv)
    win = Application()
    win.show()
    sys.exit(app.exec_())

app_window()
