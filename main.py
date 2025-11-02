import flet as ft
from database.db_manager import init_db
from src.pages.login_page import login_page

def main(page: ft.Page):
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    init_db()
    login_page(page)

ft.app(target=main)
