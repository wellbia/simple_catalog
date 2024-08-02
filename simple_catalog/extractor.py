import os
import re

import zipfile
import py7zr
import rarfile


def is_supported_archive(file_path: str) -> bool:
    return (
        re.search(r"^[^.]+\.(\w+)\..+\.(zip|rar|7z)$", os.path.basename(file_path))
        is not None
    )


def extract_zip(file_path: str, extract_to: str, password: str = None):
    with zipfile.ZipFile(file_path, "r") as archive:
        if password is not None:
            archive.setpassword(password.encode("utf-8"))
        os.makedirs(extract_to, exist_ok=True)
        archive.extractall(extract_to)


def extract_7z(file_path: str, extract_to: str, password: str = None):
    with py7zr.SevenZipFile(file_path, mode="r", password=password) as archive:
        os.makedirs(extract_to, exist_ok=True)
        archive.extractall(extract_to)


def extract_rar(file_path: str, extract_to: str, password: str = None):
    with rarfile.RarFile(file_path) as archive:
        if password is not None:
            archive.setpassword(password)
        os.makedirs(extract_to, exist_ok=True)
        archive.extractall(extract_to)


def extract_file(file_path: str, extract_to: str, password: str = None):
    if not is_supported_archive(file_path):
        raise Exception("Format is not supported")

    if file_path.lower().endswith(".zip"):
        extract_zip(file_path, extract_to, password)
    elif file_path.lower().endswith(".7z"):
        extract_7z(file_path, extract_to, password)
    elif file_path.lower().endswith(".rar"):
        extract_rar(file_path, extract_to, password)
