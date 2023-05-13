import requests
from werkzeug.utils import secure_filename
import mammoth
import fitz
from flask import Flask, request
import io

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def hello_world(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#flask.Request>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>.
    """
    return 'Hello, World!'


@app.route('/extract_document', methods=['POST'])
def extract_document(request):
    if 'file' not in request.files:
        return 'No file part in the request', 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    mimetype = file.mimetype
    print(f'File: {filename}')
    print(f'Mimetype: {mimetype}')
    if mimetype == "application/pdf":
        doc = fitz.open(stream=file.read(), filetype='pdf')
        texts = []
        for page_num, page in enumerate(doc):
            text = page.get_text()
            print('PDF detected')
            print(text)
            texts.append(text)
        return {texts: texts}, 200
    elif mimetype in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/octet-stream"]:
        print("Testing file read")
        b = bytearray(file.read())
        result = mammoth.extract_raw_text(io.BytesIO(b))
        text = result.value
        print(text)
        return {texts: text}, 200

    return "Error processing file", 400