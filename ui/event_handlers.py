from tkinter import filedialog, messagebox, tk, ttk
from sheet_correction.quadrat_processor import QuadratProcessor
from answers_manager import set_correct_answers, calculate_score, set_answer_mark, get_correct_answers
from .dialog import CorrectedSheetDialog
from pdf_utils import convert_pdf_to_image
from sheet_correction.image_processing import preprocess_image, detect_quadrats
from datetime import datetime
from ..allstudent.student import save_student_score, get_all_students
import logging
import os
import shutil
import string
import random
import cv2
import numpy as np
# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

assets_dir = "./assets"
processed_images_dir = "./assets/processed_images"

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

ensure_dir(assets_dir)
ensure_dir(processed_images_dir)

def upload_and_convert_pdf(file_path, prefix, student_id=""):
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
    
    # Create the new filename including the student ID
    if prefix == "corrected_sheet":
        new_filename = f"{prefix}{os.path.splitext(file_path)[1]}"
    else:
        new_filename = f"{prefix}_{student_id}_{timestamp}{os.path.splitext(file_path)[1]}"

    destination = os.path.join(assets_dir, new_filename)

    # Copy the file to the destination directory with the new name
    shutil.copy(file_path, destination)
    print(f"File copied to: {destination}")

    # Check if the uploaded file is a PDF
    if destination.lower().endswith('.pdf'):
        # Convert the PDF to an image and save it with the same base name as the new filename
        output_image_path = os.path.join(processed_images_dir, f"{os.path.splitext(new_filename)[0]}.jpg")
        convert_pdf_to_image(destination, output_path=output_image_path)

        if os.path.exists(output_image_path):
            print(f"PDF successfully converted to image: {output_image_path}")
            return output_image_path
        else:
            raise FileNotFoundError(f"Failed to find the converted image at: {output_image_path}")
    else:
        print("Uploaded file is not a PDF. No conversion performed.")
        return destination

def upload_corrected_sheet():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            root = tk.Tk()  # Define the root variable
            dialog = CorrectedSheetDialog(root)
            correction_system = dialog.correction_system
            answer_mark = dialog.answer_mark

            set_answer_mark(answer_mark)
            upload_and_convert_pdf(file_path, "corrected_sheet")

            processor = QuadratProcessor(prefix='corrected_sheet')
            corrected_answers = processor.extract_correct_answers_with_boxes(sheet_type='corrected')

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
            converted_image_path = upload_and_convert_pdf(file_path, "student_sheet", student_id)

            # Extract the filename from the file path
            filename = os.path.basename(converted_image_path)
            print(f"Extracted filename: {filename}")
            
            # Create a processor instance with the student sheet prefix and student ID
            processor = QuadratProcessor(prefix='student_sheet', student_id=student_id)
            
            # Process the student's sheet
            student_answers = processor.extract_correct_answers_with_boxes(filename=filename, sheet_type='student')

            # Ensure correct answers are set before calculating the score
            correct_answers = get_correct_answers()
            if not correct_answers:
                messagebox.showerror("Error", "Correct answers have not been set. Please upload the corrected sheet first.")
                return
            
            # Validate student answers
            if not isinstance(student_answers, list):
                messagebox.showerror("Error", "Invalid data format for student answers. Expected a list.")
                return

            if len(student_answers) != len(correct_answers):
                messagebox.showerror("Error", f"Length mismatch: {len(student_answers)} student answers vs {len(correct_answers)} correct answers.")
                return

            # Log student answers for debugging
            logging.debug(f"Student answers: {student_answers}")

            score = calculate_score(student_answers)

            # Paths for storing sheets
            corrected_sheet_path = f"{processed_images_dir}/{student_id}_corrected.png"
            original_answered_sheet_path = converted_image_path

            # Save the student score and relevant details
            save_student_score(
                student_id,
                score,
                student_answers_result=student_answers,
                original_answered_sheet_path=original_answered_sheet_path,
                corrected_sheet_path=corrected_sheet_path
            )
            
            messagebox.showinfo("Success", f"Student sheet processed. Score: {score} | Student ID: {student_id}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while uploading the student sheet: {e}")

def extract_results():
    result_window = tk.Toplevel()
    result_window.title("Student Results")

    tree = ttk.Treeview(result_window, columns=("ID", "Name", "Score"), show='headings')
    tree.heading("ID", text="Student ID")
    tree.heading("Name", text="Name")
    tree.heading("Score", text="Score")
    tree.pack(fill=tk.BOTH, expand=True)

    students = get_all_students()
    for student in students:
        tree.insert("", tk.END, values=(student.student_id, student.name, student.score))

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
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def process_images():
    image_paths = get_image_paths(processed_images_dir)
    for image_path in image_paths:
        image, binary = preprocess_image(image_path)
        if image is not None and binary is not None:
            result_image = detect_quadrats(image, binary)
            if result_image is not None and isinstance(result_image, np.ndarray):
                cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
                cv2.imshow('Result', result_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                messagebox.showinfo("Error", "No result image to display or result image is not a valid numpy array.")
        else:
            messagebox.showinfo("Error", "Image processing failed.")

def get_image_paths(directory):
    file_names = os.listdir(directory)
    image_files = [file for file in file_names if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return [os.path.join(directory, file) for file in image_files]