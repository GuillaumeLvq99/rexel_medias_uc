#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 10:29:37 2023

@author: gleveque
"""

# https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader
# https://docs.streamlit.io/library/api-reference/widgets

# TO DO:
    # Regarder pour mettre des photos cote à cote 

import streamlit as st
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np 
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from PIL import Image # pip install Pillow
import sys
import glob
from PIL import ImageOps
import numpy as np
import cv2 as cv

def crop(image,padding=0):
    padding = np.asarray([-1*padding, -1*padding, padding, padding])
    imageSize = image.size

    # remove alpha channel
    invert_im = image.convert("RGB")

    # invert image (so that white is 0)
    invert_im = ImageOps.invert(invert_im)
    imageBox = invert_im.getbbox()
    imageBox = tuple(np.asarray(imageBox)+padding)

    cropped=image.crop(imageBox)
    print("Size:", imageSize, "New Size:", imageBox)
    #cropped.save(filePath_cleaned)
    return cropped


# Load images 
uploaded_file = st.file_uploader("Upload a picture")
if uploaded_file is not None:
    print(1)
    # https://docs.streamlit.io/library/api-reference/media/st.image
    image=Image.open(uploaded_file)
    # image.load()
    st.image(image, caption='Image to resize')
    
    
    # Define padding (je veux pas que ça se recharge tout seul)
    # https://discuss.streamlit.io/t/how-to-maintain-images-and-text-even-if-change-some-widget-on-sidebar/1390/7
    padding = st.slider('Padding', 0, 100, 0)
    # Resize
    resize = st.button('Resize')
    if resize:
        print(2)
        image_cropped = crop(image,padding=padding)
        #st.image(image_cropped)
        st.session_state['image'] = image_cropped
    try :
        st.image(st.session_state['image'])
    except :
        pass