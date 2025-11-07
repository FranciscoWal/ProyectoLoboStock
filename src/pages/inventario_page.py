import flet as ft
import sqlite3
from database.db_manager import DB_PATH


def inventario_page(page: ft.Page):
    page.title = "Inventario — Panel de Administración"
    
   
  
   
    def obtener_inventario():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre_material, cantidad_total, cantidad_en_uso, 
                   cantidad_total - cantidad_en_uso AS cantidad_disponible 
            FROM inventario
        """)
        data = cursor.fetchall()
        conn.close()
        return data

    def guardar_material(nombre, total, en_uso, id_=None):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        disponible = total - en_uso
        
        if id_:
            cursor.execute("""
                UPDATE inventario 
                SET nombre_material=?, cantidad_total=?, cantidad_en_uso=?, cantidad_disponible=?
                WHERE id=?
            """, (nombre, total, en_uso, disponible, id_))
        else:
            cursor.execute("""
                INSERT INTO inventario (nombre_material, cantidad_total, cantidad_en_uso, cantidad_disponible)
                VALUES (?, ?, ?, ?)
            """, (nombre, total, en_uso, disponible))
        
        conn.commit()
        conn.close()
        actualizar_vista()

    def eliminar_material(id_):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventario WHERE id = ?", (id_,))
        conn.commit()
        conn.close()
        actualizar_vista()

    def actualizar_vista():
        page.clean()
        inventario_page(page)

   
    # Formularios
   
    def mostrar_formulario(material=None):
        es_edicion = material is not None
        

        nombre_field = ft.TextField(
            label="Nombre del material*",
            width=400,
            value=material[1] if es_edicion else "",
            autofocus=True
        )
        total_field = ft.TextField(
            label="Cantidad total*", 
            width=200,
            value=str(material[2]) if es_edicion else "0",
            input_filter=ft.NumbersOnlyInputFilter()
        )
        uso_field = ft.TextField(
            label="Cantidad en uso", 
            width=200,
            value=str(material[3]) if es_edicion else "0", 
            input_filter=ft.NumbersOnlyInputFilter()
        )

        def guardar(e):
            try:
                # Validaciones
                if not nombre_field.value.strip():
                    mostrar_mensaje("El nombre es obligatorio")
                    return
                    
                total = int(total_field.value)
                en_uso = int(uso_field.value) if uso_field.value.strip() else 0

                if en_uso > total:
                    mostrar_mensaje("En uso no puede ser mayor que total")
                    return

               
                if es_edicion:
                    guardar_material(nombre_field.value.strip(), total, en_uso, material[0])
                    mostrar_mensaje("Material actualizado", False)
                else:
                    guardar_material(nombre_field.value.strip(), total, en_uso)
                    mostrar_mensaje("Material agregado", False)
                    
            except ValueError:
                mostrar_mensaje("Las cantidades deben ser números")

        def cancelar(e):
            actualizar_vista()

        # Crear formulario
        formulario = ft.Container(
            content=ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Editar Material" if es_edicion else "Agregar Material", 
                                   size=20, weight=ft.FontWeight.BOLD),
                            ft.IconButton(ft.Icons.CLOSE, on_click=cancelar)
                        ]),
                        ft.Divider(),
                        nombre_field,
                        ft.Row([total_field, uso_field]),
                        ft.Container(height=20),
                        ft.Row([
                            ft.OutlinedButton("Cancelar", on_click=cancelar),
                            ft.ElevatedButton("Guardar", on_click=guardar)
                        ], alignment=ft.MainAxisAlignment.END)
                    ], spacing=15),
                    padding=30,
                    width=500
                ),
                elevation=20
            ),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.BLACK54,
            padding=50
        )

        # Mostrar overlay
        page.clean()
        page.add(
            ft.Stack([
                ft.Column([
                    ft.Container(
                        content=ft.Text("Inventario", size=28, weight=ft.FontWeight.BOLD),
                        padding=20,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.Text("Formulario abierto...", color=ft.Colors.GREY),
                        padding=20,
                        alignment=ft.alignment.center
                    ),
                ]),
                formulario
            ], expand=True)
        )
        page.update()

    def mostrar_mensaje(mensaje, es_error=True):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje, color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED if es_error else ft.Colors.GREEN,
            duration=2000
        )
        page.snack_bar.open = True
        page.update()

    def regresar(e):
        from src.pages.admin_page import admin_page
        page.clean()
        admin_page(page)

   
   

    inventario = obtener_inventario()
    
    
    filas_tabla = []
    
    if not inventario:
        # Mensaje cuando no hay datos
        filas_tabla.append(
            ft.DataRow(
                color=ft.Colors.WHITE,
                cells=[
                    ft.DataCell(ft.Text("No hay materiales registrados", color=ft.Colors.BLACK)),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text("")),
                    ft.DataCell(ft.Text(""))
                ]
            )
        )
    else:
        for material in inventario:
            id_, nombre, total, en_uso, disponible = material
            
            # Determinar color para disponible
            color_disponible = ft.Colors.BLACK
            if disponible > 0:
                color_disponible = ft.Colors.GREEN
            elif disponible < 0:
                color_disponible = ft.Colors.RED
            
            filas_tabla.append(
                ft.DataRow(
                    color=ft.Colors.WHITE,  
                    cells=[
                        ft.DataCell(ft.Text(str(id_), color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(nombre, color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(str(total), color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(str(en_uso), color=ft.Colors.BLACK)),
                        ft.DataCell(ft.Text(str(disponible), color=color_disponible)),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color=ft.Colors.BLUE,
                                    tooltip="Editar",
                                    on_click=lambda e, m=material: mostrar_formulario(m)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=ft.Colors.RED,
                                    tooltip="Eliminar",
                                    on_click=lambda e, i=id_: eliminar_material(i)
                                ),
                            ], spacing=5)
                        )
                    ]
                )
            )

    # Crear tabla
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Material", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Total", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("En Uso", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Disponible", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acciones", color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)),
        ],
        rows=filas_tabla,
        border=ft.border.all(1, ft.Colors.GREY_400),
        border_radius=10,
        horizontal_margin=10,
        column_spacing=20,
        heading_row_color=ft.Colors.BLUE,  
        heading_row_height=50,
        data_row_color=ft.Colors.WHITE,    
        data_row_max_height=60,
    )

    
    # Layout principal
    
    contenido = ft.Column([
        ft.Container(
            content=ft.Text("Inventario de Materiales", size=25, weight=ft.FontWeight.BOLD),
            padding=20,
            alignment=ft.alignment.center
        ),
        
        ft.Container(
            content=ft.ElevatedButton(
                "Agregar Material", 
                icon=ft.Icons.ADD,
                on_click=lambda e: mostrar_formulario(),
                style=ft.ButtonStyle(padding=20)
            ),
            padding=10
        ),
        
        ft.Container(
            content=ft.Column([
                tabla
            ], scroll=ft.ScrollMode.AUTO),
            padding=20
        ),
        
        ft.Container(
            content=ft.OutlinedButton(
                "Regresar al Panel", 
                icon=ft.Icons.ARROW_BACK,
                on_click=regresar
            ),
            padding=20
        )
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    page.add(contenido)