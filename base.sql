-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 27, 2017 at 03:12 AM
-- Server version: 5.6.34-log
-- PHP Version: 7.1.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `aula_virtual`
--

-- --------------------------------------------------------

--
-- Table structure for table `biblioteca`
--

CREATE TABLE `biblioteca` (
  `titulo` varchar(100) NOT NULL,
  `autor` varchar(50) NOT NULL,
  `ISSNISBN` varchar(20) NOT NULL,
  `tipo` varchar(10) NOT NULL,
  `editorial` varchar(50) NOT NULL,
  `fecha` int(50) NOT NULL,
  `idioma` varchar(20) NOT NULL,
  `resena` varchar(5000) NOT NULL,
  `link` varchar(500) NOT NULL,
  `portada` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `biblioteca`
--

INSERT INTO `biblioteca` (`titulo`, `autor`, `ISSNISBN`, `tipo`, `editorial`, `fecha`, `idioma`, `resena`, `link`, `portada`) VALUES
('El psicoanalista', 'Jonh Katzenbach', '9786074802139', 'Libro', 'zeta limitada', 2011, 'Espanol', 'Asi comienza el anonimo que recibe Frederick Starks, psicoanalista con una larga experiencia y una vida tranquila. Starks tendra que emplear toda su astucia y rapidez', 'http://www.clubdelphos.org/sites/default/files/El_Psicoanalista-John_Katzenbach.pdf', 'http://www.quelibroleo.com/images/libros/libro_1333101559.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `foro`
--

CREATE TABLE `foro` (
  `id_tema` int(100) NOT NULL,
  `autor` varchar(50) NOT NULL,
  `titulo` varchar(50) NOT NULL,
  `mensaje` varchar(240) NOT NULL,
  `fecha` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `foro`
--

INSERT INTO `foro` (`id_tema`, `autor`, `titulo`, `mensaje`, `fecha`) VALUES
(1, 'diego@diego.com', 'Sandra', 'Chillona', '2017-10-23 19:24:25'),
(2, 'diego@diego.com', 'chillona', 'sandra', '2017-10-23 19:25:08'),
(3, 'diego@diego.com', 'Tema ', 'Mensaje', '2017-10-26 18:22:49'),
(4, 'diego@diego.com', 'tema', ' nuevo', '2017-10-26 18:24:21');

-- --------------------------------------------------------

--
-- Table structure for table `mensajes`
--

CREATE TABLE `mensajes` (
  `email` varchar(50) NOT NULL,
  `id_tema` int(100) NOT NULL,
  `fecha` datetime NOT NULL,
  `mensaje` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `mensajes`
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
('fra.castilloa@outlook.com', 1, '2017-10-19 20:42:01', 'mensaje nuevo'),
('fra.castilloa@outlook.com', 1, '2017-10-23 19:00:09', 'no me se explicar'),
('diego@diego.com', 4, '2017-10-26 18:27:34', 'respuesta');

-- --------------------------------------------------------

--
-- Table structure for table `usuarios`
--

CREATE TABLE `usuarios` (
  `Nombre` varchar(30) NOT NULL,
  `Apellido` varchar(30) NOT NULL,
  `email` varchar(50) NOT NULL,
  `knd` varchar(20) NOT NULL,
  `pasw` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `usuarios`
--

INSERT INTO `usuarios` (`Nombre`, `Apellido`, `email`, `knd`, `pasw`) VALUES
('Diego', 'Rangel Castillo', 'diego@diego.com', 'Alumno', '123'),
('Francisco', 'Castillo', 'fra.castilloa@outlook.com', 'Maestro', 'mov_ah,00h'),
('fabiola', 'vela', 'fvela@hotmail.com', 'Maestro', '123'),
('Fabiola', 'Vela', 'sandra_gcb12@hotmail.com', 'Alumno', '123'),
('Fabiola Sandra', 'Vela Vazquez', 'svela@sabeve.com', 'Admin', 'sabeve');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `foro`
--
ALTER TABLE `foro`
  ADD PRIMARY KEY (`id_tema`);

--
-- Indexes for table `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `foro`
--
ALTER TABLE `foro`
  MODIFY `id_tema` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
