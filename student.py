import os
import json

# Define the path to your assets directory
assets_dir = "./assets"
processed_images_dir = "./assets/processed_images"
students_file = "students.json"

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_students_to_file(students, filename):
    with open(filename, 'w') as f:
        json.dump([student.__dict__ for student in students], f)

def load_students_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            students_data = json.load(f)
            return [Student(**data) for data in students_data]
    return []

# Example function that might delete files
def delete_student_sheet(sheet_path):
    if os.path.exists(sheet_path):
        os.remove(sheet_path)
        # Check if there is any logic that deletes student.py
        some_condition = False
        if some_condition:
            os.remove('student.py')  # This line would delete student.py

# Example usage of delete_student_sheet
def process_and_cleanup_student_sheets(sheet_paths):
    for sheet_path in sheet_paths:
        # Process the sheet (placeholder for actual processing logic)
        print(f"Processing {sheet_path}")
        
        # Delete the sheet after processing
        delete_student_sheet(sheet_path)

# Ensure the directories exist
ensure_dir(assets_dir)
ensure_dir(processed_images_dir)

class Student:
    def __init__(self, student_id, name, score, student_answers_result, original_answered_sheet_path, corrected_sheet_path):
        self.student_id = student_id
        self.name = name
        self.score = score
        self.student_answers_result = student_answers_result
        self.original_answered_sheet_path = original_answered_sheet_path
        self.corrected_sheet_path = corrected_sheet_path

    def __repr__(self):
        return (f"Student(student_id={self.student_id}, name='{self.name}', score={self.score}, "
                f"student_answers_result={self.student_answers_result}, "
                f"original_answered_sheet_path='{self.original_answered_sheet_path}', corrected_sheet_path='{self.corrected_sheet_path}')")

# Load students from file on startup
students = load_students_from_file(students_file)