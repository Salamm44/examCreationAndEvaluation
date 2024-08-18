import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
import time
from datetime import datetime
from pdf_utils import convert_pdf_to_image 
from PIL import Image, ImageTk
import cv2
import numpy as np
from image_processing import detect_quadrats, preprocess_image
from PIL import Image
import easyocr
from image_processing import detect_quadrats, preprocess_image
from quadrat_processor import QuadratProcessor
import uuid
from answers_manager import set_correct_answers, calculate_score
from student import Student, students  # Import the Student class from the appropriate module
import string
import random

# Define the path to your assets directory
assets_dir = "./assets"
processed_images_dir = "./assets/processed_images"

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Ensure the directories exist
ensure_dir(assets_dir)
ensure_dir(processed_images_dir)


def upload_and_convert_pdf(file_path, prefix, student_id = ""):
    """
    Uploads a file, converts it if it's a PDF, and saves the output with a timestamp and student ID in the filename.

    Args:
        file_path (str): The path to the file to be uploaded.
        prefix (str): A prefix for the new filename to identify the type of file.
        student_id (str): A unique identifier for the student, included in the new filename.
    """
    # Ensure the processed_images directory exists
    ensure_dir(processed_images_dir)

    # Generate a timestamp and create the new filename including the student ID
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f"{prefix}_{student_id}_{timestamp}{os.path.splitext(file_path)[1]}"
    destination = os.path.join(assets_dir, new_filename)

    # Copy the file to the destination directory
    shutil.copy(file_path, destination)

    # Check if the uploaded file is a PDF
    if file_path.lower().endswith('.pdf'):
        # Convert the PDF to an image and save it with the same base name as the new filename
        output_image_path = os.path.join(processed_images_dir, f"{os.path.splitext(new_filename)[0]}.jpg")
        convert_pdf_to_image(destination, output_path=output_image_path)
        
        # Notify the user that the PDF was uploaded and converted
        messagebox.showinfo("File Selected", f"{prefix} uploaded and converted: {output_image_path}")
    else:
        # Notify the user that a non-PDF file was uploaded
        messagebox.showinfo("File Selected", f"{prefix} uploaded: {destination}")


def upload_corrected_sheet():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            # Step 1: Upload and convert PDF
            upload_and_convert_pdf(file_path, "corrected_sheet")
            
            # Step 2: Process the image after uploading
            corrected_answers = corrected_images()  # Call the processing method immediately
            set_correct_answers(corrected_answers)
            messagebox.showinfo("Success", "Corrected sheet processed successfully.")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while uploading the corrected sheet: {e}")

def upload_student_sheets():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            # Generate a random student ID
            student_id = generate_student_id()

            # Upload and convert PDF
            upload_and_convert_pdf(file_path, "student_sheet", student_id)
            
            # Create a processor instance with the student sheet prefix and student ID
            processor = QuadratProcessor(prefix='student_sheet', student_id=student_id)
            
            # Process the student's sheet
            student_answers = processor.extract_correct_answers_with_boxes(sheet_type='student')
            score = calculate_score(student_answers)
            
            messagebox.showinfo("Success", f"Student sheet processed. Score: {score} | Student ID: {student_id}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while uploading the student sheet: {e}")

def corrected_images():
    print("Corrected Images button clicked")
    directory = './assets/processed_images'
    prefix = 'corrected_sheet'
    print(f"Looking for images in directory: {directory} with prefix: {prefix}")
    
    # List all files in the directory
    files = os.listdir(directory)
    print(f"Files in directory: {files}")
    
    # Filter files with the given prefix (case-insensitive)
    image_paths = [os.path.join(directory, f) for f in files if f.lower().startswith(prefix.lower())]
    print(f"Filtered image paths: {image_paths}")
    
    if not image_paths:
        raise FileNotFoundError(f"No image with prefix '{prefix}' found in directory '{directory}'")
    
    # Process the images and extract correct answers
    processor = QuadratProcessor(directory=directory, prefix=prefix)
    correct_answers = processor.extract_correct_answers_with_boxes(sheet_type='corrected')
    
    return correct_answers


