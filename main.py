#!/usr/bin/env python3
import time
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QWidget, QLabel, QScrollArea
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
import fitz
import os
import shutil

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(main_window)
    main_window.show()
    sys.exit(app.exec_())