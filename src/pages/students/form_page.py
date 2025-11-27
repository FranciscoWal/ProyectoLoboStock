#src/pages/students/form_page.py
import flet as ft
from database.db_manager import (
    insertar_solicitud,
    verificar_adeudo,
    buscar_materiales,
    restar_material,
    obtener_almacen_por_material
)

def formulario(page, career, usuario):
    page.title = "Solicitud de Material"

    # Datos del usuario
    nombre = ft.TextField(label="Nombre completo", width=300, value=usuario["username"], read_only=True)
    expediente = ft.TextField(label="Número de expediente", width=300, value=usuario["expediente"], read_only=True)
    carrera = ft.TextField(label="Carrera", width=300, value=usuario["carrera"], read_only=True)

    # Laboratorio
    laboratorio = ft.Dropdown(
        label="Laboratorio",
        width=300,
        options=[
            ft.dropdown.Option("Lab. Química"),
            ft.dropdown.Option("Lab. Redes"),
            ft.dropdown.Option("Lab. Mecatroníca"),
            ft.dropdown.Option("Lab. Albañiles"),
        ]
    )

    
    # MATERIALES MÚLTIPLES
    
    materiales_list = []  
    lista_visual = ft.Column()


    material_input = ft.TextField(label="Material requerido", width=300)
    cantidad_input = ft.TextField(label="Cantidad", width=120, keyboard_type=ft.KeyboardType.NUMBER)
    sugerencias = ft.Column(spacing=0)

    def actualizar_sugerencias(e):
        sugerencias.controls.clear()
        if material_input.value.strip():
            for mat in buscar_materiales(material_input.value.strip()):
                sugerencias.controls.append(
                    ft.ListTile(
                        title=ft.Text(mat),
                        on_click=lambda ev, m=mat: seleccionar_material(m)
                    )
                )
        page.update()

    def seleccionar_material(nombre_mat):
        material_input.value = nombre_mat
        sugerencias.controls.clear()
        page.update()

    material_input.on_change = actualizar_sugerencias

    def agregar_material(e):
        nombre_mat = material_input.value.strip()

        try:
            cantidad = int(cantidad_input.value)
        except:
            cantidad = 0

        if not nombre_mat or cantidad <= 0:
            return

        materiales_list.append({"material": nombre_mat, "cantidad": cantidad})

        # Mostrar visualmente
        lista_visual.controls.append(
            ft.Row([
                ft.Text(f"{nombre_mat} — {cantidad} unidades"),
                ft.IconButton(
                    icon=ft.Icons.DELETE,
                    on_click=lambda ev, m=nombre_mat: eliminar_material(m)
                )
            ])
        )

        material_input.value = ""
        cantidad_input.value = ""
        sugerencias.controls.clear()
        page.update()

    def eliminar_material(material_nombre):
        nonlocal materiales_list
        materiales_list = [m for m in materiales_list if m["material"] != material_nombre]

        lista_visual.controls.clear()
        for m in materiales_list:
            lista_visual.controls.append(
                ft.Row([
                    ft.Text(f"{m['material']} — {m['cantidad']} unidades"),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda ev, mat=m['material']: eliminar_material(mat)
                    )
                ])
            )
        page.update()

   
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
            hora_inicio_field.value = hora_inicio_picker.value.strftime("%I:%M %p")
            page.update()

    def set_hora_entrega(e):
        if hora_entrega_picker.value:
            hora_entrega_field.value = hora_entrega_picker.value.strftime("%I:%M %p")
            page.update()

    hora_inicio_picker.on_change = set_hora_inicio
    hora_entrega_picker.on_change = set_hora_entrega

 
    mensaje = ft.Text("", color=ft.Colors.GREEN)


    def enviar(e):
        if verificar_adeudo(expediente.value):
            mensaje.value = "No puedes enviar solicitudes. Tienes un adeudo pendiente."
            mensaje.color = ft.Colors.RED
            page.update()
            return

        if len(materiales_list) == 0:
            mensaje.value = "Debes agregar al menos un material."
            mensaje.color = ft.Colors.RED
            page.update()
            return

        # Crear un solo string con todos los materiales
        materiales_unificados = "\n".join(
            f"{m['material']} (x{m['cantidad']})"
            for m in materiales_list
        )

       
        almacen_destino = obtener_almacen_por_material(materiales_list[0]["material"])

       
        insertar_solicitud(
            nombre.value,
            expediente.value,
            carrera.value,
            materiales_unificados,
            laboratorio.value,
            hora_inicio_field.value,
            hora_entrega_field.value,
            almacen_destino
        )

        
        for m in materiales_list:
            for _ in range(m["cantidad"]):
                restar_material(m["material"])

        mensaje.value = "Solicitud enviada correctamente."
        mensaje.color = ft.Colors.GREEN

        # Reset
        materiales_list.clear()
        lista_visual.controls.clear()
        material_input.value = ""
        cantidad_input.value = ""
        laboratorio.value = ""
        hora_inicio_field.value = ""
        hora_entrega_field.value = ""
        page.update()

    def regresar(e):
        from .home_page import home_page
        page.clean()
        home_page(page, usuario)

   
    page.add(
        hora_inicio_picker,
        hora_entrega_picker,

        ft.Column([
            ft.Text(f"Solicitud de Material — {career}", size=25, weight="bold"),


            # SECCIÓN 1
            ft.Container(
                ft.Column([ft.Text("Datos del solicitante", size=20, weight="bold"), nombre, expediente, carrera]),
                width=350, padding=15,
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLUE),
                border_radius=10
            ),

         
            ft.Container(
                ft.Column([
                    ft.Text("Detalles de la solicitud", size=20, weight="bold"),
                    laboratorio,
                    ft.Row([ft.Container(content=hora_inicio_field, width=260), ft.IconButton(icon=ft.Icons.ACCESS_TIME, on_click=abrir_hora_inicio)], alignment="center"),
                    ft.Row([ft.Container(content=hora_entrega_field, width=260), ft.IconButton(icon=ft.Icons.ACCESS_TIME, on_click=abrir_hora_entrega)], alignment="center"),
                ]),
                width=350, padding=15,
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREEN),
                border_radius=10
            ),

            
            ft.Container(
                ft.Column([
                    ft.Text("Material requerido", size=20, weight="bold"),

                    ft.Row([
                        ft.Container(content=material_input, width=200),
                        ft.Container(content=cantidad_input, width=80),
                        ft.IconButton(icon=ft.Icons.ADD_CIRCLE, icon_size=30, on_click=agregar_material)
                    ], alignment="center"),

                    sugerencias,
                    ft.Text("Materiales añadidos:", size=18, weight="bold"),

                    ft.Container(content=lista_visual, width=320, padding=5, border_radius=10,
                                 bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.BLACK))
                ]),
                width=350, padding=15,
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.ORANGE),
                border_radius=10
            ),

            
            ft.Row([
                ft.ElevatedButton("Enviar", on_click=enviar),
                ft.OutlinedButton("Regresar", on_click=regresar)
            ], alignment="center"),

            mensaje
        ], horizontal_alignment="center")
    )