def generate_student_id(length=6):
    """Generates a random student ID consisting of uppercase letters and digits."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))



def process_images():
    # global corrected_sheet_uploaded
    # if not corrected_sheet_uploaded:
    #     messagebox.showwarning("Warning", "Please upload the corrected sheet before processing images.")
    #     return

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
                # messagebox.showinfo("Processing", "Processing the images...")
            else:
                messagebox.showinfo("Error", "No result image to display or result image is not a valid numpy array.")
                # print("Error: No result image to display or result image is not a valid numpy array.")
        else:
            messagebox.showinfo("Error", "Image processing failed.")
            # print("Error: Image processing failed.")

def get_image_paths(directory):
    file_names = os.listdir(directory)
    image_files = [file for file in file_names if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_paths = [os.path.join(directory, file) for file in image_files]
    return image_paths


def extract_correct_answers_with_boxes():
    """
    Extracts the correct answers from the corrected sheet image in the specified directory and saves them in a list.
    
    Returns:
    list: A list where each element is an array representing the answer lines for each question.
    """
    # Define the directory and prefix
    directory = './assets/processed_images'
    prefix = 'corrected_sheet'
    
    # Print the directory and prefix for debugging
    print(f"Looking for images in directory: {directory} with prefix: {prefix}")
    
    # List all files in the directory
    file_names = os.listdir(directory)
    print(f"Files in directory: {file_names}")
    
    # Filter image files with the specified prefix (case-insensitive)
    image_files = [file for file in file_names if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_paths = [os.path.join(directory, file) for file in image_files if file.lower().startswith(prefix.lower())]
    
    # Print the filtered image paths for debugging
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

def map_filled_quadrats_to_lines(quadrats, filled_quadrats, lines_per_question):
    """
    Maps each quadrat to its corresponding line number under each question and marks them as filled or empty.
    
    Args:
    quadrats (list): List of quadrat contours.
    filled_quadrats (list): List of filled quadrat contours.
    lines_per_question (int): Number of lines per question.
    
    Returns:
    list: List of tuples where each tuple contains a line number and a filled status (1 for filled, 0 for empty).
    """
    # Sort the quadrats by their y-coordinate and x-coordinate to ensure correct order
    quadrats = sorted(quadrats, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))
    
    # Extract bounding rectangles for filled quadrats
    filled_quadrats_rects = [cv2.boundingRect(fq) for fq in filled_quadrats]
    
    # Debugging: Print the sorted quadrats' coordinates
    print("Sorted quadrats by coordinates:")
    for quadrat in quadrats:
        print(cv2.boundingRect(quadrat))
    
    quadrats_with_numbers = []
    current_line = 1
    
    for i, quadrat in enumerate(quadrats):
        # Calculate the line number within the question (1-based index)
        quadrat_rect = cv2.boundingRect(quadrat)
        is_filled = quadrat_rect in filled_quadrats_rects
        quadrats_with_numbers.append((current_line, 1 if is_filled else 0))
        current_line += 1
        if current_line > lines_per_question:
            current_line = 1
    
    return quadrats_with_numbers


def init_gui():
    global root, loading_label
    root = tk.Tk()
    root.title("Exam Evaluation App")

    # Create a frame for the canvas and scrollbar
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Create a canvas widget
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a vertical scrollbar to the canvas
    v_scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas to use the scrollbar
    canvas.configure(yscrollcommand=v_scrollbar.set)
    # canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    # Create a frame inside the canvas to hold the widgets
    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor='nw')

    # Configure the grid to expand and fill the available space
    inner_frame.grid_rowconfigure(0, weight=1)
    inner_frame.grid_rowconfigure(1, weight=1)
    inner_frame.grid_rowconfigure(2, weight=1)
    inner_frame.grid_rowconfigure(3, weight=1)
    inner_frame.grid_rowconfigure(4, weight=1)
    inner_frame.grid_rowconfigure(5, weight=1) 
    inner_frame.grid_rowconfigure(6, weight=1)
    inner_frame.grid_columnconfigure(0, weight=1)
    inner_frame.grid_columnconfigure(1, weight=1)
    inner_frame.grid_columnconfigure(2, weight=1)

    # Add buttons to the inner frame in the center column
    button_width = 20
    button_height = 10  # Assuming each button has a height of 2 lines of text
    btn_upload_corrected = tk.Button(inner_frame, text="Corrected Sheet", command=upload_corrected_sheet, width=button_width, padx=20, pady=10, bg="lightblue", font=("Arial", 14))
    btn_upload_corrected.grid(row=2, column=1, pady=5, sticky='ew')

    btn_upload_students = tk.Button(inner_frame, text="Student Sheets", command=upload_student_sheets, width=button_width, padx=20, pady=10, bg="lightgreen", font=("Arial", 14))
    btn_upload_students.grid(row=3, column=1, pady=5, sticky='ew')

    btn_process = tk.Button(inner_frame, text="Process Images", command=process_images, width=button_width, padx=20, pady=10, bg="lightcoral", font=("Arial", 14))
    btn_process.grid(row=4, column=1, pady=5, sticky='ew')

    # Add new button for "Corrected Images"
    btn_corrected_images = tk.Button(inner_frame, text="Correct Images", command=corrected_images, width=button_width, padx=20, pady=10, bg="lightyellow", font=("Arial", 14))
    btn_corrected_images.grid(row=5, column=1, pady=5, sticky='ew')


    # Calculate the window size
    window_width = button_width * 10 + 40  # 10 pixels per character, plus padding
    window_height = (button_height * 3 + 20) * 3 + 100  # 3 lines of text per button, plus padding and spacing

    # Add a small margin to make the window slightly larger than the buttons
    margin = 20
    window_width += margin
    window_height += margin

    # Set the window size
    root.geometry(f"{window_width}x{window_height}")

    root.mainloop()

if __name__ == "__main__":
    init_gui()  # Call the GUI to display the main menu