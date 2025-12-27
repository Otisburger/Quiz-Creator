from app import User, Quiz, Question, Mail
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Tests login view
def test_login_correct_user(client, init_data):
    response = client.post("/login", json={
        "username": "bob",
        "password": '123'
    })
    data = response.get_json()
    assert data["status"] == 'ok'

def test_login_incorrect_password(client, init_data):
    response = client.post("/login", json={
        "username": "bob",
        "password": '1234'
    })
    data = response.get_json()
    assert data["status"] == 'error'
    assert data["message"] == 'Username and password do not match.'

def test_login_incorrect_user(client, init_data):
    response = client.post("/login", json={
        "username": "tim",
        "password": '123'
    })
    data = response.get_json()
    assert data["status"] == 'error'
    assert data["message"] == 'Something went wrong.'


# Tests createUser view
def test_createUser_successful(client, init_data):
    response = client.post("/createUser", json={
        "username": "tim",
        "password": '123'
    })
    data = response.get_json()
    assert data["status"] == 'ok'
    assert User.query.filter_by(username='tim').first() != None

def test_createUser_already_exists(client, init_data):
    response = client.post("/createUser", json={
        "username": "bob",
        "password": '123'
    })
    data = response.get_json()
    assert data["status"] == 'error'
    assert data["message"] == 'A user with that username already exists.'

def test_createUser_blank_user(client, init_data):
    response = client.post("/createUser", json={
        "username": "",
        "password": '123'
    })
    data = response.get_json()
    assert data["status"] == 'error'
    assert data["message"] == 'One of the fields are blank.'

def test_createUser_blank_password(client, init_data):
    response = client.post("/createUser", json={
        "username": "tim",
        "password": ''
    })
    data = response.get_json()
    assert data["status"] == 'error'
    assert data["message"] == 'One of the fields are blank.'


