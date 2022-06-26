--
-- Database: `Weight`
--

CREATE DATABASE IF NOT EXISTS `weight`;

-- --------------------------------------------------------

--
-- Table structure for table `containers-registered`
--

USE weight;


CREATE TABLE IF NOT EXISTS `containers_registered` (
  `container_id` varchar(15) NOT NULL,
  `weight` int(12) DEFAULT NULL,
  `unit` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`container_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE IF NOT EXISTS `transactions` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `datetime` varchar(50) DEFAULT NULL,
  `direction` varchar(10) DEFAULT NULL,
  `truck` varchar(50) DEFAULT NULL,
  `containers` varchar(10000) DEFAULT NULL,
  `bruto` int(12) DEFAULT NULL,
  `truckTara` int(12) DEFAULT NULL,
  --   "neto": <int> or "na" // na if some of containers unknown
  `neto` int(12) DEFAULT NULL,
  `produce` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;

INSERT INTO `transactions` 
(  `datetime` , `direction` , `truck` , `containers` ,
 `bruto` ,`truckTara` , `neto` ,`produce`)  VALUES
( "20220622125007", "out","87" , "66,77,88",
 891 , 90 , 100 , "bananas");

INSERT INTO `transactions` 
(  `datetime` , `direction` , `truck` , `containers` ,
 `bruto` ,`truckTara` , `neto` ,`produce`)  VALUES
( "20220622115008", "IN", "54" , " 4,5,6",
 891 , 33 , 100 , "avokado");

 INSERT INTO `transactions`                               
(  `datetime` , `direction` , `truck` , `containers` ,
 `bruto` ,`truckTara` , `neto` ,`produce`)  VALUES
( "20220621115009", "IN", "54" , " 8,11",
 891 , 33 , 100 , "nuts");

INSERT INTO `containers_registered` (`unit`, `container_id`, `weight`)  VALUES ( "kg", "C-35434", "4564");
INSERT INTO `containers_registered` (`unit`, `container_id`)  VALUES ( "lbs", "C-122");
INSERT INTO `containers_registered` (`unit`, `container_id`, `weight`)  VALUES ( "lbs", "C-12d2", "214097");
INSERT INTO `containers_registered` (`unit`, `container_id`)  VALUES ( "kg", "C-174");
INSERT INTO `containers_registered` (`unit`, `container_id`)  VALUES ( "kg", "C-123");
INSERT INTO `containers_registered` (`unit`, `container_id`)  VALUES ( "lbs", "C-12");
INSERT INTO `containers_registered` (`unit`, `container_id`)  VALUES ( "kg", "C-1");


-- show tables;

-- describe containers_registered;
-- describe transactions;



--
-- Dumping data for table `test`
--

-- INSERT INTO `test` (`id`, `aa`) VALUES
-- (1, 'aaaa'),
