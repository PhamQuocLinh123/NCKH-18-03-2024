import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
import os


class FaceRecognizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognizer Data")

        self.tree = ttk.Treeview(root, columns=("ID", "Timestamp", "Count", "Image"))
        self.tree.heading("ID", text="ID")
        self.tree.heading("Timestamp", text="Timestamp")
        self.tree.heading("Count", text="Count")
        self.tree.heading("Image", text="Image")
        self.tree.pack(fill="both", expand=True)

        self.load_data()

    def load_data(self):
        # Connect to MySQL database
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="face_recognizer"
            )

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM face_count_camera")
            rows = cursor.fetchall()

            # Insert data into treeview
            for row in rows:
                # Get the absolute path of the image file
                image_path = os.path.join(os.path.dirname(__file__), row[3])

                # Load image from file
                img = Image.open(image_path)
                img.thumbnail((100, 100))  # Resize image if needed
                img = ImageTk.PhotoImage(img)
                self.tree.insert("", "end", values=(row[0], row[1], row[2], img))

                # Keep a reference to the image to prevent it from being garbage collected
                self.tree.image_references.append(img)

            cursor.close()
            connection.close()

        except mysql.connector.Error as error:
            print("Error while connecting to MySQL", error)


def main():
    root = tk.Tk()
    app = FaceRecognizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
