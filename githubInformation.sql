DROP TABLE IF EXISTS `GithubInfo`;
DROP TABLE IF EXISTS `commitMsg`;

CREATE TABLE GithubInfo (
    `githubName` VARCHAR(256) NOT NULL,
    `commits` INT(11), 
    `branches` INT(11),
    `releases` INT(11),
    `contributors` INT(11),
    `watch` INT(11),
    `star` INT(11),
    `fork` INT(11),
    UNIQUE  KEY(`githubName`)
) ENGINE = INNODB;

CREATE TABLE commitMsg (
    `SHA` VARCHAR(256) NOT NULL,
    `user` VARCHAR(256),
    `date` VARCHAR(356),
    `commitMessage` VARCHAR(256)
    UNIQUE KEY(`SHA`)
) ENGINE = INNODB;