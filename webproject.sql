-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema webproject
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema webproject
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `webproject` DEFAULT CHARACTER SET latin1 ;
USE `webproject` ;

-- -----------------------------------------------------
-- Table `webproject`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webproject`.`categories` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `is_private` TINYINT(4) NOT NULL DEFAULT 0,
  `is_locked` TINYINT(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `webproject`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webproject`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `role` VARCHAR(45) NOT NULL DEFAULT 'user',
  `email` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `webproject`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webproject`.`messages` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `date` DATETIME NOT NULL,
  `sender_id` INT(11) NOT NULL,
  `receiver_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_messages_users3_idx` (`sender_id` ASC) VISIBLE,
  INDEX `fk_messages_users4_idx` (`receiver_id` ASC) VISIBLE,
  CONSTRAINT `fk_messages_users3`
    FOREIGN KEY (`sender_id`)
    REFERENCES `webproject`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_messages_users4`
    FOREIGN KEY (`receiver_id`)
    REFERENCES `webproject`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `webproject`.`permissions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webproject`.`permissions` (
  `category_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  `read_permission` TINYINT(4) NOT NULL DEFAULT 0,
  `write_permission` TINYINT(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`category_id`, `user_id`),
  INDEX `fk_permissions_categories_idx` (`category_id` ASC) VISIBLE,
  INDEX `fk_permissions_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_permissions_categories`
    FOREIGN KEY (`category_id`)
    REFERENCES `webproject`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_permissions_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `webproject`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `webproject`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webproject`.`topics` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `content` TEXT NOT NULL,
  `locked` TINYINT(4) NOT NULL DEFAULT 0,
  `best_reply_id` INT(11) NULL DEFAULT NULL,
  `categories_id` INT(11) NOT NULL,
  `author_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) VISIBLE,
  INDEX `fk_topics_categories1_idx` (`categories_id` ASC) VISIBLE,
  INDEX `fk_topics_users1_idx` (`author_id` ASC) VISIBLE,
  CONSTRAINT `fk_topics_categories1`
    FOREIGN KEY (`categories_id`)
    REFERENCES `webproject`.`categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_users1`
    FOREIGN KEY (`author_id`)
    REFERENCES `webproject`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `webproject`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webproject`.`replies` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `topics_id` INT(11) NOT NULL,
  `author_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_replies_topics_idx` (`topics_id` ASC) VISIBLE,
  INDEX `fk_replies_users_idx` (`author_id` ASC) VISIBLE,
  CONSTRAINT `fk_replies_topics`
    FOREIGN KEY (`topics_id`)
    REFERENCES `webproject`.`topics` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_users`
    FOREIGN KEY (`author_id`)
    REFERENCES `webproject`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `webproject`.`votes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webproject`.`votes` (
  `replies_id` INT(11) NOT NULL,
  `users_id` INT(11) NOT NULL,
  `vote` INT(11) NOT NULL,
  PRIMARY KEY (`replies_id`, `users_id`),
  INDEX `fk_votes_replies_idx` (`replies_id` ASC) VISIBLE,
  INDEX `fk_votes_users_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_votes_replies`
    FOREIGN KEY (`replies_id`)
    REFERENCES `webproject`.`replies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_votes_users`
    FOREIGN KEY (`users_id`)
    REFERENCES `webproject`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
