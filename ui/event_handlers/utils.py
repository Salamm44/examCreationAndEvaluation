# ui/event_handlers/utils.py

"""import os
from pdf_utils import convert_pdf_to_image
import string
import random
from tkinter import messagebox

def upload_and_convert_pdf(file_path, prefix, student_id=""):
    # Define directories
    assets_dir = "./assets"
    processed_images_dir = "./assets/processed_images"

    # Ensure directories exist
    for directory in [assets_dir, processed_images_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Define the destination path
    if student_id:
        destination = os.path.join(processed_images_dir, f"{prefix}_{student_id}.png")
    else:
        destination = os.path.join(processed_images_dir, f"{prefix}.png")

    # Convert PDF to image
    convert_pdf_to_image(file_path, destination)

    return destination

def generate_student_id(length=6):
    Generates a random student ID consisting of uppercase letters and digits.
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))"""



import os
from pdf_utils import convert_pdf_to_images  # Update import to reflect the modified function
import string
import random
from tkinter import messagebox

def upload_and_convert_pdf(file_path, prefix, student_id=""):
    # Define directories
    assets_dir = "./assets"
    processed_images_dir = "./assets/processed_images"

    # Ensure directories exist
    for directory in [assets_dir, processed_images_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Define the destination folder for the student's images
    if student_id:
        papers_folder = os.path.join(processed_images_dir, f"{student_id}")
        if not os.path.exists(papers_folder):
            os.makedirs(papers_folder)
    else:
        papers_folder=os.path.join(processed_images_dir , f"{prefix}")
        #raise ValueError("Student ID is required for organizing files.")

    # Convert PDF to images
    image_paths = convert_pdf_to_images(file_path, papers_folder)

    return image_paths

def generate_student_id(length=6):
    """Generates a random student ID consisting of uppercase letters and digits."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

