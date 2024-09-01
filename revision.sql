-- DROP DATABASE revision;
CREATE DATABASE IF NOT EXISTS revision;
USE revision;

CREATE TABLE IF NOT EXISTS questions (
	question_id INT NOT NULL AUTO_INCREMENT,
    programming_language VARCHAR(50) NOT NULL,
    question VARCHAR(255) NOT NULL,
    answer VARCHAR(255) NOT NULL,
    mastery_level_0_to_10 INT DEFAULT 0, -- PUT DEFAULT VALUE 0 IF NOT ENTERED
	PRIMARY KEY (question_id),
	CONSTRAINT check_confidence_range CHECK (mastery_level_0_to_10 BETWEEN 0 AND 10)
);

INSERT INTO questions (programming_language, question, answer) VALUES 
('JavaScript', 'What is a variable in JavaScript?', 'A variable in JavaScript is used to store data values.'),
('JavaScript', 'How do you declare a variable in JavaScript?', 'You can declare a variable in JavaScript using the "var", "let", or "const" keywords.'),
('JavaScript', 'What are the different data types in JavaScript?', 'JavaScript has several data types including strings, numbers, booleans, arrays, objects, and more.'),
('JavaScript', 'What is the difference between "==" and "===" in JavaScript?', '"==" in JavaScript checks for equality of value, while "===" checks for equality of value and data type.'),
('JavaScript', 'How do you comment in JavaScript?', 'In JavaScript, you can use "//" for single-line comments and "/* */" for multi-line comments.'),
('Python', 'What is a list in Python?', 'A list in Python is a collection of items, which can be of different data types, enclosed in square brackets.'),
('Python', 'How do you define a function in Python?', 'You can define a function in Python using the "def" keyword followed by the function name and parentheses containing any parameters.'),
('Python', 'What is the difference between "==" and "is" in Python?', '"==" in Python checks for equality of values, while "is" checks for object identity.'),
('Python', 'What are the different types of loops in Python?', 'Python supports "for" loops, "while" loops, and nested loops.'),
('Python', 'How do you comment in Python?', 'In Python, you can use "#" for single-line comments and triple quotes (""" """) for multi-line comments.'),
('MySQL', 'What is a primary key in MySQL?', 'A primary key in MySQL is a column or a set of columns that uniquely identifies each row in a table. It ensures that each row in a table is uniquely identifiable.'),
('MySQL', 'What is the difference between CHAR and VARCHAR in MySQL?', 'CHAR is a fixed-length character data type, while VARCHAR is a variable-length character data type.'),
('MySQL', 'How do you create a new database in MySQL?', 'You can create a new database in MySQL using the "CREATE DATABASE" statement followed by the database name.'),
('MySQL', 'What is a foreign key in MySQL?', 'A foreign key in MySQL is a column or a combination of columns that establishes a link between data in two tables.'),
('MySQL', 'How do you retrieve data from a MySQL database?', 'You can retrieve data from a MySQL database using the "SELECT" statement followed by the columns you want to retrieve from the table.');

SELECT * FROM questions;