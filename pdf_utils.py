from pdf2image import convert_from_path

def convert_pdf_to_image(pdf_path, output_path='temp_image.jpg'):
	images = convert_from_path(pdf_path)
	first_page_image = images[0]
	first_page_image.save(output_path, 'JPEG')
	return output_path