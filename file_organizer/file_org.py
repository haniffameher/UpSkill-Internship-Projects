import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# File categories and their extensions
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Programs": [".exe", ".msi", ".bat", ".cmd"],
}

# Select a directory
def select_directory():
    folder = filedialog.askdirectory()

    if folder:
        folder_path.set(folder)


# Find the category of a file
def get_category(filename):
    extension = os.path.splitext(filename)[1].lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


# Generate a unique destination name if a file already exists
def get_unique_path(destination):
    if not os.path.exists(destination):
        return destination

    directory = os.path.dirname(destination)
    filename = os.path.basename(destination)
    name, extension = os.path.splitext(filename)

    counter = 1

    while True:
        new_name = f"{name}_{counter}{extension}"
        new_path = os.path.join(directory, new_name)

        if not os.path.exists(new_path):
            return new_path

        counter += 1


# Organize the files
def organize_files():
    folder = folder_path.get()

    if not folder:
        messagebox.showwarning("No Folder Selected", "Please select a folder first.")
        return

    if not os.path.isdir(folder):
        messagebox.showerror("Error", "The selected folder does not exist.")
        return

    moved_files = 0

    try:
        for filename in os.listdir(folder):
            source_path = os.path.join(folder, filename)

            # Ignore folders
            if not os.path.isfile(source_path):
                continue

            category = get_category(filename)

            # Create category folder
            category_folder = os.path.join(folder, category)
            os.makedirs(category_folder, exist_ok=True)

            # Create destination path
            destination_path = os.path.join(category_folder, filename)

            # Avoid overwriting existing files
            destination_path = get_unique_path(destination_path)

            # Move the file
            shutil.move(source_path, destination_path)

            moved_files += 1

        messagebox.showinfo(
            "Organization Complete",
            f"Successfully organized {moved_files} file(s)."
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"Something went wrong:\n{error}"
        )


# Create the GUI window
root = tk.Tk()
root.title("File Organizer")
root.geometry("600x300")
root.resizable(False, False)

# Heading
title_label = tk.Label(
    root,
    text="File Organizer",
    font=("Arial", 24, "bold")
)
title_label.pack(pady=20)

# Description
description_label = tk.Label(
    root,
    text="Select a folder and organize its files automatically.",
    font=("Arial", 11)
)
description_label.pack(pady=5)

# Folder path variable
folder_path = tk.StringVar()

# Folder path entry
path_entry = tk.Entry(
    root,
    textvariable=folder_path,
    width=55,
    font=("Arial", 10)
)
path_entry.pack(pady=15)

# Browse button
browse_button = tk.Button(
    root,
    text="Browse Folder",
    command=select_directory,
    width=18,
    font=("Arial", 10)
)
browse_button.pack(pady=5)

# Organize button
organize_button = tk.Button(
    root,
    text="Organize Files",
    command=organize_files,
    width=18,
    font=("Arial", 11, "bold")
)
organize_button.pack(pady=20)

# Start the application
root.mainloop()