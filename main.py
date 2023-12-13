#!/usr/bin/env python3
import time
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QWidget, QLabel, QScrollArea
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
import fitz
import os
import shutil
import requests


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
        # self.dir_name = "photo"

        self.imgBrowser.mousePressEvent = self.mouse_press
        self.imgBrowser.mouseReleaseEvent = self.mouse_release

        main_window.closeEvent = self.close_event

    def update_page_label(self):
        self.page_label.setText(f"Страница {self.current_page + 1}/{self.total_pages}")

    def close_event(self, event):
        # if os.path.exists(self.dir_name):
        #     shutil.rmtree(self.dir_name)
        event.accept()

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(None, "Выберите PDF файл", "", "PDF Files (*.pdf)", options=options)
        if file_path:
            url = 'http://127.0.0.1:9990/add_file'
            with open(file_path, 'rb') as fp:
                files = {'file': fp}
                requests.post(url, files=files)

        # Логика получения 1й страницы
        # if file_path:
        #     if not os.path.exists(self.dir_name):
        #         os.mkdir(self.dir_name)
        #     with fitz.open(file_path) as doc:
        #         self.total_pages = len(doc)
        #         for i in range(len(doc)):
        #             page = doc.load_page(i)
        #             pix = page.get_pixmap(dpi=110)
        #             output = f"outfile_{i + 1}.png"
        #             pix.save(os.path.join(self.dir_name, output))
        #         time.sleep(1)
        #     self.show_image(f"{self.dir_name}/outfile_1.png")
        #     self.current_page = 0
        #     self.update_page_label()
        #     self.image_loaded = True

    def show_previous_page(self):
        if self.image_loaded:
            if self.total_pages == 1:
                self.current_page = 0
            else:
                if self.current_page == 0:
                    self.current_page = self.total_pages - 1
                else:
                    self.current_page -= 1
            self.show_image(f"{self.dir_name}/outfile_{self.current_page + 1}.png")
            self.update_page_label()

    def show_next_page(self):
        if self.image_loaded:
            if self.total_pages == 1:
                self.current_page = 0
            else:
                if self.current_page == self.total_pages - 1:
                    self.current_page = 0
                else:
                    self.current_page += 1
            self.show_image(f"{self.dir_name}/outfile_{self.current_page + 1}.png")
            self.update_page_label()

    def show_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.imgBrowser.setPixmap(pixmap)
        self.scrollArea.ensureVisible(0, 0)

    def retranslate_ui(self, main_window):
        _translate = QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "PDF Reader"))

    def mouse_press(self, event):
        if self.image_loaded:
            if event.button() == Qt.LeftButton:
                self.start_pos = event.pos()
                self.end_pos = event.pos()

    def mouse_release(self, event):
        if self.image_loaded:
            if event.button() == Qt.RightButton:
                self.end_pos = event.pos()
                self.draw_rectangle()

    def draw_rectangle(self):
        if self.start_pos and self.end_pos:
            painter = QPainter(self.imgBrowser.pixmap())
            painter.setPen(QPen(QColor("red"), 4))
            painter.drawRect(self.start_pos.x(), self.start_pos.y(), self.end_pos.x() - self.start_pos.x(),
                             self.end_pos.y() - self.start_pos.y())
            painter.end()
            self.imgBrowser.update()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(main_window)
    main_window.show()
    sys.exit(app.exec_())