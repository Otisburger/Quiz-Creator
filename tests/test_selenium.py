from app import User, Quiz, Question, Mail
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Tests logging in
def test_login_successful(driver, client, init_data):
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
    assert WebDriverWait(driver, 10).until(
        lambda d: d.current_url.endswith("/menu")
    )

def test_login_invalid_user(driver, client, init_data):
    driver.get("http://127.0.0.1:3001/")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    input_element.send_keys("pete")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    input_element.send_keys("123")
    submit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div/form/input"))
    )
    submit_btn.click()
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert alert.text == "Username and password do not match."
    alert.accept()


# Tests creating an account
def test_create_account_successful(driver, client, init_data):
    driver.get("http://127.0.0.1:3001")
    input_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "create"))
    )
    input_element.click()
    h2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[normalize-space()='Create Account']")
        )
    )
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    input_element.send_keys("pete")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    input_element.send_keys("123")
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "button"))
    )
    button.click()
    assert WebDriverWait(driver, 10).until(
        lambda d: d.current_url.endswith("/login")
    )
    assert User.query.filter_by(username='pete').first() != None

def test_create_account_already_exists(driver, client, init_data):
    driver.get("http://127.0.0.1:3001/")
    input_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "create"))
    )
    input_element.click()
    h2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[normalize-space()='Create Account']")
        )
    )
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    input_element.send_keys("bob")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    input_element.send_keys("123")
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "button"))
    )
    button.click()
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert alert.text == "A user with that username already exists."
    alert.accept()

def test_create_account_blank_user(driver, client, init_data):
    driver.get("http://127.0.0.1:3001/")
    input_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "create"))
    )
    input_element.click()
    h2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[normalize-space()='Create Account']")
        )
    )
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    input_element.send_keys("")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    input_element.send_keys("123")
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "button"))
    )
    button.click()
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert alert.text == "One of the fields are blank."
    alert.accept()

def test_create_account_blank_pass(driver, client, init_data):
    driver.get("http://127.0.0.1:3001/")
    input_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "create"))
    )
    input_element.click()
    h2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[normalize-space()='Create Account']")
        )
    )
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    input_element.send_keys("bob")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    input_element.send_keys("")
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "button"))
    )
    button.click()
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert alert.text == "One of the fields are blank."
    alert.accept()


# Tests creating a Quiz
def test_create_quiz_successful(driver, client, init_data):

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
    assert Quiz.query.filter_by(username='bob', quiz_name='About Me 3').first() != None
    assert Question.query.filter_by(username='bob', quiz_name='About Me 3', question_name = 'I have a dog.').first() != None
    assert Question.query.filter_by(username='bob', quiz_name='About Me 3', question_name = 'What is my favorite color?').first() != None
    assert Question.query.filter_by(username='bob', quiz_name='About Me 3', question_name = "What is my dog's name?").first() != None

def test_create_quiz_already_exists(driver, client, init_data):

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
    input_element.send_keys("About Me")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/form/div/input[2]"))
    )
    input_element.click()
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert alert.text == "You have already created a quiz with that name."
    alert.accept()

def test_create_quiz_blank(driver, client, init_data):

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
    input_element.send_keys("")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/form/div/input[2]"))
    )
    input_element.click()
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert alert.text == "One of the fields are blank."
    alert.accept()


# Tests editing a Quiz
def test_edit_quiz_successful(driver, client, init_data):

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
    input_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='About Me 2']"))
    )
    input_element.click()
    try:
        input_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='What is my favorite color?']"))
        )
        input_element.click()
    except:
        input_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='What is my favorite color?']"))
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
    input_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "2"))
    )
    assert Question.query.filter_by(username='bob', quiz_name='About Me 2', question_name = 'What color is my favorite?').first() != None
    assert Question.query.filter_by(username='bob', quiz_name='About Me 2', question_name = 'What is my favorite color?').first() == None
    assert WebDriverWait(driver, 10).until(
    lambda d: d.current_url.endswith("/editQuiz")
    )

def test_edit_quiz_question_already_exists(driver, client, init_data):

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
    input_element.send_keys("I have a pet dog.")
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
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert alert.text == "You have already added a question with that name."
    alert.accept()

def test_delete_question(driver, client, init_data):

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
        input_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='What is my favorite color?']"))
        )
        input_element.click()
    except:
        input_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='What is my favorite color?']"))
        )
        input_element.click()

    # Delete Question
    input_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/form/div/button"))
    )
    input_element.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "1"))
    )
    assert Question.query.filter_by(username='bob', quiz_name='About Me 2', question_name = "What is my favorite color?").first() == None
    assert WebDriverWait(driver, 10).until(
        lambda d: d.current_url.endswith("/editQuiz")
    )

