import os
import mysql.connector
from mysql.connector import Error
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk

class PDFGenerator:
    def __init__(self, host='localhost', port=3306, user='root', password='SSSShhhh_1000', database='Students'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """Establishes connection to MySQL."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error: {e}")
            self.connection = None

    def close(self):
        """Closes the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

    def fetch_students(self):
        """Fetches student data from the database."""
        if self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT stu_id, stu_Name FROM Students")
            return cursor.fetchall()  # Returns a list of tuples [(id, name), ...]
        
    def add_student(self, name):
     if self.connection:
         cursor = self.connection.cursor()
         try:
            # Example SQL statement; adjust the column names as necessary
             cursor.execute("INSERT INTO students (stu_name) VALUES (%s)", (name,))
             self.connection.commit()  # Commit the transaction
             print(f"Student '{name}' added successfully.")
         except Exception as e:
             print(f"An error occurred: {str(e)}")
         finally:
             cursor.close()  # Close the cursor
     else:
        print("No database connection.")


    def add_score(self, id ,score):
        if self.connection:
            cursor = self.connection.cursor()
            try:
                # Use UPDATE statement to set the score where the student ID matches
                cursor.execute("UPDATE students SET score = %s WHERE stu_id = %s", (score, id))
                self.connection.commit()
                print(f"Score '{score}' updated successfully for student ID '{id}'.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            finally:
                cursor.close()
        else:
            print("No database connection!")
    
    def clear_students_file(self):
        """Deletes all rows in the Students table."""
        if self.connection:
            cursor = self.connection.cursor()
            try:
                # Execute DELETE statement
                cursor.execute("DELETE FROM Students")
                self.connection.commit()  # Commit the transaction
                print("All student records have been deleted.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            finally:
                cursor.close()  # Close the cursor
        else:
            print("No database connection!")

    def generate_pdf(self, template_pdf_path, output_folder):
        """Generates PDFs for each student with their ID on the first page."""
        students = self.fetch_students()

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)  # Create folder if not exists

        for student_id, student_name in students:
            # Create output path for each student PDF
            output_path = os.path.join(output_folder, f"{student_name}.pdf")
            
            # Read the template PDF (multiple pages)
            reader = PdfReader(template_pdf_path)
            writer = PdfWriter()
            
            # Get the first page and draw the student ID
            first_page = reader.pages[0]
            
            # Create a canvas to overlay the student ID onto the first page
            temp_canvas_path = f"{student_name}_temp.pdf"
            c = canvas.Canvas(temp_canvas_path, pagesize=A4)
            c.setFont("Helvetica", 18)
            c.drawString(417.0, 812.0, f"{student_id}")  # Draw ID on first page
            c.save()
            
            # Read the canvas overlay and merge with the original first page
            overlay_reader = PdfReader(temp_canvas_path)
            first_page.merge_page(overlay_reader.pages[0])
            writer.add_page(first_page)
            
            # Add the remaining pages (if any) from the original PDF
            for page_num in range(1, len(reader.pages)):
                writer.add_page(reader.pages[page_num])
            
            # Write the final PDF to disk
            with open(output_path, 'wb') as output_pdf:
                writer.write(output_pdf)
            
            # Remove the temporary canvas file
            os.remove(temp_canvas_path)

            print(f"Generated PDF for: {student_name}")


