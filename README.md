# Project 3 : Generate an NFT with Secret Messages 

## Contributors
- John Gaffney
- Jihad Al Hussain

## Project Description 
This project will use a GAN to generate 8-bit images of the users. The user will be able to upload an image to the webapp and the GAN model will output a generated image that then will be minted to the blockchain via a solidity smart contract. 

Some technologies that will be used are:
- [TensorFlow/PyTorch](https://www.tensorflow.org/) ( GAN Model )
- Streamlit (Front end webapp)
- IPFS Protocol for NFT image storage.
- Steganography to encrypt secret data in the image.
- Ethereum Blockchain Based (For now)

## Project Goals
- Generate 8-bit images based on the user input image. 
- Provide an easy way to mint it to the blockchain. ( using front end webapp )
- Encrypting a user message within the image or a simple hashed version of the message.


## Gif of GAN model generating images based on training data set

Model trained on RTX3070Ti, on full 10k image data set for 500 epochs using Tensorflow

![GansGif](./imgs/gans_training.gif)

## Example of style transfer to GAN generated image
![StyleTransfer](./imgs/Stylized1.png)

## App Demo ! 
![App Demo](./imgs/appDemo.gif)
