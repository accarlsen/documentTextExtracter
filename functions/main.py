import requests
from werkzeug.utils import secure_filename
import mammoth
import fitz
from flask import Flask, request
import io
import re
from docx import Document
import firebase_admin
from firebase_admin import auth

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
    id_token = request.headers.get('Authorization')
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        # Authenticated, proceed with function logic
    except auth.InvalidIdTokenError:
        # Invalid token, handle unauthorized access
        return 'Unauthorized', 401

    if 'file' not in request.files:
        return 'No file part in the request', 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    mimetype = file.mimetype
    print(f'File: {filename}')
    if filename.split(".")[len(filename.split(".")) - 1] == "doc":
        return "Cannot process .doc, try .docx", 400
    print(f'Mimetype: {mimetype}')
    if mimetype == "application/pdf":
        print('PDF detected')
        doc = fitz.open(stream=file.read(), filetype='pdf')
        texts = []
        for page_num, page in enumerate(doc):
            text = page.get_text()
            texts.append(str(text))
        return {'text': texts}, 200
    elif mimetype in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/octet-stream"]:
        print("Testing file read")
        b = bytearray(file.read())
        print("Bytes found")
        try:
            result = mammoth.extract_raw_text(io.BytesIO(b))
            print("Ran mammoth")
            text = result.value
            print(text)
            return {'text': text}, 200
        except Exception as e:
            return {'error': str(e)}, 400

    return "Error processing file", 400
