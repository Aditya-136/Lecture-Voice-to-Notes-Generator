import os


UPLOAD_DIR = "uploads"


def save_uploaded_file(uploaded_file) -> str:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    dest = os.path.join(UPLOAD_DIR, uploaded_file.name)

    with open(dest, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return dest
