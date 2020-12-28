
CREATE DATABASE avatar_db;
CREATE USER rtrenneman IDENTIFIED BY 'haveyouturneditoffandonagain';
FLUSH PRIVILEGES;

SELECT DATABASE avatar_db;

CREATE TABLE avatars (
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
	bucket VARCHAR (100) NOT NULL,
	file CHAR (10) NOT NULL,
	PRIMARY KEY (id)
	);
					
GRANT SELECT, INSERT, UPDATE, DELETE on avatars to 'rtrenneman';
