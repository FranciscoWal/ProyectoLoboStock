import flet as ft
from database.db_manager import insertar_solicitud, verificar_adeudo

def formulario(page, career):
    nombre = ft.TextField(label="Nombre completo", width=300)
    expediente = ft.TextField(label="Número de expediente", width=300)
    carrera = ft.TextField(label="Carrera", width=300)
    material = ft.TextField(label="Material requerido", width=300)
    laboratorio = ft.TextField(label="Laboratorio (ej. Lab. Redes, Electrónica...)", width=300)

    # TimePickers 
    hora_inicio_picker = ft.TimePicker()
    hora_entrega_picker = ft.TimePicker()

    hora_inicio_field = ft.TextField(label="Hora de inicio", read_only=True, width=300)
    hora_entrega_field = ft.TextField(label="Hora de entrega", read_only=True, width=300)

    def abrir_hora_inicio(e):
        page.open(hora_inicio_picker)

    def abrir_hora_entrega(e):
        page.open(hora_entrega_picker)

    def set_hora_inicio(e):
        if hora_inicio_picker.value:
            hora_inicio_field.value = hora_inicio_picker.value.strftime("%H:%M")
            page.update()

    def set_hora_entrega(e):
        if hora_entrega_picker.value:
            hora_entrega_field.value = hora_entrega_picker.value.strftime("%H:%M")
            page.update()

    hora_inicio_picker.on_change = set_hora_inicio
    hora_entrega_picker.on_change = set_hora_entrega

    mensaje = ft.Text("", color=ft.Colors.GREEN)

    def enviar(e):
        if not nombre.value or not expediente.value or not carrera.value or not material.value or not laboratorio.value:
            mensaje.value = "Por favor completa todos los campos."
            mensaje.color = ft.Colors.RED

        elif not hora_inicio_field.value or not hora_entrega_field.value:
            mensaje.value = "Debes seleccionar la hora de inicio y la hora de entrega."
            mensaje.color = ft.Colors.RED

        elif verificar_adeudo(expediente.value):
            mensaje.value = "No puedes enviar solicitudes. Tienes un adeudo pendiente."
            mensaje.color = ft.Colors.RED

        else:
            insertar_solicitud(
                nombre.value,
                expediente.value,
                carrera.value,
                material.value,
                laboratorio.value,
                hora_inicio_field.value,
                hora_entrega_field.value
            )
            mensaje.value = "Solicitud enviada correctamente."
            mensaje.color = ft.Colors.GREEN

            # Limpiar campos
            nombre.value = expediente.value = carrera.value = material.value = laboratorio.value = ""
            hora_inicio_field.value = hora_entrega_field.value = ""

        page.update()

    def regresar(e):
        from src.pages.home_page import home_page
        page.clean()
        home_page(page)

    #  Estructura visual 
    page.add(
        hora_inicio_picker,
        hora_entrega_picker,
        ft.Column([
            ft.Text(f"Solicitud de Material — {career}", size=25, weight="bold"),
            nombre,
            expediente,
            carrera,
            material,
            laboratorio,

           
            ft.Row([
                ft.Container(
                    content=hora_inicio_field,
                    width=300
                ),
                ft.IconButton(icon=ft.Icons.ACCESS_TIME, tooltip="Seleccionar hora de inicio", on_click=abrir_hora_inicio)
            ], alignment="center"),

            ft.Row([
                ft.Container(
                    content=hora_entrega_field,
                    width=300
                ),
                ft.IconButton(icon=ft.Icons.ACCESS_TIME, tooltip="Seleccionar hora de entrega", on_click=abrir_hora_entrega)
            ], alignment="center"),

            ft.Row([
                ft.ElevatedButton("Enviar", on_click=enviar),
                ft.OutlinedButton("Regresar", on_click=regresar)
            ], alignment="center"),

            mensaje
        ],
        horizontal_alignment="center",
        spacing=15)
    )
