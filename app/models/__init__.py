# models module initialization
# load the model

# Dunno why, but importing from keras.models doesn't seem to work well
# Maybe due to version problems
from tensorflow.keras.models import load_model
import os

dig_model = load_model(os.path.join(os.getcwd(), 'app' , 'models', 'MNIST_model2.h5'))

print('Current working dir for models.__init__: ', os.getcwd())

MODEL_LOADED = False
