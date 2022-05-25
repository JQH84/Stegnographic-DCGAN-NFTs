# Importing the required libraries for the application

from turtle import width
import streamlit as st  # Streamlit to run our front end web app
import web3 as w3  # web3 library to interact with the blockchain
import os  # used to access the environment variables
from dotenv import load_dotenv  # to load the dot env file

st.header('NFT Minter')


# loading the image from the user
file = st.file_uploader("Upload your image file to mint",
                        type=["jpg", "jpeg", "png"])

# displaying the image uploaded on the screen
if file is not None:
    st.image(file, width=300)


# function to apply a filter on the image to change the color of the image
def apply_filter(image):
    from PIL import Image, ImageFilter
    image = Image.open(image)
    image = image.filter(ImageFilter.BoxBlur(radius=0.5))
    return image


# a button that will contain the minting logic function
if st.button("Transform Your image"):
    st.image(apply_filter(file), width=300)
