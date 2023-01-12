import bcrypt
import hashlib


def encrypt_bcrypt(password):
    bytes_password = password.encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt()
    # Hashing the password
    hash_password = bcrypt.hashpw(bytes_password, salt)
    dict_hash = {salt:hash_password}
    return dict_hash


def encrypt_sha256(hash_256):
    sha_signature = bytes.fromhex(hashlib.sha256(hash_256.encode('utf-8')).hexdigest())
    return sha_signature
