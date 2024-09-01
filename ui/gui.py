# ui/gui.py

import tkinter as tk
from ui.event_handlers.file_upload import upload_corrected_sheet, upload_student_sheets
from ui.event_handlers.results import extract_results
from allstudent.student import clear_students_file

def init_gui():
    root = tk.Tk()
    root.title("Exam Evaluation App")

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    v_scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=v_scrollbar.set)

    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor='nw')

    inner_frame.grid_rowconfigure(0, weight=1)
    inner_frame.grid_columnconfigure(0, weight=1)

    button_width = 20

    # Function to handle the reset button click
    def reset_students_file():
        clear_students_file()
        tk.messagebox.showinfo("Reset", "The students database has been reset.")


    btn_upload_corrected = tk.Button(
        inner_frame,
        text="Corrected Sheet",
        command=lambda: upload_corrected_sheet(root),
        width=button_width,
        padx=20,
        pady=10,
        bg="pink",
        font=("Arial", 14)
    )
    btn_upload_corrected.grid(row=2, column=1, pady=5, sticky='ew')

    btn_upload_students = tk.Button(
        inner_frame,
        text="Student Sheets",
        command=lambda: upload_student_sheets(root),
        width=button_width,
        padx=20,
        pady=10,
        bg="lightyellow",
        font=("Arial", 14)
    )
    btn_upload_students.grid(row=3, column=1, pady=5, sticky='ew')

    btn_reset_students = tk.Button(
        inner_frame,
        text="Reset Students",
        command=reset_students_file,
        width=button_width,
        padx=20,
        pady=10,
        bg="lightblue",
        font=("Arial", 14)
    )
    btn_reset_students.grid(row=4, column=1, pady=5, sticky='ew')

    btn_results = tk.Button(
        inner_frame,
        text="Results",
        command=extract_results,
        width=button_width,
        padx=20,
        pady=10,
        bg="lightgreen",
        font=("Arial", 14)
    )
    btn_results.grid(row=5, column=1, pady=5, sticky='ew')



    # Calculate the window size
    window_width = button_width * 10 + 40
    window_height = (button_width * 3 + 20) * 3 + 100  # Adjusted as needed

    # Add a small margin to make the window slightly larger than the buttons
    margin = 20
    window_width += margin
    window_height += margin

    # Set the window size
    root.geometry(f"{window_width}x{window_height}")

    root.mainloop()
