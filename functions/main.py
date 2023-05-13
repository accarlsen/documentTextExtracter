import requests

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


def extract_document(request):
    if 'file' not in request.files:
        return 'No file part in the request', 400

    # file = request.files['file']
    # filename = secure_filename(file.filename)
    # mimetype = file.mimetype

    # print(f'File: {filename}')
    # print(f'Mimetype: {mimetype}')

    # if mimetype == "application/pdf":
    #     reader = PdfFileReader(file)
    #     text = reader.getPage(0).extractText()
    #     print('PDF detected')
    #     print(text)
    # elif mimetype in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
    #     with file:
    #         b = bytearray(file.read())
    #         result = mammoth.extract_raw_text(io.BytesIO(b))
    #         text = result.value
    #         print(text)

    return 'Success', 200