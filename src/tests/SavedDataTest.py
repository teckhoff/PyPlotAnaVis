import PyQt5
from PyQt5 import QtCore
import Widgets
import pytestqt
import numpy
import math


def test_saving_functionality(qtbot):
    window = Widgets.AppWindow()
    qtbot.addWidget(window)

    simulation_timestamp = -1
    simulation_timestamp_data = []
    simulation_data = []

    sim_timer = QtCore.QTimer()
    sim_timer.setInterval(1000 * 65)
    sim_timer.setSingleShot(True)

    # window.DataStreamThread.set_test(simulation_timestamp_data, simulation_data)

    def click_plotting_button():
        window.toggle_plotting()

    def load_data_from_file():
        nonlocal simulation_timestamp, simulation_timestamp_data, simulation_data
        if sim_timer.isActive():
            return False

        click_plotting_button()

        loaded_data = numpy.load(str(simulation_timestamp) + ".npy")
        # print(loaded_data[0])
        # print(simulation_timestamp_data)

        calculated_data = window.DataStreamThread.DataStreamWorker.get_calculated_data()

        counter = 0
        for data in loaded_data:
            timestamp, value = data[0], data[1]
            print("Saved: " + str(timestamp) + " | In List: " + str(simulation_timestamp_data[counter])
                  + " | Calculated: " + str(calculated_data[counter][0]))
            assert (math.isclose(timestamp, simulation_timestamp_data[counter]))
            counter += 1

        return True

    def assert_lol():
        assert (load_data_from_file())

    sim_timer.timeout.connect(load_data_from_file)

    click_plotting_button()
    simulation_timestamp = window.SimulationStarted
    sim_timer.start()

    qtbot.waitUntil(assert_lol, timeout=(1000 * 100))
