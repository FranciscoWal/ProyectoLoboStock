import flet as ft
# Importaciones corregidas para la estructura de 'src'
from src.components.theme import create_ut_theme, ut_button
from src.utils.helpers import validate_credentials, get_user_carrera
# Importamos HomePage para la navegación
from src.pages.home_page import HomePage

class LoginPage:
    def __init__(self, page: ft.Page):
        self.page = page
        # Configs globales que se aplican a la página
        self.page.title = "EduStock - Iniciar Sesión"
        self.page.theme = create_ut_theme()
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        
        # self.view contendrá el ft.Container retornado por login_view()
        self.view = self.login_view()

    def login_view(self):
        # Logo UT (asegúrate que la ruta 'assets/images/logo_ut.png' exista)
        logo = ft.Image(
            src="assets/images/logo_ut.png", 
            width=200, 
            height=100, 
            fit=ft.ImageFit.CONTAIN
        )

        # Campos de texto (los definimos aquí para que sean accesibles en login_click)
        email_field = ft.TextField(
            label="Email Institucional",
            hint_text="ejemplo@ut.edu",
            prefix_icon=ft.Icons.EMAIL,
            width=300,
            border_radius=10
        )
        
        password_field = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK,
            width=300,
            border_radius=10
        )
        
        rol_dropdown = ft.Dropdown(
            label="Rol",
            options=[
                ft.dropdown.Option("estudiante"), 
                ft.dropdown.Option("administrador")
            ],
            value="estudiante",
            width=300,
            border_radius=10
        )

        def login_click(e):
            email = email_field.value
            password = password_field.value
            selected_rol = rol_dropdown.value

            # Validar credenciales (usando el helper)
            creds = validate_credentials(email, password, selected_rol)
            
            if creds["success"]:
                # 1. Guardar info en la sesión de la página
                self.page.session.set("user_rol", creds["rol"])
                self.page.session.set("user_id", creds["user_id"])
                
                # Simular obtención y guardado de carrera
                carrera = get_user_carrera(creds["user_id"])
                self.page.session.set("user_carrera", carrera)
                
                # 2. Mostrar feedback (CORREGIDO)
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"¡Bienvenido! Iniciando como {creds['rol']}..."),
                    bgcolor=ft.Colors.GREEN_500
                )
                self.page.snack_bar.open = True
                
                # 3. NAVEGAR: Limpiar la vista actual y cargar la Home Page
                self.page.controls.clear() # Limpia la vista de Login
                
                # Instancia la nueva página
                home_page_instance = HomePage(self.page)
                
                # Añade la vista de Home
                self.page.add(home_page_instance.view)
                
            else:
                # Mostrar error (CORREGIDO)
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text(creds.get("error", "Error desconocido")),
                    bgcolor=ft.Colors.RED_500
                )
                self.page.snack_bar.open = True
            
            # Actualizar la página para reflejar los cambios
            self.page.update()

        # Función helper para el botón de recuperar (CORREGIDO)
        def show_recover_snackbar(e):
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Recuperación simulada vía portal UT")
            )
            self.page.snack_bar.open = True
            self.page.update()

        # Botones
        login_btn = ut_button("Iniciar Sesión", login_click, ft.Icons.LOGIN)
        
        recover_btn = ft.TextButton(
            "¿Olvidaste tu contraseña?", 
            icon=ft.Icons.HELP_OUTLINE, 
            on_click=show_recover_snackbar # <--- CORREGIDO
        )

        # Layout centrado
        return ft.Container(
            content=ft.Column(
                [
                    logo,
                    ft.Text("EduStock - Gestión de Almacenes UT", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.TEAL_800),
                    ft.Divider(color=ft.Colors.TEAL_200, height=10),
                    email_field,
                    password_field,
                    rol_dropdown,
                    login_btn,
                    recover_btn
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                scroll=ft.ScrollMode.ADAPTIVE
            ),
            padding=20,
            border_radius=10,
            width=380 # Ancho fijo para el contenedor de login
        )