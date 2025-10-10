import flet as ft

class CustomButton(ft.ElevatedButton):
    def __init__(self, text, on_click, **kwargs):
        super().__init__(
            text=text,
            on_click=on_click,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_500,
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation={"pressed": 0, "": 2},
            ),
            **kwargs
        )