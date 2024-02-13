import tkinter as tk
from tkinter import filedialog
from sklearn.ensemble import RandomForestRegressor
from PIL import Image, ImageTk
import csv
import os

# สร้างคลาส RandomForestApp
class RandomForestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Forest App")  # ตั้งชื่อหน้าต่าง
        self.root.geometry("1080x720")  # กำหนดขนาดหน้าต่าง
        self.widgets()  # เรียกใช้เมธอดสร้างวิดเจ็ต

    # เมธอดสร้างวิดเจ็ตต่างๆ
    def widgets(self):
        greeting = tk.Label(self.root, text="Random Forest App", fg="black", font=("Arial", 16))  # ข้อความต้อนรับ
        greeting.place(x=10, y=10)  # กำหนดตำแหน่งข้อความ

        self.frame1 = tk.Frame(self.root, width=500, height=500, bg="#001466")  # สร้างเฟรมสำหรับแสดงข้อมูล
        self.frame1.place(x=30, y=50)  # กำหนดตำแหน่งเฟรม

        frame2 = tk.Frame(self.root, width=370, height=500, bg="#612180")  # เฟรมสำหรับการรับข้อมูล
        frame2.place(x=700, y=10)  # กำหนดตำแหน่งเฟรม

        frame2_text = tk.Label(frame2, text="INPUT", fg="white", font=("Arial", 20), bg="#612180")  # ข้อความส่วนหัวเฟรม
        frame2_text.place(x=260, y=10)  # กำหนดตำแหน่งข้อความ

        input_labels = ["rice varieties", "Soil quality", "temp", "fertilizer", "Pests"]  # รายการของข้อความ Label
        self.input_entries = []  # ลิสต์สำหรับเก็บ Entry ของข้อมูลที่ใส่

        # สร้าง Label และ Entry สำหรับรับข้อมูล
        for i, label_text in enumerate(input_labels):
            label = tk.Label(frame2, text=label_text, fg="white", font=("Arial", 14), bg="#612180")
            label.place(x=20, y=70 + i * 40)  # กำหนดตำแหน่ง Label
            
            var = tk.StringVar()
            var.set("0")
            entry = tk.Entry(frame2, textvariable=var, font=("Arial", 14), bg="white")
            entry.place(x=120, y=70 + i * 40)  # กำหนดตำแหน่ง Entry

            self.input_entries.append(entry)  # เก็บ Entry ลงในลิสต์

        frame3 = tk.Frame(self.root, width=1065, height=220, bg="#50E943")  # เฟรมสำหรับแสดงผลลัพธ์
        frame3.place(x=5, y=510)  # กำหนดตำแหน่งเฟรม

        frame4 = tk.Frame(self.root, width=970, height=180, bg="#FFFFFF")  # เฟรมสำหรับปุ่ม
        frame4.place(x=55, y=560)  # กำหนดตำแหน่งเฟรม

        # สร้างปุ่มเพื่อเปิดไฟล์ CSV และทำนาย
        openfile_button = tk.Button(frame4, text="Click Me", command=self.open_file, font=("Arial", 18), bg="#87ceeb", fg="black")
        openfile_button.grid(row=0, column=0, pady=30, padx=120)  # กำหนดตำแหน่งปุ่ม

        predict_button = tk.Button(frame4, text="Predict", command=self.predict, font=("Arial", 18), bg="#A577BB", fg="black")
        predict_button.grid(row=0, column=1, pady=30, padx=120)  # กำหนดตำแหน่งปุ่ม

        self.predict_label = tk.Label(frame4, text="Predict: unknown", font=("Arial", 22), bg="#FFFFFF", fg="black")
        self.predict_label.grid(row=0, column=2, pady=30, padx=30)  # กำหนดตำแหน่ง Label ผลลัพธ์

        # ข้อมูลตัวอย่าง
        self.data = [
            ["rice varieties", "Soil quality", "temp", "fertilizer", "Pests", "produk"],
            [4, 1, 30, 1, 0, 2.5],
            [4, 0, 29, 1, 0, 2.5],
            [4, 1, 30, 1, 1, 1.3],
            [4, 1, 28, 0, 1, 2.5],
            [4, 2, 31, 0, 0, 2.3],
            [4, 0, 25, 1, 1, 2.2],
            [4, 0, 27, 1, 0, 0.5],
            [4, 1, 29, 0, 0, 0.9],
            [4, 2, 30, 0, 1, 2.2],
            [4, 2, 30, 1, 1, 2.2],
            [5, 1, 29, 1, 0, 2],
            [5, 1, 27, 1, 1, 2],
            [5, 0, 24, 0, 0, 0.3],
            [5, 1, 25, 1, 1, 0.5],
            [5, 2, 25, 0, 1, 2.3],
            [4, 0, 25, 1, 1, 2.5],
            [4, 0, 29, 0, 0, 2.3],
            [4, 2, 29, 0, 0, 2.2],
            [4, 1, 30, 0, 0, 0.5],
            [4, 1, 30, 1, 1, 2],
            [3, 1, 31, 1, 1, 1.9],
            [3, 1, 8, 0, 0, 0.5],
            [3, 0, 27, 1, 1, 0.7],
            [3, 0, 27, 1, 0, 0.2],
            [3, 2, 26, 0, 1, 0.7],
            [4, 1, 26, 1, 0, 0.8],
            [4, 0, 25, 1, 0, 1],
            [5, 1, 26, 1, 1, 1.4],
            [5, 1, 24, 0, 1, 1.3],
            [5, 2, 28, 0, 0, 1.5],
            [5, 0, 29, 1, 1, 2],
            [5, 0, 30, 1, 0, 1.9],
            [4, 1, 30, 0, 0, 2.1],
            [4, 2, 30, 0, 1, 1.5],
            [4, 2, 30, 1, 1, 1.8],
            [4, 1, 31, 1, 0, 0.5],
            [3, 1, 27, 1, 0, 0.9],
            [3, 0, 26, 0, 1, 1.2],
            [3, 1, 25, 1, 1, 1.6],
            [3, 2, 25, 0, 0, 1.7],
            [4, 0, 29, 1, 1, 1.7],
            [4, 0, 29, 0, 0, 1.8],
            [2, 2, 28, 0, 0, 1.5],
            [2, 1, 24, 0, 1, 1.5],
            [2, 1, 25, 1, 1, 2],
            [2, 1, 26, 1, 0, 2.2],
            [5, 1, 27, 0, 0, 0.5],
            [2, 0, 24, 1, 1, 1.3],
            [2, 0, 25, 1, 1, 0.8],
            [5, 2, 28, 0, 0, 2.3],
            [5, 1, 26, 1, 1, 2.5],
            [5, 0, 28, 1, 0, 2.5],
            [5, 1, 25, 1, 0, 1.8],
            [5, 1, 26, 0, 1, 0.9],
            [4, 2, 29, 0, 1, 0.4],
            [4, 0, 29, 1, 0, 1.3],
            [4, 0, 28, 1, 0, 1.8],
            [2, 1, 27, 0, 1, 1.4],
            [2, 2, 23, 0, 1, 0.7],
            [2, 2, 23, 1, 0, 1.8],
            [2, 1, 25, 1, 1, 2.1],
            [2, 1, 28, 1, 0, 1.3],
            [3, 0, 28, 0, 0, 1.1],
            [3, 1, 28, 1, 1, 1.1],
            [3, 2, 28, 0, 1, 1.4],
            [3, 0, 27, 1, 0, 1.2],
            [2, 0, 26, 0, 0, 1.5],
            [2, 2, 26, 0, 1, 1.6],
            [2, 1, 25, 0, 1, 1.1],
            [2, 1, 25, 1, 0, 2.5],
            [2, 1, 25, 1, 1, 2.3],
            [5, 1, 26, 0, 0, 2],
            [4, 0, 28, 1, 0, 1.9],
            [4, 0, 29, 1, 1, 1.4],
            [4, 2, 29, 0, 1, 2.5],
            [4, 1, 30, 1, 0, 2.9],
            [2, 0, 30, 1, 0, 2.5],
            [2, 1, 30, 1, 1, 0.8],
            [2, 1, 28, 0, 1, 1],
            [2, 2, 28, 0, 0, 1.5],
            [2, 0, 27, 1, 1, 1.9],
            [5, 0, 26, 1, 0, 1.5],
            [5, 1, 29, 0, 0, 1.2],
            [5, 2, 29, 0, 1, 3.2],
            [5, 2, 29, 1, 1, 3],
            [5, 1, 26, 1, 0, 1.3],
            [5, 1, 26, 1, 0, 1.2],
            [5, 0, 25, 0, 1, 2.1],
            [5, 1, 25, 1, 1, 2.1],
            [4, 2, 27, 0, 0, 2.8],
            [4, 0, 24, 1, 1, 2.5],
            [4, 0, 23, 0, 0, 2.3],
            [4, 2, 25, 0, 0, 1.9],
            [4, 1, 28, 0, 1, 1.5],
            [3, 1, 29, 1, 1, 1.1],
            [3, 1, 29, 1, 0, 2.1],
            [3, 1, 27, 0, 0, 2.1],
            [3, 0, 25, 1, 1, 2],
            [3, 0, 28, 1, 1, 2.7],
            [4, 2, 28, 0, 0, 3.1]
        ]   

        self.update_frame1()  # เรียกใช้เมธอดเพื่อแสดงข้อมูลในเฟรมแรก

    # เมธอดสำหรับเปิดไฟล์ CSV
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.load_data_from_csv(file_path)

        
    def predict(self):
        user_input = [float(entry.get()) for entry in self.input_entries[:4]]

        # Use RandomForestRegressor instead of LinearRegression
        rf_model = RandomForestRegressor()

        X_train = [row[:-2] for row in self.data[1:]]  # เลือกข้อมูลเข้าใน X_train โดยไม่เอาสองคอลัมน์สุดท้าย
        y_train = [row[-1] for row in self.data[1:]]    # เลือกผลลัพธ์เข้าใน y_train จากคอลัมน์สุดท้าย

        rf_model.fit(X_train, y_train)  # ใช้ข้อมูลใน X_train และ y_train ในการฝึกโมเดล RandomForestRegressor
        prediction = rf_model.predict([user_input])  # ทำนายผลลัพธ์จากข้อมูลที่ผู้ใช้ป้อนเข้ามา

        predicted_value = round(prediction[0], 1)  # ปัดเศษของผลลัพธ์ที่ทำนายได้เป็นทศนิยมหนึ่งตำแหน่ง
        self.predict_label.configure(text=f"Predict: {predicted_value}")  # แสดงผลลัพธ์ที่ทำนายได้บน Label ใน GUI

    def load_data_from_csv(self, csv_file):
        try:
            with open(csv_file, 'r') as file:
                reader = csv.reader(file)
                raw_data = [row for row in reader]  # อ่านข้อมูลจากไฟล์ CSV และเก็บไว้ในรูปของรายการข้อมูล

            headers = raw_data[0]  # ใช้ข้อมูลบรรทัดแรกเป็นส่วนหัวของข้อมูล

            # แปลงข้อมูลจากสตริงเป็นตัวเลข และเก็บข้อมูลในรูปแบบที่เหมาะสมสำหรับการใช้งาน
            self.data = [headers] + [[int(cell) if i < 4 else float(cell) for i, cell in enumerate(row)] for row in raw_data[1:]]

            self.update_frame1()  # อัปเดต Frame ใน GUI ด้วยข้อมูลที่โหลดเข้ามา
        except FileNotFoundError:
            print(f"Error: CSV file '{csv_file}' not found.")  # แสดงข้อผิดพลาดเมื่อไม่พบไฟล์ CSV

    def update_frame1(self):
        for widget in self.frame1.winfo_children():
            widget.destroy()  # ลบวิดเจ็ตทั้งหมดออกจาก Frame ที่กำลังใช้งาน

        # สร้าง Label สำหรับแสดงข้อมูลในแต่ละเซลล์ของตาราง
        for i, row in enumerate(self.data):
            for j, value in enumerate(row):
                label = tk.Label(self.frame1, width=10, height=1, text=str(value), bg="#FFFFFF", fg="black")
                label.grid(row=i, column=j, padx=10, pady=10)  # จัดวาง Label ในตำแหน่งที่เหมาะสมใน Frame
                if i == 0:
                    label.configure(bg="#F1D3FF")  # ตั้งค่าสีพื้นหลังของ Label ในแถวแรกของตารางเป็นสีเทาอ่อน


def main():
    root = tk.Tk()  # สร้างหน้าต่างหลักของแอปพลิเคชัน
    app = RandomForestApp(root)  # สร้างแอปพลิเคชันโดยใช้หน้าต่างหลักที่สร้างขึ้นมา
    root.mainloop()  # เริ่มการทำงานของแอปพลิเคชัน

if __name__ == "__main__":
    main()  # เรียกฟังก์ชัน main เพื่อเริ่มต้นการทำงานของโปรแกรม
