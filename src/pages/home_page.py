import flet as ft
from src.components.custom_button import CustomButton
from src.utils.helpers import generate_greeting

class HomePage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.view = self._build_view()
    
    def _build_view(self):
        # Texto principal
        self.greeting_text = ft.Text(
            value=generate_greeting("Estudiante"),
            size=20,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD
        )
        
        # Imagen placeholder (usa tu asset)
        image = ft.Image(
            src="images/mi-imagen.png",
            width=100,
            height=100,
            fit=ft.ImageFit.CONTAIN
        )
        
        # Botón custom
        def on_button_click(e):
            self.greeting_text.value = generate_greeting("Usuario Interactivo")
            self.page.update()
        
        button = CustomButton(
            text="¡Cambiar Saludo!",
            on_click=on_button_click,
            width=200
        )
        
        # Contenedor principal
        return ft.Column(
            [
                ft.Container(
                    content=image,
                    alignment=ft.alignment.center,
                    margin=10
                ),
                self.greeting_text,
                ft.Container(
                    content=button,
                    alignment=ft.alignment.center,
                    margin=10
                )
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )