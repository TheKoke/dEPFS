import os

from models.matrix import Matrix
from models.decoding import Decoder
from controllers.painter import Painter
from controllers.schedule import Scheduler
from views.spectrumwindow import SpectraWindow
from views.inform import InformWindow

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize, QLocale, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QMainWindow, QFileDialog, QWidget, 
    QFrame, QLabel, QHBoxLayout, QVBoxLayout, 
    QSpacerItem, QPushButton, QLineEdit, QSizePolicy
)


class Ui_MainWindow:
    def setupUi(self, MainWindow: QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 750)
        MainWindow.setMinimumSize(QSize(900, 750))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("QPushButton{background-color: rgb(85, 85, 127);color: rgb(255, 255, 255);font: 63 14pt \"Bahnschrift SemiBold\";}QPushButton:pressed{background-color: rgb(55, 55, 97);}")
        MainWindow.setLocale(QLocale(QLocale.Russian, QLocale.Kazakhstan))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.services_layout = QFrame(self.centralwidget)
        self.services_layout.setMinimumSize(QSize(0, 100))
        self.services_layout.setMaximumSize(QSize(16777215, 250))
        self.services_layout.setFrameShape(QFrame.StyledPanel)
        self.services_layout.setFrameShadow(QFrame.Raised)
        self.services_layout.setObjectName("services_layout")
        self.horizontalLayout = QHBoxLayout(self.services_layout)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.info_label = QLabel(self.services_layout)
        self.info_label.setMinimumSize(QSize(100, 0))
        self.info_label.setMaximumSize(QSize(400, 16777215))
        self.info_label.setStyleSheet("font: 63 14pt \"Bahnschrift SemiBold\";")
        self.info_label.setLocale(QLocale(QLocale.Russian, QLocale.Kazakhstan))
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(True)
        self.info_label.setObjectName("info_label")
        self.horizontalLayout.addWidget(self.info_label)
        self.file_name = QLineEdit(self.services_layout)
        self.file_name.setMinimumSize(QSize(120, 90))
        self.file_name.setMaximumSize(QSize(480, 250))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(7)
        self.file_name.setFont(font)
        self.file_name.setStyleSheet("background-color: rgb(85, 85, 127);\ncolor: rgb(255, 255, 255);\nfont: 63 14pt \"Bahnschrift SemiBold\";")
        self.file_name.setText("")
        self.file_name.setAlignment(Qt.AlignCenter)
        self.file_name.setReadOnly(True)
        self.file_name.setObjectName("file_name")
        self.horizontalLayout.addWidget(self.file_name)
        self.open_button = QPushButton(self.services_layout)
        self.open_button.setMinimumSize(QSize(50, 90))
        self.open_button.setMaximumSize(QSize(200, 250))
        self.open_button.setObjectName("open_button")
        self.horizontalLayout.addWidget(self.open_button)
        self.next_button = QPushButton(self.services_layout)
        self.next_button.setMinimumSize(QSize(150, 90))
        self.next_button.setMaximumSize(QSize(600, 250))
        self.next_button.setObjectName("next_button")
        self.horizontalLayout.addWidget(self.next_button)
        self.prev_button = QPushButton(self.services_layout)
        self.prev_button.setMinimumSize(QSize(150, 90))
        self.prev_button.setMaximumSize(QSize(600, 250))
        self.prev_button.setObjectName("prev_button")
        self.horizontalLayout.addWidget(self.prev_button)
        self.save_button = QPushButton(self.services_layout)
        self.save_button.setMinimumSize(QSize(150, 90))
        self.save_button.setMaximumSize(QSize(600, 250))
        self.save_button.setObjectName("save_button")
        self.horizontalLayout.addWidget(self.save_button)
        self.verticalLayout.addWidget(self.services_layout)
        self.matplotlib_layout = QFrame(self.centralwidget)
        self.matplotlib_layout.setMinimumSize(QSize(0, 620))
        self.matplotlib_layout.setMaximumSize(QSize(16777215, 1140))
        self.matplotlib_layout.setFrameShape(QFrame.StyledPanel)
        self.matplotlib_layout.setFrameShadow(QFrame.Raised)
        self.matplotlib_layout.setObjectName("matplotlib_layout")
        self.verticalLayout.addWidget(self.matplotlib_layout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow: QMainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Spectrums picker"))
        self.info_label.setText(_translate("MainWindow", "Choose the E-dE file"))
        self.file_name.setPlaceholderText(_translate("MainWindow", "Opened File"))
        self.open_button.setText(_translate("MainWindow", "..."))
        self.next_button.setText(_translate("MainWindow", "Next Spectrum"))
        self.prev_button.setText(_translate("MainWindow", "Prev Spectrum"))
        self.save_button.setText(_translate("MainWindow", "Save"))


painter = Painter()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.ico'))

        layout = QVBoxLayout(self.matplotlib_layout)
        self.view = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.toolbar = NavigationToolbar2QT(self.view, self.matplotlib_layout)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.view)

        self.axes = self.view.figure.subplots()

        self.current: Scheduler = None

        self.open_button.clicked.connect(self.open)
        self.next_button.clicked.connect(self.next)
        self.prev_button.clicked.connect(self.prev)
        self.save_button.clicked.connect(self.save)

    def open(self) -> None:
        if self.current is not None and len(self.current.incompleted()) > 0:
            self.window = InformWindow("Please, finish all spectras.")
            self.window.show()
            return

        name, _ = QFileDialog.getOpenFileName(self, 'Open File', filter='dSigma files (*.ds)')
        if name == '':
            self.window = InformWindow("File wasn't choosen.")
            self.window.show()
            return
        self.file_name.setText(os.path.basename(name))
        
        decoder = Decoder(name)
        matrix = Matrix(decoder.get_matrix())
        self.current = Scheduler(matrix)
        self.draw(None)

    def draw(self, e) -> None:
        if self.current is None:
            self.window = InformWindow("First, open the E-dE matrix.")
            self.window.show()
            return
        
        painter.draw_matrix_slices(self.axes, self.current.matrix.numbers, self.current.completed(), self.current.incompleted())
        self.view.draw()

    def complete(self) -> None:
        if self.current is None:
            self.window = InformWindow("First, open the E-dE matrix.")
            self.window.show()
            return
        
        self.current.complete()
        self.draw(None)

    def next(self) -> None:
        if self.current is None:
            self.window = InformWindow("First, open the E-dE matrix.")
            self.window.show()
            return
        
        if len(self.current.incompleted()) == 0:
            self.window = InformWindow("All spectras are already done.")
            self.window.show()
            return
        
        slice = self.current.next()
        self.window = SpectraWindow(slice)
        self.window.save_button.clicked.connect(self.complete)
        self.window.closeEvent = self.draw
        self.window.show()

    def prev(self) -> None:
        if self.current is None:
            self.window = InformWindow("First, open the E-dE matrix.")
            self.window.show()
            return
        
        slice = self.current.prev()
        if slice is None:
            self.window = InformWindow("You are on the beginning, there is no previous spectra.")
            self.window.show()
            return

        self.window = SpectraWindow(slice)
        self.window.save_button.clicked.connect(self.complete)
        self.window.closeEvent = self.draw
        self.window.show()

    def save(self) -> None:
        if self.current is None:
            self.window = InformWindow("First, open the E-dE matrix.")
            self.window.show()
            return
        
        if len(self.current.incompleted()) > 0:
            self.window = InformWindow("Please, finish all spectras.")
            self.window.show()
            return
        
        self.current.save(os.getcwd())


if __name__ == "__main__":
    pass
