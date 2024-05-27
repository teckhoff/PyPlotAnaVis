import math

import numpy
from PyQt5 import QtCore, QtGui, QtWidgets

DEFAULT_AMPLITUDE = 1.0
DEFAULT_FREQUENCY = 1.0
DEFAULT_OFFSET = 0.0
DEFAULT_SIMULATION_RATE = int(1000 / 80)  # Default simulation rate to ~80Hz
DEFAULT_SIMULATION_RATE_HZ = 80.0  # Default simulation rate to ~80Hz


class StartSimulationSignal(QtCore.QObject):
    Begin = QtCore.pyqtSignal()


class SimulationEndedSignal(QtCore.QObject):
    Ended = QtCore.pyqtSignal()


class DataStreamThread(QtCore.QThread):
    def __init__(self, output_timestamp_list: list[float], output_value_list: list[float]):
        super().__init__()

        self.ShouldSimulate = False
        self.StartSimulationSignal = StartSimulationSignal()

        self.DataStreamWorker = SimulateDataStreamWorker(output_timestamp_list, output_value_list, self)
        self.DataStreamWorker.moveToThread(self)

    def update_inputs(self, new_amplitude: float, new_frequency: float, new_offset: float,
                      new_simulation_rate: float) -> None:
        self.DataStreamWorker.set_amplitude(new_amplitude)
        self.DataStreamWorker.set_frequency(new_frequency)
        self.DataStreamWorker.set_offset(new_offset)

        if new_simulation_rate < 1:
            new_simulation_rate = 1

        self.DataStreamWorker.set_simulation_rate(new_simulation_rate)

    def get_simulation_ended_signal_from_worker(self) -> SimulationEndedSignal:
        return self.DataStreamWorker.get_simulation_ended_signal()

    def toggle_simulation(self, should_run: bool) -> None:
        if should_run:
            self.StartSimulationSignal.Begin.emit()
            return

        self.ShouldSimulate = False
        self.DataStreamWorker.end_timer()

    def run(self):
        def start_worker() -> None:
            self.DataStreamWorker.start_simulation()

        self.StartSimulationSignal.Begin.connect(start_worker)

        super().run()


class SimulateDataStreamWorker(QtCore.QObject):
    """
    A worker that simulates a continuous data stream. Meant to be run on a separate thread.
    """

    def __init__(self, output_timestamp_list: list[float], output_value_list: list[float],
                 owning_thread: DataStreamThread):
        super().__init__()

        self.Amplitude: float = DEFAULT_AMPLITUDE
        self.Frequency: float = DEFAULT_FREQUENCY
        self.Offset: float = DEFAULT_OFFSET
        self.DataRate: int = DEFAULT_SIMULATION_RATE
        self.DataTimer = QtCore.QTimer()
        self.DataTimer.moveToThread(owning_thread)
        self.DataTimer.setInterval(self.DataRate)
        self.DataTimer.timeout.connect(self.simulate)
        self.PreviousTimestamp = -1.0
        self.simulation_begin_timestamp = -1.0

        self.OwningThread = owning_thread
        self.SimulationEndedSignal = SimulationEndedSignal()

        self.OutputTimestampList: list[float] = output_timestamp_list
        self.OutputValueList: list[float] = output_value_list

    def get_sine_value(self, time: float) -> float:
        """
        Returns the result of a sin function account for amplitude, frequency, and offset.
        :param time: Time, in seconds.
        :return: The resulting value of the sin.
        """
        return self.Amplitude * numpy.sin((2 * numpy.pi * self.Frequency) * time + self.Offset)

    def set_amplitude(self, new_amplitude: float) -> None:
        self.Amplitude = new_amplitude

    def set_frequency(self, new_frequency: float) -> None:
        self.Frequency = new_frequency

    def set_offset(self, new_offset: float) -> None:
        self.Offset = new_offset

    def update_lists(self, new_timestamp_list: list[float], new_value_list: list[float]) -> None:
        self.OutputTimestampList = new_timestamp_list
        self.OutputValueList = new_value_list

    def set_simulation_rate(self, new_simulation_rate: float) -> None:
        """
        Sets the time in milliseconds between simulation cycles.
        :param new_simulation_rate: The simulation rate in hertz.
        """
        self.DataRate = int((1 / new_simulation_rate) * 1000)
        self.DataTimer.setInterval(self.DataRate)

    def get_simulation_ended_signal(self) -> SimulationEndedSignal:
        return self.SimulationEndedSignal

    def start_simulation(self) -> None:
        """
        Starts the continuous data stream simulation. Runs until end_simulation() is called.
        """
        if self.OwningThread.ShouldSimulate:
            return

        self.OwningThread.ShouldSimulate = True
        self.simulation_begin_timestamp = QtCore.QDateTime.currentMSecsSinceEpoch()
        previous_timestamp = -1.0

        """while self.OwningThread.ShouldSimulate:
            time_elapsed = (QtCore.QDateTime.currentMSecsSinceEpoch() - simulation_begin_timestamp) / 1000

            if math.isclose(time_elapsed, previous_timestamp):
                continue

            sine_value = self.get_sine_value(time_elapsed)

            previous_timestamp = time_elapsed

            self.OutputTimestampList.append(time_elapsed)
            self.OutputValueList.append(sine_value)

            self.OwningThread.wait(self.DataRate)

        self.SimulationEndedSignal.Ended.emit()"""
        self.DataTimer.start()

    def simulate(self) -> None:
        if not self.OwningThread.ShouldSimulate:
            self.end_timer()

        time_elapsed = (QtCore.QDateTime.currentMSecsSinceEpoch() - self.simulation_begin_timestamp) / 1000

        sine_value = self.get_sine_value(time_elapsed)

        self.PreviousTimestamp = time_elapsed

        self.OutputTimestampList.append(time_elapsed)
        self.OutputValueList.append(sine_value)

    def end_timer(self) -> None:
        self.DataTimer.stop()
        self.SimulationEndedSignal.Ended.emit()
        return
