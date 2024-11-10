# Native Libraries
from io import BytesIO
import hashlib


def generate_hash(file: BytesIO = None) -> any:
    hasher: any = hashlib.md5()

    for chunk in iter(lambda: file.read(4096), b''):
        hasher.update(chunk)

    return hasher.hexdigest()


def hashes_are_equal(file_path: str, bytes: bytes) -> bool:
    received_file_hash: any = generate_hash(file=BytesIO(bytes))

    with open(file_path, 'rb') as file:
        stored_file_hash: any = generate_hash(file=file)

    return (received_file_hash == stored_file_hash)
