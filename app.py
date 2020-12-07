from flask import Flask, render_template, request
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcp_creds.json'

app = Flask(__name__)
UPLOAD_LOCATION = 'tempUploads'
app.config['UPLOAD_LOCATION'] = UPLOAD_LOCATION


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_LOCATION'], file.filename)
    file.save(f)
    import io


    from google.cloud import vision
    from google.cloud.vision_v1 import types

    client = vision.ImageAnnotatorClient()

    file_name = os.path.join(app.config['UPLOAD_LOCATION'], file.filename)

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    x= print('Texts:')

    for text in texts:
      result = print('\n"{}"'.format(text.description))

    return render_template('success.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)










