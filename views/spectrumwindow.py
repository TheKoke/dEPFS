from models.spectrum import Spectrum
from controllers.painter import Painter

from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseEvent, MouseButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize, QLocale, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QPushButton,
    QFrame, QLabel, QHBoxLayout, QVBoxLayout, QTextEdit
)


class Ui_SpectraWindow:
    def setupUi(self, SpectraWindow: QMainWindow):
        SpectraWindow.setObjectName("SpectraWindow")
        SpectraWindow.resize(900, 750)
        SpectraWindow.setMinimumSize(QSize(900, 750))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        SpectraWindow.setFont(font)
        SpectraWindow.setStyleSheet("QPushButton{background-color: rgb(85, 85, 127);color: rgb(255, 255, 255);font: 63 14pt \"Bahnschrift SemiBold\";}QPushButton:pressed{background-color: rgb(55, 55, 97);}")
        SpectraWindow.setLocale(QLocale(QLocale.Russian, QLocale.Kazakhstan))
        self.centralwidget = QWidget(SpectraWindow)
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
        self.output = QTextEdit(self.services_layout)
        self.output.setMinimumSize(QSize(200, 90))
        self.output.setMaximumSize(QSize(200, 90))
        font = QFont()
        font.setFamily("Bahnschrift SemiBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.output.setFont(font)
        self.output.setReadOnly(True)
        self.output.setObjectName("output")
        self.horizontalLayout.addWidget(self.output)
        self.delete_button = QPushButton(self.services_layout)
        self.delete_button.setMinimumSize(QSize(200, 90))
        self.delete_button.setMaximumSize(QSize(800, 250))
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout.addWidget(self.delete_button)
        self.save_button = QPushButton(self.services_layout)
        self.save_button.setMinimumSize(QSize(200, 90))
        self.save_button.setMaximumSize(QSize(800, 250))
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
        SpectraWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SpectraWindow)
        QMetaObject.connectSlotsByName(SpectraWindow)

    def retranslateUi(self, SpectraWindow: QMainWindow):
        _translate = QCoreApplication.translate
        SpectraWindow.setWindowTitle(_translate("SpectraWindow", "Spectrums picker"))
        self.info_label.setText(_translate("SpectraWindow", "Double click the peak centers"))
        self.output.setPlaceholderText(_translate("SpectraWindow", "There will be information about peaks"))
        self.delete_button.setText(_translate("SpectraWindow", "Delete"))
        self.save_button.setText(_translate("SpectraWindow", "Save"))


painter = Painter()


class SpectraWindow(QMainWindow, Ui_SpectraWindow):
    def __init__(self, spectrum: Spectrum):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.ico'))

        layout = QVBoxLayout(self.matplotlib_layout)
        self.view = FigureCanvasQTAgg(Figure(figsize=(16, 9)))
        self.view.mpl_connect('button_press_event', self.add_pointer)
        self.toolbar = NavigationToolbar2QT(self.view, self.matplotlib_layout)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.view)

        self.axes = self.view.figure.subplots()

        self.spectrum = spectrum
        self.reserve = spectrum.copy()

        self.out()
        self.draw()
        self.view.draw()

        self.delete_button.clicked.connect(self.delete)
        self.save_button.clicked.connect(self.save)

    def add_pointer(self, event: MouseEvent) -> None:
        if event.button == MouseButton.LEFT and event.dblclick:
            self.spectrum.add_peak(event.xdata)

            self.draw()
            self.out()

    def draw(self) -> None:
        painter.draw_pointers(self.axes, self.spectrum.numbers, self.spectrum.peaks)
        self.view.draw()

    def out(self) -> None:
        table = ''
        for i in self.spectrum.peaks:
            table += f'Peak => x: {i}, y: {self.spectrum.numbers[i - 1]}\n'

        self.output.setText(table)

    def delete(self) -> None:
        if len(self.spectrum.peaks) > 0:
            self.spectrum.delete_peak(self.spectrum.peaks[-1])
            self.draw()
            self.out()

    def save(self) -> bool:
        self.close()


if __name__ == "__main__":
    pass
