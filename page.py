import flet as ft
from styles import ICON_STYLE
from github import GitHubAuth


class LoginPage(ft.Column):
    def __init__(self, page: ft.Page, on_login_success):
        super().__init__()
        self.page = page
        self.on_login_success = on_login_success  
        self.icon = ft.Image(**ICON_STYLE)

        self.github_button = ft.ElevatedButton(
            text="Login com GitHub",
            icon=ft.icons.GITHUB,
            on_click=self.authenticate_github,
        )

        self.controls = [self.icon, self.github_button]

    def authenticate_github(self, e):
        auth = GitHubAuth(self.page)
        if auth.login():  
            self.on_login_success() 
