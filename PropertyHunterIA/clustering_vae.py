#!/usr/bin/env python
# coding: utf-8

# In[9]:


import numpy as np
from pathlib import Path

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from sklearn.cluster import KMeans
import pickle


# In[2]:


basepath = Path('.')
imgpath = basepath/'data'/'image'
modelpath = basepath/'models'


# In[ ]:


# load autoencoder
encoder = load_model(modelpath/'encoder_v2.h5', compile=False)


# In[4]:


# load cluster model
kmeans_file = modelpath/'kmeans_v2.pkl'
kmeans_model = pickle.load(open(kmeans_file, 'rb'))


# In[5]:


#test_img = imgpath/'6 Derbyshire view2.png'


# In[6]:


def predict_image_cluster(testimage):
    """Predict cluster number of image

    Parameters:
    imagepath: image path using pathlib.Path format

    Returns:
    int: cluster number, ranges from 0 to 6

   """
    img = image.load_img(testimage, target_size=(64, 64))
    img_data = image.img_to_array(img)
    img_data = np.expand_dims(img_data, axis=0)
    img_data = img_data.flatten()
    img_data2 = []
    img_data2.append(img_data)
    img_data2 = np.array(img_data2)
    img_data2 = img_data2/255
    encoded = encoder.predict(img_data2)
    prediction = kmeans_model.predict(encoded)
    print(f'each score {int(prediction)}')
    return int(prediction)


# In[ ]:


#predict_image_cluster(test_img)


# In[ ]:




