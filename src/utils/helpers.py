import flet as ft

def crear_tabla_usuarios(datos_usuarios: list) -> ft.DataTable:
    """
    Crea y devuelve un ft.DataTable con la estructura de la tabla 'usuarios'.
    :param datos_usuarios: Lista de diccionarios con los datos de los usuarios.
    """
    
    # --- Definir las Columnas ---
    columnas = [
        ft.DataColumn(ft.Text("ID")),
        ft.DataColumn(ft.Text("Usuario")),
        ft.DataColumn(ft.Text("Rol")),
        ft.DataColumn(ft.Text("Expediente")),
        ft.DataColumn(ft.Text("Adeudo")),
    ]

    # --- Mapear los Datos a Filas (DataRow) ---
    filas = []
    
    for usuario in datos_usuarios:
        # Lógica para convertir el indicador binario (0/1) a texto legible
        estado_adeudo = " Sin Adeudo" if usuario.get("adeudo") == 0 else " Con Adeudo"
        color_adeudo = ft.Colors.GREEN_700 if usuario.get("adeudo") == 0 else ft.Colors.RED_700

        fila = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(usuario.get("id", "")))),
                ft.DataCell(ft.Text(usuario.get("username", ""))),
                ft.DataCell(ft.Text(usuario.get("rol", ""))),
                ft.DataCell(ft.Text(usuario.get("expediente", ""))),
                ft.DataCell(ft.Container(
                    content=ft.Text(estado_adeudo, 
                                    weight=ft.FontWeight.BOLD),bgcolor=color_adeudo,padding=5,border_radius=5)
                            )
            ],
        )
        filas.append(fila)

    # --- Crear y devolver el control DataTable ---
    return ft.DataTable(
        columns=columnas,
        rows=filas,
        sort_column_index=0, 
        heading_row_height=45,
        border=ft.border.all(1, ft.Colors.BLACK12),
        horizontal_lines=ft.BorderSide(1, ft.Colors.BLACK12),
        column_spacing=25,
        # Ancho mínimo para que quepan las columnas
        min_width=650 
    )