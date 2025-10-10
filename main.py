import flet as ft
from src.pages.home_page import HomePage

def main(page: ft.Page):
    page.title = "Proyecto Universitario Flet PWA"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 300
    page.window_resizable = True
    
    # Carga la página principal
    home = HomePage(page)
    page.add(home.view)

ft.app(target=main, assets_dir="assets", view=ft.WEB_BROWSER)