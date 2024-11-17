-- Active: 1696603788118@@127.0.0.1@3306
create database ai_project;

use ai_project;

CREATE TABLE `modules` (
  `modulecode` varchar(10) PRIMARY KEY NOT NULL,
  `module` varchar(50) NOT NULL,
  `credits` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


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

select * from module_details;

drop table module_details;
CREATE TABLE `module_details` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `modulecode` VARCHAR(10) NOT NULL,
  `StdID` INT(11) NOT NULL,
  `year` VARCHAR(10) NOT NULL,
  `semester` INT(11) NOT NULL,
  `gradepoints` DECIMAL(4, 2) NOT NULL,
  FOREIGN KEY (`modulecode`) REFERENCES `modules`(`modulecode`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Insert data into module_details

-- Student 1245980 (Javii Doe)
INSERT INTO `module_details` (`modulecode`, `StdID`, `year`, `semester`, `gradepoints`)
VALUES
('CMP1024', 1245980, '2024', 1, 4),
('CMP2006', 1245980, '2024', 2, 3.67);

4 + 3.6 = 7.6


use ai_project;
insert into `module_details` (`modulecode`, `StdID`, `year`, `semester`, `gradepoints`) VALUES
("CIT3009", 1245980, '2024', 1, 3.6);


-- SELECT gradepoints, semester 
-- FROM module_details WHERE studID = 1245980 and semester = 1;

-- Student 1245981 (Shemar Allen)
INSERT INTO `module_details` (`modulecode`, `studID`, `year`, `semester`, `grade`, `gradepoints`)
VALUES
('CMP1026', 1245981, '2024', 1, 'B+', 3.33),
('CIT3002', 1245981, '2024', 2, 'B', 3);

-- Student 1245982 (Christophor Jonson)
INSERT INTO `module_details` (`modulecode`, `studID`, `year`, `semester`, `grade`, `gradepoints`)
VALUES
('CMP2019', 1245982, '2024', 1, 'A', 4),
('CIT3003', 1245982, '2024', 2, 'B+', 3.33);

-- Student 1245983 (Kevin Jacson)
INSERT INTO `module_details` (`modulecode`, `studID`, `year`, `semester`, `grade`, `gradepoints`)
VALUES
('CMP4011', 1245983, '2024', 1, 'A', 4),
('CIT4020', 1245983, '2024', 2, 'A-', 3.67);

-- Student 1245984 (Shania Gray)
INSERT INTO `module_details` (`modulecode`, `studID`, `year`, `semester`, `grade`, `gradepoints`)
VALUES
('CMP1025', 1245984, '2024', 1, 'B+', 3.33),
('CMP2018', 1245984, '2024', 2, 'A-', 3.67);


INSERT INTO `module_details` (`module`, `credits`, `year`, `semester`, `studID`, `grade`, `gradepoints`) VALUES
('CIT2004', 4, '', 0, 1011020, 'B', 3);

CREATE TABLE `staff` (
  `staffID` int(7) PRIMARY KEY NOT NULL, -- UPDATE set  staffId
  `fname` varchar(25) NOT NULL,
  `lname` varchar(25) NOT NULL,
  `email` varchar(50) NOT NULL,
  `Type` varchar(70) NOT NULL,
  `school` varchar(25) NOT NULL
--   `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

drop table staff;


create table staff_authentication (
    `staffID` int(7) PRIMARY KEY NOT NULL,
    `password` varchar(65) NOT NULL,
    Foreign Key (`staffID`) REFERENCES `staff`(`staffID`)
)

drop table staff_authentication;

INSERT INTO `staff` (`staffID`, `fname`, `lname`, `email`, `Type`, `school`) 
VALUES
(1245980, 'Javii', 'Doe', 'm', 'jdoe@gmail.com', 'Lecture', 'FOSS'),
(1245981, 'Shemar', 'Allen', 'm', 'sallen@gmail.com', 'Admin', 'SCIT'),
(1245982, 'Christophor', 'Jonson', 'm', 'cjonson@yahoo.com', 'Supervisor', 'SOBA'),
(1245983, 'Kevin', 'jacson', 'm', 'kjacson@gmail.com', 'Supervisor', 'SCIT'),
(1245984, 'Shania', 'Gray', 'f', 'sgray@gmail.com', 'Lecture', 'SOBA'),
(1245987, 'Margrett', 'Jonson', 'f', 'mjonson@gmail.com', 'Lecture', 'SCIT'),
(1245989, 'Stacey', 'Jonson', 'f', 'sjonson@yahoo.com', 'Admin', 'admin');

INSERT INTO `staff_authentication` (`staffID`, `password`) 
VALUES
(1245980, 'iamtired54'),
(1245981, 'iamtired48'),
(1245982, 'iamtireds'),
(1245983, 'iamtired8'),
(1245984, 'iamtired9'),
(1245987, 'iamtired'),
(1245989, 'iamtired2');

select * from staff where `staffID` = 1245981;



-- Normalize student table -- Update done by Jovaughn Rose
drop table `students`; -- Since there might unexpected results I am going to delete the entire database
drop database `ai_project`;

-- Recreate the database
create database `ai_project`;
use `ai_project`;
-- add student table

CREATE TABLE `students` (
  `StdID` int(7) PRIMARY KEY NOT NULL, -- Update set StdID as primary key
  `firstName` varchar(20) NOT NULL,
  `lastName` varchar(20) NOT NULL,
  `gender` char(1) NOT NULL,
  `email` varchar(50) NOT NULL,
  `programme` varchar(30) NOT NULL
--   `password` varchar(25) NOT NULL  -- Update by Jovaughn Rose
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE student_authentication (
    `StdID` INT(7) PRIMARY KEY NOT NULL,
    `password` VARCHAR(65) NOT NULL,
    FOREIGN KEY (`StdID`) REFERENCES `students`(`StdID`)
);

-- drop table student_authentication;

INSERT INTO `students` (`StdID`, `firstName`, `lastName`, `email`, `programme`) 
VALUES
(1245980, 'Javii', 'Doe', 'm', 'jdoe@gmail.com', 'Computer Science'),
(1245981, 'Shemar', 'Allen', 'm', 'sallen@gmail.com', 'Information Technology'),
(1245982, 'Christophor', 'Jonson', 'm', 'cjonson@yahoo.com', 'Software Engineering'),
(1245983, 'Kevin', 'jacson', 'm', 'kjacson@gmail.com', 'Data Science'),
(1245984, 'Shania', 'Gray', 'f', 'sgray@gmail.com', 'Computer Science'),
(1245987, 'Margrett', 'Jonson', 'f', 'mjonson@gmail.com', 'Information Technology'),
(1245989, 'Stacey', 'Jonson', 'f', 'sjonson@yahoo.com', 'Software Engineering');

INSERT INTO `student_authentication` (`StdID`, `password`) 
VALUES
(1245980, '8d1541baa48e971d174b96439c9270772c6d9acdaa69869c0209df72619cdf46'),
(1245981, 'iamtired48'),
(1245982, 'iamtireds'),
(1245983, 'iamtired8'),
(1245984, 'iamtired9'),
(1245987, 'iamtired'),
(1245989, 'iamtired2');



delete from students where StdID = 2111876;
delete from student_authentication where StdID = 2111876;