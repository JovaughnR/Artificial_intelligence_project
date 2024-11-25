-- Active: 1696603788118@@127.0.0.1@3306
create database ai_project;

drop database ai_project;
use ai_project;


select * from students;
CREATE TABLE `students` (
  `usrID` int(7) PRIMARY KEY NOT NULL, -- Update set usrID as primary key
  `firstName` varchar(20) NOT NULL,
  `lastName` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `programme` varchar(30) NOT NULL
);

CREATE TABLE `staff` (
  `usrID` int(7) PRIMARY KEY NOT NULL, -- UPDATE set  usrID
  `fname` varchar(25) NOT NULL,
  `lname` varchar(25) NOT NULL,
  `email` varchar(50) NOT NULL,
  `Type` varchar(70) NOT NULL,
  `school` varchar(25) NOT NULL
);

create table `user_auth` (
  `usrID` INT(7) PRIMARY KEY,
  `password` varchar(65) NOT NULL,
  `type` varchar(10) NOT NULL
)

CREATE TABLE `modules` (
  `modulecode` varchar(10) PRIMARY KEY NOT NULL,
  `module` varchar(50) NOT NULL,
  `credits` int(11) NOT NULL
)


drop table module_details;
CREATE TABLE `module_details` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `modulecode` VARCHAR(10) NOT NULL,
  `module` varchar(50) NOT NULL,
  `usrID` INT(11) NOT NULL,
  `year` VARCHAR(10) NOT NULL,
  `semester` INT(11) NOT NULL,
  `gradepoints` DECIMAL(4, 2) NOT NULL
  -- FOREIGN KEY (`modulecode`) REFERENCES `modules`(`modulecode`),
  -- Foreign Key (`usrID`) REFERENCES `students`(`usrID`)
);

select * from module_details;

INSERT INTO `module_details` (`modulecode`, `module`, `usrID`, `year`, `semester`, `gradepoints`) 
VALUES
('CMP1024', 'Programming 1', 2111876, '2024', 1, 3.50),
('CMP1025', 'Programming 2', 2111876, '2024', 2, 3.80),
('MAT1047', 'College Mathematics', 2111876, '2024', 1, 3.20),
('MAT2003', 'Calculus 1', 2111876, '2024', 2, 2.80),
('CIT2011', 'Web Programming', 2111876, '2024', 1, 3.70),
('CMP2019', 'Software Engineering', 2111876, '2025', 1, 3.90),
('CMP1026', 'Computer Networks', 2111876, '2025', 2, 3.40),
('CMP4011', 'Artificial Intelligence', 2111876, '2025', 2, 3.60),
('CMP2006', 'Data Structures', 2111876, '2025', 1, 3.30),
('CIT4024', 'IT Project Management', 2111876, '2025', 2, 3.85);


INSERT INTO `modules` (`module`, `modulecode`, `credits`) VALUES
('Introduction to Psychology', ' PSY1002', 4),
('Introduction to Bio-Informatics', 'BIO3004', 3),
('Object-Oriented Programming with C++', 'CIT2004', 4),
('Web Programming', 'CIT2011', 3),
('Operating Systems', 'CIT3002', 4),
('Analysis of Algorithms', 'CIT3003', 3),
('Theory of Computation', 'CIT3006', 3),
('Advanced Programming', 'CIT3009', 3),
('Analysis of Programming Languages', 'CIT4004', 3),
('Computer Security', 'CIT4020', 3),
('IT Project Management', 'CIT4024', 4),
('Computer Logic and Digital Design', 'CMP1005', 3),
('Programming 1', 'CMP1024', 4),
('Programming 2', 'CMP1025', 4),
('Computer Networks', 'CMP1026', 3),
('Data Structures', 'CMP2006', 4),
('Academic Writing 1', 'CMP2014', 3),
('Database Design', 'CMP2018', 3),
('Software Engineering', 'CMP2019', 3),
('Artificial Intelligence', 'CMP4011', 4),
('Academic writing 1', 'COM1020', 3),
('Community Service Project', 'CSP1001', 1),
('Environmental Studies', 'ENS3001', 3),
('College Level IT', 'INT1001', 3),
('Discrete Mathematics', 'MAT1008', 3),
('Linear Algebra', 'MAT1043', 3),
('College Mathematics', 'MAT1047', 4),
('Calculus 1', 'MAT2003', 3),
('Physics', 'PHS1019', 4),
('Design of Experiments', 'STA2016', 3),
('Introductory Statistics', 'STA2020', 3);


INSERT INTO `students` (`usrID`, `firstName`, `lastName`, `email`, `programme`) 
VALUES
(1245981, 'Shemar', 'Allen', 'sallen@gmail.com', 'Information Technology'),
(1245982, 'Christophor', 'Jonson',  'cjonson@yahoo.com', 'Software Engineering'),
(1245983, 'Kevin', 'jacson', 'kjacson@gmail.com', 'Data Science'),
(1245984, 'Shania', 'Gray', 'sgray@gmail.com', 'Computer Science'),
(1245987, 'Margrett', 'Jonson',  'mjonson@gmail.com', 'Information Technology');

INSERT INTO `user_auth` (`usrID`, `password`, `type`) 
VALUES
(1245981, 'iamtired48', 'student'),
(1245982, 'iamtireds', 'student'),
(1245983, 'iamtired8', 'student'),
(1245984, 'iamtired9', 'student'),
(1245987, 'iamtired', 'student');

update `user_auth` 
set `password` = '6fe8554e848a28bc4226c2d3be32f7492e2fa93f6aa3be494b91faa3de974b3e'
where usrID = 1245981;

INSERT INTO `staff` (`usrID`, `fname`, `lname`, `email`, `Type`, `school`) 
VALUES
(1245970, 'Javii', 'Doe', 'jdoe@gmail.com', 'Lecture', 'FOSS'),
(1245977, 'Shemar', 'Allen', 'sallen@gmail.com', 'Admin', 'SCIT'),
(1245989, 'Christophor', 'Jonson', 'cjonson@yahoo.com', 'Supervisor', 'SOBA'),
(1245971, 'Kevin', 'jacson', 'kjacson@gmail.com', 'Supervisor', 'SCIT'),
(1245676, 'Shania', 'Gray', 'sgray@gmail.com', 'Lecture', 'SOBA'),
(1245571, 'Margrett', 'Jonson', 'mjonson@gmail.com', 'Lecture', 'SCIT'),
(1245111, 'Stacey', 'Jonson', 'sjonson@yahoo.com', 'Admin', 'admin');


INSERT INTO `user_auth` (`usrID`, `password`, `type`) 
VALUES
(1245970, 'iamtired54', 'staff'),
(1245977, 'iamtired48', 'staff'),
(1245989, 'iamtireds', 'staff'),
(1245971, 'iamtired8', 'staff'),
(1245676, 'iamtired9', 'staff'),
(1245571, 'iamtired', 'staff'),
(1245111, 'iamtired2', 'staff');

update `user_auth`
set `password` = '8d1541baa48e971d174b96439c9270772c6d9acdaa69869c0209df72619cdf46'
where usrID = 1245970;

select * from user_auth;
select * from students;