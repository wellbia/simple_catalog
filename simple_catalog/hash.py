import os
import hashlib


def get_md5_hash(data: str) -> str:
    if os.path.exists(data):
        with open(data, "rb") as f:
            data = f.read()
    return hashlib.md5(data).hexdigest()


def get_sha256_hash(data: str) -> str:
    if os.path.exists(data):
        with open(data, "rb") as f:
            data = f.read()
    return hashlib.sha256(data).hexdigest()


def get_entry_hash(
    product: str,
    revision: str,
    hash: str,
    filename: str,
    md5: str,
    sha256: str,
    salt: str,
) -> str:
    data = "".join([product, revision, hash, filename, md5, sha256, salt]).encode()
    return get_sha256_hash(data)


def get_file_hash(file: str, product: str, revision: str, hash: str, salt: str):
    md5 = get_md5_hash(file)
    sha256 = get_sha256_hash(file)
    entry = get_entry_hash(
        product, revision, hash, os.path.basename(file), md5, sha256, salt
    )
    return md5, sha256, entry
