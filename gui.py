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
import threading

# Define the path to your assets directory
assets_dir = "./assets"
processed_images_dir = "./assets/processed_images"

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Ensure the directories exist
ensure_dir(assets_dir)
ensure_dir(processed_images_dir)

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
    inner_frame.grid_rowconfigure(6, weight=1)
    inner_frame.grid_columnconfigure(0, weight=1)
    inner_frame.grid_columnconfigure(1, weight=1)
    inner_frame.grid_columnconfigure(2, weight=1)

    # Add buttons to the inner frame in the center column
    button_width = 20
    button_height = 10  # Assuming each button has a height of 2 lines of text
    btn_upload_corrected = tk.Button(inner_frame, text="Corrected Sheet", command=lambda: upload_and_convert_pdf(filedialog.askopenfilename(), "Corrected_sheet"), width=button_width, padx=20, pady=10, bg="lightblue", font=("Arial", 14))
    btn_upload_corrected.grid(row=2, column=1, pady=5, sticky='ew')

    btn_upload_students = tk.Button(inner_frame, text="Student Sheets", command=lambda: upload_and_convert_pdf(filedialog.askopenfilename(), "Student_sheet"), width=button_width, padx=20, pady=10, bg="lightgreen", font=("Arial", 14))
    btn_upload_students.grid(row=3, column=1, pady=5, sticky='ew')

    btn_process = tk.Button(inner_frame, text="Process Images", command=process_images, width=button_width, padx=20, pady=10, bg="lightcoral", font=("Arial", 14))
    btn_process.grid(row=4, column=1, pady=5, sticky='ew')

    # Calculate the window size
    window_width = button_width * 10 + 40  # 10 pixels per character, plus padding
    window_height = (button_height * 3 + 20) * 3 + 40  # 3 lines of text per button, plus padding and spacing

    # Add a small margin to make the window slightly larger than the buttons
    margin = 20
    window_width += margin
    window_height += margin

    # Set the window size
    root.geometry(f"{window_width}x{window_height}")

    root.mainloop()

if __name__ == "__main__":
    init_gui()  # Call the GUI to display the main menu