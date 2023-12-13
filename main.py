#!/usr/bin/env python3
import time
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QWidget, QLabel, QScrollArea
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
import fitz
import os
import shutil

class Ui_MainWindow(object):
    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.setFixedSize(920, 780)
        self.centralwidget = QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")

        self.button_load = QPushButton(self.centralwidget)
        self.button_load.setGeometry(10, 10, 140, 35)
        self.button_load.setText("Открыть файл")

        self.button_page = QPushButton(self.centralwidget)
        self.button_page.setGeometry(160, 10, 180, 35)
        self.button_page.setText("Сохранить страницу")

        self.page_label = QLabel(self.centralwidget)
        self.page_label.setGeometry(400, 10, 120, 35)
        self.page_label.setAlignment(Qt.AlignCenter)

        self.button_back = QPushButton(self.centralwidget)
        self.button_back.setGeometry(700, 10, 100, 35)
        self.button_back.setText("<")
        self.button_forward = QPushButton(self.centralwidget)
        self.button_forward.setGeometry(820, 10, 100, 35)
        self.button_forward.setText(">")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(10, 50, 920, 730)
        self.scrollArea.setWidgetResizable(True)

        self.imgBrowser = QLabel()
        self.scrollArea.setWidget(self.imgBrowser)
        main_window.setCentralWidget(self.centralwidget)
        self.retranslate_ui(main_window)

        self.button_load.clicked.connect(self.open_file_dialog)

        self.current_page = 0
        self.total_pages = 0
        self.image_loaded = False
        self.button_back.clicked.connect(self.show_previous_page)
        self.button_forward.clicked.connect(self.show_next_page)
        self.start_pos = None
        self.end_pos = None
        self.dir_name = "photo"

        self.imgBrowser.mousePressEvent = self.mouse_press
        self.imgBrowser.mouseReleaseEvent = self.mouse_release

        main_window.closeEvent = self.close_event

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(main_window)
    main_window.show()
    sys.exit(app.exec_())