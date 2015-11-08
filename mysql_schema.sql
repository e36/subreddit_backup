-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.6.17 - MySQL Community Server (GPL)
-- Server OS:                    Win64
-- HeidiSQL Version:             9.3.0.4998
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Dumping database structure for pythontest
CREATE DATABASE IF NOT EXISTS `pythontest` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `pythontest`;


-- Dumping structure for table pythontest.tblcomments
CREATE TABLE IF NOT EXISTS `tblcomments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `link_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `parent_id` varchar(50) NOT NULL,
  `score` int(11) NOT NULL,
  `created_utc` varchar(50) NOT NULL,
  `author` varchar(50) NOT NULL,
  `body` text NOT NULL,
  `body_html` text NOT NULL,
  `lastchecked` datetime NOT NULL,
  `lastmodified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `post_id` (`link_id`),
  CONSTRAINT `tblcomments_ibfk_1` FOREIGN KEY (`link_id`) REFERENCES `tblposts` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.


-- Dumping structure for table pythontest.tblhistory
CREATE TABLE IF NOT EXISTS `tblhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `message` varchar(250) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.


-- Dumping structure for table pythontest.tblmessagelog
CREATE TABLE IF NOT EXISTS `tblmessagelog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` varchar(50) DEFAULT NULL,
  `created` datetime NOT NULL,
  `executed` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.


-- Dumping structure for table pythontest.tblmessages
CREATE TABLE IF NOT EXISTS `tblmessages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` varchar(50) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.


-- Dumping structure for table pythontest.tblposts
CREATE TABLE IF NOT EXISTS `tblposts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `thread_id` varchar(50) NOT NULL,
  `created_utc` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `title` text NOT NULL,
  `author` varchar(50) NOT NULL,
  `domain` int(11) NOT NULL,
  `score` int(11) NOT NULL,
  `num_comments` int(11) NOT NULL,
  `link_flair_text` varchar(50) NOT NULL,
  `upvote_ratio` int(11) NOT NULL,
  `permalink` varchar(50) NOT NULL,
  `selftext` text NOT NULL,
  `selftext_html` text NOT NULL,
  `lastchecked` datetime NOT NULL,
  `lastmodified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `domain` (`domain`),
  CONSTRAINT `tblposts_ibfk_1` FOREIGN KEY (`domain`) REFERENCES `tblsubreddits` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.


-- Dumping structure for table pythontest.tblsubreddits
CREATE TABLE IF NOT EXISTS `tblsubreddits` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `domain` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
