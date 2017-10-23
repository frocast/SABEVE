-- phpMyAdmin SQL Dump
-- version 4.7.3
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:8889
-- Tiempo de generación: 23-10-2017 a las 05:43:21
-- Versión del servidor: 5.6.35
-- Versión de PHP: 7.1.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Base de datos: `aula_virtual`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `foro`
--

CREATE TABLE `foro` (
  `id_tema` int(100) NOT NULL,
  `autor` varchar(50) NOT NULL,
  `titulo` varchar(50) NOT NULL,
  `mensaje` varchar(240) NOT NULL,
  `fecha` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `foro`
--

INSERT INTO `foro` (`id_tema`, `autor`, `titulo`, `mensaje`, `fecha`) VALUES
(1, 'fra.castilloa@outlook.com', 'Creacion de foro ', 'Como crear un foro usando Python', '2017-10-17 22:40:47'),
(2, 'sandra_gcb12@hotmail.com', 'Codigo ASCII', 'Como permitir que python interprete caracteres especiales', '2017-10-17 23:19:03');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mensajes`
--

CREATE TABLE `mensajes` (
  `email` varchar(50) NOT NULL,
  `id_tema` int(100) NOT NULL,
  `fecha` datetime NOT NULL,
  `mensaje` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `mensajes`
--

INSERT INTO `mensajes` (`email`, `id_tema`, `fecha`, `mensaje`) VALUES
('svela@sabeve.com', 0, '2017-10-18 23:46:24', 'mensaje respuesta'),
('svela@sabeve.com', 0, '2017-10-18 23:49:11', 'mensaje respuesta'),
('sandra_gcb12@hotmail.com', 1, '2017-10-18 23:51:31', 'mensaje '),
('fra.castilloa@outlook.com', 1, '2017-10-18 23:56:56', 'nuevo mensaje'),
('fra.castilloa@outlook.com', 1, '2017-10-18 23:58:24', 'FRANCISCO MENSAJE'),
('fra.castilloa@outlook.com', 1, '2017-10-19 00:01:35', 'mensaje '),
('sandra_gcb12@hotmail.com', 1, '2017-10-19 00:02:04', 'mensaje de cuenta sandra'),
('fra.castilloa@outlook.com', 2, '2017-10-19 00:05:26', 'mensaje '),
('fra.castilloa@outlook.com', 2, '2017-10-19 00:07:16', 'nuevo'),
('fra.castilloa@outlook.com', 2, '2017-10-19 00:07:45', 'nuevo'),
('fra.castilloa@outlook.com', 2, '2017-10-19 00:07:53', 'siguiente mensaje '),
('sandra_gcb12@hotmail.com', 2, '2017-10-19 00:08:02', 'nuevo mensaje '),
('svela@sabeve.com', 1, '2017-10-19 00:09:08', 'nuevo mensaje de svela'),
('svela@sabeve.com', 2, '2017-10-19 00:09:21', 'mensaje de svela'),
('fra.castilloa@outlook.com', 1, '2017-10-19 20:42:01', 'mensaje nuevo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `Nombre` varchar(30) NOT NULL,
  `Apellido` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `knd` varchar(20) NOT NULL,
  `pasw` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`Nombre`, `Apellido`, `email`, `knd`, `pasw`) VALUES
('Diego', 'Rangel Castillo', 'diego@diego.com', 'Alumno', '123'),
('Francisco', 'Castillo', 'fra.castilloa@outlook.com', 'Maestro', 'mov_ah,00h'),
('Fabiola', 'Vela', 'sandra_gcb12@hotmail.com', 'Alumno', '123'),
('Fabiola Sandra', 'Vela Vazquez', 'svela@sabeve.com', 'Admin', 'sabeve');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `foro`
--
ALTER TABLE `foro`
  ADD PRIMARY KEY (`id_tema`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `foro`
--
ALTER TABLE `foro`