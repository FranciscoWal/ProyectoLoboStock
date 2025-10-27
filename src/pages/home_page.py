import flet as ft

class HomePage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.view = self.home_view()

    def home_view(self):
        # Obtener datos de la sesión
        user_rol = self.page.session.get("user_rol")
        user_carrera = self.page.session.get("user_carrera")

        # Lógica de logout
        def logout(e):
            # Limpiar sesión (opcional, pero buena práctica)
            self.page.session.clear()
            
            # Recargar la aplicación (la forma más simple de volver al login)
            # Idealmente, usaríamos page.go("/login") si usáramos el Router de Flet
            # Pero para esta estructura, recargar la página funciona.
            
            # Dado que main.py carga LoginPage por defecto, podemos
            # simplemente limpiar y recargar la vista de login.
            
            # Importar aquí para evitar dependencia circular
            from src.pages.login_page import LoginPage
            
            login_page_instance = LoginPage(self.page)
            self.page.controls.clear()
            self.page.add(login_page_instance.view)
            self.page.update()

        # Vista simple de "Bienvenida"
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(f"¡Bienvenido a EduStock!", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Text(f"Has iniciado sesión como: {user_rol}"),
                    ft.Text(f"Carrera (simulada): {user_carrera}"),
                    ft.Divider(),
                    ft.ElevatedButton("Cerrar Sesión", icon=ft.Icons.LOGOUT, on_click=logout, color=ft.Colors.WHITE, bgcolor=ft.Colors.RED_500)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            alignment=ft.alignment.center,
            padding=20,
            expand=True
        )