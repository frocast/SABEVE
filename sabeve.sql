SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `aula_virtual` DEFAULT CHARACTER SET utf8 ;
USE `aula_virtual` ;

-- -----------------------------------------------------
-- Table `aula_virtual`.`biblioteca`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `aula_virtual`.`biblioteca` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `titulo` VARCHAR(100) NULL DEFAULT NULL ,
  `autor` VARCHAR(50) NULL DEFAULT NULL ,
  `ISSNISBN` VARCHAR(20) NULL DEFAULT NULL ,
  `tipo` VARCHAR(10) NULL DEFAULT NULL ,
  `editorial` VARCHAR(100) NULL DEFAULT NULL ,
  `fecha` INT(11) NULL DEFAULT NULL ,
  `idioma` VARCHAR(20) NULL DEFAULT NULL ,
  `resena` VARCHAR(5000) NULL DEFAULT NULL ,
  `link` VARCHAR(500) NULL DEFAULT NULL ,
  `portada` VARCHAR(5000) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aula_virtual`.`usuarios`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `aula_virtual`.`usuarios` (
  `Nombre` VARCHAR(30) NULL DEFAULT NULL ,
  `Apellido` VARCHAR(30) NULL DEFAULT NULL ,
  `email` VARCHAR(50) NOT NULL ,
  `knd` VARCHAR(20) NULL DEFAULT NULL ,
  `fecha_na` VARCHAR(15) NULL DEFAULT NULL ,
  `institucion` VARCHAR(200) NULL DEFAULT NULL ,
  `genero` VARCHAR(10) NULL DEFAULT NULL ,
  `pasw` VARCHAR(500) NULL DEFAULT NULL ,
  `id_grupo` INT(11) NULL DEFAULT NULL ,
  PRIMARY KEY (`email`) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aula_virtual`.`grupos`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `aula_virtual`.`grupos` (
  `id_grupo` INT(11) NOT NULL AUTO_INCREMENT ,
  `email` VARCHAR(50) NULL DEFAULT NULL ,
  `nombre` VARCHAR(100) NULL DEFAULT NULL ,
  PRIMARY KEY (`id_grupo`) ,
  INDEX `email_idx` (`email` ASC) ,
  CONSTRAINT `email`
    FOREIGN KEY (`email` )
    REFERENCES `aula_virtual`.`usuarios` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aula_virtual`.`moocs`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `aula_virtual`.`moocs` (
  `id_mooc` INT(11) NOT NULL AUTO_INCREMENT ,
  `descripcion` VARCHAR(500) NULL DEFAULT NULL ,
  `titulo` VARCHAR(100) NULL DEFAULT NULL ,
  `email` VARCHAR(50) NULL DEFAULT NULL ,
  `id_grupo` INT(11) NULL DEFAULT NULL ,
  PRIMARY KEY (`id_mooc`) ,
  INDEX `email_idx` (`email` ASC) ,
  INDEX `id_grupo_idx` (`id_grupo` ASC) ,
  CONSTRAINT `email`
    FOREIGN KEY (`email` )
    REFERENCES `aula_virtual`.`usuarios` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id_grupo`
    FOREIGN KEY (`id_grupo` )
    REFERENCES `aula_virtual`.`grupos` (`id_grupo` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aula_virtual`.`contenido_mooc`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `aula_virtual`.`contenido_mooc` (
  `id_contenido` INT(11) NOT NULL AUTO_INCREMENT ,
  `id_mooc` INT(11) NULL DEFAULT NULL ,
  `titulo` VARCHAR(200) NULL DEFAULT NULL ,
  `url` VARCHAR(500) NULL DEFAULT NULL ,
  `email` VARCHAR(50) NULL DEFAULT NULL ,
  PRIMARY KEY (`id_contenido`) ,
  INDEX `email_idx` (`email` ASC) ,
  INDEX `id_mooc_idx` (`id_mooc` ASC) ,
  CONSTRAINT `email`
    FOREIGN KEY (`email` )
    REFERENCES `aula_virtual`.`moocs` (`descripcion` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id_mooc`
    FOREIGN KEY (`id_mooc` )
    REFERENCES `aula_virtual`.`moocs` (`id_mooc` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aula_virtual`.`temas`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `aula_virtual`.`temas` (
  `id_tema` INT(11) NOT NULL AUTO_INCREMENT ,
  `id_grupo` INT(11) NULL DEFAULT NULL ,
  `tema` VARCHAR(100) NULL DEFAULT NULL ,
  `email` VARCHAR(50) NULL DEFAULT NULL ,
  PRIMARY KEY (`id_tema`) ,
  INDEX `email_idx` (`email` ASC) ,
  CONSTRAINT `email`
    FOREIGN KEY (`email` )
    REFERENCES `aula_virtual`.`usuarios` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aula_virtual`.`contenidos_tema`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `aula_virtual`.`contenidos_tema` (
  `id_contenido` INT(11) NOT NULL AUTO_INCREMENT ,
  `id_tema` INT(11) NULL DEFAULT NULL ,
  `subtema` VARCHAR(100) NULL DEFAULT NULL ,
  `pdf_link` VARCHAR(1000) NULL DEFAULT NULL ,
  `habilitar` VARCHAR(10) NULL DEFAULT NULL ,
  PRIMARY KEY (`id_contenido`) ,
  INDEX `id_tema_idx` (`id_tema` ASC) ,
  CONSTRAINT `id_tema`
    FOREIGN KEY (`id_tema` )
    REFERENCES `aula_virtual`.`temas` (`id_tema` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aula_virtual`.`evaluaciones`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `aula_virtual`.`evaluaciones` (
  `id_evaluaciones` INT(11) NOT NULL AUTO_INCREMENT ,
  `id_contenido` INT(11) NULL DEFAULT NULL ,
  `pregunta` VARCHAR(200) NULL DEFAULT NULL ,
  `respuesta_1` VARCHAR(500) NULL DEFAULT NULL ,
  `respuesta_2` VARCHAR(500) NULL DEFAULT NULL ,
  `respuesta_3` VARCHAR(500) NULL DEFAULT NULL ,
  PRIMARY KEY (`id_evaluaciones`) ,
  INDEX `id_contenido_idx` (`id_contenido` ASC) ,
  CONSTRAINT `id_contenido`
    FOREIGN KEY (`id_contenido` )
    REFERENCES `aula_virtual`.`contenido_mooc` (`id_contenido` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aula_virtual`.`foro`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `aula_virtual`.`foro` (
  `id_tema` INT(11) NOT NULL AUTO_INCREMENT ,
  `autor` VARCHAR(50) NULL DEFAULT NULL ,
  `titulo` VARCHAR(200) NULL DEFAULT NULL ,
  `mensaje` VARCHAR(500) NULL DEFAULT NULL ,
  `fecha` DATETIME NULL DEFAULT NULL ,
  PRIMARY KEY (`id_tema`) ,
  INDEX `email_idx` (`autor` ASC) ,
  CONSTRAINT `email`
    FOREIGN KEY (`autor` )
    REFERENCES `aula_virtual`.`usuarios` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aula_virtual`.`intereses`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `aula_virtual`.`intereses` (
  `id_intereses` INT(11) NOT NULL AUTO_INCREMENT ,
  `email` VARCHAR(50) NULL DEFAULT NULL ,
  `pais` VARCHAR(50) NULL DEFAULT NULL ,
  `habilidades` VARCHAR(1000) NULL DEFAULT NULL ,
  `nota` VARCHAR(1000) NULL DEFAULT NULL ,
  `institucion` VARCHAR(100) NULL DEFAULT NULL ,
  PRIMARY KEY (`id_intereses`) ,
  INDEX `email_idx` (`email` ASC) ,
  CONSTRAINT `email`
    FOREIGN KEY (`email` )
    REFERENCES `aula_virtual`.`usuarios` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aula_virtual`.`mensajes`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `aula_virtual`.`mensajes` (
  `id_mensaje` INT(11) NOT NULL AUTO_INCREMENT ,
  `email` VARCHAR(50) NULL DEFAULT NULL ,
  `id_tema` INT(11) NULL DEFAULT NULL ,
  `fecha` DATETIME NULL DEFAULT NULL ,
  `mensaje` VARCHAR(500) NULL DEFAULT NULL ,
  PRIMARY KEY (`id_mensaje`) ,
  INDEX `email_idx` (`email` ASC) ,
  INDEX `id_tema_idx` (`id_tema` ASC) ,
  CONSTRAINT `email`
    FOREIGN KEY (`email` )
    REFERENCES `aula_virtual`.`usuarios` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id_tema`
    FOREIGN KEY (`id_tema` )
    REFERENCES `aula_virtual`.`foro` (`id_tema` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aula_virtual`.`podcasts`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `aula_virtual`.`podcasts` (
  `id_pod` INT(11) NOT NULL AUTO_INCREMENT ,
  `titulo` VARCHAR(100) NULL DEFAULT NULL ,
  `descripcion` VARCHAR(5000) NULL DEFAULT NULL ,
  `email` VARCHAR(50) NULL DEFAULT NULL ,
  `fecha_pu` DATETIME NULL DEFAULT NULL ,
  `url` VARCHAR(500) NULL DEFAULT NULL ,
  `portada` VARCHAR(500) NULL DEFAULT NULL ,
  `tipo` VARCHAR(10) NULL DEFAULT NULL ,
  PRIMARY KEY (`id_pod`) ,
  INDEX `email_idx` (`email` ASC) ,
  CONSTRAINT `email`
    FOREIGN KEY (`email` )
    REFERENCES `aula_virtual`.`usuarios` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aula_virtual`.`resultados`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `aula_virtual`.`resultados` (
  `id_resultados` INT(11) NOT NULL AUTO_INCREMENT ,
  `email` VARCHAR(50) NULL DEFAULT NULL ,
  `id_evaluacion` INT(11) NULL DEFAULT NULL ,
  `calificacion` VARCHAR(500) NULL DEFAULT NULL ,
  PRIMARY KEY (`id_resultados`) ,
  INDEX `email_idx` (`email` ASC) ,
  INDEX `id_evaluacion_idx` (`id_evaluacion` ASC) ,
  CONSTRAINT `email`
    FOREIGN KEY (`email` )
    REFERENCES `aula_virtual`.`usuarios` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id_evaluacion`
    FOREIGN KEY (`id_evaluacion` )
    REFERENCES `aula_virtual`.`evaluaciones` (`id_evaluaciones` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `aula_virtual`.`sitios`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `aula_virtual`.`sitios` (
  `id_sitios` INT(11) NOT NULL AUTO_INCREMENT ,
  `email` VARCHAR(50) NULL DEFAULT NULL ,
  `titulo` VARCHAR(100) NULL DEFAULT NULL ,
  `link` VARCHAR(500) NULL DEFAULT NULL ,
  PRIMARY KEY (`id_sitios`) ,
  INDEX `email_idx` (`email` ASC) ,
  CONSTRAINT `email`
    FOREIGN KEY (`email` )
    REFERENCES `aula_virtual`.`usuarios` (`email` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

USE `aula_virtual` ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
