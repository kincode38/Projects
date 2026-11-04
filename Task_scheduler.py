import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

def load_task(file_path= "tasks.json"):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
def save_tasks(tasks, file_path = "tasks.json"):
    with open(file_path, "w") as file:
        json.dump(tasks, file, indent=4)
def update_task_list(tasks):
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "✅" if task["completed"] else "❌"
        task_listbox.insert(tk.END, f"{task['title']} (Due: {task['due_date']}) [{status}]")
def add_task():
    title = title_entry.get()
    due_date = due_date_entry.get()
    if title and due_date:
        tasks.append({"title": title, "due_date": due_date, "completed": False})
        save_tasks(tasks)
        update_task_list(tasks)
        title_entry.delete(0, tk.END)
        due_date_entry.delete(0, tk.END)
        messagebox.showInfo("Info", "Task added Successfully")
def mark_task_completed():
    selected_index = task_listbox.curselection()
    if selected_index:
        task[selected_index [0]]["completed"] = True 
        save_tasks(tasks)
        update_task_list(tasks)
        messagebox.showInfo("Info", "Task has been deleted successfully")

def delete_task():
    selected = task_listbox.curselection()
    if selected:
        tasks.pop(selected[0])
        save_task(tasks)
        update_task_list(tasks)

root = tk.Tk()
root.title("Task Scheduler")
root.geometry("600x400")

title_label = ttk.Label(root, text="Task Title: ")
title_label.pack(pady=5)
title_entry = ttk.Entry(root, width=40)
title_entry.pack(pady=5)

due_date_label = ttk.Label(root, text="Due Date (YYYY-MM-DD): ")
due_date_label.pack(pady=5)
due_date_entry = ttk.Entry(root, width=40)
due_date_entry.pack(pady=5)

add_button = ttk.Button(root, text="Add Task", command=add_task)
add_button.pack(pady=10)

task_listbox = tk.Listbox(root, width=50, height=10)
task_listbox.pack(pady=10)

complete_button = ttk.Button(root, text="Mark as complete", command= mark_task_completed)
complete_button.pack(pady=5)

delete_button = ttk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack(pady=5)

tasks = load_task()
update_task_list(tasks)

root.mainloop()