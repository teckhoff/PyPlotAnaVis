import sys

from PyQt5 import QtWidgets

import Widgets


def initialize_application():
    app = QtWidgets.QApplication(sys.argv)
    window = Widgets.AppWindow()

    window.show()
    sys.exit(app.exec_())


def main():
    initialize_application()


if __name__ == "__main__":
    main()
