import os
from flet.security import encrypt, decrypt

def get_secret_key():
    secret_key = os.getenv("MY_APP_SECRET_KEY")
    if not secret_key:
        raise ValueError("A variável de ambiente MY_APP_SECRET_KEY não está definida.")
    return secret_key

def encrypted_data(plain_text):
    secret_key = get_secret_key()
    return encrypt(plain_text, secret_key)


def decrypt_data(encrypted_text):
    secret_key = get_secret_key()
    return decrypt(encrypted_text, secret_key)
