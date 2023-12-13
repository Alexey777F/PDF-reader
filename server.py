from flask import Flask, request

app = Flask(__name__)

@app.route('/add_file', methods=['POST' ,"GET"])
def upload_file():
    if request.method == "GET":
        return "HELLO"
    file = request.files['file']
    file.save('uploaded_image.pdf')
    return 'File uploaded successfully'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9990)