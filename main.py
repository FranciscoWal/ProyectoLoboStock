import flet as ft
from src.pages.home_page import HomePage
from src.pages.login_page import LoginPage
def main(page: ft.Page):
    page.title = "Proyecto Universitario Flet PWA"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 300
    page.window_resizable = True
    login = LoginPage(page)
    page.add(login.view)  # Ahora view es el Container retornado
    page.update()  # Actualiza aquí

ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER)