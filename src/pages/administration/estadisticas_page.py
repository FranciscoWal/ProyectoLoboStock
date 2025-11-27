# src/pages/administration/estadisticas_page.py

import re
import sqlite3
import flet as ft

from database.db_manager import DB_PATH

# Expresión para detectar cantidades (x3)
RE_CANTIDAD = re.compile(r"\(x\s*([0-9]+)\)", re.IGNORECASE)


# -------------------------
# PARSE DE MATERIALES
# -------------------------
def parse_materiales_from_rows(rows):
    totals = {}
    for text in rows:
        if not text:
            continue

        parts = re.split(r"[\n,]+", text)
        for part in parts:
            item = part.strip()
            if not item:
                continue

            m = RE_CANTIDAD.search(item)
            if m:
                cantidad = int(m.group(1))
                nombre = RE_CANTIDAD.sub("", item).strip()
            else:
                cantidad = 1
                nombre = item

            if nombre:
                totals[nombre] = totals.get(nombre, 0) + cantidad

    return totals


# -------------------------
# TARJETA KPI
# -------------------------
def tarjeta_kpi(titulo, valor, icono):
    return ft.Container(
        width=260,
        height=90,
        bgcolor="#1E1E1E",
        border_radius=10,
        padding=15,
        content=ft.Row([
            ft.Icon(icono, size=28, color="#4A90E2"),
            ft.Container(width=10),
            ft.Column([
                ft.Text(titulo, size=12, color="#CCCCCC"),
                ft.Text(valor, size=22, weight=ft.FontWeight.BOLD, color="white")
            ], spacing=2)
        ])
    )


# -------------------------
# PÁGINA PRINCIPAL
# -------------------------
def estadisticas_page(page: ft.Page, almacen_admin: str, top_n: int = 10):
    page.title = f"Estadísticas — {almacen_admin}"
    page.bgcolor = "#121212"

    # --- Obtener datos ---
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT material, fecha FROM solicitudes WHERE almacen_destino = ? ORDER BY fecha DESC",
        (almacen_admin,)
    )
    filas = cur.fetchall()
    conn.close()

    materiales_text = [f[0] for f in filas if f and f[0]]

    if not materiales_text:
        page.clean()
        page.add(ft.Text("No hay solicitudes registradas.", size=18, color="white"))
        return

    totals = parse_materiales_from_rows(materiales_text)
    sorted_items = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
    top_items = sorted_items[:top_n]

    labels = [item[0] for item in top_items]
    values = [item[1] for item in top_items]

    # -------------------------
    # Ajustes del gráfico
    # -------------------------
    full_width = int(page.width or 900)
    graph_width = min(1000, max(520, full_width - 160))
    graph_height = max(340, 55 * len(values))

    # Barras
    bar_groups = [
        ft.BarChartGroup(
            x=i,
            bar_rods=[
                ft.BarChartRod(from_y=0, to_y=values[i], width=28, color="#4A90E2")
            ]
        )
        for i in range(len(values))
    ]

    # Ejes con color negro
    bottom_axis = ft.ChartAxis(
        labels=[
            ft.ChartAxisLabel(value=i, label=ft.Text(labels[i], size=12, color="black"))
            for i in range(len(labels))
        ]
    )

    left_axis = ft.ChartAxis(
        labels=[
            ft.ChartAxisLabel(value=v, label=ft.Text(str(v), size=12, color="black"))
            for v in range(0, max(values) + 1)
        ]
    )

    # Gráfico limpio con grid lines negras
    grafica = ft.BarChart(
    bar_groups=bar_groups,
    bottom_axis=bottom_axis,
    left_axis=left_axis,
    horizontal_grid_lines=ft.ChartGridLines(color="black", width=1),
    vertical_grid_lines=ft.ChartGridLines(color="black", width=1),
    border=ft.border.all(1, "#000000"),
    width=graph_width,
    height=graph_height,
    groups_space=40,
    tooltip_bgcolor="#FFFFFF"   # ✔️ fondo blanco → texto negro visible
)


    # KPI resumen
    total_solicitudes = len(filas)
    unidades_totales = sum(totals.values())
    top_mat = top_items[0] if top_items else ("-", 0)

    kpi_row = ft.Row(
        [
            tarjeta_kpi("Solicitudes Totales", str(total_solicitudes), ft.Icons.LIST_ALT),
            tarjeta_kpi("Unidades Pedidas", str(unidades_totales), ft.Icons.INVENTORY),
            tarjeta_kpi("Más Solicitado", f"{top_mat[0]} (x{top_mat[1]})", ft.Icons.STAR)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
        wrap=True
    )

    # Título + regresar
    header = ft.Row([
        ft.Text("Estadísticas de Materiales", size=28,
                weight=ft.FontWeight.BOLD, color="white"),
        ft.Container(expand=1),
        ft.ElevatedButton(
            "Regresar",
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda e: regresar(page, almacen_admin)
        )
    ])

    # Contenedor principal
    page.clean()
    page.add(
        ft.Container(
            padding=20,
            content=ft.Column(
                [
                    header,
                    ft.Container(height=20),
                    kpi_row,
                    ft.Container(height=25),
                    ft.Container(
                        bgcolor="#CDC8C8",
                        padding=20,
                        border_radius=12,
                        border=ft.border.all(1, "#333333"),
                        width=graph_width + 40,
                        content=ft.Column([
                            ft.Text("Materiales más pedidos",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color="black"),
                            ft.Container(height=15),
                            grafica
                        ])
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
    )


def regresar(page, almacen):
    from src.pages.administration.admin_page import admin_page
    page.clean()
    admin_page(page, almacen)
