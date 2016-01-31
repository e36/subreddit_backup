-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.7.10-log - MySQL Community Server (GPL)
-- Server OS:                    Win64
-- HeidiSQL Version:             9.3.0.5044
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for iama
CREATE DATABASE IF NOT EXISTS `iama` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `iama`;

-- Dumping structure for table iama.tblcomments
CREATE TABLE IF NOT EXISTS `tblcomments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `link_id` int(11) NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `parent_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `score` int(11) NOT NULL,
  `created_utc` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `author` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `body` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `body_html` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `lastchecked` datetime NOT NULL,
  `lastmodified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `post_id` (`link_id`),
  CONSTRAINT `tblcomments_ibfk_1` FOREIGN KEY (`link_id`) REFERENCES `tblposts` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=51574 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.
-- Dumping structure for table iama.tblhistory
CREATE TABLE IF NOT EXISTS `tblhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime DEFAULT NULL,
  `finished` datetime DEFAULT NULL,
  `message` mediumtext COLLATE utf8mb4_unicode_ci,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.
-- Dumping structure for table iama.tblmessagelog
CREATE TABLE IF NOT EXISTS `tblmessagelog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created` datetime NOT NULL,
  `executed` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.
-- Dumping structure for table iama.tblmessages
CREATE TABLE IF NOT EXISTS `tblmessages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.
-- Dumping structure for table iama.tblposts
CREATE TABLE IF NOT EXISTS `tblposts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `thread_id` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_utc` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` mediumtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `author` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `domain` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `comments` int(11) NOT NULL,
  `link_flair_text` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `upvote_ratio` int(11) NOT NULL,
  `permalink` varchar(250) COLLATE utf8mb4_unicode_ci NOT NULL,
  `selftext` mediumtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `selftext_html` mediumtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `lastchecked` datetime NOT NULL,
  `lastmodified` datetime NOT NULL,
  `archived` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `domain` (`domain`),
  CONSTRAINT `tblposts_ibfk_1` FOREIGN KEY (`domain`) REFERENCES `tblsubreddits` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.
-- Dumping structure for table iama.tblsubreddits
CREATE TABLE IF NOT EXISTS `tblsubreddits` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `domain` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
