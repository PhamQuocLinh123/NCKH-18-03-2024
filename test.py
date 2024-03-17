import tkinter as tk
from tkinter import ttk
import mysql.connector

class Database_str:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'face_recognizer'
        self.port = '3306'

    def connect(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )

    def execute_query(self, query, params=None):
        conn = self.connect()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return result

# Hàm để lấy dữ liệu từ cơ sở dữ liệu
def get_data():
    db = Database_str()
    return db.execute_query("SELECT IdAuttendance, Student_id, Name, Class, Time_in, Date FROM attendance")

# Hàm xóa dữ liệu từ cơ sở dữ liệu
def delete_data(id_attendance):
    db = Database_str()
    query = "DELETE FROM attendance WHERE IdAuttendance = %s"
    db.execute_query(query, (id_attendance,))

# Hàm cập nhật dữ liệu trong cơ sở dữ liệu
def update_data(id_attendance, student_id, name, class_name, time_in, date):
    db = Database_str()
    query = "UPDATE attendance SET Student_id = %s, Name = %s, Class = %s, Time_in = %s, Date = %s WHERE IdAuttendance = %s"
    params = (student_id, name, class_name, time_in, date, id_attendance)
    db.execute_query(query, params)

# Hàm để xử lý sự kiện nút Xóa
def delete_button_click():
    selected_item = tree.selection()
    if selected_item:
        id_attendance = tree.item(selected_item, "values")[0]
        delete_data(id_attendance)
        refresh_data()

# Hàm để xử lý sự kiện nút Sửa
def edit_button_click():
    selected_item = tree.selection()
    if selected_item:
        id_attendance = tree.item(selected_item, "values")[0]
        update_data(id_attendance, student_id_var.get(), name_var.get(), class_var.get(), time_in_var.get(), date_var.get())
        refresh_data()

# Hàm để cập nhật dữ liệu trong Treeview
def refresh_data():
    # Xóa dữ liệu cũ
    for row in tree.get_children():
        tree.delete(row)

    # Lấy dữ liệu mới từ cơ sở dữ liệu và hiển thị trong Treeview
    data = get_data()
    for i, row in enumerate(data):
        tree.insert("", "end", text=str(i+1), values=row)

# Tạo cửa sổ giao diện Tkinter
root = tk.Tk()
root.title("Attendance Data")

# Tạo một Frame để chứa Treeview và các widget nhập liệu
frame = ttk.Frame(root)
frame.pack(pady=20)

# Tạo một Treeview để hiển thị dữ liệu
tree = ttk.Treeview(frame)
tree["columns"] = ("Mã nhận diện", "Mã Người dùng ", "Tên", "Nghành", "Giờ", "Ngày")
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=100)

# Lấy dữ liệu từ cơ sở dữ liệu và hiển thị trong Treeview
refresh_data()
tree.pack(side="left")

# Tạo thanh cuộn cho Treeview
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

# Tạo một Frame để chứa các widget nhập liệu
input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

# Widget nhập liệu
student_id_var = tk.StringVar()
name_var = tk.StringVar()
class_var = tk.StringVar()
time_in_var = tk.StringVar()
date_var = tk.StringVar()

student_id_label = ttk.Label(input_frame, text="Mã:")
student_id_entry = ttk.Entry(input_frame, textvariable=student_id_var)

name_label = ttk.Label(input_frame, text="Tên:")
name_entry = ttk.Entry(input_frame, textvariable=name_var)

class_label = ttk.Label(input_frame, text="Nghành :")
class_entry = ttk.Entry(input_frame, textvariable=class_var)

time_in_label = ttk.Label(input_frame, text="Giờ:")
time_in_entry = ttk.Entry(input_frame, textvariable=time_in_var)

date_label = ttk.Label(input_frame, text="Ngày:")
date_entry = ttk.Entry(input_frame, textvariable=date_var)

student_id_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
student_id_entry.grid(row=0, column=1, padx=5, pady=5)

name_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
name_entry.grid(row=0, column=3, padx=5, pady=5)

class_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
class_entry.grid(row=1, column=1, padx=5, pady=5)

time_in_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")
time_in_entry.grid(row=1, column=3, padx=5, pady=5)

date_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
date_entry.grid(row=2, column=1, padx=5, pady=5)

# Tạo các nút Thêm, Xóa, Sửa
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

delete_button = ttk.Button(button_frame, text="Delete", command=delete_button_click)
edit_button = ttk.Button(button_frame, text="Edit", command=edit_button_click)

delete_button.grid(row=0, column=0, padx=5, pady=5)
edit_button.grid(row=0, column=1, padx=5, pady=5)

# Chạy ứng dụng
root.mainloop()
