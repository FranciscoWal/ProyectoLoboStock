import flet as ft
from database.db_manager import insertar_solicitud

def formulario(page,career):

    nombre = ft.TextField(label="Nombre completo", width=300)
    expediente = ft.TextField(label="Número de expediente", width=300)
    carrera = ft.TextField(label="Carrera", width=300)
    material = ft.TextField(label="Material requerido", width=300)
    

    mensaje = ft.Text("", color=ft.Colors.GREEN)

    def enviar(e):
        if not nombre.value or not expediente.value or not carrera.value or not material.value:
            mensaje.value = "Por favor completa todos los campos"
            mensaje.color = ft.Colors.RED
        else:
            insertar_solicitud( nombre.value, expediente.value, carrera.value, material.value,)
            mensaje.value = "Solicitud enviada correctamente"
            mensaje.color = ft.Colors.GREEN
            nombre.value = expediente.value = carrera.value = material.value = ""
        page.update()

    def regresar(e):
        from src.pages.home_page import home_page
        page.clean()
        home_page(page)

    page.add(
        ft.Column([
            ft.Text(f"Solicitud de Material — {career}", size=25, weight="bold"),
            nombre, expediente,carrera, material,
            ft.Row([
                ft.ElevatedButton("Enviar", on_click=enviar),
                ft.OutlinedButton("Regresar", on_click=regresar)
            ], alignment="center"),
            mensaje
        ], horizontal_alignment="center", spacing=15)
    )
