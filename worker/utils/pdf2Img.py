from pdf2image import convert_from_path
import os

def pdf_to_images(pdf_path, file_name, output_folder="temp"):
    images = convert_from_path(pdf_path)
    image_paths = []

    for i, image in enumerate(images):
        image_filename = f"{file_name}_page_{i + 1}.png"
        image_path = os.path.join(output_folder, image_filename)
        image.save(image_path, 'PNG')
        image_paths.append(image_path)

    return image_paths
