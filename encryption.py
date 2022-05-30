# contains functions to encrypt passwords and embed them into images

# importing libraries
import hashlib  # used to has the text using SHA-256 algorithm
# used to convert the text into the correct size bytes for the fernet encryption algorithm
from base64 import b64encode, b64decode
from stegano import lsb  # stenography library used hide and reveal messages with images

###############################
# Cryptography Part Functions #
###############################

# will be used to has the password before passing to


def hash_input(txt):
    sha = hashlib.sha256()
    text = txt.encode()
    sha.update(text)
    key = sha.digest()
    key = b64encode(key)
    return key

# used to encrypt plain text using a key (hashed key from the password)


def encrypt(plaintext, key):
    from cryptography.fernet import Fernet
    f = Fernet(key)
    return f.encrypt(plaintext)

# used to decrypt cipher text using a key (hashed key from the password)


def decrypt(ciphertext, key):
    from cryptography.fernet import Fernet
    f = Fernet(key)
    return f.decrypt(ciphertext)


###############################
# Stenography Part Functions #
###############################

# function to use the stegano library to encode a msg into an image
def hide_msg(image, msg):
    lsb.hide(image, msg).save('./encryotedimage.png')


# function to decode a msg within an image
def get_msg(image):
    msg = lsb.reveal(image)
    return msg

    ''' if password_txt != password_txt:
        return 'Password Incorrect'
    else:
        return decrypt(msg, hashed_password) '''
