from cryptography.fernet import Fernet
import os
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext

FILE_NAME = "passwords_encrypted.txt"
KEY_FILE = "key.key"
MASTER_PASSWORD = "eren yeager"  # Set your secure master password


def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)


def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as f:
        return f.read()


fernet = Fernet(load_key())



def register_user():
    username = simpledialog.askstring("Register", "Enter username:")
    password = simpledialog.askstring("Register", "Enter password:", show='*')

    if username and password:
        encrypted_password = fernet.encrypt(password.encode()).decode()
        with open(FILE_NAME, "a") as f:
            f.write(f"Username: {username}\nEncrypted Password: {encrypted_password}\n\n")
        messagebox.showinfo("Success", "User registered with encrypted password!")
    else:
        messagebox.showwarning("Input Error", "Username and password cannot be empty.")



def view_users():
    entered = simpledialog.askstring("Master Password", "Enter master password:", show='*')
    if entered != MASTER_PASSWORD:
        messagebox.showerror("Access Denied", "Wrong master password!")
        return

    if not os.path.exists(FILE_NAME):
        messagebox.showinfo("No Data", "No credentials found.")
        return

    with open(FILE_NAME, "r") as f:
        content = [line.strip() for line in f if line.strip() != ""]

    result = ""
    i = 0
    while i < len(content):
        try:
            if content[i].startswith("Username:") and content[i + 1].startswith("Encrypted Password:"):
                username = content[i].split("Username: ")[1]
                encrypted_pass = content[i + 1].split("Encrypted Password: ")[1]
                decrypted_pass = fernet.decrypt(encrypted_pass.encode()).decode()
                result += f"👤 Username: {username}\n🔑 Password: {decrypted_pass}\n\n"
                i += 2
            else:
                i += 1
        except Exception as e:
            result += f"⚠️ Skipped a corrupted entry: {e}\n"
            i += 1

    if not result:
        result = "No users found or data corrupted."
    show_output(result)



def delete_user():
    username_to_delete = simpledialog.askstring("Delete User", "Enter username to delete:")
    if not username_to_delete or not os.path.exists(FILE_NAME):
        messagebox.showerror("Error", "Invalid username or file not found.")
        return

    with open(FILE_NAME, "r") as file:
        lines = file.readlines()

    new_lines = []
    skip_next = False
    deleted = False

    for i in range(len(lines)):
        if skip_next:
            skip_next = False
            continue

        if lines[i].strip().startswith("Username:") and username_to_delete in lines[i]:
            skip_next = True
            deleted = True
            continue
        new_lines.append(lines[i])

    with open(FILE_NAME, "w") as file:
        file.writelines(new_lines)

    if deleted:
        messagebox.showinfo("Deleted", "User deleted successfully!")
    else:
        messagebox.showwarning("Not Found", "Username not found.")



def show_output(text):
    output_window = tk.Toplevel(root)
    output_window.title("Stored Users")
    st = scrolledtext.ScrolledText(output_window, width=60, height=20, font=("Arial", 11))
    st.pack(padx=10, pady=10)
    st.insert(tk.END, text)
    st.config(state=tk.DISABLED)


# GUI Setup
root = tk.Tk()
root.title("🔐 Encrypted User Manager")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="Encrypted User Manager", font=("Arial", 16, "bold")).pack(pady=20)

tk.Button(root, text="➕ Register User", command=register_user, width=25).pack(pady=5)
tk.Button(root, text="🔍 View Saved Credentials", command=view_users, width=25).pack(pady=5)
tk.Button(root, text="🗑️ Delete a User", command=delete_user, width=25).pack(pady=5)
tk.Button(root, text="❌ Exit", command=root.quit, width=25).pack(pady=20)

root.mainloop()
