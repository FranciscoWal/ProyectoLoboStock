import random  # Para simular polling futuro

MOCK_USERS = {
    "estudiante@ut.edu": {"password": "pass123", "rol": "estudiante"},
    "admin@ut.edu": {"password": "adminpass", "rol": "administrador"}
}

def validate_credentials(email: str, password: str, rol: str = "estudiante"):
    user = MOCK_USERS.get(email)
    if user and user["password"] == password and user["rol"] == rol:
        return {"success": True, "rol": rol, "user_id": email}
    return {"success": False, "error": "Credenciales inválidas"}

def get_user_carrera(email: str):
    return "Ingeniería en Desarrollo y Gestión de Software"  # Mock