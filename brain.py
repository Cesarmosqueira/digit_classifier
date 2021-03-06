import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.utils import to_categorical
#import matplotlib.pyplot as plt


from PIL import Image, ImageDraw, ImageOps, ImageFilter


# load the model we saved
model = keras.models.load_model('DigitRecognizerbak.h5')

def modelfit(x, y):
    c = np.array([0] * 10)
    c[y] = 1
    c = np.array([c])
    print(c.shape)
    model.fit(x, c)

def Predict(path):
    im = Image.open(path)
    im = ImageOps.grayscale(im) # .filter(ImageFilter.CONTOUR))
    im = im.resize((28,28))
    im = im.filter(ImageFilter.DETAIL)
    im = np.asarray(im)
    im = im/255
    #plt.imshow(im)
    #plt.show()
    im = im.reshape(1,28,28,1)
    return model.predict(im).argmax(), im
    
