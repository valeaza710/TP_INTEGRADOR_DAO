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


-- Volcando estructura de base de datos para ppaidb
CREATE DATABASE IF NOT EXISTS `ppaidb` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `ppaidb`;

-- Volcando estructura para tabla ppaidb.bodega
CREATE TABLE IF NOT EXISTS `bodega` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` text NOT NULL,
  `ultima_fecha_actualizacion` date NOT NULL,
  `historia` text NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `periodo_actualizacion` int(11) NOT NULL,
  `novedad` varchar(255) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `coord_bodega` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Volcando datos para la tabla ppaidb.bodega: ~6 rows (aproximadamente)
INSERT INTO `bodega` (`id`, `descripcion`, `ultima_fecha_actualizacion`, `historia`, `nombre`, `periodo_actualizacion`, `novedad`, `region`, `coord_bodega`) VALUES
	(1, 'Descripcion Norton', '2023-06-05', 'Historia Norton', 'Norton', 5, NULL, NULL, NULL),
	(2, 'Descripcion Trapiche', '2023-10-31', 'Historia Trapiche', 'Trapiche', 4, NULL, NULL, NULL),
	(3, 'Descripcion Salentin', '2023-07-24', 'Historia Salentin', 'Salentin', 2, NULL, NULL, NULL),
	(4, 'Descripcion Bodega del Fin del Mundo', '2023-06-05', 'Historia Bodega del Fin del Mundo', 'Bodega del Fin del Mundo', 8, NULL, NULL, NULL),
	(5, 'Descripcion Luigi Bosca', '2023-02-16', 'Historia Luigi Bosca', 'Luigi Bosca', 2, NULL, NULL, NULL),
	(6, 'Descripcion El Enemigo', '2023-09-15', 'Historia El Enemigo', 'El Enemigo', 1, NULL, NULL, NULL);

-- Volcando estructura para tabla ppaidb.enofilo
CREATE TABLE IF NOT EXISTS `enofilo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `imagen_perfil` varchar(255) DEFAULT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `enofilo_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Volcando datos para la tabla ppaidb.enofilo: ~6 rows (aproximadamente)
INSERT INTO `enofilo` (`id`, `nombre`, `apellido`, `imagen_perfil`, `usuario_id`) VALUES
	(1, 'Benjamin', 'Castagno', NULL, 1235),
	(2, 'Mateo', 'Estrada', NULL, 1236),
	(3, 'Florencia', 'Issetta', NULL, 1237),
	(4, 'Valentina', 'Bermudez', NULL, 1238),
	(5, 'Valeria', 'Azañero', NULL, 1239),
	(6, 'Juan Cruz', 'Ceballos', NULL, 1240);

-- Volcando estructura para tabla ppaidb.maridaje
CREATE TABLE IF NOT EXISTS `maridaje` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` text NOT NULL,
  `nombre` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Volcando datos para la tabla ppaidb.maridaje: ~18 rows (aproximadamente)
INSERT INTO `maridaje` (`id`, `descripcion`, `nombre`) VALUES
	(1, 'Vino fuerte y seco para el acompañamiento de Carne Vacuna como carnes de Res carne de Toro, entre otras', 'carnes rojas'),
	(2, 'Su acidez y vivacidad complementan perfectamente la dulzura natural de las langostas, camarones, y cangrejos.', 'mariscos'),
	(3, 'Magnifico compañamiento para todo de ensaldas mixtas o', 'ensaladas'),
	(4, 'Magnifico compañamiento para todo tipo de quesos desde los más suaves hasta los más intensos, como: semi-curados, curados, suaves, azules', 'quesos'),
	(5, 'Fiel compañero de pastas caseras, buena comida Italiana', 'pasta'),
	(6, 'Vino delicado y liviano para degustar junto carnes Blancas, especialemente de Aves', 'pollo'),
	(7, 'Vino para equilibrar y realzar los sabores intenso de estos tipos de queso', 'quesos fuertes'),
	(8, 'Vino delicado y liviano para degustar junto carnes Blancas del Mar, realzando sus sabores frescos en cada sorbo', 'pescado'),
	(9, 'Vino para realza los sabores jugosos y ahumados de las carnes', 'carnes asadas'),
	(10, 'Vino justo para acompañar los potentes sabores de los platos de coccion lenta', 'guisos'),
	(11, 'Su vivacidad complementan perfectamente con el pescado crudo', 'sushi'),
	(12, 'Fiel compañero de la perfecta combinación de salsa y queso', 'pizzas'),
	(13, 'Vino para equilibrar y realzar los sabores Suaves de estos tipos de queso', 'quesos suaves'),
	(14, 'Vino delicado y liviano para degustar una amplia variedad de exquisitos postre', 'postres'),
	(15, 'Vino que genera una experiencia sensorial única destacando los sabores ricos del chocolate', 'chocolates'),
	(16, 'Vino intenso para incluir en platos rústicos en base a carnes frescas recién cazadas', 'carnes cazadas'),
	(17, 'Vino complementa y realza los sabores jugosos y vibrantes de la fruta, creando una experiencia refrescante', 'ensaladas de frutas'),
	(18, 'Realza los sabores robustos y terrosos de los quesos curados, creando una experiencia gastronómica excepcional', 'quesos curados');

