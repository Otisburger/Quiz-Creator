CREATE TABLE users (
    username VARCHAR(80) PRIMARY KEY,
    password VARCHAR(80)
);

CREATE TABLE quizzes (
    quiz_name VARCHAR(80),
    username VARCHAR(80),
    PRIMARY KEY (quiz_name, username)
);

CREATE TABLE questions (
    quiz_name VARCHAR(80),
    username VARCHAR(80),
    question_name VARCHAR(80),
    question_type VARCHAR(80),
    correct_answer VARCHAR(80),
    answer1 VARCHAR(80),
    answer2 VARCHAR(80),
    answer3 VARCHAR(80),
    PRIMARY KEY (quiz_name, username, question_name)
);

CREATE TABLE mail (
    sender VARCHAR(80),
    receiver VARCHAR(80),
    quiz_name VARCHAR(80),
    PRIMARY KEY (sender, receiver, quiz_name)
);
