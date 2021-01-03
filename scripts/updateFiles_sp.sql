/* Stored Procedure to replace the 'image'
   folder with 'avatar' in the database. 
   
   The Secondary update will replace the bucket
   Names with the updated bucket (new-image)
*/


USE avatar_db;

DROP PROCEDURE IF EXISTS updateFiles;

DELIMITER ;;
CREATE PROCEDURE updateFiles()
BEGIN

-- Replace 'avatar' with the folder name of the 'new' folder (if necessary)
	UPDATE avatars SET file = CONCAT("avatar/",SUBSTRING_INDEX(file,"/",-1));

-- Replace with your Bucket Names here. Old->New. From->To
	UPDATE avatars SET bucket = replace(bucket,'jaysons-legacy-image-bucket','jaysons-new-image-bucket');

END ;;
DELIMITER ;

