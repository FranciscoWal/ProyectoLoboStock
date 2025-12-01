import flet as ft
from database.db_manager import init_db
from src.pages.login_page import login_page


def main(page: ft.Page):
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Ayuda a que el viewport web no “corte” el alto
    page.window_min_height = 640

    init_db()
    login_page(page)


ft.app(
    target=main,
    assets_dir="assets",
    view=ft.AppView.WEB_BROWSER,
)
