import datetime
import flet as ft
from src.pages.students.home_page import home_page
from src.pages.administration.admin_page import admin_page
from database.db_manager import validar_usuario


def login_page(page: ft.Page):
    # ------------------ Configuración global (sin tocar la lógica) ------------------
    page.title = "Login Sistema de Solicitud de Materiales"
    page.padding = 0
    page.spacing = 0
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Fuente y tema
    page.fonts = page.fonts or {}
    page.fonts.update({"ConcertOne": "fonts/ConcertOne-Regular.ttf"})
    page.theme = page.theme or ft.Theme()
    page.theme.font_family = "ConcertOne"

    # ----------------------------- Paleta -----------------------------------
    UT_GREEN = "#0AA67A"
    BG_DARK_1 = "#0E1224"
    BG_DARK_2 = "#1A2038"
    CARD_DARK = "#1F2541"
    FIELD_BG = "#2A3052"
    FIELD_TXT = "#E7E9F2"
    FIELD_HINT = "#A8AEC7"
    MUTED = "#8E94B8"

    txt = ft.TextStyle(color=FIELD_TXT, size=14, font_family="ConcertOne")
    hint = ft.TextStyle(color=FIELD_HINT, size=13, font_family="ConcertOne")

    # --------------------------- Controles UI --------------------------------
    username = ft.TextField(
        hint_text="Usuario",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        width=360,
        bgcolor=FIELD_BG,
        color=FIELD_TXT,
        text_style=txt,
        hint_style=hint,
        border_radius=14,
        border_color="transparent",
        focused_border_color=UT_GREEN,
    )

    password = ft.TextField(
        hint_text="Contraseña",
        password=True,
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK_OUTLINED,
        width=360,
        bgcolor=FIELD_BG,
        color=FIELD_TXT,
        text_style=txt,
        hint_style=hint,
        border_radius=14,
        border_color="transparent",
        focused_border_color=UT_GREEN,
    )

    rol_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option("estudiante"), ft.dropdown.Option("admin")],
        value="estudiante",
        width=360,
        bgcolor=FIELD_BG,
        color=FIELD_TXT,
        hint_style=hint,
        border_radius=14,
        border_color="transparent",
        focused_border_color=UT_GREEN,
    )

    mensaje = ft.Text("", color=ft.Colors.RED, text_align=ft.TextAlign.CENTER)

    # ---------------------- Botón con loader (solo UI) -----------------------
    loading = {"value": False}

    def set_loading(v: bool):
        loading["value"] = v
        iniciar_btn.disabled = v
        iniciar_btn.content = (
            ft.Row(
                [ft.ProgressRing(width=16, height=16, stroke_width=2),
                 ft.Text(" Validando...", color=ft.Colors.WHITE)],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
            )
            if v else ft.Row(
                [ft.Icon(ft.Icons.LOGIN), ft.Text(" Iniciar sesión")],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        page.update()

    # ----------------------------- Lógica ORIGINAL ---------------------------
    def iniciar_sesion(e):
        username.error_text = None if username.value.strip() else "Ingresa tu usuario"
        password.error_text = None if password.value.strip() else "Ingresa tu contraseña"
        page.update()

        if username.error_text or password.error_text:
            return

        set_loading(True)
        try:
            usuario = validar_usuario(username.value, password.value, rol_dropdown.value)

            if usuario:
                if usuario["rol"] == "usuario":
                    page.clean()
                    # puedes pasarle datos al home_page si quieres:
                    home_page(page)
                elif usuario["rol"] == "admin":
                    page.clean()
                   
                    admin_page(page, usuario["carrera"])
                else:
                    mensaje.value = "Rol desconocido. Contacta al administrador."
                    page.update()
            else:
                mensaje.value = "Usuario o contraseña incorrectos"
                page.update()

        finally:
            set_loading(False)


    iniciar_btn = ft.ElevatedButton(
        content=ft.Row([ft.Icon(ft.Icons.LOGIN), ft.Text(" Iniciar sesión")],
                       spacing=8, alignment=ft.MainAxisAlignment.CENTER),
        on_click=iniciar_sesion,
        width=360,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.with_opacity(1.0, UT_GREEN),
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=14),
            elevation=6
        ),
    )

    # ----------------------------- Header ------------------------------------
    h = datetime.datetime.now().hour
    saludo = "Buenos días" if 5 <= h < 12 else ("Buenas tardes" if h < 19 else "Buenas noches")

    logo = ft.Image(src="images/logo_ut.png", width=160, height=60, fit=ft.ImageFit.CONTAIN)

    titulo = ft.Text(
        "LOBO STOCK",
        size=28,
        weight=ft.FontWeight.BOLD,
        color=UT_GREEN,
        text_align=ft.TextAlign.CENTER,
    )

    header_block = ft.Column(
        [
            ft.Row([logo], alignment=ft.MainAxisAlignment.CENTER),
            titulo,
            ft.Text(saludo, size=22, weight=ft.FontWeight.W_600, color=FIELD_TXT),
            ft.Text("Ingresa tus credenciales para continuar",
                    size=11, color=MUTED, text_align=ft.TextAlign.CENTER),
            ft.Text("Login", size=16, weight=ft.FontWeight.BOLD, color=FIELD_TXT),
        ],
        spacing=4,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    recover_btn = ft.TextButton(
        "¿Olvidaste tu contraseña?",
        style=ft.ButtonStyle(color=ft.Colors.GREY_400),
    )

    # --------------------- Layout interno balanceado -------------------------
    # Usamos "espaciadores" expandibles para distribuir verticalmente.
    top_spacer = ft.Container(expand=1)      # ocupa espacio libre arriba del form
    middle_spacer = ft.Container(expand=1)   # entre el form y acciones
    bottom_spacer = ft.Container(expand=1)   # bajo las acciones

    form_block = ft.Column(
        [username, password, rol_dropdown, recover_btn],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    actions_block = ft.Column(
        [iniciar_btn, mensaje],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # ----------------------------- Card --------------------------------------
    # Mantenemos ancho/padding y dejamos que el contenido se distribuya con spacers.
    card = ft.Container(
        width=520,
        padding=ft.padding.symmetric(horizontal=28, vertical=24),
        bgcolor=CARD_DARK,
        border_radius=22,
        shadow=ft.BoxShadow(blur_radius=28, color="#00000055"),
        content=ft.Column(
            controls=[
                header_block,
                top_spacer,        # <- reparte aire por encima del formulario
                form_block,
                middle_spacer,     # <- asegura que no se concentre todo abajo
                actions_block,
                bottom_spacer,     # <- deja un margen inferior proporcional
            ],
            expand=True,                           # <- para usar todo el alto del card
            alignment=ft.MainAxisAlignment.START,  # distribución con los spacers
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    # ---------------------- Fondo full-screen + círculos ----------------------
    circles = [
        ft.Container(left=-70,  top=-60, width=280, height=280, border_radius=9999,
                     bgcolor=ft.Colors.with_opacity(0.12, UT_GREEN)),
        ft.Container(right=-60, top=40,  width=220, height=220, border_radius=9999,
                     bgcolor=ft.Colors.with_opacity(0.18, UT_GREEN)),
        ft.Container(left=120, bottom=-80, width=260, height=260, border_radius=9999,
                     bgcolor=ft.Colors.with_opacity(0.18, UT_GREEN)),
        ft.Container(right=140, bottom=-60, width=200, height=200, border_radius=9999,
                     bgcolor=ft.Colors.with_opacity(0.12, UT_GREEN)),
    ]

    background = ft.Container(
        width=page.width or 1200,
        height=page.height or 800,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1),
            colors=[BG_DARK_1, BG_DARK_2],
        ),
        content=ft.Stack(
            controls=[
                *circles,
                ft.Container(
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(horizontal=24, vertical=24),
                    content=card,
                ),
            ],
            expand=True,
        ),
    )

    root = ft.Container(expand=True, alignment=ft.alignment.center, content=background)
    page.add(root)

    # Mantener el fondo al tamaño del viewport en cada resize
    def _resize(_=None):
        background.width = page.width
        background.height = page.height
        page.update()

    page.on_resize = _resize
    _resize()
