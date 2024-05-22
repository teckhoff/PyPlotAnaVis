import pyqtgraph
import images_qr
from PyQt5 import QtGui, QtWidgets


class AppWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Plot AnaVis")
        self.setMinimumSize(700, 300)
        self.setGeometryFromScreenResolution(700, 300)

        self.WidgetStack = QtWidgets.QStackedWidget(self)

        self.setCentralWidget(self.WidgetStack)

        self.PlotterPage = QtWidgets.QWidget(self)

        self.Page1HorizontalLayout = QtWidgets.QHBoxLayout(self.PlotterPage)
        self.Page1LeftLayout = PlottingInput(self.PlotterPage)

        self.PlotGraph = pyqtgraph.PlotWidget()

        self.Page1HorizontalLayout.addLayout(self.Page1LeftLayout)
        self.Page1HorizontalLayout.addWidget(self.PlotGraph)

        self.WidgetStack.addWidget(self.PlotterPage)

    # Pep8 suggests function names are lowercase, this has been ignored here for parity with PyQt5 functions.
    def setGeometryFromScreenResolution(self, default_window_size_x: int, default_window_size_y: int) -> None:
        """Uses the screen resolution from PyQt5 to place the window in the middle of the screen.
        """
        screen = QtWidgets.QApplication.primaryScreen()
        screen_size_x, screen_size_y = screen.size().width(), screen.size().height()
        position_x = int((screen_size_x / 2) - (default_window_size_x / 2))
        position_y = int((screen_size_y / 2) - (default_window_size_y / 2))
        self.setGeometry(position_x, position_y, default_window_size_x, default_window_size_y)


class PlottingInput(QtWidgets.QVBoxLayout):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)

        self.IsPlotting = False

        self.AmplitudeInputField = FloatInputField("Amplitude", 1.0, parent)
        self.addLayout(self.AmplitudeInputField)

        self.FrequencyInputField = FloatInputField("Frequency", 1.0, parent)
        self.addLayout(self.FrequencyInputField)

        self.OffsetInputField = FloatInputField("Offset", 0.0, parent)
        self.addLayout(self.OffsetInputField)

        self.ButtonStartIcon = QtGui.QIcon(':/img/Play.png')
        self.ButtonStopIcon = QtGui.QIcon(':/img/Stop.png')

        self.TogglePlottingButton = QtWidgets.QPushButton(parent)
        self.TogglePlottingButton.setText("Start Plotting")
        self.TogglePlottingButton.setIcon(self.ButtonStartIcon)
        self.TogglePlottingButton.clicked.connect(self.toggle_plotting)
        self.addWidget(self.TogglePlottingButton)

    def toggle_plotting(self):
        self.TogglePlottingButton.setText("Stop Plotting" if not self.IsPlotting else "Start Plotting")
        self.TogglePlottingButton.setIcon(self.ButtonStopIcon if not self.IsPlotting else self.ButtonStartIcon)
        self.IsPlotting = not self.IsPlotting


class FloatInputField(QtWidgets.QHBoxLayout):
    def __init__(self, input_field_label: str, default_value: float, parent: QtWidgets.QWidget):
        super().__init__(parent)

        self.setObjectName(input_field_label + "InputField")

        spacer_1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.addItem(spacer_1)

        self.FieldLabel = QtWidgets.QLabel(input_field_label + ": ", parent)
        self.setObjectName(input_field_label + "FieldLabel")
        self.FieldLabel.setFixedWidth(80)
        self.addWidget(self.FieldLabel)

        spacer_2 = QtWidgets.QSpacerItem(15, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.addItem(spacer_2)

        self.InputField = QtWidgets.QLineEdit(parent)
        self.setObjectName(input_field_label + "InputBox")
        self.InputField.setText(str(default_value))
        self.InputField.setValidator(QtGui.QDoubleValidator())
        self.addWidget(self.InputField)

        spacer_3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.addItem(spacer_3)
