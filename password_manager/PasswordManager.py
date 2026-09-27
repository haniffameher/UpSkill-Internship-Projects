import sqlite3
import secrets
import string
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

# Encryption Key

KEY_FILE = "secret.key"

def load_key():
    try:
        with open(KEY_FILE, "rb") as file:
            return file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()

        with open(KEY_FILE, "wb") as file:
            file.write(key)

        return key


key = load_key()
cipher = Fernet(key)


# Database Setup


def create_database():
    connection = sqlite3.connect("passwords.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# Generate Strong Password

def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation

    password = ''.join(
        secrets.choice(characters) for _ in range(16)
    )

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


# Add Password


def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if website == "" or username == "" or password == "":
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all fields."
        )
        return

    encrypted_password = cipher.encrypt(
        password.encode()
    )

    connection = sqlite3.connect("passwords.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO passwords (website, username, password)
        VALUES (?, ?, ?)
    """, (website, username, encrypted_password.decode()))

    connection.commit()
    connection.close()

    messagebox.showinfo(
        "Success",
        "Password saved successfully!"
    )

    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


# View Passwords


def view_passwords():
    connection = sqlite3.connect("passwords.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM passwords")
    records = cursor.fetchall()

    connection.close()

    if not records:
        messagebox.showinfo(
            "Saved Passwords",
            "No passwords stored."
        )
        return

    result = ""

    for record in records:
        decrypted_password = cipher.decrypt(
            record[3].encode()
        ).decode()

        result += (
            f"ID: {record[0]}\n"
            f"Website: {record[1]}\n"
            f"Username: {record[2]}\n"
            f"Password: {decrypted_password}\n"
            f"{'-' * 35}\n"
        )

    messagebox.showinfo(
        "Saved Passwords",
        result
    )


# Delete Password


def delete_password():

    password_id = delete_entry.get()

    if password_id == "":
        messagebox.showwarning(
            "Missing ID",
            "Please enter the ID to delete."
        )
        return

    try:
        password_id = int(password_id)
    except ValueError:
        messagebox.showwarning(
            "Invalid ID",
            "Please enter a valid number."
        )
        return

    connection = sqlite3.connect("passwords.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM passwords WHERE id = ?",
        (password_id,)
    )

    connection.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo(
            "Success",
            "Password deleted successfully!"
        )
    else:
        messagebox.showwarning(
            "Not Found",
            "No password found with that ID."
        )

    connection.close()
    delete_entry.delete(0, tk.END)

    # Create Database

create_database()

    # GUI Window

root = tk.Tk()
root.title("Password Manager")
root.geometry("500x600")
root.resizable(False, False)


# Title


title_label = tk.Label(
    root,
    text="PASSWORD MANAGER",
    font=("Arial", 20, "bold")
)

title_label.pack(pady=20)


# Website


tk.Label(
    root,
    text="Website / App Name",
    font=("Arial", 11)
).pack()

website_entry = tk.Entry(
    root,
    width=40,
    font=("Arial", 11)
)

website_entry.pack(pady=5)



# Username


tk.Label(
    root,
    text="Username / Email",
    font=("Arial", 11)
).pack()

username_entry = tk.Entry(
    root,
    width=40,
    font=("Arial", 11)
)

username_entry.pack(pady=5)


# Password


tk.Label(
    root,
    text="Password",
    font=("Arial", 11)
).pack()

password_entry = tk.Entry(
    root,
    width=40,
    font=("Arial", 11)
)

password_entry.pack(pady=5)



# Generate Button


generate_button = tk.Button(
    root,
    text="Generate Strong Password",
    command=generate_password,
    width=25
)

generate_button.pack(pady=10)


# Save Button


save_button = tk.Button(
    root,
    text="Save Password",
    command=save_password,
    width=25
)

save_button.pack(pady=5)


# View Button

view_button = tk.Button(
    root,
    text="View Saved Passwords",
    command=view_passwords,
    width=25
)

view_button.pack(pady=5)


# Delete Section


tk.Label(
    root,
    text="Enter ID to Delete",
    font=("Arial", 11)
).pack(pady=(20, 5))

delete_entry = tk.Entry(
    root,
    width=20,
    font=("Arial", 11)
)

delete_entry.pack(pady=5)


delete_button = tk.Button(
    root,
    text="Delete Password",
    command=delete_password,
    width=25
)

delete_button.pack(pady=5)


# Exit Button

exit_button = tk.Button(
    root,
    text="Exit",
    command=root.destroy,
    width=25
)

exit_button.pack(pady=20)


# Start GUI


root.mainloop()