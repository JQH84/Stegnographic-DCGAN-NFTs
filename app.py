# Importing the required libraries for the application

from ctypes import alignment
from turtle import width
import streamlit as st  # Streamlit to run our front end web app
import web3 as w3  # web3 library to interact with the blockchain
import os  # used to access the environment variables
from dotenv import load_dotenv  # to load the dot env file

# Side Bar
st.sidebar.title('Welcome !')
st.sidebar.image('https://cdn.pixabay.com/photo/2021/11/26/10/45/nft-6825614_960_720.png', width=300)

option = st.sidebar.selectbox("Select Your Option", options=[
                              'Transform Image', 'Mint', 'Check encoded Message'])

st.write(option)

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
    image = image.filter(ImageFilter.EMBOSS)
    return image


# a button that will contain the minting logic function
if st.button("Transform Your image"):
    st.image(apply_filter(file), width=300)

# function to use the stegano library to encode a msg into an image


def hide_msg(image, msg):
    from stegano import lsb
    lsb.hide(image, msg).save('./encryotedimage.png')


# get the hidden input from the user and store in var
input_txt = st.text_input('Type Here')


def hash_input(txt):
    import hashlib
    sha = hashlib.sha256()
    text = txt.encode()
    sha.update(text)
    return sha.hexdigest()


if st.button('Enter a messege to embed in the image'):
    hide_msg(image=apply_filter(file), msg=hash_input(input_txt))

# function to decode that msg
def get_msg(image):
    from stegano import lsb
    return lsb.reveal(image)


# Action button to decrypt from the saved image
if st.button('click to decrypt'):
    decrypt = get_msg(image='./encryotedimage.png')
    st.write(f'The Hidden Message is : "{decrypt}"')
