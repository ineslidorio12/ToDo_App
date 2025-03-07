import flet as ft
from task import Task
from storage import save_task, load_task


class ToDoApp(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.new_task = ft.TextField(hint_text="O que precisas fazer?", expand = True)
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
                            ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=self.add_task)
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
        self.load_task_saved()
        
        
    def load_task_saved(self):
        tasking_loading = load_task(self.page)
        for t in tasking_loading:
            task = Task(t["nome"], self.update_view, self.remove_task)
            task.completed = t["concluida"]
            task.display_task.value = t["concluida"]
            self.tasks.controls.append(task)
        self.update_view()
    
    
    def add_task(self, e):
        if self.new_task.value.strip():
            task = Task(self.new_task.value.strip(), self.update_view, self.remove_task)
            self.tasks.controls.append(task)
            self.new_task.value = ""
            self.update_view()
            
        
    def remove_task(self, task):
        self.tasks.controls.remove(task)
        self.update_view()
    
    def clear_completed(self, e):
        self.tasks.controls = [task for task in self.tasks.controls if not task.completed]
        self.update_view()
    
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
        save_task(self.page, self.tasks.controls)
        self.page.update()

    
def main(page: ft.Page):
    page.title="TO DO LIST"        
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    
    todo = ToDoApp(page)
    page.add(todo)
    
ft.app(target=main, view=ft.WEB_BROWSER)