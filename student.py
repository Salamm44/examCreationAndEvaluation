import os
import json
from dataclasses import dataclass, field, asdict
from typing import List

# Define the path to your assets directory
ASSETS_DIR = "./assets"
PROCESSED_IMAGES_DIR = "./assets/processed_images"
STUDENTS_FILE = "students.json"

@dataclass
class Student:
    student_id: str
    name: str = "Unknown"  # Default value if the name is not provided
    score: float = 0.0
    student_answers_result: List[str] = field(default_factory=list)
    original_answered_sheet_path: str = ""
    corrected_sheet_path: str = ""

    def __post_init__(self):
        if not isinstance(self.student_id, str):
            raise ValueError("student_id must be a string")
        if not isinstance(self.name, str):
            raise ValueError("name must be a string")
        if not isinstance(self.score, (int, float)):
            raise ValueError("score must be a number")
        if not isinstance(self.student_answers_result, list):
            raise ValueError("student_answers_result must be a list")
        if not isinstance(self.original_answered_sheet_path, str):
            raise ValueError("original_answered_sheet_path must be a string")
        if not isinstance(self.corrected_sheet_path, str):
            raise ValueError("corrected_sheet_path must be a string")

def ensure_dir(directory: str):
    """Ensures that a directory exists."""
    os.makedirs(directory, exist_ok=True)

def save_student_score(student: Student):
    """Saves a single student's score to the students file."""
    students = load_students_from_file(STUDENTS_FILE)
    students.append(student)
    save_students_to_file(students, STUDENTS_FILE)

def save_students_to_file(students: List[Student], filename: str):
    """Saves the list of students to a JSON file."""
    with open(filename, 'w') as f:
        json.dump([asdict(student) for student in students], f, indent=4)

def load_students_from_file(filename: str) -> List[Student]:
    """Loads students from a JSON file."""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                students_data = json.load(f)
                return [Student(**data) for data in students_data]
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {filename}. Returning empty list.")
            return []
    else:
        print(f"File {filename} does not exist. Returning empty list.")
        return []

def delete_student_sheet(sheet_path: str):
    """Deletes a student sheet file if it exists."""
    if os.path.exists(sheet_path):
        os.remove(sheet_path)
        print(f"Deleted sheet: {sheet_path}")
    else:
        print(f"Sheet {sheet_path} does not exist.")

def process_and_cleanup_student_sheets(sheet_paths: List[str]):
    """Processes and cleans up a list of student sheet files."""
    for sheet_path in sheet_paths:
        # Placeholder for actual processing logic
        print(f"Processing {sheet_path}")
        # After processing, delete the sheet
        delete_student_sheet(sheet_path)

def get_all_students() -> List[Student]:
    """Retrieves all students from the students file."""
    return load_students_from_file(STUDENTS_FILE)

# Ensure necessary directories exist
ensure_dir(ASSETS_DIR)
ensure_dir(PROCESSED_IMAGES_DIR)

# Example usage
if __name__ == "__main__":
    # Create a sample student and save
    sample_student = Student(
        student_id="12345",
        name="John Doe",
        score=95.5,
        student_answers_result=["A", "B", "C", "D"],
        original_answered_sheet_path="./assets/original/12345.png",
        corrected_sheet_path="./assets/processed_images/12345_corrected.png"
    )
    save_student_score(sample_student)

    # Retrieve all students
    all_students = get_all_students()
    print(all_students)