# Tests createQuiz view
def test_createQuiz_successful(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
    response = client.post("/createQuiz", json={
        "name": "Dog Quiz"
    })
    data = response.get_json()
    assert data["status"] == 'ok'
    assert Quiz.query.filter_by(username='bob', quiz_name='Dog Quiz').first() != None
    with client.session_transaction() as sess:
        assert sess['quiz'] == "Dog Quiz"

def test_createQuiz_already_exists(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
    response = client.post("/createQuiz", json={
        "name": "About Me"
    })
    data = response.get_json()
    assert data["status"] == 'error'
    assert data["message"] == 'You have already created a quiz with that name.'

def test_createQuiz_blank(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
    response = client.post("/createQuiz", json={
        "name": ""
    })
    data = response.get_json()
    assert data["status"] == 'error'
    assert data["message"] == 'One of the fields are blank.'


# Tests editQuiz view
def test_editQuiz_get(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
    response = client.get("/editQuiz")
    data = response.get_json()
    assert {'name': "I have a pet dog."} in data['names']
    assert {'name': "What is my dog's name?"} in data['names']
    assert {'name': "What is my favorite color?"} in data['names']

def test_editQuiz_post(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
    response = client.post("/editQuiz", json={
        "name": "What is my favorite color?"
    })
    data = response.get_json()
    assert data["status"] == 'ok'
    with client.session_transaction() as sess:
        assert sess['question'] == "What is my favorite color?"

def test_editQuiz_delete(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
    response = client.delete("/editQuiz")
    data = response.get_json()
    assert data["status"] == 'ok'
    with client.session_transaction() as sess:
        assert Question.query.filter_by(username=sess['username'], quiz_name=sess['quiz']).all() == []
        assert Quiz.query.filter_by(username=sess['username'], quiz_name=sess['quiz']).first() == None


# Tests chooseQuiz view
def test_chooseQuiz_get(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
    response = client.get("/chooseQuiz")
    data = response.get_json()
    assert {'name': "About Me"} in data['quizzes']

def test_chooseQuiz_post(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
    response = client.post("/chooseQuiz", json={
        "name": "About Me"
    })
    data = response.get_json()
    assert data.get('status') == 'ok'
    with client.session_transaction() as sess:
        assert sess['quiz'] == 'About Me'


# Tests addQuestion view
def test_addQuestion_missing_value(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
    response = client.post("/addQuestion", json={
        "questionType": "Multiple Choice",
        'name': '',
        'correctAnswer': 'correct',
        'incorrectAnswer': 'wrong',
        'incorrectAnswer2': 'wrong',
        'incorrectAnswer3': 'wrong'
    })
    data = response.get_json()
    assert data.get('status') == 'error'
    assert data.get('message') == 'One of the fields are blank.'

def test_addQuestion_duplicate(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
    response = client.post("/addQuestion", json={
        "questionType": "Multiple Choice",
        'name': 'What is my favorite color?',
        'correctAnswer': 'correct',
        'incorrectAnswer': 'wrong',
        'incorrectAnswer2': 'wrong',
        'incorrectAnswer3': 'wrong'
    })
    data = response.get_json()
    assert data.get('status') == 'error'
    assert data.get('message') == 'You have already added a question with that name.'

def test_addQuestion_multiple_choice_successful(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
    response = client.post("/addQuestion", json={
        "questionType": "Multiple Choice",
        'name': 'new',
        'correctAnswer': 'correct',
        'incorrectAnswer': 'wrong',
        'incorrectAnswer2': 'wrong',
        'incorrectAnswer3': 'wrong'
    })
    data = response.get_json()
    assert data.get('status') == 'ok'
    with client.session_transaction() as sess:
        assert Question.query.filter_by(username=sess['username'], quiz_name=sess['quiz'], question_name = 'new').first() != None

def test_addQuestion_true_false_successful(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
    response = client.post("/addQuestion", json={
        "questionType": "True or False",
        'name': 'new',
        'truthValue': 'True',
    })
    data = response.get_json()
    assert data.get('status') == 'ok'
    with client.session_transaction() as sess:
        assert Question.query.filter_by(username=sess['username'], quiz_name=sess['quiz'], question_name = 'new').first() != None

def test_addQuestion_short_answer_successful(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
    response = client.post("/addQuestion", json={
        "questionType": "Short Answer",
        'name': 'new',
        'correctAnswer': 'correct',
    })
    data = response.get_json()
    assert data.get('status') == 'ok'
    with client.session_transaction() as sess:
        assert Question.query.filter_by(username=sess['username'], quiz_name=sess['quiz'], question_name = 'new').first() != None


# Tests editQuestion view
def test_editQuestion_get(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
        sess['question'] = 'What is my favorite color?'
    response = client.get("/editQuestion")
    data = response.get_json()
    assert data.get('name') == 'What is my favorite color?'
    assert data.get('questionType') == 'Multiple Choice'
    assert data.get('correctAnswer') == 'green'
    assert data.get('incorrectAnswer') == 'blue'
    assert data.get('incorrectAnswer2') == 'red'
    assert data.get('incorrectAnswer3') == 'orange'

def test_editQuestion_delete(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
        sess['question'] = 'What is my favorite color?'
    response = client.delete("/editQuestion")
    data = response.get_json()
    assert data.get('status') == 'ok'
    assert Question.query.filter_by(username='bob', quiz_name='About Me', question_name='What is my favorite color?').first() == None

def test_editQuestion_missing_value(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
        sess['question'] = 'What is my favorite color?'
    response = client.post("/editQuestion", json={
        'name': '',
        "questionType": "Multiple Choice",
        'correctAnswer': 'correct',
        'incorrectAnswer': 'wrong',
        'incorrectAnswer2': 'wrong',
        'incorrectAnswer3': 'wrong'
    })
    data = response.get_json()
    assert data.get('status') == 'error'
    assert data.get('message') == 'One of the fields are blank.'

def test_editQuestion_duplicate(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
        sess['question'] = 'What is my favorite color?'
    response = client.post("/editQuestion", json={
        'name': "What is my dog's name?",
        "questionType": "Multiple Choice",
        'correctAnswer': 'correct',
        'incorrectAnswer': 'wrong',
        'incorrectAnswer2': 'wrong',
        'incorrectAnswer3': 'wrong'
    })
    data = response.get_json()
    assert data.get('status') == 'error'
    assert data.get('message') == 'You have already added a question with that name.'

def test_editQuestion_multiple_choice_successful(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
        sess['question'] = 'What is my favorite color?'
    response = client.post("/editQuestion", json={
        'name': "new",
        "questionType": "Multiple Choice",
        'correctAnswer': 'correct',
        'incorrectAnswer': 'wrong',
        'incorrectAnswer2': 'wrong',
        'incorrectAnswer3': 'wrong'
    })
    data = response.get_json()
    assert data.get('status') == 'ok'
    assert Question.query.filter_by(username='bob', quiz_name='About Me', question_name='new').one().question_type == "Multiple Choice"
    assert Question.query.filter_by(username='bob', quiz_name='About Me', question_name='new').one().correct_answer == "correct"
    assert Question.query.filter_by(username='bob', quiz_name='About Me', question_name='new').one().answer1 == "wrong"
    assert Question.query.filter_by(username='bob', quiz_name='About Me', question_name='new').one().answer2 == "wrong"
    assert Question.query.filter_by(username='bob', quiz_name='About Me', question_name='new').one().answer3 == "wrong"

def test_editQuestion_true_false_successful(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
        sess['question'] = 'What is my favorite color?'
    response = client.post("/editQuestion", json={
        'name': "new",
        "questionType": "True or False",
        'truthValue': 'True'
    })
    data = response.get_json()
    assert data.get('status') == 'ok'
    assert Question.query.filter_by(username='bob', quiz_name='About Me', question_name='new').one().question_type == "True or False"
    assert Question.query.filter_by(username='bob', quiz_name='About Me', question_name='new').one().correct_answer == "True"

def test_editQuestion_short_answer_successful(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
        sess['question'] = 'What is my favorite color?'
    response = client.post("/editQuestion", json={
        'name': "new",
        "questionType": "Short Answer",
        'correctAnswer': 'correct'
    })
    data = response.get_json()
    assert data.get('status') == 'ok'
    assert Question.query.filter_by(username='bob', quiz_name='About Me', question_name='new').one().question_type == "Short Answer"
    assert Question.query.filter_by(username='bob', quiz_name='About Me', question_name='new').one().correct_answer == "correct"


# Tests takeQuiz view
def test_takeQuiz_get(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
    response = client.get("/takeQuiz")
    data = response.get_json()
    assert {'name': "About Me"} in data['quizzes']

def test_takeQuiz_post(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
    response = client.post("/takeQuiz", json={
        "name": "About Me"
    })
    data = response.get_json()
    assert data.get('status') == 'ok'
    with client.session_transaction() as sess:
        assert sess['quiz'] == 'About Me'
        assert sess['index'] == 0
        assert sess['points'] == 0
        assert sess['total'] == 0
        assert {'username': 'bob',
					'quiz_name': 'About Me',
					'question_name': 'What is my favorite color?',
					'question_type': 'Multiple Choice',
					'correct_answer': 'green',
					'answer1': 'blue',
					'answer2': 'red',
					'answer3': 'orange'
                } in sess['questions']
        assert {'username': 'bob',
					'quiz_name': 'About Me',
					'question_name': 'I have a pet dog.',
					'question_type': 'True or False',
					'correct_answer': 'True',
					'answer1': '',
					'answer2': '',
					'answer3': ''
                } in sess['questions']
        assert {'username': 'bob',
					'quiz_name': 'About Me',
					'question_name': "What is my dog's name?",
					'question_type': 'Short Answer',
					'correct_answer': 'Daisy',
					'answer1': '',
					'answer2': '',
					'answer3': ''
                } in sess['questions']


# Tests answering view
def test_answering_done(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
        sess['index'] = 3
        sess['points'] = 3
        sess['total'] = 3
        sess['questions'] = [{'username': 'bob',
			'quiz_name': 'About Me',
			'question_name': 'What is my favorite color?',
			'question_type': 'Multiple Choice',
			'correct_answer': 'green',
			'answer1': 'blue',
			'answer2': 'red',
			'answer3': 'orange'
        },
        {'username': 'bob',
            'quiz_name': 'About Me',
			'question_name': 'I have a pet dog.',
			'question_type': 'True or False',
			'correct_answer': 'True',
			'answer1': '',
			'answer2': '',
			'answer3': ''
        },
        {'username': 'bob',
			'quiz_name': 'About Me',
			'question_name': "What is my dog's name?",
			'question_type': 'Short Answer',
			'correct_answer': 'Daisy',
			'answer1': '',
			'answer2': '',
			'answer3': ''
        }]
    response = client.get("/answering")
    data = response.get_json()
    assert data.get('status') == 'done'

def test_answering_get(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
        sess['index'] = 0
        sess['points'] = 0
        sess['total'] = 0
        sess['questions'] = [{'username': 'bob',
			'quiz_name': 'About Me',
			'question_name': 'What is my favorite color?',
			'question_type': 'Multiple Choice',
			'correct_answer': 'green',
			'answer1': 'blue',
			'answer2': 'red',
			'answer3': 'orange'
        },
        {'username': 'bob',
            'quiz_name': 'About Me',
			'question_name': 'I have a pet dog.',
			'question_type': 'True or False',
			'correct_answer': 'True',
			'answer1': '',
			'answer2': '',
			'answer3': ''
        },
        {'username': 'bob',
			'quiz_name': 'About Me',
			'question_name': "What is my dog's name?",
			'question_type': 'Short Answer',
			'correct_answer': 'Daisy',
			'answer1': '',
			'answer2': '',
			'answer3': ''
        }]
    response = client.get("/answering")
    data = response.get_json()
    assert data.get('name') == 'What is my favorite color?'
    assert data.get('questionType') == 'Multiple Choice'
    assert data.get('correctAnswer') == 'green'
    assert data.get('incorrectAnswer') == 'blue'
    assert data.get('incorrectAnswer2') == 'red'
    assert data.get('incorrectAnswer3') == 'orange'

def test_answering_post(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
        sess['index'] = 0
        sess['points'] = 0
        sess['total'] = 0
        sess['questions'] = [{'username': 'bob',
			'quiz_name': 'About Me',
			'question_name': 'What is my favorite color?',
			'question_type': 'Multiple Choice',
			'correct_answer': 'green',
			'answer1': 'blue',
			'answer2': 'red',
			'answer3': 'orange'
        },
        {'username': 'bob',
            'quiz_name': 'About Me',
			'question_name': 'I have a pet dog.',
			'question_type': 'True or False',
			'correct_answer': 'True',
			'answer1': '',
			'answer2': '',
			'answer3': ''
        },
        {'username': 'bob',
			'quiz_name': 'About Me',
			'question_name': "What is my dog's name?",
			'question_type': 'Short Answer',
			'correct_answer': 'Daisy',
			'answer1': '',
			'answer2': '',
			'answer3': ''
        }]
    response = client.post("/answering", json={
        "questionType": "Multiple Choice",
        'name': 'new',
        'correctAnswer': 'correct',
        'incorrectAnswer': 'wrong',
        'incorrectAnswer2': 'wrong',
        'incorrectAnswer3': 'wrong'
    })
    data = response.get_json()
    assert data.get('name') == 'I have a pet dog.'
    assert data.get('questionType') == 'True or False'
    assert data.get('correctAnswer') == 'True'
    assert data.get('incorrectAnswer') == ''
    assert data.get('incorrectAnswer2') == ''
    assert data.get('incorrectAnswer3') == ''


# Tests end view
def test_answering_get(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
        sess['quiz'] = 'About Me'
        sess['index'] = 3
        sess['points'] = 3
        sess['total'] = 3
        sess['questions'] = [{'username': 'bob',
			'quiz_name': 'About Me',
			'question_name': 'What is my favorite color?',
			'question_type': 'Multiple Choice',
			'correct_answer': 'green',
			'answer1': 'blue',
			'answer2': 'red',
			'answer3': 'orange'
        },
        {'username': 'bob',
            'quiz_name': 'About Me',
			'question_name': 'I have a pet dog.',
			'question_type': 'True or False',
			'correct_answer': 'True',
			'answer1': '',
			'answer2': '',
			'answer3': ''
        },
        {'username': 'bob',
			'quiz_name': 'About Me',
			'question_name': "What is my dog's name?",
			'question_type': 'Short Answer',
			'correct_answer': 'Daisy',
			'answer1': '',
			'answer2': '',
			'answer3': ''
        }]
    response = client.get("/end")
    data = response.get_json()
    assert data.get('points') == 3
    assert data.get('total') == 3


# Tests send view
def test_send_successful(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'adam'
    response = client.post("/send", json={
        "send": "bob",
        'quiz': 'About Me'
    })
    data = response.get_json()
    assert data.get('status') == 'ok'
    assert Mail.query.filter_by(sender='adam', receiver='bob', quiz_name='About Me').first() != None

def test_send_wrong_user(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
    response = client.post("/send", json={
        "send": "fred",
        'quiz': 'About Me'
    })
    data = response.get_json()
    assert data.get('status') == 'error'
    assert data.get('message') == 'Quiz or User not found.'

def test_send_wrong_quiz(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'bob'
    response = client.post("/send", json={
        "send": "adam",
        'quiz': 'Dog Quiz'
    })
    data = response.get_json()
    assert data.get('status') == 'error'
    assert data.get('message') == 'Quiz or User not found.'


# Tests inbox view
def test_inbox_get(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'adam'
    response = client.get("/inbox")
    data = response.get_json()
    assert {'sender': 'bob', 'receiver': 'adam','quiz_name': 'About Me'} in data.get('mail')
    assert {'sender': 'bob', 'receiver': 'adam','quiz_name': 'About Me 2'} in data.get('mail')

def test_inbox_duplicate_quiz(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'adam'
    response = client.post("/inbox", json={
        "index": 0
    })
    data = response.get_json()
    assert data.get('status') == 'error'
    assert data.get('message') == 'Quiz with that name already exists.'
    assert data.get('mail') == [{'sender': 'bob', 'receiver': 'adam', 'quiz_name': 'About Me 2'}]
    assert Mail.query.filter_by(sender='bob', receiver='adam', quiz_name='About Me').first() == None

def test_inbox_successful(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'adam'
    response = client.post("/inbox", json={
        "index": 1
    })
    data = response.get_json()
    assert data.get('status') == 'ok'
    assert data.get('mail') == [{'sender': 'bob', 'receiver': 'adam', 'quiz_name': 'About Me'}]
    assert Question.query.filter_by(username='adam', quiz_name='About Me 2', question_name='What is my favorite color?').first() != None
    assert Question.query.filter_by(username='adam', quiz_name='About Me 2', question_name='I have a pet dog.').first() != None
    assert Question.query.filter_by(username='adam', quiz_name='About Me 2', question_name="What is my dog's name?").first() != None
    assert Quiz.query.filter_by(username='adam', quiz_name='About Me 2').first() != None
    assert Mail.query.filter_by(sender='bob', receiver='adam', quiz_name='About Me 2').first() == None

def test_inbox_delete(client, init_data):
    with client.session_transaction() as sess:
        sess['username'] = 'adam'
    response = client.delete("/inbox", json={
        "index": 0
    })
    data = response.get_json()
    assert data.get('status') == 'ok'
    assert data.get('mail') == [{'sender': 'bob', 'receiver': 'adam', 'quiz_name': 'About Me 2'}]
    assert Mail.query.filter_by(sender='bob', receiver='adam', quiz_name='About Me').first() == None


# Tests creating an account
def test_create_account(driver, client, init_data):
    driver.get("http://127.0.0.1:3001/")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='button' and text()='Create Account']"))
    )
    input_element.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    input_element.send_keys("pete")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    input_element.send_keys("123")
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.submit"))
    )
    button.click()
    assert WebDriverWait(driver, 10).until(
        lambda d: d.current_url.endswith("/login")
    )


# Tests creating a Quiz
def test_create_quiz(driver, client, init_data):

    # Log in
    driver.get("http://127.0.0.1:3001/")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    input_element.send_keys("bob")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    input_element.send_keys("123")
    submit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div/form/input"))
    )
    submit_btn.click()

    # Create Quiz
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='button' and text()='Create a Quiz']"))
    )
    input_element.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "name"))
    )
    input_element.send_keys("About Me 3")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/form/div/input[2]"))
    )
    input_element.click()

    # Add Questions
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='button' and text()='Add a Question']"))
    )
    input_element.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/form/div/input[1]"))
    )
    input_element.send_keys("What is my favorite color?")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "selectedType"))
    )
    select = Select(input_element)
    select.select_by_visible_text("Multiple Choice")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "correctAnswer"))
    )
    input_element.send_keys("green")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "incorrectAnswer"))
    )
    input_element.send_keys("red")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "incorrectAnswer2"))
    )
    input_element.send_keys("blue")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "incorrectAnswer3"))
    )
    input_element.send_keys("orange")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "button"))
    )
    input_element.click()


    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='button' and text()='Add a Question']"))
    )
    input_element.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "name"))
    )
    input_element.send_keys("I have a dog.")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "selectedType"))
    )
    select = Select(input_element)
    select.select_by_visible_text("True or False")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "trueOrFalse"))
    )
    select = Select(input_element)
    select.select_by_visible_text("True")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "button"))
    )
    input_element.click()

    
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='button' and text()='Add a Question']"))
    )
    input_element.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/form/div/input[1]"))
    )
    input_element.send_keys("What is my dog's name?")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "selectedType"))
    )
    select = Select(input_element)
    select.select_by_visible_text("Short Answer")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "correctAnswer"))
    )
    input_element.send_keys("Daisy")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "button"))
    )
    input_element.click()
    assert WebDriverWait(driver, 10).until(
        lambda d: d.current_url.endswith("/editQuiz")
    )


