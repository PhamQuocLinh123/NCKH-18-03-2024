import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
import os


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Tạo thanh cuộn dọc
        vscrollbar = tk.Scrollbar(self, orient="vertical")
        vscrollbar.pack(side="right", fill="y", expand=False)
        # Tạo thanh cuộn ngang
        hscrollbar = tk.Scrollbar(self, orient="horizontal")
        hscrollbar.pack(side="bottom", fill="x", expand=False)

        # Tạo canvas để chứa khung cuộn
        canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set,
                           xscrollcommand=hscrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)

        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)

        # Tạo khung để chứa nội dung
        self.scrollable_frame = tk.Frame(canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("DỮ LIỆU ĐẾM TỪ ẢNH")

        # Thiết lập kích thước tối đa cho cửa sổ
        self.geometry('1400x900')

        # Tạo khung chứa dữ liệu có thể cuộn
        self.scroll_frame = ScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True)

        self.display_images()

        # Tạo nút chuyển trang
        self.create_button()

    def display_images(self):
        # Kết nối đến cơ sở dữ liệu MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='face_recognizer'
        )
        cursor = conn.cursor()

        # Truy vấn dữ liệu từ bảng face_count
        cursor.execute("SELECT image_name, timestamp, count FROM face_count")
        results = cursor.fetchall()

        row_num = 0  # Số dòng hiện tại
        col_num = 0  # Số cột hiện tại
        max_cols = 4  # Số cột tối đa trên mỗi dòng

        # Hiển thị hình ảnh, timestamp và count từ các bản ghi trong kết quả truy vấn
        for result in results:
            image_path = result[0]
            timestamp = result[1]
            count = result[2]

            image = Image.open(image_path)
            image = image.resize((350, 250), Image.BILINEAR)

            photo = ImageTk.PhotoImage(image)
            label = tk.Label(self.scroll_frame.scrollable_frame, image=photo,
                             text=f"Timestamp: {timestamp}\nCount: {count}", compound=tk.BOTTOM)
            label.image = photo

            # Đặt khung vào dòng và cột tương ứng
            label.grid(row=row_num, column=col_num, padx=10, pady=10)

            col_num += 1
            if col_num == max_cols:
                row_num += 1
                col_num = 0

        # Đóng kết nối đến cơ sở dữ liệu
        cursor.close()
        conn.close()

    def create_button(self):
        # Tạo nút "Đếm số người"
        button = tk.Button(self, text="Đếm số người", command=self.open_face_count)
        button.pack()

    def open_face_count(self):
        # Mở trang face_count.py
        os.system("python face_count.py")


app = App()
app.mainloop()
