import flet as ft

def main(page: ft.Page):
    page.title="TO DO LIST"
    
    def add_clicked(e):
            tasks_view.controls.append(ft.Checkbox(label=new_task.value))
            new_task.value = ""
            page.update()

    new_task = ft.TextField(hint_text="O QUE QUERES FAZER?", expand=True)
    tasks_view = ft.Column()
    
    view=ft.SafeArea(
    ft.Column(
        width=500,
        controls=[
            ft.Row(
                controls=[
                    new_task, 
                    ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_clicked)
                ],
            ),
            tasks_view,
        ],
    ))
    
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(view)
    
    page.update()
    
ft.app(target=main, view=ft.WEB_BROWSER)