-- --------------------------------------------------------
-- Script SQL para Sprint 1: Fundación y Autenticación
-- Proyecto: EduStock (App Almacenes UT)
-- Base de Datos: MariaDB
-- --------------------------------------------------------

-- 1. CREACIÓN DE LA BASE DE DATOS
CREATE DATABASE IF NOT EXISTS `edustock_db`
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

USE `edustock_db`;

-- --------------------------------------------------------
-- TABLAS SPRINT 1 (Autenticación - HU-001, HU-002)
-- --------------------------------------------------------

-- Tabla para Roles (Estudiante, Administrador)
CREATE TABLE IF NOT EXISTS `Roles` (
    `id_rol` INT AUTO_INCREMENT PRIMARY KEY,
    `nombre_rol` VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- Tabla para Carreras (IDGS, etc.)
CREATE TABLE IF NOT EXISTS `Carreras` (
    `id_carrera` INT AUTO_INCREMENT PRIMARY KEY,
    `nombre_carrera` VARCHAR(150) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- Tabla de Usuarios (Para Login)
CREATE TABLE IF NOT EXISTS `Usuarios` (
    `id_usuario` INT AUTO_INCREMENT PRIMARY KEY,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    
    -- ADVERTENCIA DE SEGURIDAD:
    -- Tu archivo helpers.py usa texto plano. En producción, NUNCA guardes
    -- contraseñas en texto plano. Usa hashes (ej. SHA256, Argon2).
    -- La columna debería ser `password_hash` VARCHAR(255).
    -- Se usa VARCHAR(100) para compatibilidad con tu mock actual.
    `password` VARCHAR(100) NOT NULL,
    
    `nombre_completo` VARCHAR(150),
    `id_rol_fk` INT NOT NULL,
    `id_carrera_fk` INT,
    `fecha_registro` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (`id_rol_fk`) REFERENCES `Roles`(`id_rol`),
    FOREIGN KEY (`id_carrera_fk`) REFERENCES `Carreras`(`id_carrera`)
) ENGINE=InnoDB;

-- --------------------------------------------------------
-- DATOS INICIALES (Mocks de helpers.py)
-- --------------------------------------------------------

-- Insertar Roles (basado en login_page.py)
INSERT INTO `Roles` (`nombre_rol`) VALUES
('estudiante'),
('administrador')
ON DUPLICATE KEY UPDATE nombre_rol=nombre_rol; -- No hacer nada si ya existen

-- Insertar Carrera (basado en helpers.py)
INSERT INTO `Carreras` (`nombre_carrera`) VALUES
('Ingeniería en Desarrollo y Gestión de Software')
ON DUPLICATE KEY UPDATE nombre_carrera=nombre_carrera;

-- Insertar Usuarios (basado en helpers.py MOCK_USERS)
-- (Obteniendo los IDs de Rol y Carrera)
INSERT INTO `Usuarios` (`email`, `password`, `nombre_completo`, `id_rol_fk`, `id_carrera_fk`)
VALUES
(
    'estudiante@ut.edu', 
    'pass123',  -- Texto plano (ver advertencia)
    'Estudiante de Prueba',
    (SELECT id_rol FROM Roles WHERE nombre_rol = 'estudiante'),
    (SELECT id_carrera FROM Carreras WHERE nombre_carrera = 'Ingeniería en Desarrollo y Gestión de Software')
),
(
    'admin@ut.edu', 
    'adminpass', -- Texto plano (ver advertencia)
    'Administrador de Prueba',
    (SELECT id_rol FROM Roles WHERE nombre_rol = 'administrador'),
    NULL -- Admin puede no tener carrera
)
ON DUPLICATE KEY UPDATE email=email; -- No hacer nada si ya existen

-- --------------------------------------------------------
-- TABLAS SPRINT 1 (Fundación - Estructura futura)
-- --------------------------------------------------------

-- Tabla de Almacenes (Vinculados a Carreras según PDF)
CREATE TABLE IF NOT EXISTS `Almacenes` (
    `id_almacen` INT AUTO_INCREMENT PRIMARY KEY,
    `nombre_almacen` VARCHAR(100) NOT NULL,
    `ubicacion` VARCHAR(255),
    `id_carrera_fk` INT,
    FOREIGN KEY (`id_carrera_fk`) REFERENCES `Carreras`(`id_carrera`)
) ENGINE=InnoDB;

-- Tabla de Categorías de Materiales
CREATE TABLE IF NOT EXISTS `Categorias` (
    `id_categoria` INT AUTO_INCREMENT PRIMARY KEY,
    `nombre_categoria` VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- Tabla de Materiales (Inventario)
CREATE TABLE IF NOT EXISTS `Materiales` (
    `id_material` INT AUTO_INCREMENT PRIMARY KEY,
    `nombre_material` VARCHAR(150) NOT NULL,
    `descripcion` TEXT,
    `sku` VARCHAR(50) UNIQUE, -- Identificador único
    `stock_total` INT NOT NULL DEFAULT 0,
    `stock_disponible` INT NOT NULL DEFAULT 0,
    `id_almacen_fk` INT NOT NULL,
    `id_categoria_fk` INT,
    FOREIGN KEY (`id_almacen_fk`) REFERENCES `Almacenes`(`id_almacen`),
    FOREIGN KEY (`id_categoria_fk`) REFERENCES `Categorias`(`id_categoria`)
) ENGINE=InnoDB;

-- Tabla de Préstamos (Gestión de pedidos)
CREATE TABLE IF NOT EXISTS `Prestamos` (
    `id_prestamo` INT AUTO_INCREMENT PRIMARY KEY,
    `id_usuario_fk` INT NOT NULL,
    `id_material_fk` INT NOT NULL,
    `cantidad_solicitada` INT NOT NULL,
    `fecha_solicitud` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `fecha_entrega_prevista` DATE, -- Cuándo debe devolverlo
    `fecha_devolucion_real` DATETIME NULL,
    `estado` ENUM(
        'pendiente', 
        'aprobado', 
        'rechazado', 
        'entregado', -- Entregado al estudiante
        'devuelto', -- Devuelto al almacén
        'con_adeudo' -- No devuelto a tiempo
    ) NOT NULL DEFAULT 'pendiente',
    `observaciones` TEXT,
    
    FOREIGN KEY (`id_usuario_fk`) REFERENCES `Usuarios`(`id_usuario`),
    FOREIGN KEY (`id_material_fk`) REFERENCES `Materiales`(`id_material`)
) ENGINE=InnoDB;

-- Tabla de Adeudos (basado en PDF)
CREATE TABLE IF NOT EXISTS `Adeudos` (
    `id_adeudo` INT AUTO_INCREMENT PRIMARY KEY,
    `id_prestamo_fk` INT NOT NULL,
    `id_usuario_fk` INT NOT NULL,
    `monto` DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    `motivo` VARCHAR(255),
    `pagado` BOOLEAN DEFAULT FALSE,
    `fecha_generacion` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (`id_prestamo_fk`) REFERENCES `Prestamos`(`id_prestamo`),
    FOREIGN KEY (`id_usuario_fk`) REFERENCES `Usuarios`(`id_usuario`)
) ENGINE=InnoDB;