from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.backends.openssl.rsa import RSAPrivateKey, RSAPublicKey

from Exceptions import StaticObjectOnlyException

class Crypto:
    def __init__(self):
        raise StaticObjectOnlyException()

    @staticmethod
    def generate_private_key() -> RSAPrivateKey:
        return rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

    @staticmethod
    def generate_public_key(private_key: RSAPrivateKey) -> RSAPublicKey:
        return private_key.public_key()

    @staticmethod
    def load_private_key(keyfile: str) -> RSAPrivateKey:
        with open(keyfile, "rb") as f:
            return Crypto.private_bytes_to_key(f.read())

    @staticmethod
    def private_bytes_to_key(key_in_bytes: bytes) -> RSAPrivateKey:
        return serialization.load_pem_private_key(
                key_in_bytes,
                password=None,
                backend=default_backend()
            )

    @staticmethod
    def public_bytes_to_key(key_in_bytes: bytes) -> RSAPublicKey:
        return serialization.load_pem_public_key(
                key_in_bytes,
                backend=default_backend()
            )

    @staticmethod
    def load_public_key(keyfile: str) -> RSAPublicKey:
        with open(keyfile, "rb") as f:
            return Crypto.public_bytes_to_key(f.read())

    @staticmethod
    def store_private_key(key: RSAPrivateKey, keyfile: str):
        with open(keyfile, "wb") as f:
            f.write(Crypto.key_to_private_bytes(key))

    @staticmethod
    def key_to_private_bytes(key: RSAPrivateKey):
        return key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )

    @staticmethod
    def key_to_public_bytes(key: RSAPublicKey):
        return key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )

    @staticmethod
    def store_public_key(key: RSAPublicKey, keyfile: str):
        with open(keyfile, "wb") as f:
            f.write(Crypto.key_to_public_bytes(key))

    @staticmethod
    def encrypt(message: bytes, key: RSAPublicKey) -> bytes:
        return key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(
                    algorithm=hashes.SHA256()
                ),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    @staticmethod
    def decrypt(message: bytes, key: RSAPrivateKey) -> bytes:
        return key.decrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(
                    algorithm=hashes.SHA256()
                ),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
