DROP TABLE IF EXISTS `Github_Info`;

CREATE TABLE Github_Info(
    `github_name` varchar(256) NOT NULL,
    `commits` int(11), 
    `branches` int(11),
    `releases` int(11),
    `contributors` int(11),
    `watch` int(11),
    `star` int(11),
    `fork` int(11),
    UNIQUE  KEY(`github_name`)
) ENGINE = INNODB;