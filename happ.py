import sys, mood_db
# from pathlib import Path
# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar
# from PyQt5.QtGui import QIcon
from interface import Ui_MainWindow

#BUG: Clicking on anywhere on the slider makes it go to either 0 or 10
#BUG: Slider is scrollable with mouse scroll. Also, scrolling with mouse does not invoke sliderMoved, so the label does not update the text

class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        print("\033[1;35;40mStarting:\033[1;32;40m Daily Mood Rater\033[0;37;40m")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #  TODO: Show current date on status bar
        # self.setStatusBar(QStatusBar(self).setStatusTip("string"))

        self.ui.lbl_mood.setText(f"Rate Your Mood - {self.ui.slider_mood.sliderPosition()}")
        self.ui.textEdit_description.setToolTip("You can describe how you feel")



        # Functionality
        self.ui.slider_mood.sliderMoved.connect(self.label_update)

        # TODO: text edit will be disabled by default. so change it to setEnabled when connecting
        self.ui.checkBox_mood.stateChanged.connect(self.enable_text)
        
        # Send slider position and description to database
        self.ui.btn_save.clicked.connect(self.save_to_db)

        # Create a chart from saved data
        self.ui.btn_chart.clicked.connect(self.show_chart)

    def label_update(self):
        self.ui.lbl_mood.setText(f"Rate Your Mood - {self.ui.slider_mood.sliderPosition()}")

    def enable_text(self, value):
        if value == 2:
            self.ui.textEdit_description.setEnabled(True)
        else:
            self.ui.textEdit_description.clear()
            self.ui.textEdit_description.setDisabled(True)

    def save_to_db(self):
        # TODO: Show a prompt that says whether data entry was successful. Also show what was entered into database.
        # TODO: If a rating was already entered for the current day, show warning box with OK | Cancel that it will override the existing entry.
        mood_db.save_values(
            self.ui.slider_mood.sliderPosition(),
            self.ui.textEdit_description.toPlainText()
        )

    def show_chart(self):
        # TODO: if not mood_db.show_values():pass ; else: create a for loop for a chart with retrieved values from database
        print("\033[1;37;40mCurrent values in database\033[0;37;40m")
        for each in mood_db.show_values():
            print(each)
        # print()

def app_window():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = Application()
    win.show()
    sys.exit(app.exec_())

app_window()
