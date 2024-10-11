# ui/event_handlers/file_upload.py

import os
from tkinter import filedialog, messagebox
from allstudent.student import save_student_score, Student

from ..dialog import CorrectedSheetDialog
from sheet_correction.quadrat_processor import QuadratProcessor
from answers_manager import set_correct_answers, calculate_score, set_answer_mark, get_correct_answers
from .utils import upload_and_convert_pdf, generate_student_id
import logging


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# Upload corrected sheet
def upload_corrected_sheet(root):
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            dialog = CorrectedSheetDialog(root)
            # Assuming correction_system and answer_mark are strings, not widgets
            correction_system = dialog.correction_system
            answer_mark = dialog.answer_mark
            print(f"Correction System: {correction_system}")
            print(f"Mark per Correct Answer: {answer_mark}")

            # Set the answer mark in answers_manager
            set_answer_mark(float(answer_mark))

            # Step 1: Upload and convert PDF
            image_paths=upload_and_convert_pdf(file_path, "corrected_sheet")
            print(image_paths)

            # Create a processor instance with the corrected sheet prefix
            processor = QuadratProcessor(prefix='corrected_sheet')
            all_corrected_answers = []
            for image_path in image_paths:
                processor.directory = os.path.dirname(image_path)
                filename = os.path.basename(image_path)
                # Process the corrected sheet to extract correct answers
                #corrected_answers = processor.extract_correct_answers_with_boxes(sheet_type='corrected')
                corrected_answers = processor.extract_correct_answers_with_boxes(filename=filename, sheet_type='corrected')
                all_corrected_answers.extend(corrected_answers)

            # Set the correct answers
            #set_correct_answers(corrected_answers)
            set_correct_answers(all_corrected_answers)

            messagebox.showinfo("Success", "Corrected sheet processed successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while uploading the corrected sheet: {e}")

# Upload student sheets
def upload_student_sheets(root):
     # Ask the user whether they want to upload a single file or a folder
    choice = messagebox.askyesno("Upload Type", "Would you like to upload multiple PDFs from a folder?")

    if choice:  # User chooses to upload multiple PDFs from a folder
        folder_path = filedialog.askdirectory()  # Ask for folder selection
        if folder_path:
            # Get all PDF files from the folder
            pdf_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]
            if pdf_files:
                try:
                    for file_path in pdf_files:
                        student_id, student_name, student_answers, converted_image_path = process_student_sheet(file_path)
                        validate_and_save_student_sheet(student_id, student_name, student_answers, converted_image_path)
                    messagebox.showinfo("Success", "All student sheets have been processed successfully.")
                except Exception as e:
                    logging.error(f"An error occurred while uploading the student sheets: {e}")
                    messagebox.showerror("Error", f"An error occurred while uploading the student sheets: {e}")
            else:
                messagebox.showwarning("No PDFs", "No PDF files were found in the selected folder.")
        else:
            messagebox.showwarning("No Folder", "No folder selected.")
    
    else:  # User chooses to upload a single file
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])  # Ask for single file
        if file_path:
            try:
                student_id, student_name, student_answers, converted_image_path = process_student_sheet(file_path)
                validate_and_save_student_sheet(student_id, student_name, student_answers, converted_image_path)
                messagebox.showinfo("Success", "Student sheet has been processed successfully.")
            except Exception as e:
                logging.error(f"An error occurred while uploading the student sheet: {e}")
                messagebox.showerror("Error", f"An error occurred while uploading the student sheet: {e}")
        else:
            messagebox.showwarning("No File", "No file selected.")

