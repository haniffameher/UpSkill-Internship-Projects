import tkinter as tk
import sqlite3

# ---------------- DATABASE SETUP ----------------

connection = sqlite3.connect("quiz.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    option4 TEXT NOT NULL,
    answer TEXT NOT NULL
)
""")

# Add questions only if the database is empty
cursor.execute("SELECT COUNT(*) FROM questions")
count = cursor.fetchone()[0]

if count == 0:
    questions_data = [
        (
            "Which keyword is used to define a function in Python?",
            "func", "def", "function", "define",
            "def"
        ),
        (
            "Which data type is used to store whole numbers?",
            "float", "str", "int", "bool",
            "int"
        ),
        (
            "Which symbol is used for comments in Python?",
            "//", "#", "/*", "--",
            "#"
        ),
        (
            "Which function is used to display output in Python?",
            "input()", "display()", "print()", "show()",
            "print()"
        ),
        (
            "Which of these is a Python list?",
            "(1, 2, 3)", "[1, 2, 3]", "{1, 2, 3}", "<1, 2, 3>",
            "[1, 2, 3]"
        ),
        (
            "Which keyword is used to create a loop over a sequence?",
            "repeat", "loop", "for", "iterate",
            "for"
        ),
        (
            "Which operator is used for exponentiation?",
            "^", "//", "**", "%%",
            "**"
        ),
        (
            "Which function is used to get input from the user?",
            "scan()", "input()", "get()", "read()",
            "input()"
        ),
        (
            "Which keyword is used to make a decision in Python?",
            "if", "when", "check", "case",
            "if"
        ),
        (
            "Which library is commonly used to create GUIs in Python?",
            "NumPy", "Tkinter", "Pandas", "Math",
            "Tkinter"
        )
    ]

    cursor.executemany("""
    INSERT INTO questions
    (question, option1, option2, option3, option4, answer)
    VALUES (?, ?, ?, ?, ?, ?)
    """, questions_data)

    connection.commit()

# Get questions from database
cursor.execute("SELECT * FROM questions")
questions = cursor.fetchall()

connection.close()


# ---------------- QUIZ VARIABLES ----------------

current_question = 0
score = 0


# ---------------- GUI WINDOW ----------------

root = tk.Tk()
root.title("Python Quiz Game")
root.geometry("600x450")
root.resizable(False, False)


# ---------------- FUNCTIONS ----------------

def show_question():
    question_data = questions[current_question]

    question_label.config(text=question_data[1])

    for i in range(4):
        option_buttons[i].config(
            text=question_data[i + 2],
            command=lambda answer=question_data[i + 2]:
            check_answer(answer)
        )

    progress_label.config(
        text=f"Question {current_question + 1} of {len(questions)}"
    )


def check_answer(selected_answer):
    global current_question, score

    correct_answer = questions[current_question][6]

    if selected_answer == correct_answer:
        score += 1

    current_question += 1

    if current_question < len(questions):
        show_question()
    else:
        show_result()


def show_result():
    question_label.config(
        text=f"Quiz Completed!\n\nYour Score: {score}/{len(questions)}"
    )

    progress_label.config(text="Quiz Finished")

    for button in option_buttons:
        button.pack_forget()

    restart_button.pack(pady=20)


def restart_quiz():
    global current_question, score

    current_question = 0
    score = 0

    restart_button.pack_forget()

    for button in option_buttons:
        button.pack(pady=8)

    show_question()


# ---------------- GUI ELEMENTS ----------------

title_label = tk.Label(
    root,
    text="Python Quiz Game",
    font=("Arial", 22, "bold")
)
title_label.pack(pady=15)


progress_label = tk.Label(
    root,
    text="",
    font=("Arial", 11)
)
progress_label.pack()


question_label = tk.Label(
    root,
    text="",
    font=("Arial", 16),
    wraplength=520,
    justify="center"
)
question_label.pack(pady=25)


option_buttons = []

for i in range(4):
    button = tk.Button(
        root,
        text="",
        width=40,
        font=("Arial", 11)
    )
    button.pack(pady=8)
    option_buttons.append(button)


restart_button = tk.Button(
    root,
    text="Restart Quiz",
    width=20,
    font=("Arial", 11),
    command=restart_quiz
)


# ---------------- START QUIZ ----------------

show_question()

root.mainloop()