import flet as ft
from src.pages.solicitudes_page import solicitudes_page

def admin_page(page: ft.Page):
    page.title = "Panel de Administración"

    def abrir_solicitudes(e):
        page.clean()
        solicitudes_page(page)

    # para luego agregar mas 
    secciones = [
        ("Solicitudes", ft.Icons.DESCRIPTION, abrir_solicitudes),
       
    ]

    cards = []
    for titulo, icono, funcion in secciones:
        card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(icono, size=50, color=ft.Colors.BLUE),
                    ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                on_click=funcion
            ),
            width=200,
            height=150
        )
        cards.append(card)

    def salir(e):
        from src.pages.login_page import login_page
        page.clean()
        login_page(page)

    page.add(
        ft.Column([
            ft.Text("Panel de Administración", size=30, weight=ft.FontWeight.BOLD),
            ft.Row(cards, alignment=ft.MainAxisAlignment.CENTER, spacing=20, wrap=True),
            ft.OutlinedButton("Cerrar sesión", on_click=salir)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
