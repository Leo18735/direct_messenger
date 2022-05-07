import socket
from threading import Thread
from time import sleep
import pickle
from Connection import User
from Crypto import Crypto
from os.path import exists


class Connection:
    _encrypt: bool = True
    def __init__(self, destination_ip: str, destination_port: int, source_ip: str = "0.0.0.0", source_port: int = None):
        super().__init__()
        self._destination_ip: str = destination_ip
        self._destination_port: int = destination_port
        self._source_ip: str = source_ip
        self._source_port: int = source_port

        self._socket: socket.socket = None

        self._opposite: User

        private_key = Crypto.generate_private_key()
        public_key = Crypto.generate_public_key(private_key)

        self._me: User = User(public_key, private_key)

    def start(self):
        listen_sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect_sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        listen_sock.bind((self._source_ip, self._source_port))
        listen_sock.listen()
        listen_sock.settimeout(5)

        print(f"Listen on {self._source_ip}, {self._source_port}\nConnecting to {self._destination_ip}, {self._destination_port}")

        while True:
            print("Connect")
            try:
                connect_sock.connect((self._destination_ip, self._destination_port))
                connect_sock.sendall(Crypto.key_to_public_bytes(self._me.get_public_key()))
                self._opposite = User(Crypto.public_bytes_to_key(connect_sock.recv(1024)))
                self._socket = connect_sock
                break
            except ConnectionRefusedError:
                pass
            print("Connect failed")
            print("Listen")
            try:
                connection, address = listen_sock.accept()

                self._opposite = User(Crypto.public_bytes_to_key(connection.recv(1024)))
                connection.sendall(Crypto.key_to_public_bytes(self._me.get_public_key()))
                self._socket = connection
                break
            except TimeoutError:
                pass
            print("Listen failed")
        self._handle()

    def _handle(self):
        Thread(target=self._write).start()
        Thread(target=self._listen).start()

        while True:
            sleep(1)

    def _write(self):
        while True:
            user_input: str = input("> ")
            print(f"[You]: {user_input}")
            self._socket.sendall(Crypto.encrypt(user_input.encode("UTF-8"), self._opposite.get_public_key()) if self._encrypt else user_input.encode("UTF-8"))

    def _listen(self):
        while True:
            opposite_input: bytes = self._socket.recv(1024)
            print(f"[Opposite]: {Crypto.decrypt(opposite_input, self._me.get_private_key()).decode('UTF-8')  if self._encrypt else opposite_input.decode('UTF-8')}")
