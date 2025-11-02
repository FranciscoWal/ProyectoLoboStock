import flet as ft
import sqlite3
from database.db_manager import DB_PATH

def solicitudes_page(page: ft.Page):
    page.title = "Solicitudes — Panel de Administración"

    def obtener_solicitudes():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, carrera, material, fecha, estado FROM solicitudes ORDER BY fecha DESC")
        data = cursor.fetchall()
        conn.close()
        return data

    def mostrar_detalle(e, solicitud):
        id, nombre, carrera, material, fecha, estado = solicitud

        dialog = ft.AlertDialog(
            title=ft.Text(f"Detalles de solicitud #{id}"),
            content=ft.Column([
                ft.Text(f" Nombre: {nombre}"),
                ft.Text(f" Carrera: {carrera}"),
                ft.Text(f"Material: {material}"),
                ft.Text(f"Fecha: {fecha}"),
                ft.Text(f"Estado: {estado}")
            ], tight=True, spacing=5),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: page.dialog.close())],
            actions_alignment="end"
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def regresar(e):
        from src.pages.admin_page import admin_page
        page.clean()
        admin_page(page)

    solicitudes = obtener_solicitudes()
    lista = []

    if not solicitudes:
        lista.append(ft.Text("No hay solicitudes aún.", color=ft.Colors.GREY))
    else:
        for s in solicitudes:
            id, nombre, carrera, material, fecha, estado = s
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"{nombre} — {carrera}", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Material: {material}"),
                        ft.Text(f"Estado: {estado}"),
                        ft.Text(f"Fecha: {fecha}", size=12, color=ft.Colors.GREY)
                    ], spacing=3),
                    padding=15,
                    on_click=lambda e, solicitud=s: mostrar_detalle(e, solicitud)
                ),
                width=500
            )
            lista.append(card)

    page.add(
        ft.Column([
            ft.Text("Solicitudes recibidas", size=25, weight=ft.FontWeight.BOLD),
            ft.Column(lista, spacing=10, scroll="auto"),
            ft.OutlinedButton("Regresar", on_click=regresar)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
    )
