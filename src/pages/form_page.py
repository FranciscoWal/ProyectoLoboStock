import flet as ft
from database.db_manager import insertar_solicitud, verificar_adeudo

def formulario(page,career):

    nombre = ft.TextField(label="Nombre completo", width=300)
    expediente = ft.TextField(label="Número de expediente", width=300)
    carrera = ft.TextField(label="Carrera", width=300)
    material = ft.TextField(label="Material requerido", width=300)
    tiempo_uso = ft.TextField(label="Tiempo de uso (horas)", width=300)
    

    mensaje = ft.Text("", color=ft.Colors.GREEN)

    def enviar(e):
        if not nombre.value or not expediente.value or not carrera.value or not material.value or not tiempo_uso.value:
            mensaje.value = "Por favor completa todos los campos"
            mensaje.color = ft.Colors.RED

        elif not tiempo_uso.value.isdigit():
            mensaje.value = "Ingresa un número válido en tiempo de uso"
            mensaje.color = ft.Colors.RED

       
        elif verificar_adeudo(expediente.value):
            mensaje.value = "No puedes enviar solicitudes. Tienes un adeudo pendiente."
            mensaje.color = ft.Colors.RED
            
        else:
            insertar_solicitud( nombre.value, expediente.value, carrera.value, material.value,  int(tiempo_uso.value))
            mensaje.value = "Solicitud enviada correctamente"
            mensaje.color = ft.Colors.GREEN
            nombre.value = expediente.value = carrera.value = material.value = tiempo_uso.value = ""
        page.update()

    def regresar(e):
        from src.pages.home_page import home_page
        page.clean()
        home_page(page)

    page.add(
        ft.Column([
            ft.Text(f"Solicitud de Material — {career}", size=25, weight="bold"),
            nombre, expediente,carrera, material, tiempo_uso,
            ft.Row([
                ft.ElevatedButton("Enviar", on_click=enviar),
                ft.OutlinedButton("Regresar", on_click=regresar)
            ], alignment="center"),
            mensaje
        ], horizontal_alignment="center", spacing=15)
    )
