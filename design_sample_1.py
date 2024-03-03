from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #Stellt MainWindow auf
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1080, 720)
        MainWindow.setWindowIcon(QtGui.QIcon('TurmDefense.png'))

        #Erstellt Widget für das Scoreboard mit allen Infos und Buttons
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(905, 0, 195, 200))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.side_bar_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.side_bar_label.setObjectName("side_bar_label")
        self.verticalLayout.addWidget(self.side_bar_label)
        self.runde_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.runde_label.setObjectName("runde_label")
        self.verticalLayout.addWidget(self.runde_label)
        self.geld_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.geld_label.setObjectName("geld_label")
        self.verticalLayout.addWidget(self.geld_label)
        self.hp_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.hp_label.setObjectName("hp_label")
        self.verticalLayout.addWidget(self.hp_label)
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(905, 600, 80, 80))
        self.start_button.setObjectName("start_button")
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setGeometry(QtCore.QRect(995, 600, 80, 80))
        self.stop_button.setObjectName("stop_button")
        self.turm1_button = QtWidgets.QPushButton(self.centralwidget)
        self.turm1_button.setGeometry(QtCore.QRect(930, 200, 120, 100))
        self.turm1_button.setObjectName("turm1_button")
        self.turm2_button = QtWidgets.QPushButton(self.centralwidget)
        self.turm2_button.setGeometry(QtCore.QRect(930, 305, 120, 100))
        self.turm2_button.setObjectName("turm2_button")
        self.turm3_button = QtWidgets.QPushButton(self.centralwidget)
        self.turm3_button.setGeometry(QtCore.QRect(930, 410, 120, 100))
        self.turm3_button.setObjectName("turm3_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1440, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        #Gibt den Labels und Button visuelle Namen, werden in Frm_main überschrieben, für aktuelle Daten
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tower Defense"))
        self.side_bar_label.setText(_translate("MainWindow", "Side Bar"))
        self.runde_label.setText(_translate("MainWindow", "Runde:"))
        self.geld_label.setText(_translate("MainWindow", "Geld:"))
        self.hp_label.setText(_translate("MainWindow", "HP Stadt:"))
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.stop_button.setText(_translate("MainWindow", "Stop"))
        self.turm1_button.setText(_translate("MainWindow", "RohButter\nSCHADEN: 10\nREICHWEITE: 5\nPREIS: 100\nFEUERRATE: 1"))
        self.turm2_button.setText(_translate("MainWindow", "Minion\nSCHADEN: 15\nREICHWEITE: 6\nPREIS: 100\nFEUERRATE: 0.8"))
        self.turm3_button.setText(_translate("MainWindow", "JoJo\nSCHADEN: 30\nREICHWEITE: 10\nPREIS: 100\nFEUERRATE: 0.5"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
