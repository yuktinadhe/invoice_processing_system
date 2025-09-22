import os
from fastapi import UploadFile
from config import DATA_DIR


def save_upload_file(uploaded_file: UploadFile, save_dir: str = DATA_DIR) -> str:
    """
    Save uploaded file to the given directory and return its path.
    """
    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, uploaded_file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(uploaded_file.file.read())

    return file_path
