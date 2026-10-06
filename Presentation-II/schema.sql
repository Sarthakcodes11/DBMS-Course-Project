-- MySQL 8.0.16+; non-destructive creation. Use an empty project database.
CREATE DATABASE IF NOT EXISTS campus_placement;
USE campus_placement;
CREATE TABLE Department (dept_id INT PRIMARY KEY AUTO_INCREMENT, dept_name VARCHAR(150) NOT NULL UNIQUE, hod_name VARCHAR(150) NOT NULL);
CREATE TABLE Student (student_id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(150) NOT NULL, dept_id INT NOT NULL, cgpa DECIMAL(3,2) NOT NULL CHECK(cgpa BETWEEN 0 AND 10), email VARCHAR(150) NOT NULL UNIQUE, FOREIGN KEY(dept_id) REFERENCES Department(dept_id));
CREATE TABLE Company (company_id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(150) NOT NULL, sector VARCHAR(150) NOT NULL, hr_contact VARCHAR(150) NOT NULL);
CREATE TABLE Drive (drive_id INT PRIMARY KEY AUTO_INCREMENT, company_id INT NOT NULL, role VARCHAR(150) NOT NULL, ctc DECIMAL(8,2) NOT NULL CHECK(ctc>0), drive_date DATE NOT NULL, min_cgpa DECIMAL(3,2) NOT NULL DEFAULT 7 CHECK(min_cgpa BETWEEN 0 AND 10), FOREIGN KEY(company_id) REFERENCES Company(company_id));
CREATE TABLE Application (application_id INT PRIMARY KEY AUTO_INCREMENT, student_id INT NOT NULL, drive_id INT NOT NULL, status ENUM('Applied','Interview','Selected','Rejected') NOT NULL DEFAULT 'Applied', UNIQUE(student_id,drive_id), FOREIGN KEY(student_id) REFERENCES Student(student_id), FOREIGN KEY(drive_id) REFERENCES Drive(drive_id));
CREATE TABLE Interview (interview_id INT PRIMARY KEY AUTO_INCREMENT, application_id INT NOT NULL, round_no INT NOT NULL CHECK(round_no>0), result ENUM('Pending','Passed','Failed') NOT NULL DEFAULT 'Pending', UNIQUE(application_id,round_no), FOREIGN KEY(application_id) REFERENCES Application(application_id));
CREATE TABLE Placement (placement_id INT PRIMARY KEY AUTO_INCREMENT, application_id INT NOT NULL UNIQUE, package DECIMAL(8,2) NOT NULL CHECK(package>0), placement_date DATE NOT NULL, FOREIGN KEY(application_id) REFERENCES Application(application_id));
DELIMITER $$
CREATE TRIGGER application_eligibility_insert BEFORE INSERT ON Application FOR EACH ROW
BEGIN
 IF (SELECT cgpa FROM Student WHERE student_id=NEW.student_id)<(SELECT min_cgpa FROM Drive WHERE drive_id=NEW.drive_id) THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Student does not meet the drive CGPA requirement.'; END IF;
END$$
CREATE TRIGGER application_eligibility_update BEFORE UPDATE ON Application FOR EACH ROW
BEGIN
 IF (NEW.student_id<>OLD.student_id OR NEW.drive_id<>OLD.drive_id) AND (SELECT cgpa FROM Student WHERE student_id=NEW.student_id)<(SELECT min_cgpa FROM Drive WHERE drive_id=NEW.drive_id) THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Student does not meet the drive CGPA requirement.'; END IF;
 IF NEW.status<>'Selected' AND EXISTS(SELECT 1 FROM Placement WHERE application_id=OLD.application_id) THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Remove the placement before changing selected status.'; END IF;
END$$
CREATE TRIGGER placement_selected_insert BEFORE INSERT ON Placement FOR EACH ROW
BEGIN
 IF COALESCE((SELECT status FROM Application WHERE application_id=NEW.application_id),'')<>'Selected' THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Only a Selected application can receive a placement.'; END IF;
END$$
CREATE TRIGGER placement_selected_update BEFORE UPDATE ON Placement FOR EACH ROW
BEGIN
 IF COALESCE((SELECT status FROM Application WHERE application_id=NEW.application_id),'')<>'Selected' THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT='Only a Selected application can receive a placement.'; END IF;
END$$
DELIMITER ;