# Tests editing a Quiz
def test_edit_quiz(driver, client, init_data):

    # Log in
    driver.get("http://127.0.0.1:3001/")
    input_element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "username"))
    )
    input_element.send_keys("bob")
    input_element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "password"))
    )
    input_element.send_keys("123")
    submit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div/form/input"))
    )
    submit_btn.click()

    # Edit Quiz
    input_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and text()='Edit a Quiz']"))
    )
    input_element.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "1"))
    )
    input_element.click()
    try:
        input_element = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "2"))
        )
        input_element.click()
    except:
        input_element = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "2"))
        )
        input_element.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "name"))
    )
    input_element.clear()
    input_element.send_keys("What color is my favorite?")
    input_element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.NAME, "selectedType"))
    )
    select = Select(input_element)
    select.select_by_visible_text("Short Answer")
    input_element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "correctAnswer"))
    )
    input_element.clear()
    input_element.send_keys("pink")
    input_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "button"))
    )
    input_element.click()
    try:
        input_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "1"))
        )
        assert input_element.get_attribute("value") == "What color is my favorite?"
    except:
        input_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "1"))
        )
        assert input_element.get_attribute("value") == "What color is my favorite?"

    # Delete Quiz
    input_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div/button[2]"))
    )
    input_element.click()
    assert WebDriverWait(driver, 10).until(
        lambda d: d.current_url.endswith("/chooseQuiz")
    )


