import sys, mood_db
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget
from PyQt5.QtGui import QIcon
from interface import Ui_MainWindow
from pathlib import Path

cur_dir = Path.cwd()

#TODO: Check Qt event filter for these bugs.
    #BUG: Clicking on anywhere on the slider makes it go to either 0 or 10
    #BUG: Slider is scrollable with mouse scroll. Also, scrolling with mouse does not invoke sliderMoved, so the label does not update the text

class Application(QMainWindow):
    def __init__(self):
        super(Application, self).__init__()
        print("\033[1;35;40mStarting:\033[1;32;40m Daily Mood Rater\033[0;37;40m")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Icon customization: https://thenounproject.com/term/faces/4127357/
        self.setWindowIcon(QIcon((cur_dir / "test/icon.png").as_posix()))

        #  TODO: Show current date on status bar
        # self.setStatusBar(QStatusBar(self).setStatusTip("string"))

        self.ui.lbl_mood.setText(f"Rate Your Mood - {self.ui.slider_mood.sliderPosition()}")
        self.ui.textEdit_description.setToolTip("You can describe how you feel")


        ### Functionality ###
        self.ui.slider_mood.sliderMoved.connect(self.label_update)

        self.ui.checkBox_mood.stateChanged.connect(self.enable_text)
        
        # Send slider position and description to database
        self.ui.btn_save.clicked.connect(self.save_to_db)

        # Create a chart from saved data
        self.ui.btn_chart.clicked.connect(self.show_graph)

        # Populate ComboBox
        current_months = [month[0] for month in mood_db.current_months()]
        self.ui.comboBox_date.addItems(current_months)
        self.ui.comboBox_date.setCurrentIndex(current_months.index(str(datetime.now())[:7]))

    def label_update(self):
        self.ui.lbl_mood.setText(f"Rate Your Mood - {self.ui.slider_mood.sliderPosition()}")

    def enable_text(self, value):
        if value == 2:
            self.ui.textEdit_description.setEnabled(True)
        else:
            self.ui.textEdit_description.clear()
            self.ui.textEdit_description.setDisabled(True)

    def save_to_db(self):
        textedit = self.ui.textEdit_description.toPlainText()
        description = textedit if bool(self.ui.textEdit_description.toPlainText()) else " "
        save = mood_db.save_values(
                self.ui.slider_mood.sliderPosition(),
                description
            )

        if save != 1:
            # Cannot save because an entry already exists
            # A prompt to ask whether user wants to update current entry or cancel
            msg = QMessageBox()

            msg.setWindowTitle("Overwrite current entry?")
            msg.setText(f"There is already an existing entry for today. Would you like to overwrite it?")
            msg.setDetailedText(f"Mood Rating: {save[0]}\nDescription: {save[1]}\nDate: {save[2]}")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)

            response = msg.exec_()

            # If user clicks OK, overwrite the current entry
            if response == QMessageBox.Ok:
                try:
                    mood_db.update_values(
                        self.ui.slider_mood.sliderPosition(),
                        self.ui.textEdit_description.toPlainText()
                    )
                    # TODO: Show Entry update was successful in status bar
                except:
                    # TODO: Show Entry update was unsuccessful in status bar
                    pass
            elif response == QMessageBox.Cancel:
                pass
            else:
                raise Exception(f"Unhandled Exception! Something went wrong.\nQMessageBox responded with: {response}\nExpected: QMessageBox.Ok or QMessageBox.Cancel\n\033[1;37;40mPlease let me know about this error so I can work on it ^^\033[0;37;40m")
        else:
            msg = QMessageBox()

            msg.setWindowTitle("Success!")
            msg.setText("Your mood rating for today was successfully saved into the database.")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDefaultButton(QMessageBox.Ok)

    def show_graph(self):
        # Using a separate window to show Matplotlib Graph, Embedded into a QWidget window
        import mood_graph
        self.graph = mood_graph.AppWindow(self.ui.comboBox_date.currentText())
        self.graph.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = Application()
    win.show()
    sys.exit(app.exec_())
