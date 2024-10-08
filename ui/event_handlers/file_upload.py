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
            upload_and_convert_pdf(file_path, "corrected_sheet")

            # Create a processor instance with the corrected sheet prefix
            processor = QuadratProcessor(prefix='corrected_sheet')

            # Process the corrected sheet to extract correct answers
            corrected_answers = processor.extract_correct_answers_with_boxes(sheet_type='corrected')

            # Set the correct answers
            set_correct_answers(corrected_answers)

            messagebox.showinfo("Success", "Corrected sheet processed successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while uploading the corrected sheet: {e}")

# Upload student sheets
def upload_student_sheets(root):
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            student_id, student_name, student_answers, converted_image_path = process_student_sheet(file_path)
            validate_and_save_student_sheet(student_id, student_name, student_answers, converted_image_path)
        except Exception as e:
            logging.error(f"An error occurred while uploading the student sheet: {e}")
            messagebox.showerror("Error", f"An error occurred while uploading the student sheet: {e}")

# Process the student sheet
def process_student_sheet(file_path):
    # Create a processor instance
    processor = QuadratProcessor(prefix='student_sheet')

    # Extract student info from the sheet
    student_info = processor.detect_student_info(file_path)
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

    messagebox.showinfo("Success", f"Student sheet processed. Score: {score} | Student ID: {student_id}")


