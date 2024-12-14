# Native Libraries
from io import BytesIO
import hashlib


from io import BytesIO
import hashlib

def generate_hash(file: BytesIO = None) -> str:
    '''
    Generates an MD5 hash for the contents of a given file-like object.

    Args:
        file (BytesIO, optional): A file-like object that supports reading binary data.
                                   The file is read in chunks of 4096 bytes.

    Returns:
        str: A hexadecimal string representing the computed MD5 hash of the file's contents.
    '''
    hasher: hashlib.Hash = hashlib.md5()

    for chunk in iter(lambda: file.read(4096), b''):
        hasher.update(chunk)

    return hasher.hexdigest()

def hashes_are_equal(file_path: str, bytes_data: bytes) -> bool:
    '''
    Compares the MD5 hash of a file stored on disk with the MD5 hash of a given byte sequence.

    Args:
        file_path (str): The path to the file stored on disk.
        bytes_data (bytes): A byte sequence to compare against the file's contents.

    Returns:
        bool: True if the hashes match, False otherwise.
    '''
    received_file_hash: str = generate_hash(file=BytesIO(bytes_data))

    with open(file_path, 'rb') as file:
        stored_file_hash: str = generate_hash(file=file)

    return received_file_hash == stored_file_hash
