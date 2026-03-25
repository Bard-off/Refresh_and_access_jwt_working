from OpenSSL import crypto
from functools import wraps
from typing import Callable

from pathlib import Path

def trace(func: Callable):
    @wraps(func)
    def wr(*args, **kwargs):
        try:
            func(*args, **kwargs)
            print(f"\n Функция содания сертификатов отработала без ошибок")
        except Exception as e:
            print(f"\n Произошла ошибка во время создания сертификатов:\n{e}")
    return wr

@trace
def making_certs():
    k = crypto.PKey()

    k.generate_key(crypto.TYPE_RSA, 2048)


    private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
    public_key = crypto.dump_publickey(crypto.FILETYPE_PEM, k)

    path = Path(__file__).parent
    with open(f"{path}/private.pem", "wb") as f:
        f.write(private_key)


    with open(f"{path}/public.pem", "wb") as f:
        f.write(public_key)


if __name__ == "__main__":
    making_certs()