def test_delete_quiz(driver, client, init_data):

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
    input_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='About Me 2']"))
    )
    input_element.click()

    # Delete Quiz
    input_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div/div/button[2]"))
    )
    input_element.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "0"))
    )
    assert Quiz.query.filter_by(username='bob', quiz_name='About Me 2').first() == None
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
    for _ in range(3):
        time.sleep(3)
        h2 = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.TAG_NAME, "h2")))
        if(h2.text.strip() == "I have a pet dog."):
            input_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "true"))
            )
            input_element.click()
        elif(h2.text.strip() == "What is my dog's name?"):
            input_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "answer"))
            )
            input_element.send_keys("Daisy")
            input_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, "submit"))
            )
            input_element.click()
        elif(h2.text.strip() == "What is my favorite color?"):
            for i in range(1, 5):
                time.sleep(3)
                btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, f"answer{i}")) 
                )
                if btn.get_attribute("value") == "green":
                    btn.click()
                    break
    assert WebDriverWait(driver, 10).until(
        lambda d: d.current_url.endswith("/end")
    )
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/p"))
    )
    assert input_element.text == 'You answered 3 out of 3 questions correctly!'


# Tests sending a Quiz
def test_send_quiz_successful(driver, client, init_data):

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
    h2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[normalize-space()='Menu']")
        )
    )
    assert Mail.query.filter_by(sender='adam', receiver='bob', quiz_name='About Me').first() != None
    assert WebDriverWait(driver, 10).until(
        lambda d: d.current_url.endswith("/menu")
    )

def test_send_quiz_wrong_user(driver, client, init_data):

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

    # Send Quiz
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='button' and text()='Send a Quiz']"))
    )
    input_element.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "send"))
    )
    input_element.send_keys("fred")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "quiz"))
    )
    input_element.send_keys("About Me")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "button"))
    )
    input_element.click()
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert alert.text == "Quiz or User not found."
    alert.accept()

def test_send_quiz_wrong_quiz(driver, client, init_data):

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

    # Send Quiz
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='button' and text()='Send a Quiz']"))
    )
    input_element.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "send"))
    )
    input_element.send_keys("adam")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "quiz"))
    )
    input_element.send_keys("Dog Quiz")
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "button"))
    )
    input_element.click()
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert alert.text == "Quiz or User not found."
    alert.accept()


# Tests inbox
def test_inbox_successful(driver, client, init_data):

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
                (By.CSS_SELECTOR, 'input[type="button"][value="Accept"][name="About Me 2"]')
            )
        )
        button.click()
    except:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'input[type="button"][value="Accept"][name="About Me 2"]')
            )
        )
        button.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "menu"))
    )
    input_element.click()
    h2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[normalize-space()='Menu']")
        )
    )
    assert WebDriverWait(driver, 10).until(
        lambda d: d.current_url.endswith("/menu")
    )
    assert Question.query.filter_by(username='adam', quiz_name='About Me 2', question_name='What is my favorite color?').first() != None
    assert Question.query.filter_by(username='adam', quiz_name='About Me 2', question_name='I have a pet dog.').first() != None
    assert Question.query.filter_by(username='adam', quiz_name='About Me 2', question_name="What is my dog's name?").first() != None
    assert Quiz.query.filter_by(username='adam', quiz_name='About Me 2').first() != None
    assert Mail.query.filter_by(sender='bob', receiver='adam', quiz_name='About Me 2').first() == None

def test_inbox_duplicate_quiz(driver, client, init_data):

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
                (By.CSS_SELECTOR, 'input[type="button"][value="Accept"][name="About Me"]')
            )
        )
        button.click()
    except:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'input[type="button"][value="Accept"][name="About Me"]')
            )
        )
        button.click()
    alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
    assert alert.text == "Quiz with that name already exists."
    alert.accept()

def test_inbox_delete(driver, client, init_data):

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
    input_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "1"))
    )
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'input[type="button"][value="Deny"][name="About Me"]')
            )
        )
        button.click()
    except:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'input[type="button"][value="Deny"][name="About Me"]')
            )
        )
        button.click()
    input_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "menu"))
    )
    input_element.click()
    h2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[normalize-space()='Menu']")
        )
    )
    assert WebDriverWait(driver, 10).until(
        lambda d: d.current_url.endswith("/menu")
    )
    assert Mail.query.filter_by(sender='bob', receiver='adam', quiz_name='About Me').first() == None