# ui/event_handlers/results.py

import tkinter as tk
from tkinter import ttk
from answers_manager import get_correct_answers
from student import get_all_students

def extract_results():
    # Create a new window for displaying results
    result_window = tk.Toplevel()
    result_window.title("Student Results")

    # Create a treeview to display the results
    tree = ttk.Treeview(result_window, columns=("ID", "Name", "Score"), show='headings')
    tree.heading("ID", text="Student ID")
    tree.heading("Name", text="Name")
    tree.heading("Score", text="Score")
    tree.pack(fill=tk.BOTH, expand=True)

    # Get all students
    students = get_all_students()

    # Insert student data into the treeview
    for student in students:
        tree.insert("", tk.END, values=(student.student_id, student.name, student.score))
