

@app.route('/extractDocument', methods=['POST'])
def extract_document():
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    mimetype = file.mimetype

    print(f'File: {filename}')
    print(f'Mimetype: {mimetype}')

    if mimetype == "application/pdf":
        reader = PdfFileReader(file)
        text = reader.getPage(0).extractText()
        print('PDF detected')
        print(text)
    elif mimetype in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        with file:
            b = bytearray(file.read())
            result = mammoth.extract_raw_text(io.BytesIO(b))
            text = result.value
            print(text)
    else:
        return 'Unsupported file type', 400

    return 'Success', 200