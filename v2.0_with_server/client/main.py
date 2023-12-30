from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QWidget, QLabel, QScrollArea, QComboBox, QMessageBox
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
import requests
import os
import logging

logger = logging.getLogger('my_logger')
logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('client.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class UiMainWindow(object):
    def setup_ui(self, main_window):
        main_window.setObjectName('MainWindow')
        main_window.setFixedSize(920, 780)
        self.centralwidget = QWidget(main_window)
        self.centralwidget.setObjectName('centralwidget')

        self.menu_button = QComboBox(self.centralwidget)
        self.menu_button.setGeometry(10, 10, 140, 35)
        self.menu_button.addItem('Меню')
        self.menu_button.addItem('Открыть файл')
        self.menu_button.addItem('Сохранить страницу как картинку')

        self.page_label = QLabel(self.centralwidget)
        self.page_label.setGeometry(400, 10, 120, 35)
        self.page_label.setAlignment(Qt.AlignCenter)

        self.button_back = QPushButton(self.centralwidget)
        self.button_back.setGeometry(700, 10, 100, 35)
        self.button_back.setText('<')
        self.button_forward = QPushButton(self.centralwidget)
        self.button_forward.setGeometry(820, 10, 100, 35)
        self.button_forward.setText('>')
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(10, 50, 920, 730)
        self.scrollArea.setWidgetResizable(True)

        self.imgBrowser = QLabel()
        self.scrollArea.setWidget(self.imgBrowser)
        main_window.setCentralWidget(self.centralwidget)
        self.retranslate_ui(main_window)

        self.menu_button.activated[str].connect(self.handle_menu_option)

        self.images = []
        self.server_socket = 'http://127.0.0.1:9990'
        self.current_page = 0
        self.total_pages = 0
        self.image_loaded = False
        self.button_back.clicked.connect(self.show_previous_page)
        self.button_forward.clicked.connect(self.show_next_page)
        self.start_pos = None
        self.end_pos = None

        self.imgBrowser.mousePressEvent = self.mouse_press
        self.imgBrowser.mouseReleaseEvent = self.mouse_release

        main_window.closeEvent = self.close_event

    def update_page_label(self):
        """Метод который обновляет лейбл с отображением количества страниц и текущей страницы"""
        self.page_label.setText(f'Страница {self.current_page + 1}/{self.total_pages}')

    def handle_menu_option(self, option):
        """Метод QComboBox разделения кнопок и вызываемых ими других методов"""
        if option == 'Открыть файл':
            self.open_file_dialog()
        elif option == 'Сохранить страницу как картинку':
            self.save_page_as_image()

    def is_server_available(self):
        """Метод для проверки доступности сервера"""
        try:
            response = requests.get(f'{self.server_socket}/check_server')
            if response.status_code == 200:
                return True
            else:
                logger.error(f'Ошибка при подключении к серверу, код ошибки: {response.status_code}')
                return False
        except requests.exceptions.ConnectionError:
            logger.error('Ошибка при подключении к серверу, сервер недоступен')
            return False

    def request_url(self, router, method, **kwargs):
        """Метод запроса на сервер в зависимости от передаваемых параметров"""
        if not self.is_server_available():
            return False
        else:
            url = os.path.join(self.server_socket, router)
            if method == 'get':
                response = requests.get(url)
            elif method == 'post':
                if 'files' in kwargs:
                    files = kwargs.pop('files', None)
                    response = requests.post(url, files=files)
                else:
                    json_data = kwargs.pop('json', None)
                    response = requests.post(url, json=json_data)
            elif method == 'delete':
                response = requests.delete(url)
            else:
                logger.error('Неподдерживаемый метод')
                raise ValueError('Неподдерживаемый метод')
            return response

    def close_event(self, event):
        """Метод удаления файлов на сервере при закрытии приложения"""
        if self.image_loaded and self.is_server_available():
            self.request_url('delete_files', 'delete')
        event.accept()

    def open_file_dialog(self):
        """Метод который отправляет файл на сервер, а потом показывает изображения с сервера"""
        if not self.is_server_available():
            QMessageBox.warning(None, "Сервер недоступен", "Сервер недоступен. Попробуйте позже.")
            return
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(None, "Выберите PDF файл", "", "PDF Files (*.pdf)", options=options)
        if file_path:
            try:
                with open(file_path, 'rb') as fp:
                    files = {'file': fp}
                    self.request_url('add_file', 'post', files=files)
                    response = self.request_url('send_images_list', 'get')
                    images = response.json()['images']
                    self.images = images
                    server_total_pages = response.json()['total_pages']
                    self.total_pages = server_total_pages
                self.show_image(self.images[0])
                self.current_page = 0
                self.update_page_label()
                self.image_loaded = True
            except FileNotFoundError:
                logger.error('Файл не найден')
            except PermissionError:
                logger.error('Нет разрешения на доступ к файлу pdf')
            except requests.exceptions.RequestException as e:
                logger.error(f'Произошла ошибка при запросе: {e}')
            except Exception as e:
                logger.error(f'Произошла ошибка: {e}')

    def save_page_as_image(self):
        """Метод сохранения изображения которое прислал сервер"""
        if self.image_loaded and self.is_server_available():
            image_name = f'outfile_{self.current_page + 1}.png'
            response = self.request_url('save_image', 'post', json={'image_name': image_name})
            try:
                with open(f'saved_image{self.current_page + 1}.png', 'wb') as f:
                    f.write(response.content)
            except Exception as e:
                logger.error(f'Произошла ошибка при сохранении: {e}')
        elif self.image_loaded and not self.is_server_available():
            QMessageBox.warning(None, 'Сервер недоступен', 'Сервер недоступен. Попробуйте позже.')
            return

    def show_previous_page(self):
        """Метод который показывает предыдущую страницу"""
        if self.image_loaded:
            if self.total_pages == 1:
                self.current_page = 0
            else:
                if self.current_page == 0:
                    self.current_page = self.total_pages - 1
                else:
                    self.current_page -= 1
            self.show_image(f'{self.server_socket}/photos/outfile_{self.current_page + 1}.png')
            self.update_page_label()

    def show_next_page(self):
        """Метод который показывает следующую страницу"""
        if self.image_loaded:
            if self.total_pages == 1:
                self.current_page = 0
            else:
                if self.current_page == self.total_pages - 1:
                    self.current_page = 0
                else:
                    self.current_page += 1
            self.show_image(f'{self.server_socket}/photos/outfile_{self.current_page + 1}.png')
            self.update_page_label()

    def show_image(self, image_url):
        """Метод отображения страниц"""
        if not self.is_server_available():
            QMessageBox.warning(None, 'Сервер недоступен', 'Сервер недоступен. Попробуйте позже.')
            return
        pixmap = QPixmap()
        pixmap.loadFromData(requests.get(image_url).content)
        self.imgBrowser.setPixmap(pixmap)
        self.scrollArea.ensureVisible(0, 0)

    def retranslate_ui(self, main_window):
        _translate = QCoreApplication.translate
        main_window.setWindowTitle(_translate('MainWindow', 'PDF Reader'))

    def mouse_press(self, event):
        """Метод начала рисования прямоугольника при нажатии левой клавишей мыши"""
        if self.image_loaded:
            if event.button() == Qt.LeftButton:
                self.start_pos = event.pos()
                self.end_pos = event.pos()

    def mouse_release(self, event):
        """Метод конца рисования прямоугольника при нажатии правой клавишей мыши"""
        if self.image_loaded:
            if event.button() == Qt.RightButton:
                self.end_pos = event.pos()
                self.draw_rectangle()

    def draw_rectangle(self):
        """Метод рисования прямоугольника"""
        if self.start_pos and self.end_pos:
            painter = QPainter(self.imgBrowser.pixmap())
            painter.setPen(QPen(QColor('red'), 4))
            painter.drawRect(self.start_pos.x(), self.start_pos.y(), self.end_pos.x() - self.start_pos.x(),
                             self.end_pos.y() - self.start_pos.y())
            painter.end()
            self.imgBrowser.update()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(main_window)
    main_window.show()
    sys.exit(app.exec_())