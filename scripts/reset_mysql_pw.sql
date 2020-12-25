/* Reset the MySQL Password after automated
   Installation. This can be either run remote
   from console, or from the local host
*/

-- You should...probably replace supersecretsquirrel....
FLUSH PRIVILEGES;
USE mysql;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'supersecretsquirrel';
quit

