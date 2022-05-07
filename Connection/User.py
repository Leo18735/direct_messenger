from cryptography.hazmat.backends.openssl.rsa import RSAPrivateKey, RSAPublicKey

class User:
    def __init__(self, public_key: RSAPublicKey, private_key: RSAPrivateKey = None):
        self._public_key: RSAPublicKey = public_key
        self._private_key: RSAPrivateKey = private_key

    def get_public_key(self) -> RSAPublicKey:
        return self._public_key

    def get_private_key(self) -> RSAPrivateKey:
        return self._private_key
