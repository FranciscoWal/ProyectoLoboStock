import flet as ft
from .solicitudes_page import solicitudes_page
from .inventario_page import inventario_page

# 🔹 Ahora recibe también la carrera del administrador
def admin_page(page: ft.Page, carrera_admin: str):
    page.title = f"Panel de Administración — {carrera_admin}"

    # 🔹 Estas funciones ahora pasan la carrera al abrir cada subpágina
    def abrir_solicitudes(e):
        page.clean()
        solicitudes_page(page, carrera_admin)

    def abrir_inventario(e):
        page.clean()
        inventario_page(page, carrera_admin)

    # 🔹 Lista de secciones
    secciones = [
        ("Solicitudes", ft.Icons.DESCRIPTION, abrir_solicitudes),
        ("Inventario", ft.Icons.COMPUTER, abrir_inventario),
        ("Estadisticas", ft.Icons.STACKED_BAR_CHART, abrir_inventario)
        
    ]

    # 🔹 Genera los botones tipo tarjeta
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

    # 🔹 Botón para cerrar sesión
    def salir(e):
        from src.pages.login_page import login_page
        page.clean()
        login_page(page)

    # 🔹 Estructura visual
    page.add(
        ft.Column([
            ft.Text(f"Panel de Administración ({carrera_admin})", size=30, weight=ft.FontWeight.BOLD),
            ft.Row(cards, alignment=ft.MainAxisAlignment.CENTER, spacing=20, wrap=True),
            ft.OutlinedButton("Cerrar sesión", on_click=salir)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
