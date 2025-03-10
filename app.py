import flet as ft
from task import Task
from styles import NEW_TASK_STYLE, ADD_BUTTON_STYLE
from encrypt_decrypt import encrypt_data, decrypt_data
import json

class ToDoApp(ft.Column):
    STORAGE_KEY = "tasks"
    
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.new_task = ft.TextField(hint_text="O que precisas fazer?", expand = True, **NEW_TASK_STYLE)
        self.tasks = ft.Column()
        
        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.update_view,
            tabs=[ft.Tab(text="all"), ft.Tab(text="active"), ft.Tab(text="completed")],
        )
        self.items_left = ft.Text("0 items left")
        
        self.view = ft.SafeArea(
            ft.Column(
                width=500,
                controls=[
                    ft.Row(
                        [ft.Text(value="To-Dos", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                            self.new_task, 
                            ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=self.add_task, **ADD_BUTTON_STYLE)
                        ],
                    ),
                    self.filter,
                    self.tasks,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            self.items_left,
                            ft.TextButton("Clear completed", on_click=self.clear_completed)
                        ]
                    ),
                ],
            )
        )
        self.controls.append(self.view)
        self.load_tasks()
        
    
    def add_task(self, e):
        if self.new_task.value.strip():
            task = Task(self.new_task.value.strip(), self.update_view, self.remove_task)
            self.tasks.controls.append(task)
            self.new_task.value = ""
            self.update_view()
            self.save_tasks()
            
        
    def remove_task(self, task):
        self.tasks.controls.remove(task)
        self.update_view()
        self.save_tasks()
    
    def clear_completed(self, e):
        self.tasks.controls = [task for task in self.tasks.controls if not task.completed]
        self.update_view()
        self.save_tasks()
    
    def update_view(self, e=None):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and task.completed == False)
                or (status == "completed" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} active item(s) left"
        self.page.update()


    def save_tasks(self):
        tasks_data = [{"name": task.display_task.label, "completed": task.completed} for task in self.tasks.controls]
        tasks_json = json.dumps(tasks_data)
        
        encrypted_data = encrypt_data(tasks_json)
        self.page.client_storage.set(self.STORAGE_KEY, encrypted_data)
    
    
    def load_tasks(self):
        encrypted_data = self.page.client_storage.get(self.STORAGE_KEY)
        if encrypted_data:
            try:
                decrypted_data = decrypt_data(encrypted_data)
                tasks_data = json.loads(decrypted_data)
                
                for task_info in tasks_data:
                    task = Task(task_info["name"], self.update_view, self.remove_task)
                    task.completed = task_info["completed"]
                    task.display_task.value = task.completed
                    self.tasks.controls.append(task)
                self.update_view()
            except Exception as e:
                print("Erro carregamento de tarefas:", e)
        
        
def main(page: ft.Page):
    page.title="TO DO LIST"        
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    
    todo = ToDoApp(page)
    page.add(todo)
    
ft.app(target=main, view=ft.WEB_BROWSER, host="0.0.0.0", port=5000)
