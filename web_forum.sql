-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema web_forum
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema web_forum
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `web_forum` DEFAULT CHARACTER SET utf8mb4 ;
USE `web_forum` ;

-- -----------------------------------------------------
-- Table `web_forum`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web_forum`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `role` VARCHAR(45) NOT NULL DEFAULT 'user',
  `email` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `web_forum`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web_forum`.`messages` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(45) NOT NULL,
  `date` DATETIME NULL,
  `sender_id` INT NOT NULL,
  `receiver_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_messages_users_idx` (`sender_id` ASC) VISIBLE,
  INDEX `fk_messages_users1_idx` (`receiver_id` ASC) VISIBLE,
  CONSTRAINT `fk_messages_users`
    FOREIGN KEY (`sender_id`)
    REFERENCES `web_forum`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_messages_users1`
    FOREIGN KEY (`receiver_id`)
    REFERENCES `web_forum`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `web_forum`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web_forum`.`categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `is_private` TINYINT NULL,
  `is_locked` TINYINT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `web_forum`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web_forum`.`replies` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `topics_id` INT NOT NULL,
  `author_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_replies_topics1_idx` (`topics_id` ASC) VISIBLE,
  INDEX `fk_replies_users1_idx` (`author_id` ASC) VISIBLE,
  CONSTRAINT `fk_replies_topics1`
    FOREIGN KEY (`topics_id`)
    REFERENCES `web_forum`.`topics` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_users1`
    FOREIGN KEY (`author_id`)
    REFERENCES `web_forum`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `web_forum`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web_forum`.`topics` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `content` TEXT NOT NULL,
  `locked` TINYINT NOT NULL,
  `categories_id` INT NOT NULL,
  `author_id` INT NOT NULL,
  `best_reply_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) VISIBLE,
  INDEX `fk_topics_categories1_idx` (`categories_id` ASC) VISIBLE,
  INDEX `fk_topics_users1_idx` (`author_id` ASC) VISIBLE,
  INDEX `fk_topics_replies1_idx` (`best_reply_id` ASC) VISIBLE,
  CONSTRAINT `fk_topics_categories1`
    FOREIGN KEY (`categories_id`)
    REFERENCES `web_forum`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_users1`
    FOREIGN KEY (`author_id`)
    REFERENCES `web_forum`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_replies1`
    FOREIGN KEY (`best_reply_id`)
    REFERENCES `web_forum`.`replies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `web_forum`.`permissions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web_forum`.`permissions` (
  `categories_id` INT NOT NULL,
  `users_id` INT NOT NULL,
  `read_permission` TINYINT NOT NULL DEFAULT 0,
  `write_permission` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`categories_id`, `users_id`),
  INDEX `fk_categories_has_users_users1_idx` (`users_id` ASC) VISIBLE,
  INDEX `fk_categories_has_users_categories1_idx` (`categories_id` ASC) VISIBLE,
  CONSTRAINT `fk_categories_has_users_categories1`
    FOREIGN KEY (`categories_id`)
    REFERENCES `web_forum`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_categories_has_users_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `web_forum`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `web_forum`.`votes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `web_forum`.`votes` (
  `users_id` INT NOT NULL,
  `replies_id` INT NOT NULL,
  `vote` INT NULL DEFAULT NULL,
  PRIMARY KEY (`users_id`, `replies_id`),
  INDEX `fk_users_has_replies_replies1_idx` (`replies_id` ASC) VISIBLE,
  INDEX `fk_users_has_replies_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_replies_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `web_forum`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_replies_replies1`
    FOREIGN KEY (`replies_id`)
    REFERENCES `web_forum`.`replies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
