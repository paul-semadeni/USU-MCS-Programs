-- CREATE DATABASE intro_to_data_analysis

-- SHOW DATABASES;

USE intro_to_data_analysis;
CREATE TABLE wiki_edit(
	revision_id 		INT 				AUTO_INCREMENT
    , article_name 		VARCHAR(500)
    , edit_date 		DATE
    , user_name 		VARCHAR(50)
    , CONSTRAINT pk_id 	PRIMARY KEY 		(revision_id)
);

SELECT * FROM wiki_edit;
