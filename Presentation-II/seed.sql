USE campus_placement;
START TRANSACTION;
INSERT INTO `Department` (`dept_id`,`dept_name`,`hod_name`) VALUES
(1,'CSE','Department Coordinator'),
(2,'ECE','Department Coordinator'),
(3,'IT','Department Coordinator'),
(4,'ME','Department Coordinator');
INSERT INTO `Student` (`student_id`,`name`,`dept_id`,`cgpa`,`email`) VALUES
(1,'Aarav Mehta',1,8.9,'aarav@example.edu'),
(2,'Sara Iyer',2,8.2,'sara@example.edu'),
(3,'Rohan Das',1,7.8,'rohan@example.edu'),
(4,'Priya Nair',3,9.1,'priya@example.edu'),
(5,'Kunal Shah',4,7.4,'kunal@example.edu');
INSERT INTO `Company` (`company_id`,`name`,`sector`,`hr_contact`) VALUES
(1,'TCS','Technology','tcs@example.com'),
(2,'Infosys','Technology','infosys@example.com'),
(3,'Wipro','Technology','wipro@example.com'),
(4,'Accenture','Technology','accenture@example.com'),
(5,'Cognizant','Technology','cognizant@example.com');
INSERT INTO `Drive` (`drive_id`,`company_id`,`role`,`ctc`,`drive_date`,`min_cgpa`) VALUES
(101,1,'Analyst',6.5,'2026-08-11',7),
(102,2,'SDE',7.2,'2026-08-12',7),
(103,3,'SDE',6,'2026-08-13',7),
(104,4,'Consultant',8,'2026-08-14',7),
(105,5,'SDE',6.8,'2026-08-15',7);
INSERT INTO `Application` (`application_id`,`student_id`,`drive_id`,`status`) VALUES
(1,1,101,'Selected'),
(2,2,102,'Interview'),
(3,3,103,'Rejected'),
(4,4,104,'Selected'),
(5,5,105,'Applied');
INSERT INTO `Interview` (`interview_id`,`application_id`,`round_no`,`result`) VALUES
(1,2,1,'Pending');
INSERT INTO `Placement` (`placement_id`,`application_id`,`package`,`placement_date`) VALUES
(1,1,6.5,'2026-08-11'),
(2,4,8,'2026-08-14');
COMMIT;
