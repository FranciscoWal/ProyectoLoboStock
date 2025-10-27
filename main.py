import flet as ft
# Importamos las páginas desde el paquete 'src'
from src.pages.home_page import HomePage
from src.pages.login_page import LoginPage

def main(page: ft.Page):
    page.title = "EduStock - App Almacenes UT"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Ajustes de ventana para PWA/Web
    page.window_width = 400
    page.window_height = 650
    page.window_resizable = True
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Inicializa la página de login y obtiene su 'vista'
    login_page_instance = LoginPage(page)
    
    # Añade la vista de login a la página
    page.add(login_page_instance.view)
    
    page.update()

# Ejecuta la aplicación
ft.app(
    target=main, 
    assets_dir="assets",  # Apunta a la carpeta de assets
    view=ft.WEB_BROWSER   # Optimizado para PWA/Web
)