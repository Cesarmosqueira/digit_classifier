import numpy as np
import tensorflow as tf
from tensorflow import keras


from PIL import Image, ImageDraw, ImageOps, ImageFilter


# load the model we saved
model = keras.models.load_model('DigitRecognizer.h5')
model.compile(loss='categorical_crossentropy',
      optimizer='adam',
      metrics=['accuracy'])

def Predict(path):
    im = Image.open(path)
    im = ImageOps.grayscale(im.filter(ImageFilter.CONTOUR))
    im = im.resize((28,28))
    im = np.asarray(im)
    im = im/255
    im = im.reshape(1,28,28,1)
    return model.predict(im).argmax()
    
