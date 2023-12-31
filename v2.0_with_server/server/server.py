from flask import Flask, request, redirect, url_for, jsonify, send_from_directory, send_file
import os
import fitz
import shutil
import io
import logging

logger = logging.getLogger('my_logger')
logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('server.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class ServerBack:
    app = Flask(__name__)
    dir_name = 'photos'
    total_pages = 0
    host = '0.0.0.0'
    port = 9990

    @classmethod
    def convert_to_image(cls):
        """Метод класса который разделяет pdf файл на изображения формата png"""
        if os.path.exists(cls.dir_name):
            try:
                with fitz.open(os.path.join(cls.dir_name, 'uploaded_file.pdf')) as doc:
                    total_pages_file = len(doc)
                    cls.total_pages = total_pages_file
                    for i in range(len(doc)):
                        page = doc.load_page(i)
                        pix = page.get_pixmap(dpi=110)
                        output = f'outfile_{i + 1}.png'
                        pix.save(os.path.join(cls.dir_name, output))
            except FileNotFoundError:
                logger.error('Файл не найден')
            except Exception as ex:
                logger.error(f'Ошибка при чтении файла, {ex}')


app = ServerBack.app
dir_name = ServerBack.dir_name
host = ServerBack.host
port = ServerBack.port


@app.route('/add_file', methods=['POST', 'GET'])
def upload_file():
    """Роутер который принимает файл и сохраняет его в директорию photos, далее вызывает метод нарезки файла"""
    if request.method == 'GET':
        return 'Ждем добавления файлов'
    elif request.method == 'POST':
        file = request.files['file']
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        file.save(os.path.join(dir_name, 'uploaded_file.pdf'))
        ServerBack.convert_to_image()
        return redirect(url_for('success_uploaded'))


@app.route('/check_server', methods=['GET'])
def check_server():
    return 'Сервер запущен'


@app.route('/send_images_list', methods=['GET'])
def send_images_list():
    """Роутер который в ответ на get запрос клиента присылает ему список url картинок и общее количество файлов"""
    if os.path.exists(dir_name):
        images = [f'http://{host}:{port}/{dir_name}/outfile_{i + 1}.png' for i in range(ServerBack.total_pages)]
        return jsonify({'images': images, 'total_pages': ServerBack.total_pages})


@app.route('/delete_files', methods=['DELETE', 'GET'])
def delete_files():
    """Роутер который удаляет файлы с сервера"""
    if request.method == 'GET':
        return 'Wait for delete files'
    elif request.method == 'DELETE':
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            return redirect(url_for('delete_success'))


@app.route('/save_image', methods=['POST'])
def save_image():
    """Роутер для отправки изображения клиенту"""
    data = request.get_json()
    image_name = data['image_name']
    image_path = os.path.join(dir_name, image_name)
    try:
        with open(image_path, 'rb') as f:
            image_content = f.read()
    except Exception as ex:
        logger.error(f'Ошибка при чтении файла, {ex}')
    return send_file(io.BytesIO(image_content), as_attachment=True, mimetype='image/png', download_name=image_name)


@app.route('/success_uploaded')
def success_uploaded():
    return 'File uploaded successfully'


@app.route('/delete_success')
def delete_success():
    return 'Files deleted successfully'


@app.route('/photos/<path:filename>')
def get_photo(filename):
    """Роутер который отображает изображения с нарезанного pdf"""
    return send_from_directory(dir_name, filename)


if __name__ == '__main__':
    app.run(host=host, port=port)
