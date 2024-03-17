import cv2
import numpy as np
import mysql.connector
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk
import dlib
import os

# Khởi tạo bộ nhận diện khuôn mặt dlib
detector = dlib.get_frontal_face_detector()

# Kết nối đến MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="face_recognizer"
)

mycursor = mydb.cursor()

# Tạo bảng để lưu dữ liệu
mycursor.execute("CREATE TABLE IF NOT EXISTS face_count_camera (id INT AUTO_INCREMENT PRIMARY KEY, timestamp DATETIME, count INT, image_path VARCHAR(255))")

# Hàm để đếm số lượng người từ ảnh sử dụng dlib
def count_people(image):
    # Chuyển ảnh sang đen trắng
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Sử dụng bộ nhận diện khuôn mặt dlib để xác định các khuôn mặt trong ảnh
    faces = detector(gray)

    # Trả về số lượng khuôn mặt được phát hiện
    return len(faces)

# Hàm để lưu dữ liệu vào MySQL và ảnh vào thư mục img_face_count_camera của dự án

def save_to_database(count, image, label):
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H-%M-%S')

    # Lưu thông tin vào MySQL
    sql = "INSERT INTO face_count_camera (timestamp, count, image_path) VALUES (%s, %s, %s)"
    image_path = f"img_face_count_camera/{timestamp}.jpg"
    full_image_path = os.path.join("D:/Nghiên cứu khoa học-2024/face_recognizer/img_face_count_camera", image_path)

    # Lưu ảnh vào thư mục img_face_count_camera
    cv2.imwrite(full_image_path, image)

    # Lưu thông tin vào MySQL
    val = (timestamp, count, image_path)
    mycursor.execute(sql, val)
    mydb.commit()

    # Hiển thị số người và khung xung quanh khuôn mặt sau khi lưu dữ liệu
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(image, f"Tong So Nguoi: {count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Hiển thị frame trên giao diện Tkinter
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(image)
    img = ImageTk.PhotoImage(image=img)
    label.img = img
    label.config(image=img)

    # Hiển thị số người trên label bên phải
    label.config(text=f"Số người: {count}", font=("Helvetica", 14, "bold"), fg="blue")

# Hàm xử lý sự kiện nhấn nút để lưu dữ liệu
# Hàm xử lý sự kiện nhấn nút để lưu dữ liệu
# Hàm xử lý sự kiện nhấn nút để lưu dữ liệu
def save_data(label1, label2, save_label):
    global count, frame
    save_to_database(count, frame, label2)
    # Cập nhật số người trên nhãn hiển thị số lượng người
    save_label.config(text=f"Số người: {count}", font=("Helvetica", 14, "bold"), fg="blue")

# Hàm main
def main():
    global count, frame

    # Mở camera
    cap = cv2.VideoCapture(0)

    # Tạo giao diện người dùng Tkinter
    root = tk.Tk()
    root.title("Face Counter")
    root.geometry("1200x600")

    # Hiển thị video từ camera
    label1 = tk.Label(root)
    label1.pack(side="left")

    # Hiển thị hình ảnh vừa chụp và số người
    label2 = tk.Label(root)
    label2.pack(side="right")

    # Hiển thị số người sau khi nhấn nút "Lưu dữ liệu"
    save_label = tk.Label(root, text="", font=("Helvetica", 14, "bold"), fg="blue")
    save_label.pack(anchor=tk.CENTER)
    # Tạo nút để lưu dữ liệu
    save_button = tk.Button(root, text="Lưu dữ liệu", command=lambda: save_data(label1, label2, save_label))
    save_button.pack(anchor=tk.CENTER)

    # Hiển thị video từ camera và hình ảnh chụp được cùng lúc
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Chuyển frame sang đen trắng để sử dụng bộ nhận diện khuôn mặt dlib
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Sử dụng bộ nhận diện khuôn mặt dlib để xác định các khuôn mặt trong frame
        faces = detector(gray)

        # Vẽ khung xung quanh khuôn mặt và di chuyển theo khuôn mặt
        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Đếm số người trong frame sử dụng dlib
            count = len(faces)

            # Hiển thị số người trên frame camera
            cv2.putText(frame, f"Tong So Nguoi: {count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Hiển thị frame camera trên giao diện Tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img1 = Image.fromarray(frame)
            img1 = ImageTk.PhotoImage(image=img1)
            label1.img = img1
            label1.config(image=img1)

        # Cập nhật giao diện
        root.update()

        # Thoát khỏi vòng lặp khi nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Giải phóng camera
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
