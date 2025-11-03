import flet as ft
import sqlite3
from functools import partial
from database.db_manager import DB_PATH, asignar_adeudo, quitar_adeudo, obtener_estado_adeudo

def solicitudes_page(page: ft.Page):
    page.title = "Solicitudes — Panel de Administración"

    def obtener_solicitudes():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, expediente, carrera, material, fecha, estado FROM solicitudes ORDER BY fecha DESC")
        data = cursor.fetchall()
        conn.close()
        return data

    def eliminar_solicitud(id_):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM solicitudes WHERE id=?", (id_,))
        conn.commit()
        conn.close()
        actualizar_vista()

    def actualizar_vista():
        page.clean()
        solicitudes_page(page)

    # --- Funciones de adeudo ---
    def asignar_adeudo_click(e, expediente, nombre):
        asignar_adeudo(expediente)
        page.snack_bar = ft.SnackBar(ft.Text(f"Se asignó adeudo al estudiante {nombre}"))
        page.snack_bar.open = True
        actualizar_vista()

    def quitar_adeudo_click(e, expediente, nombre):
        quitar_adeudo(expediente)
        page.snack_bar = ft.SnackBar(ft.Text(f"Se quitó adeudo al estudiante {nombre}"))
        page.snack_bar.open = True
        actualizar_vista()

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
            id_, nombre, expediente, carrera, material, fecha, estado = s
            estado_adeudo = obtener_estado_adeudo(expediente)
            color_adeudo = ft.Colors.RED if estado_adeudo else ft.Colors.GREEN
            texto_adeudo = "Con adeudo" if estado_adeudo else "Sin adeudo"

            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(f"{nombre} — {carrera}", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Expediente: {expediente}", size=12, color=ft.Colors.GREY)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                        ft.Text(f"Material: {material}"),
                        ft.Text(f"Estado: {estado}"),
                        ft.Text(f"Fecha: {fecha}", size=12, color=ft.Colors.GREY),
                        ft.Text(f"Adeudo: {texto_adeudo}", color=color_adeudo),

                        ft.Row([
                            ft.ElevatedButton(
                                text="Asignar adeudo",
                                icon=ft.Icons.BLOCK,
                                bgcolor=ft.Colors.RED,
                                color=ft.Colors.WHITE,
                                on_click=partial(asignar_adeudo_click, expediente=expediente, nombre=nombre)
                            ),
                            ft.ElevatedButton(
                                text="Quitar adeudo",
                                icon=ft.Icons.CHECK,
                                bgcolor=ft.Colors.GREEN,
                                color=ft.Colors.WHITE,
                                on_click=partial(quitar_adeudo_click, expediente=expediente, nombre=nombre)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                tooltip="Eliminar solicitud",
                                on_click=partial(lambda e, id=id_: eliminar_solicitud(id))
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
                    ]),
                    padding=15
                ),
                width=550
            )
            lista.append(card)

    page.add(
        ft.Column([
            ft.Text("Solicitudes recibidas", size=25, weight=ft.FontWeight.BOLD),
            ft.Column(lista, spacing=10, scroll="auto"),
            ft.OutlinedButton("Regresar", on_click=regresar, icon=ft.Icons.ARROW_BACK),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
    )