# Tests taking a Quiz
def test_take_quiz(driver, client, init_data):

    # Log in
    driver.get("http://127.0.0.1:3001/")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    input_element.send_keys("bob")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    input_element.send_keys("123")
    submit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div/form/input"))
    )
    submit_btn.click()

    # Taking Quiz
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='button' and text()='Take a Quiz']"))
    )
    input_element.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "0"))
    )
    input_element.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "true"))
    )
    input_element.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "answer"))
    )
    input_element.send_keys("Daisy")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "submit"))
    )
    input_element.click()
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[value="green"]'))
    )
    button.click()
    assert WebDriverWait(driver, 10).until(
        lambda d: d.current_url.endswith("/end")
    )
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/p"))
    )
    assert input_element.text == 'You answered 3 out of 3 questions correctly!'


# Tests sending a Quiz
def test_send_quiz(driver, client, init_data):

    # Log in
    driver.get("http://127.0.0.1:3001/")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    input_element.send_keys("adam")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    input_element.send_keys("1234")
    submit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div/form/input"))
    )
    submit_btn.click()

    # Send Quiz
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='button' and text()='Send a Quiz']"))
    )
    input_element.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "send"))
    )
    input_element.send_keys("bob")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "quiz"))
    )
    input_element.send_keys("About Me")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "button"))
    )
    input_element.click()
    assert WebDriverWait(driver, 10).until(
        lambda d: d.current_url.endswith("/menu")
    )


# Tests inbox
def test_inbox(driver, client, init_data):

    # Log in
    driver.get("http://127.0.0.1:3001/")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    input_element.send_keys("adam")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    input_element.send_keys("1234")
    submit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div/form/input"))
    )
    submit_btn.click()

    # Open inbox
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='button' and text()='Inbox']"))
    )
    input_element.click()
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'input[type="button"][value="Deny"][name="0"]')
            )
        )
        button.click()
    except:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'input[type="button"][value="Deny"][name="0"]')
            )
        )
        button.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "menu"))
    )
    input_element.click()
    assert WebDriverWait(driver, 10).until(
        lambda d: d.current_url.endswith("/menu")
    )