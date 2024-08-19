import os
import cv2
from image_processing import detect_quadrats, preprocess_image

class QuadratProcessor:
    def __init__(self, directory='./assets/processed_images', prefix='corrected_sheet', student_id=None):
        self.directory = directory
        self.prefix = prefix
        self.student_id = student_id

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
