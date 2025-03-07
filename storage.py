APP_PREFIX = "mycompany.todo_app"

def save_task(page, task):
    task_add = [{"nome": t.task_name, "concluida": t.completed} for t in task]
    page.client_storage.set(f"{APP_PREFIX}.tasks", task_add)

def load_task(page):
    task_load = page.client_storage.get(f"{APP_PREFIX}.tasks", [])
    return task_load if isinstance(task_load, list) else []
