import flet as ft
from src.pages.form_page import formulario


def home_page(page: ft.Page):

    
    def abrir_formulario(career):
        page.clean()
        formulario(page, career)

    
    def salir(e):
        from src.pages.login_page import login_page 
        page.clean()
        login_page(page)

    page.title = "Solicitud de Materiales"
    page.scroll = "adaptive"

    
    career = [
        ("Química", ft.Icons.SCIENCE),
        ("Mecatrónica", ft.Icons.MISCELLANEOUS_SERVICES),
        ("Tecnologías de la Información", ft.Icons.COMPUTER),
        ("Farmacéutica", ft.Icons.BIOTECH)
    ]

   
    cards = []
    for career, icono in career:
        card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(icono, size=50, color=ft.Colors.BLUE),
                    ft.Text(career, size=18, weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.CENTER,
                   horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                on_click=lambda e, c=career: abrir_formulario(c)
            ),
            width=200,
            height=150
        )
        cards.append(card)

   
    page.add(
    ft.Column([
        ft.Text("Solicitud de Materiales", size=30, weight=ft.FontWeight.BOLD),
        ft.Row(cards, alignment=ft.MainAxisAlignment.CENTER, wrap=True, spacing=20),
        ft.OutlinedButton("Salir", on_click=salir)
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER) 
)

