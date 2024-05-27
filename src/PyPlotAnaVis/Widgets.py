import math

import numpy
import pyqtgraph
import images_qr
from PyQt5 import QtCore, QtGui, QtWidgets
import Threads

CACHE_COUNTER_DEFAULT_STATE = 9  # Our first cache is going to be created at 9 seconds, because we start at 0.
CACHE_INCREMENT = 10  # We want to cache our data off of the graph every 10 seconds.
GRAPH_RENDER_RATE = int(1000 / 60)  # The graph will be rendered in ~60FPS.
KEEP_FROM_CACHE: int = 50  # How many cached data points to rollover into the current data to ensure there are no gaps.
WINDOW_SIZE_X: int = 700  # The initial window size on the X axis.
WINDOW_SIZE_Y: int = 300  # The initial window size on the Y axis.


class AppWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the window.
        self.setWindowTitle("Python Plot AnaVis")
        self.setGeometryFromScreenResolution()

        self.WidgetStack = QtWidgets.QStackedWidget(self)

        self.setCentralWidget(self.WidgetStack)

        self.PlotterPage = QtWidgets.QWidget(self)

        self.Page1HorizontalLayout = QtWidgets.QHBoxLayout(self.PlotterPage)
        self.PlottingControls = PlottingInput(self.PlotterPage)

        self.PlottingControls.TogglePlottingButton.clicked.connect(self.toggle_plotting)

        self.PlotGraph = PlotGraph()

        self.DataPoints = []
        self.TimePoints = []

        self.PlottedLine = self.PlotGraph.plot(self.DataPoints, self.TimePoints)
        self.CachedLine = self.PlotGraph.plot()

        self.Page1HorizontalLayout.addLayout(self.PlottingControls)
        self.Page1HorizontalLayout.addWidget(self.PlotGraph)

        self.DataStreamThread = Threads.DataStreamThread(self.TimePoints, self.DataPoints)
        self.DataStreamThread.get_simulation_ended_signal_from_worker().Ended.connect(self.enable_start_button)
        self.DataStreamThread.start()

        self.GraphUpdateTimer = QtCore.QTimer()
        self.GraphUpdateTimer.setInterval(GRAPH_RENDER_RATE)
        self.GraphUpdateTimer.timeout.connect(self.update_graph)

        self.SimulationStarted: int = 0

        self.CacheCounter = CACHE_COUNTER_DEFAULT_STATE
        self.PreviousCacheIndex = 0
        self.CachedLines = []

        self.WidgetStack.addWidget(self.PlotterPage)

    # Pep8 suggests function names are lowercase, this has been ignored here for parity with PyQt5 functions.
    def setGeometryFromScreenResolution(self) -> None:
        """Uses the screen resolution from PyQt5 to place the window in the middle of the screen.
        """
        screen = QtWidgets.QApplication.primaryScreen()
        screen_size_x, screen_size_y = screen.size().width(), screen.size().height()
        position_x = int((screen_size_x / 2) - (WINDOW_SIZE_X / 2))
        position_y = int((screen_size_y / 2) - (WINDOW_SIZE_Y / 2))
        self.setGeometry(position_x, position_y, WINDOW_SIZE_X, WINDOW_SIZE_Y)

    def toggle_plotting(self) -> None:
        self.PlottingControls.toggle_plotting()
        self.DataStreamThread.toggle_simulation(self.PlottingControls.IsPlotting)
        self.DataStreamThread.update_inputs(self.PlottingControls.get_amplitude(),
                                            self.PlottingControls.get_frequency(),
                                            self.PlottingControls.get_offset(),
                                            self.PlottingControls.get_datastream_simulation_rate())

        self.PlotGraph.setYRange(-self.PlottingControls.get_amplitude() - 0.5,
                                 self.PlottingControls.get_amplitude() + 0.5)

        if self.PlottingControls.IsPlotting:
            self.PlottedLine.clear()
            self.SimulationStarted = QtCore.QDateTime.currentSecsSinceEpoch()
            self.GraphUpdateTimer.start()
            return

        # self.PlottingControls.toggle_plotting_button_enabled(False)
        self.GraphUpdateTimer.stop()

    def reset_plotting(self) -> None:
        # Clear our lists to facilitate new data
        self.TimePoints.clear()
        self.DataPoints.clear()
        self.CachedLines.clear()
        # Reset our lines
        self.CachedLine.clear()
        self.PlotGraph.removeItem(self.CachedLine)
        del self.CachedLine
        self.CachedLine = self.PlotGraph.plot()
        self.PlottedLine.clear()
        self.PlotGraph.removeItem(self.PlottedLine)
        del self.PlottedLine
        self.PlottedLine = self.PlotGraph.plot()

        # Update the thread and counter to default state
        self.DataStreamThread.DataStreamWorker.update_lists(self.TimePoints, self.DataPoints)
        self.CacheCounter = CACHE_COUNTER_DEFAULT_STATE

    def enable_start_button(self) -> None:
        print("test")
        self.PlottingControls.toggle_plotting_button_enabled(True)
        self.show_cached_lines()

    def add_cached_lines_to_lists(self, time_points: list[float], data_points: list[float], initial_cache: bool):
        for cache in self.CachedLines:
            if initial_cache:
                time_points.extend(cache[0])
                data_points.extend(cache[1])
                initial_cache = False
                continue
            time_points.extend(cache[0][KEEP_FROM_CACHE:])
            data_points.extend(cache[1][KEEP_FROM_CACHE:])

    def show_cached_lines(self):
        total_time_points = []
        total_data_points = []
        initial_cache = True
        self.add_cached_lines_to_lists(total_time_points, total_data_points, initial_cache)

        if len(total_time_points) == 0:
            total_time_points.extend(self.TimePoints)
            total_data_points.extend(self.DataPoints)
        else:
            total_time_points.extend(self.TimePoints[KEEP_FROM_CACHE:])
            total_data_points.extend(self.DataPoints[KEEP_FROM_CACHE:])

        self.reset_plotting()
        self.PlottedLine.setData(total_time_points, total_data_points)

    def save_data_to_file(self):
        print("saving")
        saving_time_points = []
        saving_data_points = []
        initial_cache = True if self.CacheCounter <= 60 else False
        self.add_cached_lines_to_lists(saving_time_points, saving_data_points, initial_cache)
        numpy.save(str(self.SimulationStarted), numpy.asarray([saving_time_points, saving_data_points]))

    def update_graph(self):
        current_max_point = len(self.TimePoints) - 1

        if current_max_point < 1:
            return

        current_second = math.floor(self.TimePoints[current_max_point])

        if current_second > self.CacheCounter:
            self.CacheCounter += 10
            print()
            self.CachedLines.append(self.PlottedLine.getData())
            self.CachedLine.clear()
            self.CachedLine.setData(self.PlottedLine.getData()[0], self.PlottedLine.getData()[1])
            self.PlottedLine.clear()
            self.TimePoints = self.TimePoints[current_max_point - KEEP_FROM_CACHE:]
            self.DataPoints = self.DataPoints[current_max_point - KEEP_FROM_CACHE:]
            self.DataStreamThread.DataStreamWorker.update_lists(self.TimePoints, self.DataPoints)
            if (self.CacheCounter - CACHE_COUNTER_DEFAULT_STATE) % 60 == 0:
                self.save_data_to_file()

        self.PlottedLine.setData(self.TimePoints[:-1], self.DataPoints[:-1])
        self.PlotGraph.setXRange(self.TimePoints[len(self.TimePoints) - 1] - 8,
                                 self.TimePoints[len(self.TimePoints) - 1] + 8)


class PlotGraph(pyqtgraph.PlotWidget):
    def __init__(self):
        super().__init__()

        self.setBackground("w")
        self.setTitle("Plot Graph")
        self.setLabel("bottom", "Time (sec.)")
        self.setLabel("left", "Data")


class PlottingInput(QtWidgets.QVBoxLayout):
    def __init__(self, parent: QtWidgets.QWidget):
        super().__init__(parent)

        self.IsPlotting: bool = False

        self.AmplitudeInputField: FloatInputField = FloatInputField("Amplitude",
                                                                    Threads.DEFAULT_AMPLITUDE, parent)
        self.addLayout(self.AmplitudeInputField)

        self.FrequencyInputField: FloatInputField = FloatInputField("Frequency",
                                                                    Threads.DEFAULT_FREQUENCY, parent)
        self.addLayout(self.FrequencyInputField)

        self.OffsetInputField: FloatInputField = FloatInputField("Offset",
                                                                 Threads.DEFAULT_OFFSET, parent)
        self.addLayout(self.OffsetInputField)

        self.DataStreamInputField: FloatInputField = FloatInputField("Data Rate (Hz)",
                                                                     Threads.DEFAULT_SIMULATION_RATE_HZ, parent)
        self.addLayout(self.DataStreamInputField)

        self.ButtonStartIcon: QtGui.QIcon = QtGui.QIcon(':/img/Play.png')
        self.ButtonStopIcon: QtGui.QIcon = QtGui.QIcon(':/img/Stop.png')

        self.TogglePlottingButton: QtWidgets.QPushButton = QtWidgets.QPushButton(parent)
        self.TogglePlottingButton.setText("Start Plotting")
        self.TogglePlottingButton.setIcon(self.ButtonStartIcon)
        self.addWidget(self.TogglePlottingButton)

    def toggle_plotting(self):
        self.TogglePlottingButton.setText("Stop Plotting" if not self.IsPlotting else "Start Plotting")
        self.TogglePlottingButton.setIcon(self.ButtonStopIcon if not self.IsPlotting else self.ButtonStartIcon)
        self.IsPlotting = not self.IsPlotting
        self.AmplitudeInputField.toggle_enabled(not self.IsPlotting)
        self.FrequencyInputField.toggle_enabled(not self.IsPlotting)
        self.OffsetInputField.toggle_enabled(not self.IsPlotting)
        self.DataStreamInputField.toggle_enabled(not self.IsPlotting)

    def get_amplitude(self):
        return float(self.AmplitudeInputField.InputField.text())

    def get_frequency(self):
        return float(self.FrequencyInputField.InputField.text())

    def get_offset(self):
        return float(self.OffsetInputField.InputField.text())

    def get_datastream_simulation_rate(self):
        return float(self.DataStreamInputField.InputField.text())

    def toggle_plotting_button_enabled(self, is_enabled: bool):
        print("Toggling plotting button to " + str(is_enabled))
        self.TogglePlottingButton.setEnabled(is_enabled)


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

    def toggle_enabled(self, is_enabled: bool) -> None:
        self.InputField.setEnabled(is_enabled)
