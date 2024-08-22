# ui/event_handlers/file_upload.py

import os
from tkinter import filedialog, messagebox
from ..dialog import CorrectedSheetDialog
from quadrat_processor import QuadratProcessor
from answers_manager import set_correct_answers, calculate_score, set_answer_mark, get_correct_answers
from student import Student, save_student_score, get_all_students
from pdf_utils import convert_pdf_to_image
from image_processing import preprocess_image, detect_quadrats
from .utils import upload_and_convert_pdf, generate_student_id
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


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



def upload_student_sheets(root):
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            # Generate a random student ID
            student_id = generate_student_id()

            # Upload and convert PDF
            converted_image_path = upload_and_convert_pdf(file_path, "student_sheet", student_id)

            # Extract the filename from the file path
            filename = os.path.basename(converted_image_path)
            logging.debug(f"Extracted filename: {filename}")

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

            # Log student answers with a timestamp
            logging.debug(f"Student answers: {student_answers}")

            score = calculate_score(student_answers)

            # Paths for storing sheets
            processed_images_dir = "./assets/processed_images"
            original_answered_sheet_path = converted_image_path
            corrected_sheet_path = os.path.join(processed_images_dir, f"{student_id}_corrected.png")

            # Create a Student object
            new_student = Student(
                student_id=student_id,
                name="Unknown",  # You can update this with the actual student name if available
                score=score,
                student_answers_result=student_answers,
                original_answered_sheet_path=original_answered_sheet_path,
                corrected_sheet_path=corrected_sheet_path
            )

            # Save the student score using the Student object
            save_student_score(new_student)

            messagebox.showinfo("Success", f"Student sheet processed. Score: {score} | Student ID: {student_id}")

        except Exception as e:
            logging.error(f"An error occurred while uploading the student sheet: {e}")
            messagebox.showerror("Error", f"An error occurred while uploading the student sheet: {e}")


