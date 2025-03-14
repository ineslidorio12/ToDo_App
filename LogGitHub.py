import os
import flet as ft
from flet import ElevatedButton, LoginEvent, Page
from flet.auth.providers import GitHubOAuthProvider

class GitHubAuth:
    def __init__(self, page: Page):
        self.page = page
        self.provider = GitHubOAuthProvider(
            client_id=os.getenv("GITHUB_CLIENT_ID"),
            client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
            redirect_url="http://localhost:5000/oauth_callback",
        )

        self.login_button = ElevatedButton("Login with GitHub", on_click=self.login_button_click)
        self.logout_button = ElevatedButton("Logout", on_click=self.logout_button_click)

        self.page.on_login = self.on_login
        self.page.on_logout = self.on_logout

        self.toggle_login_buttons()
        self.page.add(self.login_button, self.logout_button)


    def login_button_click(self, e):
        self.page.login(self.provider, scope=["public_repo"])

    def on_login(self, e: LoginEvent):
        if not e.error:
            self.toggle_login_butttons()
    
    def logout_button_click(self, e):
        self.page.logout()
    
    def on_logout(self, e):
        self.toggle_login_buttons()

    def toggle_login_buttons(self):
        self.login_button.visible = self.page.auth is None
        self.logout_button.visible = self.page.auth is not None
        self.page.update()


