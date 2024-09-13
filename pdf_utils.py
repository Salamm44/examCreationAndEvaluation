from pdf2image import convert_from_path
import os

"""def convert_pdf_to_image(pdf_path, output_path='temp_image.jpg'):

	images = convert_from_path(pdf_path)
	
	first_page_image = images[0]
	first_page_image.save(output_path, 'JPEG')
	return output_path"""
def convert_pdf_to_images(pdf_path, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Convert PDF pages to images
    images = convert_from_path(pdf_path)

    image_paths = []

    # Save each image (for each page) with a unique filename
    for i, image in enumerate(images):
        output_path = os.path.join(output_folder, f'page_{i + 1}.jpg')  # No prefix
        image.save(output_path, 'JPEG')
        image_paths.append(output_path)

    return image_paths

                       
    
