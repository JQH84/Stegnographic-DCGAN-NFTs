# Importing the required libraries for the application

# used to ensure proper byte size inputs for the Fernet encryption method
from base64 import b64decode, b64encode
from encryption import *
from IpsfAccess import *  # access to the helper function for using ipfs
import streamlit as st  # Streamlit to run our front end web app
from web3 import Web3  # web3 library to interact with the blockchain
import os  # used to access the environment variables
from pathlib import Path
import pandas as pd
import requests as rq
import json
import tensorflow as tf
from PIL import Image, ImageFilter  # image IO
from dotenv import load_dotenv  # to load the dot env file
load_dotenv()
# initiate the connection to the blockchain
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# function to connect to the NFT contract


@st.cache(allow_output_mutation=True)
def load_contract():
    # Load the contract ABI
    with open(Path('./nft_abi.json')) as f:
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    return w3.eth.contract(address=contract_address, abi=contract_abi)


# Load the contract
contract = load_contract()

#################
# Side Bar Menu #
#################

# Side Bar
st.sidebar.markdown(
    "<h1 style='text-align: center; color: green; font-size:40px;'>Mint Your NFT </h1>", unsafe_allow_html=True)

option = st.sidebar.selectbox("Select an Option from the Menu", options=[
    'Transform Image', 'Mint', 'Check encoded Message'])

st.sidebar.image(
    'https://cdn.pixabay.com/photo/2021/11/26/10/45/nft-6825614_960_720.png', width=300)

######################################################################################
# Loading the image from the user and encrypting a message into it using a password  #
######################################################################################

if option == 'Transform Image':
    st.header('1. Transform Your Image and encode a secret message')

    # loading the image from the user

    file = st.file_uploader("Upload your image file to mint",
                            type=["jpg", "jpeg", "png"])

    # displaying the image uploaded on the screen
    if file is not None:
        st.image(file, width=300)

    # function to apply a filter on the image to change the color of the image /
    @st.cache(allow_output_mutation=True)
    def apply_filter(image):
        image = Image.open(image)
        image = image.filter(ImageFilter.EMBOSS)
        return image

    # a button that will contain the minting logic function
    if st.button("Transform Your image"):
        if file == None:
            st.write('Please Select An Image ')
        else:
            st.image(apply_filter(file), width=300)

    # get the hidden input from the user and store in var
    input_txt = st.text_input('Enter a message to embed in the image')
    password_txt = st.text_input(
        'Enter a Password to encrypt the message', type='password')

    # action to imbed the msg into the image and ave it to the folder for pinata
    if st.button('Click to Embed'):
        hash = hash_input(password_txt)
        hide_msg(image=apply_filter(file), msg=encrypt(
            input_txt.encode(), hash))  # issue

    # Action button to decrypt from the saved image
    if st.button('click to decrypt'):
        msg_from_image = get_msg(image='encryotedimage.png')
        decrypted = decrypt(msg_from_image.encode(),
                            hash_input(password_txt)).decode()
        st.write(f'The Hidden Message is : "{decrypted}"')

#######################################
# Minting the image to the blockchain #
#######################################
elif option == 'Mint':
    st.header('2. NFT Minter')
    #st.text('Choose the modified image to mint')
    #image_to_mint = st.image('./encryotedimage.png')
    #image_file = st.file_uploader("Upload the modified image to mint", type=["jpg", "jpeg", "png"])
    with open(Path('./encryotedimage.png'), 'rb') as f:
        image_file = f.read()
        owner = st.text_input('Public ETH Address')
    image_name = st.text_input('Give Your Image a name for the blockchain')
    nickname_minter = st.text_input('Enter a Nickname for yourself')

    # send image to IPFS and get the image uri
    @st.cache(allow_output_mutation=True)
    def pin_image(image_name, image_file):
        # Pin the file to IPFS with Pinata
        ipfs_file_hash = pin_file_to_ipfs(image_file)  # issue

        # Build a token metadata file for the artwork
        token_json = {
            "name": image_name,
            "image": ipfs_file_hash
        }
        json_data = convert_data_to_json(token_json)

        # Pin the json to IPFS with Pinata
        json_ipfs_hash = pin_json_to_ipfs(json_data)

        return json_ipfs_hash, ipfs_file_hash

    if st.button('Click to Mint'):
        ipfs_hash, file_hash = pin_image(image_name, image_file)
        image_uri = f"ipfs://{ipfs_hash}"

        tx_hash = contract.functions.mintImage(
            owner,
            image_name,
            nickname_minter,
            image_uri

        ).transact({'from': owner, 'gas': 1000000})

        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("Transaction receipt mined:")
        st.write(dict(receipt))
        st.write(
            "You can view the pinned metadata file with the following IPFS Gateway Link")
        st.markdown(
            f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{file_hash})", unsafe_allow_html=True)
        
##################################################################################
# Retrieve the image from the blockchain and decrypt the secret message within it #
##################################################################################
else:
    st.header('3. Get NFT and Decrypt the message')
    password = st.text_input('Enter your password to decrypt the message' , type='password')
    address = st.text_input('Enter your public ETH address to check for NFTs')
    #if st.button('Click to Check'):
    balanceOf = contract.functions.balanceOf(address).call()
    NFT_item = st.selectbox('Select the NFT you want to retrieve', [i for i in range(balanceOf)])
    NFT = contract.functions.userMint(NFT_item).call()
    NFT_df = pd.DataFrame(NFT)
            
    uri_image = NFT[3].split('/')[2]
    uri_image = f"https://gateway.pinata.cloud/ipfs/{uri_image}"
    st.write(uri_image)
    image_url = rq.get(uri_image).content
    
    # convert bytes to json
    image_json = json.loads(image_url)
    st.write(image_json)
    image_url = f"https://gateway.pinata.cloud/ipfs/{image_json['image']}"
    st.table(NFT_df)
    # save image to local
    with open(Path('./decryptedimage.png'), 'wb') as f:
        f.write(rq.get(image_url).content)
    image_to_decrypt = st.image(image_url, width=300)
    
        
    if st.button('click to decrypt'):
        msg_from_image = get_msg(image='decryptedimage.png')
        decrypted = decrypt(msg_from_image.encode(), hash_input(password)).decode()
        st.write(f'The Hidden Message is : "{decrypted}"')
            
       #decrypt_msg = decrypt(get_msg(image_to_decrypt).encode(), hash_input(password))
        
        #st.write(f'https://ipfs.io/{NFT[3]}')
        #image = rq.get(f'https://ipfs.io/{NFT[3]}').content
        #st.image(image, width=300)