CREATE TABLE users (
    username VARCHAR(80) PRIMARY KEY,
    password VARCHAR(80)
);

CREATE TABLE quizzes (
    quiz_name VARCHAR(80),
    username VARCHAR(80),
    PRIMARY KEY (quiz_name, username),
    FOREIGN KEY (username) REFERENCES users(username)
        ON DELETE CASCADE ON UPDATE CASCADE
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
    PRIMARY KEY (quiz_name, username, question_name),
    FOREIGN KEY (quiz_name, username) REFERENCES quizzes(quiz_name, username)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE mail (
    sender VARCHAR(80),
    receiver VARCHAR(80),
    quiz_name VARCHAR(80),
    PRIMARY KEY (sender, receiver, quiz_name),
    FOREIGN KEY (sender) REFERENCES users(username)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (receiver) REFERENCES users(username)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (quiz_name, sender) REFERENCES quizzes(quiz_name, username)
        ON DELETE CASCADE ON UPDATE CASCADE
);