-- Volcando estructura para tabla ppaidb.siguiendo
CREATE TABLE IF NOT EXISTS `siguiendo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha_inicio` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `id_bodega` int(11) DEFAULT NULL,
  `id_amigo` int(11) DEFAULT NULL,
  `id_sommelier` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_bodega` (`id_bodega`),
  KEY `id_amigo` (`id_amigo`),
  KEY `id_sommelier` (`id_sommelier`),
  CONSTRAINT `siguiendo_ibfk_1` FOREIGN KEY (`id_bodega`) REFERENCES `bodega` (`id`) ON DELETE SET NULL,
  CONSTRAINT `siguiendo_ibfk_2` FOREIGN KEY (`id_amigo`) REFERENCES `enofilo` (`id`) ON DELETE SET NULL,
  CONSTRAINT `siguiendo_ibfk_3` FOREIGN KEY (`id_sommelier`) REFERENCES `sommelier` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Volcando datos para la tabla ppaidb.siguiendo: ~6 rows (aproximadamente)
INSERT INTO `siguiendo` (`id`, `fecha_inicio`, `fecha_fin`, `id_bodega`, `id_amigo`, `id_sommelier`) VALUES
	(1, '2023-01-01', NULL, 1, NULL, NULL),
	(2, '2023-01-01', NULL, 3, NULL, NULL),
	(3, '2023-01-01', NULL, 6, NULL, NULL),
	(4, '2023-01-01', NULL, 4, NULL, NULL),
	(5, '2023-01-01', NULL, 2, NULL, NULL),
	(6, '2023-01-01', NULL, 2, NULL, NULL);

-- Volcando estructura para tabla ppaidb.sommelier
CREATE TABLE IF NOT EXISTS `sommelier` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fecha_validacion` date DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `nota_presentacion` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Volcando datos para la tabla ppaidb.sommelier: ~0 rows (aproximadamente)

