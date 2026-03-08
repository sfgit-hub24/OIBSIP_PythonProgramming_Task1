# -------------------------------------------------------------
# BMI Calculator with History + Graph (GUI Version)
# -------------------------------------------------------------
import csv
import os
from datetime import date, datetime
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# -------------------------------------------------------------
# Validate Input
# -------------------------------------------------------------
def validate_input(w, h):
    if w <= 0 or w > 300:
        return False
    elif h <= 0 or h > 2.5:
        return False
    else:
        return True

# -------------------------------------------------------------
# Calculate BMI
# -------------------------------------------------------------
def calculate_bmi(w, h):
    return w / (h ** 2)

# -------------------------------------------------------------
# Categorize BMI
# -------------------------------------------------------------
def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# -------------------------------------------------------------
# Save Data to CSV
# -------------------------------------------------------------
def save_data(name, weight, height, bmi):
    today = date.today()
    file_exists = os.path.exists("bmi_data.csv")

    with open("bmi_data.csv", "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Name", "Date", "Weight", "Height", "BMI"])

        writer.writerow([name, today, weight, height, bmi])

# -------------------------------------------------------------
# Show History
# -------------------------------------------------------------
def show_history():
    if not os.path.exists("bmi_data.csv"):
        messagebox.showinfo("History", "No history found.")
        return

    history_text = ""

    with open("bmi_data.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            history_text += f"{row[0]}  |  {row[1]}  |  BMI: {float(row[4]):.2f}\n"

    if history_text == "":
        history_text = "No records available."

    messagebox.showinfo("BMI History", history_text)

# -------------------------------------------------------------
# Plot Graph
# -------------------------------------------------------------
def plot_graph():
    if not os.path.exists("bmi_data.csv"):
        messagebox.showerror("Error", "No data file found.")
        return

    dates = []
    bmis = []

    with open("bmi_data.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            try:
                dates.append(datetime.strptime(row[1], "%Y-%m-%d"))
                bmis.append(float(row[4]))
            except:
                pass

    if not bmis:
        messagebox.showerror("Error", "No BMI records found.")
        return

    plt.plot(dates, bmis, marker="o")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.title("BMI Trend Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# -------------------------------------------------------------
# Run BMI (Button Function)
# -------------------------------------------------------------
def run_bmi():
    try:
        name = name_entry.get()
        w = float(weight_entry.get())
        h = float(height_entry.get())

        if not name:
            messagebox.showerror("Error", "Please enter your name.")
            return

        if not validate_input(w, h):
            messagebox.showerror("Error", "Invalid weight or height range.")
            return

        bmi = calculate_bmi(w, h)
        category = categorize_bmi(bmi)

        result_label.config(
            text=f"BMI: {bmi:.2f}\nCategory: {category}"
        )

        save_data(name, w, h, bmi)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

# -------------------------------------------------------------
# GUI Setup
# -------------------------------------------------------------
root = tk.Tk()
root.title("BMI Calculator with History + Graph")
root.geometry("450x500")
root.configure(bg="lightblue")

tk.Label(root, text="BMI Calculator", font=("Arial", 18, "bold"),
         bg="lightblue").pack(pady=15)

tk.Label(root, text="Name", bg="lightblue").pack()
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

tk.Label(root, text="Weight (kg)", bg="lightblue").pack()
weight_entry = tk.Entry(root)
weight_entry.pack(pady=5)

tk.Label(root, text="Height (m)", bg="lightblue").pack()
height_entry = tk.Entry(root)
height_entry.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12),
                        bg="lightblue")
result_label.pack(pady=15)

tk.Button(root, text="Calculate BMI",
          command=run_bmi,
          bg="green", fg="white").pack(pady=5)

tk.Button(root, text="View History",
          command=show_history,
          bg="orange").pack(pady=5)

tk.Button(root, text="Show BMI Graph",
          command=plot_graph,
          bg="purple", fg="white").pack(pady=5)

#-------------------------------------------------------------
# Run Main Application
#-------------------------------------------------------------
root.mainloop()

