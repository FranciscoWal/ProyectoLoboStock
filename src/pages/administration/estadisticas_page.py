import flet as ft
import sqlite3
from database.db_manager import DB_PATH


def estadisticas_page(page: ft.Page):
    page.title = "Estadísticas — Panel de Administración"

    # --- Obtener datos de la base de datos ---
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Top 5 materiales más solicitados
    cursor.execute("""
        SELECT material, COUNT(material) AS cantidad
        FROM solicitudes
        GROUP BY material
        ORDER BY cantidad DESC
        LIMIT 5
    """)
    top_materiales = cursor.fetchall()

    conn.close()

    # --- Preparar los datos para la gráfica ---
    data = [
        ft.ChartDataPoint(material, cantidad)
        for material, cantidad in top_materiales
    ]

    # --- Crear la gráfica de barras ---
    grafica = ft.BarChart(
        bar_groups=[
            ft.BarChartGroup(
                x=material,
                bar_rods=[ft.BarChartRod(from_y=0, to_y=cantidad)]
            ) for material, cantidad in top_materiales
        ],
        border=ft.Border(
            top=ft.BorderSide(1, ft.colors.GREY_400),
            left=ft.BorderSide(1, ft.colors.GREY_400),
        ),
        width=700,
        height=400,
        tooltip_bgcolor=ft.colors.BLUE_200,
    )

    # --- Título y contenido ---
    layout = ft.Column(
        [
            ft.Text("📊 Estadísticas de materiales más solicitados", size=20, weight=ft.FontWeight.BOLD),
            grafica,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )

    page.clean()
    page.add(layout)
