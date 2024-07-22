import os
import cv2
from pdf_utils import convert_pdf_to_image
import gui 

def main():
    gui.init_gui()

    pdf_path = "./assets"
    output_directory = "./assets/processed_images"

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Check if there are any PDF files in the pdf_path directory
    pdf_files = [f for f in os.listdir(pdf_path) if f.endswith('.pdf')]
    if not pdf_files:
        print("No PDF files found. Please upload the sheets.")
        return  # Exit the function or handle accordingly

    # Assuming you want to process each PDF file
    for pdf_file in pdf_files:
        full_pdf_path = os.path.join(pdf_path, pdf_file)
        output_image_path = os.path.join(output_directory, f"{os.path.splitext(pdf_file)[0]}.jpg")
        image_path = convert_pdf_to_image(full_pdf_path, output_path=output_image_path)

    # Add code here to do something with the image_path

if __name__ == "__main__":
    main()