import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
import time

from datetime import datetime

# Define the path to your assets directory
assets_dir = "./assets"

def upload_corrected_sheet():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Generate a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Rename the file with "Corrected_sheet" prefix and timestamp
        new_filename = f"Corrected_sheet_{timestamp}{os.path.splitext(file_path)[1]}"
        destination = os.path.join(assets_dir, new_filename)
        shutil.copy(file_path, destination)
        messagebox.showinfo("File Selected", f"Corrected Sheet uploaded to assets: {new_filename}")

def upload_student_sheets():
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        uploaded_files = []
        for file_path in file_paths:
            # Generate a timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Rename the file with "Student_sheet" prefix and timestamp
            new_filename = f"Student_sheet_{timestamp}{os.path.splitext(file_path)[1]}"
            destination = os.path.join(assets_dir, new_filename)
            shutil.copy(file_path, destination)
            uploaded_files.append(new_filename)
            # Ensure each file gets a unique timestamp by adding a slight delay
            time.sleep(1)
        messagebox.showinfo("Files Selected", f"Student Sheets uploaded to assets: {', '.join(uploaded_files)}")

def process_images():
	# Placeholder for your image processing logic
	messagebox.showinfo("Processing", "Processing the images...")

def init_gui():
	root = tk.Tk()
	root.title("Exam Evaluation App")

	btn_upload_corrected = tk.Button(root, text="Upload Corrected Answer Sheet", command=upload_corrected_sheet)
	btn_upload_corrected.pack(pady=10)

	btn_upload_students = tk.Button(root, text="Upload Student Answer Sheets", command=upload_student_sheets)
	btn_upload_students.pack(pady=10)

	btn_process = tk.Button(root, text="Process Images and Display Results", command=process_images)
	btn_process.pack(pady=10)

	root.mainloop()