-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         11.5.2-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para tpdaobd
CREATE DATABASE IF NOT EXISTS `tpdaobd` /*!40100 DEFAULT CHARACTER SET armscii8 COLLATE armscii8_bin */;
USE `tpdaobd`;

-- Volcando estructura para tabla tpdaobd.agenda_turno
CREATE TABLE IF NOT EXISTS `agenda_turno` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `id_paciente` int(11) NOT NULL,
  `id_estado_turno` int(11) NOT NULL,
  `id_horario_medico` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_paciente` (`id_paciente`),
  KEY `id_estado_turno` (`id_estado_turno`),
  KEY `id_horario_medico` (`id_horario_medico`),
  CONSTRAINT `FK_agenda_turno_horario_medico` FOREIGN KEY (`id_horario_medico`) REFERENCES `horario_medico` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `agenda_turno_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `paciente` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `agenda_turno_ibfk_3` FOREIGN KEY (`id_estado_turno`) REFERENCES `estado_turno` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla tpdaobd.agenda_turno: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tpdaobd.enfermedades
CREATE TABLE IF NOT EXISTS `enfermedades` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla tpdaobd.enfermedades: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tpdaobd.especialidad
CREATE TABLE IF NOT EXISTS `especialidad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla tpdaobd.especialidad: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tpdaobd.estado_turno
CREATE TABLE IF NOT EXISTS `estado_turno` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla tpdaobd.estado_turno: ~4 rows (aproximadamente)
INSERT INTO `estado_turno` (`id`, `nombre`) VALUES
	(3, 'Cancelado'),
	(4, 'Completado'),
	(2, 'Confirmado'),
	(1, 'Pendiente');

-- Volcando estructura para tabla tpdaobd.historial_clinico
CREATE TABLE IF NOT EXISTS `historial_clinico` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_paciente` int(11) DEFAULT NULL,
  `peso` float NOT NULL DEFAULT 0,
  `altura` float NOT NULL DEFAULT 0,
  `grupo_sanguineo` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `id_paciente` (`id_paciente`),
  CONSTRAINT `historial_clinico_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `paciente` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla tpdaobd.historial_clinico: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tpdaobd.historial_enfermedad
CREATE TABLE IF NOT EXISTS `historial_enfermedad` (
  `id_historial` int(11) NOT NULL,
  `id_enfermedad` int(11) NOT NULL,
  PRIMARY KEY (`id_historial`,`id_enfermedad`),
  KEY `id_enfermedad` (`id_enfermedad`),
  CONSTRAINT `historial_enfermedad_ibfk_1` FOREIGN KEY (`id_historial`) REFERENCES `historial_clinico` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `historial_enfermedad_ibfk_2` FOREIGN KEY (`id_enfermedad`) REFERENCES `enfermedades` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla tpdaobd.historial_enfermedad: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tpdaobd.horario_medico
CREATE TABLE IF NOT EXISTS `horario_medico` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_medico` int(11) NOT NULL,
  `mes` int(11) NOT NULL,
  `anio` int(11) NOT NULL,
  `dia_semana` enum('Lunes','Martes','Miercoles','Jueves','Viernes') DEFAULT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `duracion_turno_min` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_medico` (`id_medico`),
  CONSTRAINT `horario_medico_ibfk_1` FOREIGN KEY (`id_medico`) REFERENCES `medico` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla tpdaobd.horario_medico: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tpdaobd.medico
CREATE TABLE IF NOT EXISTS `medico` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `matricula` varchar(50) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `matricula` (`matricula`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `medico_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla tpdaobd.medico: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tpdaobd.medico_x_especialidad
CREATE TABLE IF NOT EXISTS `medico_x_especialidad` (
  `id_medico` int(11) NOT NULL,
  `id_especialidad` int(11) NOT NULL,
  PRIMARY KEY (`id_medico`,`id_especialidad`),
  KEY `FK__especialidad` (`id_especialidad`),
  KEY `id_medico` (`id_medico`),
  CONSTRAINT `FK__especialidad` FOREIGN KEY (`id_especialidad`) REFERENCES `especialidad` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK__medico` FOREIGN KEY (`id_medico`) REFERENCES `medico` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla tpdaobd.medico_x_especialidad: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tpdaobd.paciente
CREATE TABLE IF NOT EXISTS `paciente` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `dni` varchar(20) DEFAULT NULL,
  `edad` int(11) DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `mail` varchar(120) DEFAULT NULL,
  `telefono` varchar(30) DEFAULT NULL,
  `direccion` varchar(150) DEFAULT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dni` (`dni`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `paciente_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla tpdaobd.paciente: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tpdaobd.receta
CREATE TABLE IF NOT EXISTS `receta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_visita` int(11) NOT NULL,
  `id_paciente` int(11) NOT NULL,
  `descripcion` text NOT NULL,
  `fecha_emision` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_paciente` (`id_paciente`),
  KEY `id_visita` (`id_visita`),
  CONSTRAINT `FK_receta_visita` FOREIGN KEY (`id_visita`) REFERENCES `visita` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `receta_ibfk_1` FOREIGN KEY (`id_paciente`) REFERENCES `paciente` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla tpdaobd.receta: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tpdaobd.tipo_usuario
CREATE TABLE IF NOT EXISTS `tipo_usuario` (
  `id` int(11) NOT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla tpdaobd.tipo_usuario: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tpdaobd.usuario
CREATE TABLE IF NOT EXISTS `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_usuario` varchar(100) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `rol` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre_usuario` (`nombre_usuario`),
  KEY `rol` (`rol`),
  CONSTRAINT `FK_usuario_tipo_usuario` FOREIGN KEY (`rol`) REFERENCES `tipo_usuario` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla tpdaobd.usuario: ~0 rows (aproximadamente)

-- Volcando estructura para tabla tpdaobd.visita
CREATE TABLE IF NOT EXISTS `visita` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_historial_clinico` int(11) NOT NULL DEFAULT 0,
  `id_turno` int(11) NOT NULL DEFAULT 0,
  `comentario` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `id_historial_clinico` (`id_historial_clinico`),
  KEY `id_turno` (`id_turno`),
  CONSTRAINT `FK_visita_agenda_turno` FOREIGN KEY (`id_turno`) REFERENCES `agenda_turno` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_visita_historial_clinico` FOREIGN KEY (`id_historial_clinico`) REFERENCES `historial_clinico` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla tpdaobd.visita: ~0 rows (aproximadamente)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
