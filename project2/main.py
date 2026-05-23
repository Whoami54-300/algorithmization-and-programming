import tkinter as tk
from tkinter import messagebox
import json
import os


TASKS_FILE = "tasks.json"


class StudentTaskTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Task Tracker")
        self.root.geometry("600x500")

        self.tasks = []

        self.create_widgets()
        self.load_tasks()
        self.update_task_list()

    def create_widgets(self):
        title_label = tk.Label(
            self.root,
            text="Трекер заданий студента",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)

        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        subject_label = tk.Label(form_frame, text="Предмет:")
        subject_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.subject_entry = tk.Entry(form_frame, width=35)
        self.subject_entry.grid(row=0, column=1, padx=5, pady=5)

        task_label = tk.Label(form_frame, text="Задание:")
        task_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.task_entry = tk.Entry(form_frame, width=35)
        self.task_entry.grid(row=1, column=1, padx=5, pady=5)

        deadline_label = tk.Label(form_frame, text="Дедлайн:")
        deadline_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

        self.deadline_entry = tk.Entry(form_frame, width=35)
        self.deadline_entry.grid(row=2, column=1, padx=5, pady=5)

        add_button = tk.Button(
            self.root,
            text="Добавить задание",
            command=self.add_task,
            width=25
        )
        add_button.pack(pady=10)

        self.task_listbox = tk.Listbox(self.root, width=80, height=12)
        self.task_listbox.pack(pady=10)

        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=10)

        delete_button = tk.Button(
            buttons_frame,
            text="Удалить выбранное",
            command=self.delete_task,
            width=20
        )
        delete_button.grid(row=0, column=0, padx=5)

        save_button = tk.Button(
            buttons_frame,
            text="Сохранить",
            command=self.save_tasks,
            width=20
        )
        save_button.grid(row=0, column=1, padx=5)

        self.status_label = tk.Label(
            self.root,
            text="Готово",
            fg="green"
        )
        self.status_label.pack(pady=10)

    def add_task(self):
        subject = self.subject_entry.get().strip()
        task = self.task_entry.get().strip()
        deadline = self.deadline_entry.get().strip()

        if not subject or not task or not deadline:
            messagebox.showwarning(
                "Ошибка",
                "Заполни все поля: предмет, задание и дедлайн."
            )
            return

        new_task = {
            "subject": subject,
            "task": task,
            "deadline": deadline
        }

        self.tasks.append(new_task)
        self.update_task_list()
        self.save_tasks()

        self.subject_entry.delete(0, tk.END)
        self.task_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)

        self.status_label.config(text="Задание добавлено", fg="green")

    def delete_task(self):
        selected_index = self.task_listbox.curselection()

        if not selected_index:
            messagebox.showwarning(
                "Ошибка",
                "Сначала выбери задание из списка."
            )
            return

        index = selected_index[0]
        deleted_task = self.tasks.pop(index)

        self.update_task_list()
        self.save_tasks()

        self.status_label.config(
            text=f"Удалено: {deleted_task['task']}",
            fg="red"
        )

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)

        for task in self.tasks:
            line = f"{task['subject']} | {task['task']} | дедлайн: {task['deadline']}"
            self.task_listbox.insert(tk.END, line)

    def save_tasks(self):
        with open(TASKS_FILE, "w", encoding="utf-8") as file:
            json.dump(self.tasks, file, ensure_ascii=False, indent=4)

        self.status_label.config(text="Данные сохранены", fg="green")

    def load_tasks(self):
        if not os.path.exists(TASKS_FILE):
            self.tasks = []
            return

        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as file:
                self.tasks = json.load(file)
        except json.JSONDecodeError:
            self.tasks = []
            messagebox.showerror(
                "Ошибка",
                "Файл tasks.json поврежден. Список заданий очищен."
            )


def main():
    root = tk.Tk()
    app = StudentTaskTracker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
