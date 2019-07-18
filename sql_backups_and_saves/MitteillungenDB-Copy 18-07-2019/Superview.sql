-- --------------------------------------------------------
-- Hôte :                        soldb.oma.be
-- Version du serveur:           5.5.62-0ubuntu0.14.04.1 - (Ubuntu)
-- SE du serveur:                debian-linux-gnu
-- HeidiSQL Version:             10.2.0.5599
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Listage de la structure de la base pour DATA_SILSO_HISTO
CREATE DATABASE IF NOT EXISTS `DATA_SILSO_HISTO` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `DATA_SILSO_HISTO`;

-- Listage de la structure de la vue DATA_SILSO_HISTO. SuperView
-- Création d'une table temporaire pour palier aux erreurs de dépendances de VIEW
CREATE TABLE `SuperView` (
	`ID` INT(11) NOT NULL,
	`DATE` DATE NULL,
	`GROUPS` INT(11) NULL,
	`SUNSPOTS` INT(11) NULL,
	`WOLF` INT(11) NULL,
	`RubricID` INT(11) NOT NULL,
	`RUBRICS_NUMBER` INT(11) UNSIGNED NOT NULL COMMENT 'ATTENTION: àpd chapitre 125 numérotation changée (3 chiffres chapitre + 2 chiffres Mitt) pe : 12501',
	`MITT_NUMBER` INT(11) UNSIGNED NOT NULL,
	`PAGE_NUMBER` INT(11) UNSIGNED NULL,
	`SOURCE` TEXT NOT NULL COLLATE 'utf8_general_ci',
	`SOURCE_DATE` DATE NULL,
	`COMMENTS` TEXT NULL COLLATE 'utf8_general_ci',
	`DATE_INSERT` DATETIME NULL,
	`ObserversID` INT(11) NOT NULL,
	`ALIAS` VARCHAR(50) NULL COLLATE 'utf8_general_ci',
	`FIRST_NAME` VARCHAR(50) NULL COLLATE 'utf8_general_ci',
	`LAST_NAME` VARCHAR(50) NULL COLLATE 'utf8_general_ci',
	`COUNTRY` VARCHAR(50) NULL COLLATE 'utf8_general_ci',
	`INSTRUMENT` VARCHAR(50) NULL COLLATE 'utf8_general_ci',
	`COMMENT` TEXT NULL COLLATE 'utf8_general_ci'
) ENGINE=MyISAM;

-- Listage de la structure de la vue DATA_SILSO_HISTO. SuperView
-- Suppression de la table temporaire et création finale de la structure d'une vue
DROP TABLE IF EXISTS `SuperView`;
CREATE ALGORITHM=UNDEFINED DEFINER=`silsomgr`@`%.oma.be` SQL SECURITY DEFINER VIEW `SuperView` AS select `d`.`ID` AS `ID`,`d`.`DATE` AS `DATE`,`d`.`GROUPS` AS `GROUPS`,`d`.`SUNSPOTS` AS `SUNSPOTS`,`d`.`WOLF` AS `WOLF`,`r`.`RUBRICS_ID` AS `RubricID`,`r`.`RUBRICS_NUMBER` AS `RUBRICS_NUMBER`,`r`.`MITT_NUMBER` AS `MITT_NUMBER`,`r`.`PAGE_NUMBER` AS `PAGE_NUMBER`,`r`.`SOURCE` AS `SOURCE`,`r`.`SOURCE_DATE` AS `SOURCE_DATE`,`r`.`COMMENTS` AS `COMMENTS`,`r`.`DATE_INSERT` AS `DATE_INSERT`,`o`.`ID` AS `ObserversID`,`o`.`ALIAS` AS `ALIAS`,`o`.`FIRST_NAME` AS `FIRST_NAME`,`o`.`LAST_NAME` AS `LAST_NAME`,`o`.`COUNTRY` AS `COUNTRY`,`o`.`INSTRUMENT` AS `INSTRUMENT`,`o`.`COMMENT` AS `COMMENT` from ((`DATA` `d` join `RUBRICS` `r`) join `OBSERVERS` `o`) where ((`d`.`FK_RUBRICS` = `r`.`RUBRICS_ID`) and (`d`.`FK_OBSERVERS` = `o`.`ID`)) WITH CASCADED CHECK OPTION;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
