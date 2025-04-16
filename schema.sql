CREATE USER 'flaskapp'@'%' IDENTIFIED BY 'TOdo_app25';
GRANT ALL PRIVILEGES ON todo_db.* TO 'flaskapp'@'%';
FLUSH PRIVILEGES;

CREATE DATABASE IF NOT EXISTS todo_db;

USE todo_db;

CREATE TABLE todos ( 
	id INT AUTO_INCREMENT PRIMARY KEY, 
	title VARCHAR(255) NOT NULL, 
	complete BOOLEAN DEFAULT FALSE, 
	date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
	);
