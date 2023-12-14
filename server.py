from flask import Flask, request, redirect, url_for, jsonify
import os
import fitz
import shutil

class ServerBack():
    def __init__(self):
        self.app = Flask(__name__)
        self.dir_name = "photos"
        self.total_pages = 0

    def convert_to_image(self):
        if os.path.exists(self.dir_name):
            with fitz.open(os.path.join(self.dir_name, 'uploaded_file.pdf')) as doc:
                total_pages_file = len(doc)
                self.total_pages = total_pages_file
                for i in range(len(doc)):
                    page = doc.load_page(i)
                    pix = page.get_pixmap(dpi=110)
                    output = f'outfile_{i + 1}.png'
                    pix.save(os.path.join(self.dir_name, output))

    def send_files_to_client(self):
        if os.path.exists(self.dir_name):
            pass

create_app = ServerBack()
app = create_app.app
dir_name = create_app.dir_name


@app.route('/add_file', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'GET':
        return "Wait for add files"
    elif request.method == 'POST':
        file = request.files['file']
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        file.save(os.path.join(dir_name, 'uploaded_file.pdf'))
        create_app.convert_to_image()
        return redirect(url_for('success_uploaded'))


@app.route('/send_images', methods=['GET'])
def send_image():
    if os.path.exists(dir_name):
        images = [f'{dir_name}/outfile_{i + 1}' for i in range(create_app.total_pages)]
        return jsonify({'images': images})


@app.route('/delete_files', methods=['DELETE', 'GET'])
def delete_files():
    if request.method == 'GET':
        return 'Wait for delete files'
    elif request.method == 'DELETE':
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            return redirect(url_for('delete_success'))

@app.route('/success_uploaded')
def success_uploaded():
    return 'File uploaded successfully'

@app.route('/delete_success')
def delete_success():
    return 'Files deleted successfully'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9990)
