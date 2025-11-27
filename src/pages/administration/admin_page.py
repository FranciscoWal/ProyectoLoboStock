#src/pages/adminitration/admin_page.py
import flet as ft
from .solicitudes_page import solicitudes_page
from .inventario_page import inventario_page
from .estadisticas_page import estadisticas_page

def admin_page(page: ft.Page, carrera_admin: str):
    page.title = f"Panel de Administración — {carrera_admin}"

    
    def abrir_solicitudes(e):
        page.clean()
        solicitudes_page(page, carrera_admin)

    def abrir_inventario(e):
        page.clean()
        inventario_page(page, carrera_admin)

    def abrir_estadisticas(e):
        page.clean()
        estadisticas_page(page, carrera_admin)

   
    secciones = [
        ("Solicitudes", ft.Icons.DESCRIPTION, abrir_solicitudes),
        ("Inventario", ft.Icons.COMPUTER, abrir_inventario),
        ("Estadísticas", ft.Icons.STACKED_BAR_CHART, abrir_estadisticas)
        
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
            ft.Text(f"Panel de Administración ({carrera_admin})", size=30, weight=ft.FontWeight.BOLD),
            ft.Row(cards, alignment=ft.MainAxisAlignment.CENTER, spacing=20, wrap=True),
            ft.OutlinedButton("Cerrar sesión", on_click=salir)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
