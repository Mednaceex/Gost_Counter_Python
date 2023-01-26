import sys
from PyQt5.QtWidgets import QApplication
import PyQt5.QtGui

from windows.main_window import Window


def main():
    app = QApplication([])
    application = Window()
    application.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
