import random

def generate_greeting(name: str) -> str:
    """Genera un saludo aleatorio para el usuario."""
    greetings = [
        f"¡Hola, {name}! Bienvenido a tu PWA universitaria.",
        f"¡Saludos, {name}! Este es un proyecto en Flet.",
        f"¡Hey {name}, interactúa con esta app PWA!"
    ]
    return random.choice(greetings)