import os
from flet.security import encrypt, decrypt

SECRET_KEY = os.getenv("MY_APP_SECRET_KEY")

def encrypt_data(data: str) -> str:
    if not SECRET_KEY:
        raise ValueError("Não esta definida a chave")
    return encrypt(data, SECRET_KEY)


def decrypt_data(encrypted_data: str) -> str:
    if not SECRET_KEY:
        raise ValueError("Não esta definida a chave")
    return decrypt(encrypted_data, SECRET_KEY)
