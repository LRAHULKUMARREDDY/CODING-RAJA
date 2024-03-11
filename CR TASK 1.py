#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import json
from datetime import datetime, timedelta

class ToDoList:
    def __init__(self, file_path="tasks.json"):
        self.file_path = file_path
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                tasks = json.load(file)
            return tasks
        return {"tasks": []}

    def save_tasks(self):
        with open(self.file_path, "w") as file:
            json.dump(self.tasks, file, indent=2)

    def add_task(self, title, priority, due_date=None):
        new_task = {
            "title": title,
            "priority": priority,
            "due_date": due_date.strftime("%Y-%m-%d") if due_date else None,
            "completed": False,
        }
        self.tasks["tasks"].append(new_task)
        self.save_tasks()

    def remove_task(self, task_index):
        if 0 <= task_index < len(self.tasks["tasks"]):
            del self.tasks["tasks"][task_index]
            self.save_tasks()

    def mark_completed(self, task_index):
        if 0 <= task_index < len(self.tasks["tasks"]):
            self.tasks["tasks"][task_index]["completed"] = True
            self.save_tasks()

    def display_tasks(self):
        if not self.tasks["tasks"]:
            print("No tasks found.")
            return

        print("\nTask List:")
        for i, task in enumerate(self.tasks["tasks"]):
            status = " [ ]"
            if task["completed"]:
                status = " [X]"
            print(f"{i + 1}. {status} {task['title']} - Priority: {task['priority']}", end="")
            if task["due_date"]:
                print(f", Due Date: {task['due_date']}", end="")
            print()

def main():
    todo_list = ToDoList()

    while True:
        print("\nOptions:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Mark Task as Completed")
        print("4. Display Tasks")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            title = input("Enter task title: ")
            priority = input("Enter priority (high/medium/low): ")
            due_date_str = input("Enter due date (YYYY-MM-DD) or press Enter for no due date: ")
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d") if due_date_str else None
            todo_list.add_task(title, priority, due_date)

        elif choice == "2":
            todo_list.display_tasks()
            task_index = int(input("Enter the task number to remove: ")) - 1
            todo_list.remove_task(task_index)

        elif choice == "3":
            todo_list.display_tasks()
            task_index = int(input("Enter the task number to mark as completed: ")) - 1
            todo_list.mark_completed(task_index)

        elif choice == "4":
            todo_list.display_tasks()

        elif choice == "5":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()


# In[ ]:




