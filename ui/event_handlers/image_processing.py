# ui/event_handlers/image_processing.py

import os
import cv2
import numpy as np
from tkinter import messagebox
from quadrat_processor import QuadratProcessor
from image_processing import preprocess_image, detect_quadrats

def process_images(processed_images_dir):
    image_paths = get_image_paths(processed_images_dir)
    for image_path in image_paths:
        image, binary = preprocess_image(image_path)
        if image is not None and binary is not None:
            result_image = detect_quadrats(image, binary)
            if result_image is not None and isinstance(result_image, np.ndarray):
                print("Result image shape:", result_image.shape)
                # Create a resizable window
                cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
                cv2.imshow('Result', result_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                messagebox.showinfo("Error", "No result image to display or result image is not a valid numpy array.")
        else:
            messagebox.showinfo("Error", "Image processing failed.")

def extract_correct_answers_with_boxes(directory='./assets/processed_images', prefix='corrected_sheet'):
    print(f"Looking for images in directory: {directory} with prefix: {prefix}")

    # List all files in the directory
    file_names = os.listdir(directory)
    print(f"Files in directory: {file_names}")

    # Filter image files with the specified prefix (case-insensitive)
    image_files = [file for file in file_names if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_paths = [os.path.join(directory, file) for file in image_files if file.lower().startswith(prefix.lower())]

    print(f"Filtered image paths: {image_paths}")

    if not image_paths:
        raise FileNotFoundError(f"No image with prefix '{prefix}' found in directory '{directory}'")

    # Process only the first corrected sheet found
    image_path = image_paths[0]

    # Preprocess the image
    image, binary = preprocess_image(image_path)

    if image is not None and binary is not None:
        # Detect quadrats
        processed_image, filled_quadrats, empty_quadrats = detect_quadrats(image, binary)

        # Print the number of detected quadrats for debugging
        print(f"Detected {len(filled_quadrats)} filled quadrats and {len(empty_quadrats)} empty quadrats")

        # Combine filled and empty quadrats
        all_quadrats = filled_quadrats + empty_quadrats

        # Extract bounding rectangles for filled quadrats
        filled_quadrats_rects = [cv2.boundingRect(fq) for fq in filled_quadrats]

        # Create a list to store quadrat contours with their values
        quadrats_with_values = []

        # Draw contours and values around all quadrats
        for quadrat in all_quadrats:
            quadrat_rect = cv2.boundingRect(quadrat)
            is_filled = quadrat_rect in filled_quadrats_rects
            value = 1 if is_filled else 0
            quadrats_with_values.append((quadrat, value))

        # Sort quadrats by their bounding rectangle to ensure the order is correct
        quadrats_with_values.sort(key=lambda item: (cv2.boundingRect(item[0])[1], cv2.boundingRect(item[0])[0]))

        # Extract the values to a separate array in the same order
        quadrat_values = [value for _, value in quadrats_with_values]

        # Draw contours and values on the processed image
        for quadrat, value in quadrats_with_values:
            color = (0, 255, 0) if value == 1 else (0, 0, 255)  # Green for filled, Red for empty
            cv2.drawContours(processed_image, [quadrat], -1, color, 2)
            x, y, w, h = cv2.boundingRect(quadrat)
            cv2.putText(processed_image, str(value), (x - 30, y + h // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        # Save the processed image with colored contours and values
        output_path = os.path.join(directory, 'processed_image_with_contours_and_values.jpg')
        cv2.imwrite(output_path, processed_image)
        print(f"Processed image saved to {output_path}")

    print(quadrat_values)
    return quadrat_values

def get_image_paths(directory):
    file_names = os.listdir(directory)
    image_files = [file for file in file_names if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_paths = [os.path.join(directory, file) for file in image_files]
    return image_paths
