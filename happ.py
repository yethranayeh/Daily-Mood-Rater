import sys, mood_db
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from interface import Ui_MainWindow
from pathlib import Path

cur_dir = Path.cwd()

#TODO: Change button "Show Chart" to "Show Graph"

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

    def label_update(self):
        self.ui.lbl_mood.setText(f"Rate Your Mood - {self.ui.slider_mood.sliderPosition()}")

    def enable_text(self, value):
        if value == 2:
            self.ui.textEdit_description.setEnabled(True)
        else:
            self.ui.textEdit_description.clear()
            self.ui.textEdit_description.setDisabled(True)

    def save_to_db(self):        
        save = mood_db.save_values(
                self.ui.slider_mood.sliderPosition(),
                self.ui.textEdit_description.toPlainText()
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
        values = mood_db.show_values()

        if not values:
            print("There are currently no mood ratings saved in database.")
        else:
            import matplotlib.pyplot as plt
            import mplcursors
            print("\033[1;37;40mCurrent values in database:\033[0;37;40m")
            x = [x[2] for x in values]
            y = [y[0] for y in values]
            descriptions = [d[1] for d in values]
            print("Descriptions:", descriptions)
            ax1 = plt.subplot2grid((1,1), (0,0))

            # print("x:", x)
            # print("y:", y)

            plt.ion() # This solves a Qt Exec error. Without this, more than 1 instance of QApplication is being attempted to run.

            lines = ax1.bar(x, y, color="lightsteelblue", edgecolor="black", width=0.95)

            for label in ax1.xaxis.get_ticklabels():
                label.set_rotation(45)
        
            ax1.tick_params(axis="x", colors="tab:blue")
            ax1.tick_params(axis="y", colors="tab:blue")

            ax1.xaxis.label.set_color("tab:blue")
            plt.xlabel("Days (Year - Month - Day)")

            ax1.yaxis.label.set_color("tab:blue")
            plt.ylabel("Mood Rating")

            plt.title("Your Mood Rating Graph")

            plt.yticks([1,2,3,4,5,6,7,8,9,10]) # Only shows the available Y values
            plt.subplots_adjust(left=0.097, bottom=0.23, right=0.977, top=0.922)

            # Cursor Click Annotions
            # This adds the functionality of showing mood descriptions for each day.
            cursor = mplcursors.cursor(lines)
            cursor.connect(
                "add", 
                lambda sel: sel.annotation.set_text(descriptions[sel.target.index]))

            plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = Application()
    win.show()
    sys.exit(app.exec_())


# def app_window():
#     app = QApplication(sys.argv)
#     app.setStyle("Fusion")
#     win = Application()
#     win.show()
#     sys.exit(app.exec_())

# app_window()
