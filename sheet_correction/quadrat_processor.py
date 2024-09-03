import os
import cv2
from .image_processing import detect_quadrats, preprocess_image
import pytesseract
from PIL import Image
import logging
import re
from ui.event_handlers.utils import upload_and_convert_pdf 

class QuadratProcessor:
    def __init__(self, directory='./assets/processed_images', prefix='corrected_sheet', student_id=None):
        self.directory = directory
        self.prefix = prefix
        self.student_id = student_id

    def extract_text_from_region(self, image_path, region):
        """
        Extracts text from a specified region of the image.

        Args:
            image_path (str): The path to the image file.
            region (tuple): A tuple specifying the region (x, y, width, height).

        Returns:
            str: The extracted text.
        """
        image = Image.open(image_path)
        cropped_image = image.crop(region)
        text = pytesseract.image_to_string(cropped_image)
        return text.strip()

    
    def detect_student_info(self, image_path):
        """
        Detects student information from the given image.

        Args:
            image_path (str): Path to the image file.

        Returns:
            dict: A dictionary containing student information such as student_id and student_name.
        """
        nameroi=None
        idroi=None
        try:
            # Load the image using OpenCV
            image = cv2.imread(image_path)
            
            # Check if the image was loaded successfully
            if image is None:
                logging.error(f"Failed to load image from path: {image_path}")
                return {}

            # Convert the image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            list_of_info_locations=[[ 1045 , 27 , 171 , 40 ] , [ 996 , 69 , 223 , 39]]
            for i, location in enumerate(list_of_info_locations):
                if i == 0:
                    x, y, w, h = location
                    nameroi=gray[y:y+h , x:x+w]
                elif i == 1:
                    x2, y2, w2, h2 = location
                    idroi=gray[y2:y2+h2 , x2:x2+w2 ]


            # Apply binary thresholding
            _, binary_image1 = cv2.threshold(nameroi, 128, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            _, binary_image2 = cv2.threshold(idroi, 128, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            # Detect text regions and recognize text
            student_id, student_name = self.detect_and_recognize_text(binary_image1, binary_image2)

            return {
                'student_id': student_id,
                'student_name': student_name
            }

        except Exception as e:
            logging.error(f"An error occurred while detecting student info: {e}")
            return {}

    def detect_and_recognize_text(self, binary_image1, binary_image2):
        """
        Detects text regions in the binary image and recognizes handwritten text.

        Args:
            binary_image (numpy.ndarray): The binary image.
            original_image (numpy.ndarray): The original image.

        Returns:
            tuple: A tuple containing the student ID and student name.
        """
        #contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        student_id = ""
        student_name = ""
        student_name=pytesseract.image_to_string(binary_image1 , config='--psm 7')
        student_id=pytesseract.image_to_string(binary_image2 , config='--psm 7')
        """for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            roi = original_image[y:y+h, x:x+w]
            text = pytesseract.image_to_string(roi, config='--psm 7')
            if text.isdigit():
                student_id = text
            elif text.isalpha():
                student_name = text"""
        

        return student_id, student_name
    
    
    def extract_correct_answers_with_boxes(self, filename=None, sheet_type='corrected'):
        if filename:
            image_path = os.path.join(self.directory, filename)
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"No image with filename '{filename}' found in directory '{self.directory}'")
        else:
            # List all files in the directory
            file_names = os.listdir(self.directory)
            print(f"Files in directory: {file_names}") 
            
            # Filter image files with the specified prefix (case-insensitive)
            image_files = [file for file in file_names if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
            image_paths = [os.path.join(self.directory, file) for file in image_files if file.lower().startswith(self.prefix.lower())]
            
            # Debugging: Print the filtered image paths
            print(f"Filtered image paths: {image_paths}")
            
            if not image_paths:
                raise FileNotFoundError(f"No image with prefix '{self.prefix}' found in directory '{self.directory}'")
            
            # Process only the first sheet found
            image_path = image_paths[0]
        
        # Preprocess the image
        image, binary = preprocess_image(image_path)
        
        if image is None or binary is None:
            raise ValueError("Image preprocessing failed.")
        
        # Detect quadrats
        processed_image, filled_quadrats, empty_quadrats = detect_quadrats(image, binary)
        
        # Debugging: Print the number of detected quadrats
        print(f"Detected {len(filled_quadrats)} filled quadrats and {len(empty_quadrats)} empty quadrats")
        
        # Combine and sort quadrats
        all_quadrats = filled_quadrats + empty_quadrats
        all_quadrats = sorted(all_quadrats, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))
        
        # Extract bounding rectangles for filled quadrats
        filled_quadrats_rects = [cv2.boundingRect(fq) for fq in filled_quadrats]
        
        # Create an array to store the quadrat values (1 for filled, 0 for empty)
        quadrat_values = []
        
        # Draw contours and line numbers around all quadrats
        for quadrat in all_quadrats:
            quadrat_rect = cv2.boundingRect(quadrat)
            is_filled = quadrat_rect in filled_quadrats_rects
            quadrat_values.append(1 if is_filled else 0)
            color = (0, 255, 0) if is_filled else (0, 0, 255)  # Green for filled, Red for empty
            cv2.drawContours(processed_image, [quadrat], -1, color, 2)
            x, y, w, h = quadrat_rect
            cv2.putText(processed_image, str(1 if is_filled else 0), (x - 30, y + h // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        # Save the processed image with the student ID in the filename
        output_filename = f'processed_image_with_contours_and_values_{sheet_type}'
        if self.student_id:
            output_filename += f'_ID_{self.student_id}'
        output_filename += '.jpg'
        output_path = os.path.join(self.directory, output_filename)
        cv2.imwrite(output_path, processed_image)
        print(f"Processed image saved to {output_path}")
        
        return quadrat_values
