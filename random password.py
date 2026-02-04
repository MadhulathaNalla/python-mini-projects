import tkinter as tk
from tkinter import messagebox
import random
import string

# ================= GENERATE PASSWORD =================
def generate_password():
    length_str = length_entry.get().strip()

    if not length_str.isdigit():
        messagebox.showerror("Input Error", "Password length must be a number")
        return

    length = int(length_str)

    if length < 6:
        messagebox.showwarning("Length Warning", "Password should be at least 6 characters")
        return

    chars = ""
    mandatory = []

    # Letters
    if letters_var.get():
        chars += string.ascii_letters
        mandatory.append(random.choice(string.ascii_letters))
    # Numbers
    if numbers_var.get():
        chars += string.digits
        mandatory.append(random.choice(string.digits))
    # Symbols
    if symbols_var.get():
        chars += string.punctuation
        mandatory.append(random.choice(string.punctuation))

    if not chars:
        messagebox.showerror("Selection Error", "Select at least one character type")
        return

    # Generate password
    password_chars = [random.choice(chars) for _ in range(length - len(mandatory))]
    password_chars += mandatory
    random.shuffle(password_chars)
    password = "".join(password_chars)

    # Show in entry
    result_entry.delete(0, tk.END)
    result_entry.insert(0, password)

# ================= COPY TO CLIPBOARD =================
def copy_to_clipboard():
    password = result_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard")
    else:
        messagebox.showwarning("No Password", "Generate a password first")

# ================= GUI =================
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("400x350")

tk.Label(root, text="Password Length:").pack()
length_entry = tk.Entry(root)
length_entry.pack()

letters_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Letters (A-Z, a-z)", variable=letters_var).pack()
tk.Checkbutton(root, text="Numbers (0-9)", variable=numbers_var).pack()
tk.Checkbutton(root, text="Symbols (!,@,#,...) ", variable=symbols_var).pack()

tk.Button(root, text="Generate Password", command=generate_password).pack(pady=10)
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).pack(pady=5)

tk.Label(root, text="Generated Password:").pack(pady=5)
result_entry = tk.Entry(root, width=30)
result_entry.pack()

root.mainloop()
