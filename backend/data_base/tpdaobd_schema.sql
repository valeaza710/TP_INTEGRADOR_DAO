-- ============================================
-- SCHEMA SQLite adaptado de tpdaobd (MariaDB)
-- ============================================

PRAGMA foreign_keys = ON;

-- Tabla: tipo_usuario
CREATE TABLE IF NOT EXISTS tipo_usuario (
    id INTEGER PRIMARY KEY,
    tipo TEXT
);

-- Tabla: usuario
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario TEXT NOT NULL UNIQUE,
    contrasena TEXT NOT NULL,
    rol INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (rol) REFERENCES tipo_usuario(id)
);

-- Tabla: paciente
CREATE TABLE IF NOT EXISTS paciente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL DEFAULT '',
    apellido TEXT NOT NULL DEFAULT '',
    dni TEXT UNIQUE,
    edad INTEGER,
    fecha_nacimiento TEXT,
    mail TEXT,
    telefono TEXT,
    direccion TEXT,
    id_usuario INTEGER,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Tabla: medico
CREATE TABLE IF NOT EXISTS medico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    matricula TEXT NOT NULL UNIQUE,
    id_usuario INTEGER,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Tabla: especialidad
CREATE TABLE IF NOT EXISTS especialidad (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
);

-- Tabla: medico_x_especialidad
CREATE TABLE IF NOT EXISTS medico_x_especialidad (
    id_medico INTEGER NOT NULL,
    id_especialidad INTEGER NOT NULL,
    PRIMARY KEY (id_medico, id_especialidad),
    FOREIGN KEY (id_medico) REFERENCES medico(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_especialidad) REFERENCES especialidad(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabla: horario_medico
CREATE TABLE IF NOT EXISTS horario_medico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_medico INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    anio INTEGER NOT NULL,
    dia_semana TEXT CHECK (dia_semana IN ('Lunes','Martes','Miercoles','Jueves','Viernes')),
    hora_inicio TEXT NOT NULL,
    hora_fin TEXT NOT NULL,
    duracion_turno_min INTEGER NOT NULL,
    FOREIGN KEY (id_medico) REFERENCES medico(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabla: estado_turno
CREATE TABLE IF NOT EXISTS estado_turno (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE
);

-- Tabla: agenda_turno
CREATE TABLE IF NOT EXISTS agenda_turno (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    hora TEXT NOT NULL,
    id_paciente INTEGER NOT NULL,
    id_estado_turno INTEGER NOT NULL,
    id_horario_medico INTEGER,
    FOREIGN KEY (id_paciente) REFERENCES paciente(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_estado_turno) REFERENCES estado_turno(id) ON UPDATE CASCADE,
    FOREIGN KEY (id_horario_medico) REFERENCES horario_medico(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabla: historial_clinico
CREATE TABLE IF NOT EXISTS historial_clinico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_paciente INTEGER,
    peso REAL NOT NULL DEFAULT 0,
    altura REAL NOT NULL DEFAULT 0,
    grupo_sanguineo TEXT NOT NULL DEFAULT '',
    FOREIGN KEY (id_paciente) REFERENCES paciente(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabla: enfermedades
CREATE TABLE IF NOT EXISTS enfermedades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE
);

-- Tabla: historial_enfermedad
CREATE TABLE IF NOT EXISTS historial_enfermedad (
    id_historial INTEGER NOT NULL,
    id_enfermedad INTEGER NOT NULL,
    fecha_diagnostico TEXT,
    observaciones TEXT,
    PRIMARY KEY (id_historial, id_enfermedad),
    FOREIGN KEY (id_historial) REFERENCES historial_clinico(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_enfermedad) REFERENCES enfermedades(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabla: visita
CREATE TABLE IF NOT EXISTS visita (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_historial_clinico INTEGER NOT NULL DEFAULT 0,
    id_turno INTEGER NOT NULL DEFAULT 0,
    comentario TEXT,
    FOREIGN KEY (id_historial_clinico) REFERENCES historial_clinico(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_turno) REFERENCES agenda_turno(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabla: receta
CREATE TABLE IF NOT EXISTS receta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_visita INTEGER NOT NULL,
    id_paciente INTEGER NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_emision TEXT NOT NULL,
    FOREIGN KEY (id_visita) REFERENCES visita(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES paciente(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================
-- DATOS INICIALES
-- ============================================

INSERT OR IGNORE INTO especialidad (id, nombre) VALUES (1, 'Cardiologia');

INSERT OR IGNORE INTO estado_turno (id, nombre) VALUES
    (1, 'Pendiente'),
    (2, 'Confirmado'),
    (3, 'Cancelado'),
    (4, 'Completado');

INSERT OR IGNORE INTO paciente (id, nombre, apellido, dni)
VALUES (6, 'Juan', 'Perez', '12145764');
