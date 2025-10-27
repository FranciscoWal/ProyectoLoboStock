import flet as ft

def create_ut_theme():
    return ft.Theme(
        color_scheme_seed=ft.Colors.TEAL,  # Verde/teal UT
        use_material3=True,
        visual_density=ft.VisualDensity.COMPACT  # Responsive
    )

def ut_button(text: str, on_click, icon=ft.Icons.LOGIN):
    return ft.ElevatedButton(
        text=text,
        icon=icon,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.TEAL_600,  # Verde oscuro
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10),
            elevation=5  # Sombra suave
        ),
        on_click=on_click,
        width=300,
        height=50
    )