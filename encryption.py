# contains functions to encrypt passwords and embed them into images

# will be used to has the password before passing to AES_encrypt

def hash_input(txt):
    import hashlib
    from base64 import b64encode
    sha = hashlib.sha256()
    text = txt.encode()
    sha.update(text)
    key = sha.digest()
    key = b64encode(key)
    
    return key

def AES_encrypt(plaintext, key):
    from cryptography.fernet import Fernet
    f = Fernet(key)
    return f.encrypt(plaintext)

def AES_decrypt(ciphertext, key):
    from cryptography.fernet import Fernet
    f = Fernet(key)
    return f.decrypt(ciphertext)