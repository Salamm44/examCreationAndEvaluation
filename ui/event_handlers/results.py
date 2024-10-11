# ui/event_handlers/results.py

import tkinter as tk
from tkinter import ttk
from sheet_correction.db_con import PDFGenerator

from allstudent.student import get_all_students

def extract_results():
    # Create a new window for displaying results
    """result_window = tk.Toplevel()
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
    pass"""
    result_window = tk.Toplevel()
    result_window.title("Student Results")
    frame = tk.Frame(result_window)
    frame.pack(fill=tk.BOTH, expand=True)

    # Create a treeview to display the results
    tree = ttk.Treeview(frame, columns=("ID", "Name", "Score"), show='headings')
    tree.heading("ID", text="Student ID")
    tree.heading("Name", text="Name")
    tree.heading("Score", text="Score")
    tree.pack(fill=tk.BOTH, expand=True)
    y_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=y_scrollbar.set)

    # Pack the treeview and scrollbar
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    

    # Create an instance of PDFGenerator (assumes database is passed or preset in PDFGenerator)
    pdf_gen = PDFGenerator()
    pdf_gen.connect()  # Connect to the database

    # Query to fetch all student data from the database
    query = "SELECT stu_id, stu_name, score FROM Students"
    cursor = pdf_gen.connection.cursor()
    cursor.execute(query)
    
    # Fetch all data
    students = cursor.fetchall()

    # Insert student data into the treeview
    for student in students:
        tree.insert("", tk.END, values=(student[0], student[1], student[2]))

    # Close database connection
    cursor.close()
    pdf_gen.close()