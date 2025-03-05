import flet as ft
from task import Task


class ToDoApp(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.new_task = ft.TextField(hint_text="O que precisas fazer?", expand = True)
        self.tasks_view = ft.Column()
        self.view = ft.SafeArea(
            ft.Column(
                width=500,
                controls=[
                    ft.Row(
                        controls=[
                            self.new_task, 
                            ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=self.add_clicked)
                        ],
                    ),
                    self.tasks_view,
                ],
            )
        )
        self.controls.append(self.view)
    
    def add_clicked(self, e):
        if self.new_task.value.strip():
            task = Task(self.new_task.value, self.task_delete)
            self.tasks_view.controls.append(task)
            self.new_task.value = ""
            self.page.update()
        
    def task_delete(self, task):
        self.tasks_view.controls.remove(task)
        self.page.update()
        
    
def main(page: ft.Page):
    page.title="TO DO LIST"        
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    
    todo = ToDoApp(page)
    page.add(todo)
    
ft.app(target=main, view=ft.WEB_BROWSER)