-- Volcando estructura para tabla ppaidb.tipouva
CREATE TABLE IF NOT EXISTS `tipouva` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` text DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Volcando datos para la tabla ppaidb.tipouva: ~18 rows (aproximadamente)
INSERT INTO `tipouva` (`id`, `descripcion`, `nombre`) VALUES
	(1, 'Variedad tinta emblemática de Argentina, con intensos sabores a ciruela, cereza negra y notas de chocolate, con taninos suaves y sedosos, ideal para carnes asadas y platos ricos.', 'Malbec'),
	(2, 'Variedad tinta mundialmente reconocida, con sabores a grosella negra, cassis y estructura robusta, ampliamente cultivada en todo el mundo.', 'Cabernet'),
	(3, 'Variedad tinta conocida por su profundo color y sabores a frutas oscuras, violetas y especias, especialmente asociada con Argentina.', 'Merlot'),
	(4, 'Variedad tinta con sabores a frutas rojas y negras, suave y redonda en boca, a menudo utilizada para suavizar mezclas de vino tinto.', 'Syrah'),
	(5, 'Variedad tinta con sabores a moras, pimienta negra y especias, produciendo vinos potentes y complejos', 'Bonarda'),
	(6, 'Variedad tinta con intensos sabores a moras y violetas, a menudo utilizada en pequeñas cantidades para añadir color y estructura a los vinos tintos.', 'Petit Verdot'),
	(7, 'Variedad tinta española con sabores a frutas rojas, cuero y vainilla, ampliamente utilizada en vinos de Rioja y Ribera del Duero.', 'Tempranillo'),
	(8, 'Variedad blanca conocida por sus sabores a cítricos, hierbas y notas herbáceas, fresca y vibrante en boca.', 'Sauvignon Blanc'),
	(9, 'Variedad tinta con sabores a frutas rojas, hierbas y pimienta, a menudo utilizada en mezclas de vino tinto.', 'Cabernet Franc'),
	(10, 'Variedad tinta delicada y elegante, con sabores a frutas rojas, especias y terroir, especialmente asociada con Borgoña.', 'Pinot Noir'),
	(11, 'Variedad tinta con sabores a frutas rojas y especias, produciendo vinos suaves y afrutados.', 'Garnacha'),
	(12, 'Variedad blanca aromática, típica de Argentina, con sabores a flores blancas, frutas tropicales y un toque de especias.', 'Torrontés'),
	(13, 'Variedad blanca con sabores a frutas de hueso, cítricos y miel, produciendo vinos frescos y fragantes, típicos de Alemania.', 'Riesling'),
	(14, 'Variedad blanca aromática con sabores a uvas frescas, florales y tropicales, utilizada para producir vinos dulces y secos.', 'Moscatel'),
	(15, 'Variedad blanca aromática con sabores a lichi, rosa y especias, conocida por su carácter distintivo y complejo.', 'Gewürztraminer'),
	(16, 'Variedad tinta mundialmente reconocida, con sabores a grosella negra, cassis y estructura robusta, ampliamente cultivada en todo el mundo.', 'Cabernet Sauvigno'),
	(17, 'Variedad blanca conocida por sus aromas a durazno, albaricoque y flores, con una textura rica y un final suave. Ideal para maridar con platos especiados y mariscos.', 'Viognier'),
	(18, 'Variedad blanca versátil, conocida por sus sabores a miel, cítricos y frutas de hueso, con una capacidad de envejecimiento que desarrolla notas complejas con el tiempo. Ideal para maridar con pescados, aves y quesos suaves.', 'Semillón');

-- Volcando estructura para tabla ppaidb.usuario
CREATE TABLE IF NOT EXISTS `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `contraseña` varchar(100) DEFAULT NULL,
  `premium` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1241 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Volcando datos para la tabla ppaidb.usuario: ~6 rows (aproximadamente)
INSERT INTO `usuario` (`id`, `nombre`, `contraseña`, `premium`) VALUES
	(1235, 'BenjaCasta', '1234', 0),
	(1236, 'MateoEst', '333', 1),
	(1237, 'FlorIsseta', '222', 1),
	(1238, 'ValBermu', '000', 0),
	(1239, 'ValeriaAzañero', '3030', 0),
	(1240, 'JuanCCeballos', '9876', 1);

-- Volcando estructura para tabla ppaidb.varietal
CREATE TABLE IF NOT EXISTS `varietal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` text NOT NULL,
  `porcentaje_composicion` varchar(50) NOT NULL,
  `tipo_uva_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tipo_uva_id` (`tipo_uva_id`),
  CONSTRAINT `varietal_ibfk_1` FOREIGN KEY (`tipo_uva_id`) REFERENCES `tipouva` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Volcando datos para la tabla ppaidb.varietal: ~0 rows (aproximadamente)

