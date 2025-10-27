# src/pages/login_page.py
import flet as ft
from src.components.theme import create_ut_theme, ut_button
from src.utils.helpers import validate_credentials, get_user_carrera

class LoginPage:
    def __init__(self, page: ft.Page):
        self.page = page
        # Configs globales aquí o en main.py
        self.page.title = "EduStock - Iniciar Sesión"
        self.page.theme = create_ut_theme()
        self.page.window_width = 400
        self.page.window_height = 600
        self.page.scroll = ft.ScrollMode.AUTO
        self.view = self.login_view()  # Ahora retorna la UI

    def login_view(self):  # <- ¡Agregado self! No toma page.
        # Logo UT (estilizado)
        logo = ft.Image(src="assets/images/logo_ut.png", width=200, height=100, fit=ft.ImageFit.CONTAIN)

        def login_click(e):
            email = email_field.value  # Aún accesible como local
            password = password_field.value
            selected_rol = rol_dropdown.value
            creds = validate_credentials(email, password, selected_rol)
            if creds["success"]:
                self.page.session.set("user_rol", creds["rol"])
                self.page.session.set("user_carrera", get_user_carrera(email))
                self.page.go("/dashboard")
                self.page.show_snack_bar(ft.SnackBar(
                    content=ft.Text(f"¡Bienvenido, {creds['rol']}!", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.TEAL_600
                ))
            else:
                self.page.show_snack_bar(ft.SnackBar(
                    content=ft.Text(creds.get("error", "Error desconocido"), color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_400
                ))

        # Campos formulario (estilizados)
        email_field = ft.TextField(
            label="Correo Universitario (e.g., estudiante@ut.edu)",
            icon=ft.Icons.EMAIL,  # Usa Icons en minúscula
            width=300,
            border_radius=10,
            autofocus=True,
            on_blur=lambda e: setattr(email_field, "error_text", "Formato inválido" if "@ut.edu" not in email_field.value else None),
        )
        password_field = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            icon=ft.Icons.LOCK,
            width=300,
            border_radius=10
        )
        rol_dropdown = ft.Dropdown(
            label="Rol",
            options=[ft.dropdown.Option("estudiante"), ft.dropdown.Option("administrador")],
            value="estudiante",
            width=300,
            border_radius=10
        )
        login_btn = ut_button("Iniciar Sesión", login_click, ft.Icons.LOGIN)
        recover_btn = ft.TextButton("¿Olvidaste tu contraseña?", icon=ft.Icons.HELP, 
                                    on_click=lambda e: self.page.show_snack_bar(ft.SnackBar(content=ft.Text("Recuperación simulada vía portal UT"))))

        # Layout centrado — RETORNA esto como view
        return ft.Container(
            content=ft.Column(
                [
                    logo,
                    ft.Text("EduStock - Gestión de Almacenes UT", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.TEAL_800),
                    ft.Divider(color=ft.Colors.TEAL_200),
                    email_field,
                    password_field,
                    rol_dropdown,
                    login_btn,
                    recover_btn
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                expand=True
            ),
            padding=20,
            expand=True
        )
        # No más page.add() ni update() aquí!