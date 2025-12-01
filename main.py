# main.py
import flet as ft
import os
from database.db_manager import init_db
from src.pages.login_page import login_page

def main(page: ft.Page):
    page.title = "Mi App PWA"                    # Pon aquí el nombre de tu app
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_min_height = 640
    page.padding = 0
    page.spacing = 0

    # Esto hace que funcione como PWA y quede bien en móviles
    page.window_width = 450          # ancho típico de móvil
    page.window_height = 800
    page.window_resizable = False

    init_db()
    login_page(page)

# ──────────────────────────────────────────────────────────────
#  CLAVE: estas líneas hacen que funcione OFFLINE y en Render
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Render asigna un puerto dinámico → hay que usarlo
    port = int(os.environ.get("PORT", 8000))

    ft.app(
        target=main,
        assets_dir="assets",
        view=ft.WEB_BROWSER,
        port=port,
        host="0.0.0.0",                    # obligatorio en Render
        web_renderer="html",               # ← OFFLINE 100 % desde la primera vez
        use_color_emoji=True,              # emojis bonitos
        # Opcional pero muy recomendado para PWA:
        route_url_strategy="hash",         # evita errores 404 al recargar páginas
    )