-- Volcando estructura para tabla ppaidb.vino
CREATE TABLE IF NOT EXISTS `vino` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `añada` int(11) NOT NULL,
  `imagen_etiqueta` varchar(255) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `fecha_actualizacion` date NOT NULL,
  `nota_de_cata` text NOT NULL,
  `precio_ARS` double NOT NULL,
  `bodega_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `bodega_id` (`bodega_id`),
  CONSTRAINT `vino_ibfk_1` FOREIGN KEY (`bodega_id`) REFERENCES `bodega` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Volcando datos para la tabla ppaidb.vino: ~16 rows (aproximadamente)
INSERT INTO `vino` (`id`, `añada`, `imagen_etiqueta`, `nombre`, `fecha_actualizacion`, `nota_de_cata`, `precio_ARS`, `bodega_id`) VALUES
	(49, 1993, 'https://example.com/etiqueta1.jpg', 'Talisman', '2023-05-05', 'notas fuertes', 3125, 1),
	(50, 1994, 'https://example.com/etiqueta2.jpg', 'Aurora', '2023-05-05', 'suave y afrutado', 3500, 1),
	(51, 1995, 'https://example.com/etiqueta3.jpg', 'Estrella', '2023-05-05', 'aroma a frutos rojos', 2800, 1),
	(52, 1999, 'https://example.com/etiqueta7.jpg', 'Brisas del Sur', '2023-05-05', 'suave y redondo', 2900, 3),
	(53, 2000, 'https://example.com/etiqueta8.jpg', 'Campo Verde', '2023-05-05', 'herbal y fresco', 3100, 3),
	(54, 2001, 'https://example.com/etiqueta9.jpg', 'Oro del Sol', '2023-05-05', 'dulce y afrutado', 2700, 3),
	(55, 2005, 'https://example.com/etiqueta13.jpg', 'Cumbre', '2023-05-05', 'elegante y complejo', 4700, 6),
	(56, 2006, 'https://example.com/etiqueta14.jpg', 'Alma de Viña', '2023-05-05', 'floral y afrutado', 3500, 6),
	(57, 2007, 'https://example.com/etiqueta15.jpg', 'Valle Encantado', '2023-05-05', 'frutal y fresco', 2900, 6),
	(58, 2011, 'https://example.com/etiqueta19.jpg', 'Sol de Medianoche', '2023-05-05', 'suave y redondo', 2800, 4),
	(59, 2012, 'https://example.com/etiqueta20.jpg', 'Rio de Plata', '2023-05-05', 'afrutado y fresco', 3100, 4),
	(60, 2013, 'https://example.com/etiqueta21.jpg', 'Terra Roja', '2023-05-05', 'terroso y robusto', 4500, 4),
	(61, 2017, 'https://example.com/etiqueta25.jpg', 'Campo de Oro', '2023-05-05', 'suave y afrutado', 3500, 2),
	(62, 2018, 'https://example.com/etiqueta26.jpg', 'Estrella del Sur', '2023-05-05', 'aroma a frutos rojos', 2800, 2),
	(63, 2019, 'https://example.com/etiqueta27.jpg', 'Sol y Sombra', '2023-05-05', 'toques de vainilla', 4000, 2),
	(64, 2022, 'https://example.com/etiqueta30.jpg', 'Brisas de Mendoza', '2023-05-05', 'suave y redondo', 2900, 5);

-- Volcando estructura para tabla ppaidb.vino_maridaje
CREATE TABLE IF NOT EXISTS `vino_maridaje` (
  `vino_id` int(11) NOT NULL,
  `maridaje_id` int(11) NOT NULL,
  PRIMARY KEY (`vino_id`,`maridaje_id`),
  KEY `maridaje_id` (`maridaje_id`),
  CONSTRAINT `vino_maridaje_ibfk_1` FOREIGN KEY (`vino_id`) REFERENCES `vino` (`id`) ON DELETE CASCADE,
  CONSTRAINT `vino_maridaje_ibfk_2` FOREIGN KEY (`maridaje_id`) REFERENCES `maridaje` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Volcando datos para la tabla ppaidb.vino_maridaje: ~32 rows (aproximadamente)
INSERT INTO `vino_maridaje` (`vino_id`, `maridaje_id`) VALUES
	(49, 1),
	(60, 1),
	(63, 1),
	(49, 2),
	(57, 2),
	(59, 2),
	(50, 3),
	(53, 3),
	(57, 3),
	(59, 3),
	(61, 3),
	(50, 4),
	(61, 4),
	(51, 5),
	(52, 5),
	(58, 5),
	(62, 5),
	(64, 5),
	(51, 6),
	(58, 6),
	(62, 6),
	(55, 7),
	(63, 7),
	(60, 10),
	(53, 11),
	(52, 12),
	(64, 12),
	(54, 13),
	(54, 14),
	(56, 14),
	(55, 16),
	(56, 17);

-- Volcando estructura para tabla ppaidb.vino_varietal
CREATE TABLE IF NOT EXISTS `vino_varietal` (
  `vino_id` int(11) NOT NULL,
  `varietal_id` int(11) NOT NULL,
  PRIMARY KEY (`vino_id`,`varietal_id`),
  KEY `varietal_id` (`varietal_id`),
  CONSTRAINT `vino_varietal_ibfk_1` FOREIGN KEY (`vino_id`) REFERENCES `vino` (`id`) ON DELETE CASCADE,
  CONSTRAINT `vino_varietal_ibfk_2` FOREIGN KEY (`varietal_id`) REFERENCES `varietal` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Volcando datos para la tabla ppaidb.vino_varietal: ~0 rows (aproximadamente)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
