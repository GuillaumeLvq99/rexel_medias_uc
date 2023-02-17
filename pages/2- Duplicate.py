#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 10:29:37 2023

@author: gleveque
"""

# https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader
# https://docs.streamlit.io/library/api-reference/widgets

import streamlit as st
import pandas as pd, numpy as np
import os
import imagehash
from PIL import Image
import itertools
from pandarallel import pandarallel
from matplotlib import pyplot
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
import plotly.io as pio
from sklearn import metrics
pio.renderers.default='browser'
import plotly.express as px

hashfuncs = {
	'ahash': imagehash.average_hash,
	'phash': imagehash.phash,
	'dhash': imagehash.dhash,
	'whash-haar': imagehash.whash,
	'whash-db4': lambda img: imagehash.whash(img, mode='db4'),
	'colorhash': imagehash.colorhash,
}

def distance_hash(file1, file2, func):
    '''
    Returns a boolean indicating if file1 and file2 are duplicates, 
    based distance between their hashes
    
            Parameters:
                    file1 (str): Path to an image
                    file2 (str): Path to an image
                    func: Hash function to compute the distance
    
            Returns:
                    (int): Hash distance between the 2 images
    '''
    try:
        # TODO : benchmark distances and thresh
        img1 = Image.open(file1) ; hash1 = func(img1)
        img2 = Image.open(file2); hash2 = func(img2)
        
        def distance(hash1, hash2):
            return hash1 - hash2
    
        return distance(hash1, hash2)
    except FileNotFoundError: # Caused by .eps files --> TODO : fix !
        return np.nan
    
def distance_hash_2(img1, img2, func):
    '''
    Returns a boolean indicating if file1 and file2 are duplicates, 
    based distance between their hashes
    
            Parameters:
                    file1 (str): Path to an image
                    file2 (str): Path to an image
                    func: Hash function to compute the distance
    
            Returns:
                    (int): Hash distance between the 2 images
    '''
    try:
        # TODO : benchmark distances and thresh
        hash1 = func(img1)
        hash2 = func(img2)
        
        def distance(hash1, hash2):
            return hash1 - hash2
    
        return distance(hash1, hash2)
    except FileNotFoundError: # Caused by .eps files --> TODO : fix !
        return np.nan

# Load images 
uploaded_file = st.file_uploader("Upload a first picture")
uploaded_file_2 = st.file_uploader("Upload a second picture")



if uploaded_file is not None and uploaded_file_2 is not None:
    image=Image.open(uploaded_file)
    image_2=Image.open(uploaded_file_2)
    col1, col2 = st.columns(2)

    # Add the images to the columns
    with col1:
        
        # Convertir l'image en mode RGBA si elle ne l'est pas déjà
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        
        # Créer un nouveau fond blanc de la même taille que l'image
        new_background = Image.new("RGBA", image.size, (255, 255, 255))
        
        # Combiner l'image d'origine avec le nouveau fond blanc
        result = Image.alpha_composite(new_background, image)
        
        st.image(result, use_column_width=True)
    
    with col2:
        st.image(image_2, use_column_width=True)
        
    #st.image([image,image_2])
    #st.image(image_2, caption='Image to resize')
    distance_dhash = distance_hash_2(result, image_2, func=hashfuncs['dhash'])
    distance_phash = distance_hash_2(result, image_2, func=hashfuncs['phash'])

    
    # Dhash < 4
    # Phash < ?
    #distance
    
    # Selon le résultat définir une couleur
    if distance_dhash < 4 and distance_phash < 12:
        st.header("They are simiar")
        st.write("difference dhash: {}".format(distance_dhash))
        st.write("difference phash: {}".format(distance_phash))
    else :
        st.header("They are different")
        st.write("difference dhash: {}".format(distance_dhash))
        st.write("difference phash: {}".format(distance_phash))


    #st.write(distance)
    
    # Definir les distances et écrire si dupliquées ou non