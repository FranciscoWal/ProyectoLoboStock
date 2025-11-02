import flet as ft
from src.pages.home_page import home_page
from src.pages.admin_page import admin_page  
from database.db_manager import validar_usuario

def login_page(page: ft.Page):
    page.title = "Login Sistema de Solicitud de Materiales"
    
    username = ft.TextField(label="Usuario", width=300)
    password = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    mensaje = ft.Text("", color=ft.Colors.RED)
    
    def iniciar_sesion(e):
        rol = validar_usuario(username.value, password.value)
        if rol == "estudiante":
            page.clean()
            home_page(page)  #  a la pantalla de solicitudes
        elif rol == "admin":
            page.clean()
            admin_page(page)  # Pantalla de administración
        else:
            mensaje.value = "Usuario o contraseña incorrectos"
            page.update()
    
    page.add(
        ft.Column([
            ft.Text("Login", size=30, weight=ft.FontWeight.BOLD),
            username,
            password,
            ft.ElevatedButton("Iniciar sesión", on_click=iniciar_sesion),
            mensaje
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
    )
