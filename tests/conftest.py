import os
import pytest
from app import create_app, db, User, Quiz, Question, Mail
import bcrypt

@pytest.fixture(scope="session")
def app():
    app = create_app(True)
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def init_data(app):
    with app.app_context():
        db.session.query(Question).delete()
        db.session.query(Quiz).delete()
        db.session.query(User).delete()
        db.session.query(Mail).delete()
        db.session.commit()

        hashed_pw = bcrypt.hashpw("123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = User(username="bob", password=hashed_pw)
        db.session.add(user)

        hashed_pw = bcrypt.hashpw("1234".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = User(username="adam", password=hashed_pw)
        db.session.add(user)

        quiz = Quiz(quiz_name="About Me", username="bob")
        db.session.add(quiz)

        quiz = Quiz(quiz_name="About Me", username="adam")
        db.session.add(quiz)

        quiz = Quiz(quiz_name="About Me 2", username="bob")
        db.session.add(quiz)

        question = Question(
            quiz_name="About Me",
            username="bob",
            question_name="What is my favorite color?",
            question_type="Multiple Choice",
            correct_answer="green",
            answer1="blue",
            answer2="red",
            answer3="orange"
        )
        db.session.add(question)

        question = Question(
            quiz_name="About Me",
            username="bob",
            question_name="I have a pet dog.",
            question_type="True or False",
            correct_answer="True",
            answer1="",
            answer2="",
            answer3=""
        )
        db.session.add(question)

        question = Question(
            quiz_name="About Me",
            username="bob",
            question_name="What is my dog's name?",
            question_type="Short Answer",
            correct_answer="Daisy",
            answer1="",
            answer2="",
            answer3=""
        )
        db.session.add(question)

        question = Question(
            quiz_name="About Me",
            username="adam",
            question_name="What is my favorite color?",
            question_type="Multiple Choice",
            correct_answer="green",
            answer1="blue",
            answer2="red",
            answer3="orange"
        )
        db.session.add(question)

        question = Question(
            quiz_name="About Me",
            username="adam",
            question_name="I have a pet dog.",
            question_type="True or False",
            correct_answer="True",
            answer1="",
            answer2="",
            answer3=""
        )
        db.session.add(question)

        question = Question(
            quiz_name="About Me",
            username="adam",
            question_name="What is my dog's name?",
            question_type="Short Answer",
            correct_answer="Daisy",
            answer1="",
            answer2="",
            answer3=""
        )
        db.session.add(question)

        question = Question(
            quiz_name="About Me 2",
            username="bob",
            question_name="What is my favorite color?",
            question_type="Multiple Choice",
            correct_answer="green",
            answer1="blue",
            answer2="red",
            answer3="orange"
        )
        db.session.add(question)

        question = Question(
            quiz_name="About Me 2",
            username="bob",
            question_name="I have a pet dog.",
            question_type="True or False",
            correct_answer="True",
            answer1="",
            answer2="",
            answer3=""
        )
        db.session.add(question)

        question = Question(
            quiz_name="About Me 2",
            username="bob",
            question_name="What is my dog's name?",
            question_type="Short Answer",
            correct_answer="Daisy",
            answer1="",
            answer2="",
            answer3=""
        )
        db.session.add(question)

        mail = Mail(
            sender="bob",
            receiver="adam",
            quiz_name="About Me",
        )
        db.session.add(mail)

        mail = Mail(
            sender="bob",
            receiver="adam",
            quiz_name="About Me 2",
        )
        db.session.add(mail)

        db.session.commit()
        yield

        try:
            db.session.query(Question).delete()
            db.session.query(Quiz).delete()
            db.session.query(User).delete()
            db.session.query(Mail).delete()
            db.session.commit()
        except Exception:
            db.session.rollback()