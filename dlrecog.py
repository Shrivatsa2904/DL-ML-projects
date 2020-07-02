from flask import Flask,render_template,request
from werkzeug import secure_filename
import base64
import pytesseract as tess
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
from skimage import data, filters
from PIL import ImageEnhance
import cv2
import numpy as np

app = Flask(__name__)
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')
@app.route("/upload")
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      f = request.files['file']
      str = f.filename
      with open(str, "rb") as image_file:
          encoded_string = base64.b64encode(image_file.read())
      imgstring = encoded_string
      imgdata = base64.b64decode(imgstring)
      filename = './image.png'
      with open(filename, 'wb') as f:
          f.write(imgdata)
          f.close()
      img = cv2.imread(filename)
      img = cv2.resize(img, None, fx=1.7, fy=1.7, interpolation=cv2.INTER_CUBIC)
      img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      kernel = np.ones((1, 1), np.uint8)
      img = cv2.dilate(img, kernel, iterations=1)
      img = cv2.erode(img, kernel, iterations=1)
      img = cv2.GaussianBlur(img, (5, 5), 0)
      img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
      height, width = img.shape[0:2]
      startRow = int(height * .15)

      startCol = int(width * .15)

      endRow = int(height * .85)

      endCol = int(width * .85)
      cimg = img[startRow:endRow, startCol:endCol]
      cv2.imwrite(filename, cimg)
      text = tess.image_to_string(img, lang="eng")
      val = text.split("\n")
      return render_template('Details.html', data=val, len=len(val))


if __name__ == '__main__':
    app.run(debug = True)