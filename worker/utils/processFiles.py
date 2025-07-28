import os
from utils.pdf2Img import pdf_to_images

def processFiles(file_path):
    file_name = os.path.basename(file_path).split(".")[0]
    file_ext = os.path.splitext(file_path)[1].lower()
    images_paths = []

    if file_ext == ".pdf":
        images_paths = pdf_to_images(file_path, file_name)
    elif file_ext in [".png", ".jpg", ".jpeg"]:
        images_paths = [file_path]
    else:
        raise ValueError("Unsupported File Format.")
    
    return images_paths