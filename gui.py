import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
import time
from datetime import datetime
from pdf_utils import convert_pdf_to_image 
from PIL import Image, ImageTk

# Define the path to your assets directory
assets_dir = "./assets"
processed_images_dir = "./assets/processed_images"

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def upload_and_convert_pdf(file_path, prefix):
    ensure_dir(processed_images_dir)  # Ensure the processed_images directory exists
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_filename = f"{prefix}_{timestamp}{os.path.splitext(file_path)[1]}"
    destination = os.path.join(assets_dir, new_filename)
    shutil.copy(file_path, destination)
    if file_path.lower().endswith('.pdf'):
        # Convert and save the PDF as an image
        output_image_path = os.path.join(processed_images_dir, f"{os.path.splitext(new_filename)[0]}.jpg")
        convert_pdf_to_image(destination, output_path=output_image_path)
        messagebox.showinfo("File Selected", f"{prefix} uploaded and converted: {output_image_path}")
    else:
        messagebox.showinfo("File Selected", f"{prefix} uploaded: {destination}")

def upload_corrected_sheet():
    file_path = filedialog.askopenfilename()
    if file_path:
        upload_and_convert_pdf(file_path, "Corrected_sheet")

def upload_student_sheets():
    file_paths = filedialog.askopenfilenames()
    if file_paths:
        for file_path in file_paths:
            upload_and_convert_pdf(file_path, "Student_sheet")
            time.sleep(1)  # Ensure each file gets a unique timestamp

def process_images():
	# Placeholder for your image processing logic
	messagebox.showinfo("Processing", "Processing the images...")

def init_gui():
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
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    # Create a frame inside the canvas to hold the widgets
    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor='nw')

    # Add buttons to the inner frame
    btn_upload_corrected = tk.Button(inner_frame, text="Upload Corrected Answer Sheet", command=upload_corrected_sheet)
    btn_upload_corrected.pack(pady=10)

    btn_upload_students = tk.Button(inner_frame, text="Upload Student Answer Sheets", command=upload_student_sheets)
    btn_upload_students.pack(pady=10)

    btn_process = tk.Button(inner_frame, text="Process Images and Display Results", command=process_images)
    btn_process.pack(pady=10)

    root.mainloop()