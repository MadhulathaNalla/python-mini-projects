import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# ================= DATABASE SETUP =================
def init_db():
    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bmi_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        weight REAL NOT NULL,
        height REAL NOT NULL,
        bmi REAL NOT NULL,
        date TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

init_db()

# ================= FUNCTIONS =================
def calculate_bmi():
    name = name_entry.get().strip()
    weight = weight_entry.get().strip()
    height = height_entry.get().strip()

    if not name or not weight or not height:
        messagebox.showwarning("Input Error", "All fields are required")
        return

    try:
        weight = float(weight)
        height = float(height)

        if weight <= 0 or height <= 0:
            messagebox.showerror("Input Error", "Values must be positive")
            return

        bmi = weight / (height ** 2)

        # ---- BMI CATEGORY ----
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        date = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect("bmi_data.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bmi_records (name, weight, height, bmi, date) VALUES (?,?,?,?,?)",
            (name, weight, height, round(bmi, 2), date)
        )
        conn.commit()
        conn.close()

        # ---- DISPLAY RESULT ----
        result_label.config(
            text=f"BMI: {bmi:.2f}\nCategory: {category}"
        )

        messagebox.showinfo("Success", "BMI record saved successfully")

    except ValueError:
        messagebox.showerror("Input Error", "Weight and height must be numbers")

def view_history():
    name = name_entry.get().strip()

    if not name:
        messagebox.showwarning("Input Error", "Please enter name")
        return

    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT bmi, date FROM bmi_records WHERE name=? ORDER BY date",
        (name,)
    )
    records = cursor.fetchall()
    conn.close()

    history_text.delete(1.0, tk.END)

    if records:
        for bmi, date in records:
            history_text.insert(tk.END, f"{date}  →  BMI: {bmi}\n")
    else:
        history_text.insert(tk.END, "No records found")

def show_graph():
    name = name_entry.get().strip()

    if not name:
        messagebox.showwarning("Input Error", "Please enter name")
        return

    conn = sqlite3.connect("bmi_data.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT bmi, date FROM bmi_records WHERE name=? ORDER BY date",
        (name,)
    )
    records = cursor.fetchall()
    conn.close()

    if not records:
        messagebox.showwarning("No Data", "No data available for graph")
        return

    bmis = [r[0] for r in records]
    dates = [r[1] for r in records]

    plt.figure()
    plt.plot(dates, bmis, marker='o')
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.title(f"BMI Trend for {name}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ================= GUI =================
root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("450x520")

tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Weight (kg)").pack()
weight_entry = tk.Entry(root)
weight_entry.pack()

tk.Label(root, text="Height (m)").pack()
height_entry = tk.Entry(root)
height_entry.pack()

tk.Button(root, text="Calculate & Save BMI", command=calculate_bmi).pack(pady=5)
tk.Button(root, text="View History", command=view_history).pack(pady=5)
tk.Button(root, text="Show BMI Trend Graph", command=show_graph).pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.pack(pady=5)

history_text = tk.Text(root, height=12, width=50)
history_text.pack(pady=10)

root.mainloop()
