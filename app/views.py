# views.py

from flask import render_template
from flask import send_file, request
from app import app

# I'm going to avoid making this too complex and do the prediction thing right here
import json
import re
import base64
import io
from app.models import dig_model, MODEL_LOADED
from PIL import Image
import numpy as np

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/reference')
def reference():
    return render_template('reference.html')

@app.route('/download')
def download():
    return send_file('static/WhoDigit_Client.apk', as_attachment=True, attachment_filename="WhoDigit Client.apk")

# Now for the actual predictor API

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    base64EncodedPic = str(request.args['pic'])

    # Tomfoolery: apparently the plusses in the string passed get converted into spaces
    # Better use POST, TODO: change this in client

    base64EncodedPic = re.sub(' ', '+', base64EncodedPic)

    print('The encoded pic has: ' + str(len(base64EncodedPic)) + ' characters. Dividing it by 4 gives ' + str(len(base64EncodedPic)/4))
    dig_pic = Image.open(io.BytesIO(base64.b64decode(base64EncodedPic)))

    print('Yay! I got an image:')
    if dig_pic.size != (28, 28):
        dig_pic = dig_pic.resize((28, 28))

    dig_inp = np.array(dig_pic)
    print(dig_inp)
    print(dig_inp.shape)

    # Recall that the image currently has 3 channels
    dig_inp = dig_inp[:, :, 0]
    print(dig_inp.shape)
    dig_inp = np.reshape(dig_inp, (1, 28, 28, 1))

    pred = dig_model.predict(dig_inp)
        
    CLASSES = np.array(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

    # Gives top 2 predictions as a list
    preds_w = [CLASSES[np.argmax(pred, axis=-1)][0], CLASSES[np.argmax(np.delete(pred, np.argmax(pred, axis=-1)), axis=-1)]]

    print(preds_w)

    resp = {'pred': preds_w}
    return json.dumps(resp)
