from Crypto.Cipher import AES
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import random
import os
from io import BytesIO, TextIOWrapper, SEEK_END
from string import ascii_letters, digits
from typing import BinaryIO, Literal
from types import TracebackType


FileDescriptorOrPath = int | str | bytes | os.PathLike[str] | os.PathLike[bytes]


def generatePassword(length: int):
    return "".join(random.choices(ascii_letters + digits, k=length))


def getKey(password: str, salt: bytes, size: int):
    return PBKDF2(
        password,
        salt,
        dkLen=size,
        count=1_000_000,
        hmac_hash_module=SHA512,
    )


def hashBytes(data: bytes):
    return SHA512.new(data).digest()


class CBinaryIO(BytesIO):
    ################################
    #       File structure         #
    ################################
    #           NONCE              #
    #           SALT               #
    #           MAC                #
    #           DATA               #
    ################################
    NONCE_SIZE = 16
    SALT_SIZE = 32
    MAC_LEN = 16
    MAX_PASSWORD_SIZE = 64
    KEY_SIZE = 32

    @classmethod
    def _get_cipher(cls, key: bytes, nonce: bytes):
        return AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=cls.MAC_LEN)

    @classmethod
    def _get_file_parts(cls, file: BinaryIO):
        nonce = file.read(cls.NONCE_SIZE)
        if len(nonce) != cls.NONCE_SIZE:
            raise ValueError("File corrupted, missing nonce")
        #
        salt = file.read(cls.SALT_SIZE)
        if len(salt) != cls.SALT_SIZE:
            raise ValueError("File corrupted, missing salt")
        #
        mac = file.read(cls.MAC_LEN)
        if len(mac) != cls.MAC_LEN:
            raise ValueError("File corrupted, missing mac")
        #
        ciphertext = file.read()
        return nonce, salt, mac, ciphertext

    @classmethod
    def _set_file_parts(
        cls, file: BinaryIO, nonce: bytes, salt: bytes, mac: bytes, ciphertext: bytes
    ):
        file.write(nonce)
        file.write(salt)
        file.write(mac)
        file.write(ciphertext)

    @classmethod
    def createKey(cls, path: FileDescriptorOrPath, password: str):
        with open(path, "rb") as file:
            _, salt, _, _ = cls._get_file_parts(file)
        return getKey(password, salt, cls.KEY_SIZE)

    @classmethod
    def open(
        cls,
        path: FileDescriptorOrPath,
        mode: Literal["r", "w", "a", "x"],
        password: str | None = None,
        salt: bytes | None = None,
        key: bytes | None = None,
        plain: bool = False
    ):
        if password is None and key is None:
            raise ValueError("Password or key have to be set")
        plaintext = bytes()
        match mode:
            case "r" | "a":
                with open(path, "rb") as file:
                    if plain:
                        plaintext = file.read()
                    else:
                        nonce, salt, mac, ciphertext = cls._get_file_parts(file)
                        #
                        if key is None:
                            key = getKey(password, salt, cls.KEY_SIZE)
                        #
                        cipher = cls._get_cipher(key, nonce)
                        #
                        plaintext = cipher.decrypt_and_verify(ciphertext, mac)
            case "x":
                if os.path.exists(path):
                    raise FileExistsError()
            case "w":
                pass
        #
        if password is not None:
            new_salt = get_random_bytes(cls.SALT_SIZE)
            new_key = getKey(password, new_salt, cls.KEY_SIZE)
        else:
            if mode != "r":
                raise ValueError("Cannot use key in writing mode")
            if salt is None:
                raise ValueError("Salt is not set")
            new_salt = salt
            new_key = key
        #
        buf = cls(plaintext, path, new_key, new_salt)
        #
        if mode == "a":
            buf.seek(0, SEEK_END)
        if plain:
            buf._hash += b"0"
        #
        return buf

    def __init__(
        self, plaintext: bytes, path: FileDescriptorOrPath, key: bytes, salt: bytes
    ):
        super().__init__(plaintext)
        self._path = path
        self._key = key
        self._salt = salt
        self._hash = hashBytes(plaintext)

    def setPassword(self, password: str):
        self._salt = get_random_bytes(self.SALT_SIZE)
        self._key = getKey(password, self._salt, self.KEY_SIZE)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        self.close()

    def close(self):
        buffer = self.getvalue()
        if hashBytes(buffer) != self._hash:
            nonce = get_random_bytes(self.NONCE_SIZE)
            cipher = self._get_cipher(self._key, nonce)
            ciphertext, mac = cipher.encrypt_and_digest(buffer)
            with open(self._path, "wb") as file:
                self._set_file_parts(file, nonce, self._salt, mac, ciphertext)
        super().close()


class CTextIO(TextIOWrapper):
    @classmethod
    def open(
        cls,
        path: FileDescriptorOrPath,
        mode: Literal["r", "w", "a", "x"],
        password: str,
        salt: bytes | None = None,
    ):
        return cls(CBinaryIO.open(path, mode, password, salt))

    def __init__(self, cbinaryio: CBinaryIO):
        super().__init__(cbinaryio)
        self._cbinaryio = cbinaryio

    def setPassword(self, password: str):
        self._cbinaryio.setPassword(password)
