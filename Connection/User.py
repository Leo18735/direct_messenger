from cryptography.hazmat.backends.openssl.rsa import RSAPrivateKey, RSAPublicKey
from Crypto import Crypto


class User:
    def __init__(self, identifier: int, name: str, public_key: RSAPublicKey, private_key: RSAPrivateKey = None):
        self._identifier: int = identifier
        self._name: str = name
        self._public_key: RSAPublicKey = public_key
        self._private_key: RSAPrivateKey = private_key

        # unpickle
        self._public_key_bytes: bytes = b""

    def get_public_key(self) -> RSAPublicKey:
        return self._public_key

    def get_private_key(self) -> RSAPrivateKey:
        return self._private_key

    def get_name(self) -> str:
        return self._name

    def __getstate__(self):
        return {key: value for (key, value) in self.__dict__.items() if key not in ["_private_key", "_public_key"]} | {"_public_key_bytes": Crypto.key_to_public_bytes(self._public_key)}

    def __setstate__(self, state):
        self.__dict__ = state
        self._public_key = Crypto.public_bytes_to_key(self._public_key_bytes)
