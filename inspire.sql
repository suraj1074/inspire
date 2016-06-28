-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 03, 2016 at 06:36 PM
-- Server version: 5.5.49-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `inspire`
--

-- --------------------------------------------------------

--
-- Table structure for table `college_info`
--

CREATE TABLE IF NOT EXISTS `college_info` (
  `college_id` int(11) NOT NULL,
  `college_name` varchar(2000) NOT NULL,
  `college_state` int(11) NOT NULL,
  `college_pincode` int(11) NOT NULL,
  `college_representative` int(11) NOT NULL,
  PRIMARY KEY (`college_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `inspire_info`
--

CREATE TABLE IF NOT EXISTS `inspire_info` (
  `inspire_id` int(11) NOT NULL AUTO_INCREMENT,
  `inspire_jnv` int(11) NOT NULL,
  `inspire_date` date DEFAULT NULL,
  `step_1` int(11) DEFAULT '0',
  `step_2` double NOT NULL DEFAULT '0',
  `step_3` double NOT NULL DEFAULT '0',
  `comment` text,
  `power_break` int(11) NOT NULL DEFAULT '0',
  `time_inspireAdded` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`inspire_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=17 ;

--
-- Dumping data for table `inspire_info`
--

INSERT INTO `inspire_info` (`inspire_id`, `inspire_jnv`, `inspire_date`, `step_1`, `step_2`, `step_3`, `comment`, `power_break`, `time_inspireAdded`) VALUES
(4, 1, '2016-04-23', 100, 0, 0, 'This is done', 0, '0000-00-00 00:00:00'),
(5, 1, '2016-04-22', 100, 0, 0, 'Great work', 0, '0000-00-00 00:00:00'),
(6, 1, NULL, 50, 0, 0, NULL, 0, '0000-00-00 00:00:00'),
(7, 1, '0000-00-00', 50, 0, 0, NULL, 0, '0000-00-00 00:00:00'),
(8, 1, '2016-04-16', 50, 0, 0, NULL, 0, '0000-00-00 00:00:00'),
(9, 1, '2016-04-23', 50, 0, 0, NULL, 0, '0000-00-00 00:00:00'),
(10, 1, '0000-00-00', 50, 0, 0, NULL, 0, '2016-04-10 19:23:23'),
(11, 1, '0000-00-00', 50, 0, 0, NULL, 0, '2016-04-10 19:37:05'),
(12, 1, '2016-04-22', 50, 0, 0, NULL, 0, '2016-04-11 07:03:34'),
(13, 1, '2016-04-22', 50, 0, 0, NULL, 0, '2016-04-11 07:03:35'),
(14, 1, '2016-04-29', 50, 0, 0, NULL, 0, '2016-04-11 07:07:36'),
(15, 1, '2016-04-29', 50, 0, 0, NULL, 0, '2016-04-11 07:07:37'),
(16, 1, '2016-04-23', 50, 0, 0, NULL, 0, '2016-04-11 07:12:02');

-- --------------------------------------------------------

--
-- Table structure for table `inspire_volunteer`
--

CREATE TABLE IF NOT EXISTS `inspire_volunteer` (
  `inspire_volunteer_id` int(11) NOT NULL AUTO_INCREMENT,
  `inspire_id` int(11) NOT NULL,
  `volunteer_id` int(11) NOT NULL,
  PRIMARY KEY (`inspire_volunteer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `jnv_info`
--

CREATE TABLE IF NOT EXISTS `jnv_info` (
  `jnv_id` int(11) NOT NULL AUTO_INCREMENT,
  `jnv_name` varchar(1000) NOT NULL,
  `jnv_district` varchar(1000) NOT NULL,
  `jnv_state` int(11) NOT NULL,
  `jnv_address` text NOT NULL,
  `jnv_pincode` int(11) NOT NULL,
  `jnv_email` varchar(1000) NOT NULL,
  `jnv_howToReach` text NOT NULL,
  PRIMARY KEY (`jnv_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `jnv_info`
--

INSERT INTO `jnv_info` (`jnv_id`, `jnv_name`, `jnv_district`, `jnv_state`, `jnv_address`, `jnv_pincode`, `jnv_email`, `jnv_howToReach`) VALUES
(1, 'testjnv1', '', 0, '', 0, 'sjha1519@gmail.com', ''),
(2, 'testjnv2', '', 0, '', 0, 'puneet3821@gmail.com', '');

-- --------------------------------------------------------

--
-- Table structure for table `mail`
--

CREATE TABLE IF NOT EXISTS `mail` (
  `mail_id` int(11) NOT NULL AUTO_INCREMENT,
  `inspire_id` int(11) NOT NULL,
  `thread` varchar(1000) NOT NULL,
  `mail_type` int(11) NOT NULL,
  PRIMARY KEY (`mail_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=17 ;

--
-- Dumping data for table `mail`
--

INSERT INTO `mail` (`mail_id`, `inspire_id`, `thread`, `mail_type`) VALUES
(4, 4, '153fc018bf3cf8b1', 1),
(5, 5, '153fc1d23bf85603', 1),
(6, 6, '153fc20fe411c9b2', 1),
(7, 7, '153fc2926b0d37a2', 1),
(8, 8, '153fc2c0562d4318', 1),
(9, 9, '15400a576208c8ef', 1),
(10, 10, '15401a0a9d17aea9', 1),
(11, 11, '15401ad3630dda0b', 1),
(12, 12, '1540421b27a9d1d6', 1),
(13, 13, '1540421b6b9fcffd', 1),
(14, 14, '15404256362e5cf0', 1),
(15, 15, '15404256703ea459', 1),
(16, 16, '154042973386ec60', 1);

-- --------------------------------------------------------

--
-- Table structure for table `principal_info`
--

CREATE TABLE IF NOT EXISTS `principal_info` (
  `principal_id` int(11) NOT NULL AUTO_INCREMENT,
  `principal_name` varchar(1000) NOT NULL,
  `principal_gender` int(11) NOT NULL,
  `principal_email` varchar(1000) NOT NULL,
  `principal_jnv` int(11) NOT NULL,
  `principal_contactNo` bigint(11) NOT NULL,
  PRIMARY KEY (`principal_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `principal_info`
--

INSERT INTO `principal_info` (`principal_id`, `principal_name`, `principal_gender`, `principal_email`, `principal_jnv`, `principal_contactNo`) VALUES
(1, 'Suraj', 1, '', 1, 8214748364),
(2, 'Sheela', 2, '', 2, 0);

-- --------------------------------------------------------

--
-- Table structure for table `states`
--

CREATE TABLE IF NOT EXISTS `states` (
  `state_id` int(11) NOT NULL AUTO_INCREMENT,
  `state_name` varchar(1000) NOT NULL,
  PRIMARY KEY (`state_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `volunteer_info`
--

CREATE TABLE IF NOT EXISTS `volunteer_info` (
  `volunteer_id` int(11) NOT NULL AUTO_INCREMENT,
  `volunteer_name` varchar(1000) NOT NULL,
  `volunteer_email` varchar(1000) NOT NULL,
  `volunteer_contactNo` int(11) NOT NULL,
  `volunteer_college` int(11) NOT NULL,
  PRIMARY KEY (`volunteer_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `volunteer_info`
--

INSERT INTO `volunteer_info` (`volunteer_id`, `volunteer_name`, `volunteer_email`, `volunteer_contactNo`, `volunteer_college`) VALUES
(1, 'Volunteer 1', 'sjha1519@gmail.com', 0, 0),
(2, 'Volunteer 2', 'puneet3821@gmail.com', 0, 0);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
