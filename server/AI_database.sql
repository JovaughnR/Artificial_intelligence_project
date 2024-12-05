-- Create databases (no need to use USE command)
CREATE DATABASE ai_project;

-- Connect to the database
c ai_project;

-- Create `students` table
CREATE TABLE students (
  usrID INT PRIMARY KEY,
  firstName VARCHAR(20) NOT NULL,
  lastName VARCHAR(20) NOT NULL,
  email VARCHAR(50) NOT NULL,
  programme VARCHAR(30) NOT NULL
);

-- Create `staff` table
CREATE TABLE staff (
  usrID INT PRIMARY KEY,
  fname VARCHAR(25) NOT NULL,
  lname VARCHAR(25) NOT NULL,
  email VARCHAR(50) NOT NULL
);

-- Create `user_auth` table
CREATE TABLE user_auth (
  usrID INT PRIMARY KEY,
  password VARCHAR(65) NOT NULL,
  type VARCHAR(10) NOT NULL
);

-- Create `modules` table
CREATE TABLE modules (
  modulecode VARCHAR(10) PRIMARY KEY,
  module VARCHAR(50) NOT NULL,
  credits INT NOT NULL
);

-- Create `module_details` table
CREATE TABLE module_details (
  id SERIAL PRIMARY KEY,
  modulecode VARCHAR(10) NOT NULL,
  module VARCHAR(50) NOT NULL,
  usrID INT NOT NULL,
  year VARCHAR(10) NOT NULL,
  semester INT NOT NULL,
  gradepoints DECIMAL(4, 2) NOT NULL
  -- FOREIGN KEY (modulecode) REFERENCES modules(modulecode),
  -- FOREIGN KEY (usrID) REFERENCES students(usrID)
);

-- Insert data into `students` table
INSERT INTO students (usrID, firstName, lastName, email, programme) VALUES
(1245981, 'Shemar', 'Allen', 'sallen@gmail.com', 'Information Technology'),
(1245982, 'Christophor', 'Jonson', 'cjonson@yahoo.com', 'Software Engineering'),
(1245983, 'Kevin', 'Jacson', 'kjacson@gmail.com', 'Data Science'),
(1245984, 'Shania', 'Gray', 'sgray@gmail.com', 'Computer Science'),
(1245987, 'Margrett', 'Jonson', 'mjonson@gmail.com');

-- Insert data into `user_auth` table
INSERT INTO user_auth (usrID, password, type) VALUES
(1245981, 'iamtired48', 'student'),
(1245982, 'iamtireds', 'student'),
(1245983, 'iamtired8', 'student'),
(1245984, 'iamtired9', 'student'),
(1245987, 'iamtired', 'student');

-- Update password in `user_auth`
UPDATE user_auth 
SET password = '6fe8554e848a28bc4226c2d3be32f7492e2fa93f6aa3be494b91faa3de974b3e'
WHERE usrID = 1245981;

-- Insert data into `staff` table
INSERT INTO staff (usrID, fname, lname, email) VALUES
(1245970, 'Javii', 'Doe', 'jdoe@gmail.com'),
(1245977, 'Shemar', 'Allen', 'sallen@gmail.com'),
(1245989, 'Christophor', 'Jonson', 'cjonson@yahoo.com'),
(1245971, 'Kevin', 'Jacson', 'kjacson@gmail.com'),
(1245676, 'Shania', 'Gray', 'sgray@gmail.com'),
(1245571, 'Margrett', 'Jonson', 'mjonson@gmail.com'),
(1245111, 'Stacey', 'Jonson', 'sjonson@yahoo.com');

-- Insert more data into `user_auth`
INSERT INTO user_auth (usrID, password, type) VALUES
(1245970, 'iamtired54', 'staff'),
(1245977, 'iamtired48', 'staff'),
(1245989, 'iamtireds', 'staff'),
(1245971, 'iamtired8', 'staff'),
(1245676, 'iamtired9', 'staff'),
(1245571, 'iamtired', 'staff'),
(1245111, 'iamtired2', 'staff');

-- Update password in `user_auth`
UPDATE user_auth 
SET password = '8d1541baa48e971d174b96439c9270772c6d9acdaa69869c0209df72619cdf46'
WHERE usrID = 1245970;

-- Select statements
SELECT * FROM user_auth;
SELECT * FROM students;

-- Add an administrator to the system
INSERT INTO user_auth (usrID, password, type) VALUES (
  1111111, '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin'
);
