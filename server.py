from flask import Flask, request, redirect, url_for
import os
import fitz
import shutil

app = Flask(__name__)
dir_name = "photos"

@app.route('/add_file', methods=['POST' ,'GET'])
def upload_file():
    if request.method == 'GET':
        return "Wait for add files"
    elif request.method == 'POST':
        file = request.files['file']
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        file.save(os.path.join(dir_name, 'uploaded_file.pdf'))
        convert_to_image()
        return redirect(url_for('success_uploaded'))

@app.route('/success_uploaded')
def success_uploaded():
    return 'File uploaded successfully'

@app.route('/delete_success')
def delete_success():
    return 'Files deleted successfully'

def convert_to_image():
    if os.path.exists(dir_name):
        with fitz.open(os.path.join(dir_name, 'uploaded_file.pdf')) as doc:
            total_pages = len(doc)
            for i in range(len(doc)):
                page = doc.load_page(i)
                pix = page.get_pixmap(dpi=110)
                output = f'outfile_{i + 1}.png'
                pix.save(os.path.join(dir_name, output))

@app.route('/delete_files', methods=['DELETE', 'GET'])
def delete_files():
    if request.method == 'GET':
        return 'Wait for delete files'
    elif request.method == 'DELETE':
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            return redirect(url_for('delete_success'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9990)