# Process the student sheet
"""def process_student_sheet(file_path):
    # Create a processor instance
    processor = QuadratProcessor(prefix='student_sheet')

    converted_image_path_for_info=upload_and_convert_pdf(file_path,"student_sheet_for_info")

    # Extract student info from the sheet
    student_info = processor.detect_student_info(converted_image_path_for_info)
    logging.debug(f"Student info: {student_info}")
    student_id = student_info.get('student_id')
    student_name = student_info.get('student_name', 'Unknown')

    # If student_id is not detected, generate a random student_id
    if not student_id:
        student_id = generate_student_id()
        logging.warning("Student ID could not be detected from the sheet. Generated a new Student ID.")

    # Upload and convert PDF
    converted_image_path = upload_and_convert_pdf(file_path, "student_sheet", student_id)
    logging.debug(f"Converted image path: {converted_image_path}")

    # Check if the converted image path is valid
    if not converted_image_path or not os.path.exists(converted_image_path):
        raise ValueError("Converted image path is invalid or does not exist.")

    # Extract the filename from the file path
    filename = os.path.basename(converted_image_path)
    logging.debug(f"Extracted filename: {filename}")

    # Process the student's sheet
    student_answers = processor.extract_correct_answers_with_boxes(filename=filename, sheet_type='student')
    logging.debug(f"Student answers: {student_answers}")

    return student_id, student_name, student_answers, converted_image_path

# Validate student answers and save the student sheet
def validate_and_save_student_sheet(student_id, student_name, student_answers, converted_image_path):
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

    score = calculate_score(student_answers)

    # Paths for storing sheets
    processed_images_dir = "./assets/processed_images"
    original_answered_sheet_path = converted_image_path
    corrected_sheet_path = os.path.join(processed_images_dir, f"{student_id}_corrected.png")

    # Create a Student object
    new_student = Student(
        student_id=student_id,
        name=student_name,
        score=score,
        student_answers_result=student_answers,
        original_answered_sheet_path=original_answered_sheet_path,
        corrected_sheet_path=corrected_sheet_path
    )

    # Save the student score using the Student object
    save_student_score(new_student)

    # Log the Student Name and Student ID
    logging.info(f"Uploaded Student Name: {new_student.name}")
    logging.info(f"Uploaded Student ID: {new_student.student_id}")

    messagebox.showinfo("Success", f"Student sheet processed. Score: {score} | Student ID: {student_id}")"""
def process_student_sheet(file_path):
    # Create a processor instance
    processor = QuadratProcessor(prefix='student_sheet')

    # Convert the PDF into multiple images (one for each page)
    image_paths_for_info = upload_and_convert_pdf(file_path, "student_sheet_for_info")

    # Extract student info from the first image in the list (assuming the first page has the info)
    student_info = processor.detect_student_info(image_paths_for_info[0])  # Process first page for student info
    logging.debug(f"Student info: {student_info}")
    student_id = student_info.get('student_id')
    student_name = student_info.get('student_name', 'Unknown')

    # If student_id is not detected, generate a random student_id
    if not student_id:
        student_id = generate_student_id()
        logging.warning("Student ID could not be detected from the sheet. Generated a new Student ID.")

    # Convert the entire PDF to a list of image paths (each page)
    image_paths = upload_and_convert_pdf(file_path, "student_sheet", student_id)
    logging.debug(f"Converted image paths: {image_paths}")

    # Check if the image paths list is valid
    if not image_paths or any(not os.path.exists(image_path) for image_path in image_paths):
        raise ValueError("One or more converted image paths are invalid or do not exist.")

    # Initialize a list to store student answers from all pages
    all_student_answers = []

    # Process each image (page) to extract student answers
    for image_path in image_paths:
        # Extract the filename from the file path
        filename = os.path.basename(image_path)
        logging.debug(f"Processing filename: {filename}")
        filename_with_id = os.path.join(student_id, filename)

        # Process the student's sheet for this page
        student_answers = processor.extract_correct_answers_with_boxes(filename=filename_with_id, sheet_type='student')
        logging.debug(f"Student answers from page {filename}: {student_answers}")

        # Add answers from this page to the combined answers list
        all_student_answers.extend(student_answers)

    return student_id, student_name, all_student_answers, image_paths

# Validate student answers and save the student sheet
def validate_and_save_student_sheet(student_id, student_name, student_answers, image_paths):
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

    # Calculate the student's score
    score = calculate_score(student_answers)

    # Paths for storing sheets
    processed_images_dir = "./assets/processed_images"
    original_answered_sheet_paths = image_paths
    corrected_sheet_path = os.path.join(processed_images_dir, f"{student_id}_corrected.png")

    # Create a Student object
    new_student = Student(
        student_id=student_id,
        name=student_name,
        score=score,
        student_answers_result=student_answers,
        original_answered_sheet_path=original_answered_sheet_paths[0],  # Assuming we're storing only the first page
        corrected_sheet_path=corrected_sheet_path
    )

    # Save the student score using the Student object
    save_student_score(new_student)

    # Log the Student Name and Student ID
    logging.info(f"Uploaded Student Name: {new_student.name}")
    logging.info(f"Uploaded Student ID: {new_student.student_id}")

    messagebox.showinfo("Success", f"Student sheet processed. Score: {score} | Student ID: {student_id}")



