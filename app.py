from flask import Flask
from flask import request
from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

app.config['SQLALCHEMY_DATABASE_URI']=os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SECRET_KEY']=os.getenv("SECRET_KEY")

db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = 'users'
	username = db.Column(db.String(80), primary_key = True)
	password = db.Column(db.String(80))

class Quiz(db.Model):
	__tablename__ = 'quizzes'
	quiz_name = db.Column(db.String(80), primary_key = True)
	username = db.Column(db.String(80), primary_key = True)

class Question(db.Model):
	__tablename__ = 'questions'
	quiz_name = db.Column(db.String(80), primary_key = True)
	username = db.Column(db.String(80), primary_key = True)
	question_name = db.Column(db.String(80), primary_key = True)
	question_type = db.Column(db.String(80))
	correct_answer = db.Column(db.String(80))
	answer1 = db.Column(db.String(80))
	answer2 = db.Column(db.String(80))
	answer3 = db.Column(db.String(80))

@app.route('/login',  methods=['GET', 'POST'])
def login():
	# displays the menu screen if the userid and password are valid
	try:
		data = request.get_json()
		username = data.get('username',None)
		password = data.get('password',None)
		if(isValid(username, password)):
			session['username'] = username
			return {'status':'ok'}
		else:
			return {'status':'error','message':'Username and password do not match.'}
	except:
		return {'status':'error','message':'Something went wrong.'}

@app.route('/createUser',  methods=['GET', 'POST'])
def createUser():
	# adds another user to the database
	data = request.get_json()
	username = data.get('username')
	password = data.get('password')
	if (username != '' and password != ''):
		try:
			newUser = User(username=username, password=password)
			db.session.add(newUser)
			db.session.commit()
			return {'status':'ok'}
		except:
			return {'status':'error','message':'A user with that username already exists.'}
	else:
		return {'status':'error','message':'One of the fields are blank.'}

@app.route('/createQuiz',  methods=['GET', 'POST'])
def createQuiz():
	# adds another user to the database
	data = request.get_json()
	name = data.get('name')
	if (name != ''):
		try:
			newQuiz = Quiz(quiz_name=name, username=session.get('username'))
			db.session.add(newQuiz)
			db.session.commit()
			session['quiz'] = name
			return {'status':'ok'}
		except:
			return {'status':'error','message':'You have already created a quiz with that name.'}
	else:
		return {'status':'error','message':'One of the fields are blank.'}

@app.route('/editQuiz',  methods=['GET', 'POST', 'DELETE'])
def editQuiz():
	if(request.method == 'GET'):
		questions = Question.query.filter_by(username=session['username']).filter_by(quiz_name=session['quiz'])
		question_dicts = [
			{
				'name': question.question_name
			}
			for question in questions
		]
		return {'names': question_dicts}
	elif(request.method == 'POST'):
		try:
			data = request.get_json()
			session['question'] = data.get('name')
			return {'status':'ok'}
		except:
			return {'status': 'error', 'message': 'Something went wrong.'}
	elif(request.method == 'DELETE'):
		try:
			questions = Question.query.filter_by(username=session['username'], quiz_name=session['quiz']).all()
			for question in questions:
				db.session.delete(question)
			db.session.commit()
			quiz = Quiz.query.filter_by(username=session['username'], quiz_name=session['quiz']).one()
			db.session.delete(quiz)
			db.session.commit()
			return {'status':'ok'}
		except:
			return {'status': 'error', 'message': 'Something went wrong.'}
	else:
		return {'status':'error','message':'Invalid request method.'}

@app.route('/chooseQuiz',  methods=['GET', 'POST'])
def chooseQuiz():
	if(request.method == 'GET'):
		quizzes = Quiz.query.filter_by(username=session.get('username'))
		quiz_dicts = [
			{
				'name': quiz.quiz_name
			}
			for quiz in quizzes
		]
		return {'quizzes': quiz_dicts}
	elif(request.method == 'POST'):
		try:
			data = request.get_json()
			session['quiz'] = data.get('name')
			return {'status':'ok'}
		except:
			return {'status': 'error', 'message': 'Something went wrong.'}
	else:
		return {'status':'error','message':'Invalid request method.'}

@app.route('/addQuestion',  methods=['GET', 'POST'])
def addQuestion():
	# adds question to the database
	data = request.get_json()
	if (data.get('questionType') == 'Multiple Choice'):
		if(data.get('name') != '' and data.get('correctAnswer') != '' and data.get('incorrectAnswer') != '' and data.get('incorrectAnswer2') != '' and data.get('incorrectAnswer3') != ''):
			try:
				newQuestion = Question(quiz_name = session.get('quiz'), username = session.get('username'), question_name = data.get('name'), question_type = data.get('questionType'), correct_answer = data.get('correctAnswer'), answer1 = data.get('incorrectAnswer'), answer2 = data.get('incorrectAnswer2'), answer3 = data.get('incorrectAnswer3'))
				db.session.add(newQuestion)
				db.session.commit()
				return {'status':'ok'}
			except Exception as e:
				print('error', e)
				return {'status':'error','message':'You have already added a question with that name.'}
		else:
			return {'status':'error','message':'One of the fields are blank.'}
	elif (data.get('questionType') == 'True or False'):
		if(data.get('name') != '' and data.get('truthValue') != ''):
			try:
				newQuestion = Question(quiz_name = session.get('quiz'), username = session.get('username'), question_name = data.get('name'), question_type = data.get('questionType'), correct_answer = data.get('truthValue'), answer1 = '', answer2 = '', answer3 = '')
				db.session.add(newQuestion)
				db.session.commit()
				return {'status':'ok'}
			except:
				return {'status':'error','message':'You have already added a question with that name.'}
		else:
			return {'status':'error','message':'One of the fields are blank.'}
	elif (data.get('questionType') == 'Short Answer'):
		if(data.get('name') != '' and data.get('correctAnswer') != ''):
			try:
				newQuestion = Question(quiz_name = session['quiz'], username = session['username'], question_name = data.get('name'), question_type = data.get('questionType'), correct_answer = data.get('correctAnswer'), answer1 = '', answer2 = '', answer3 = '')
				db.session.add(newQuestion)
				db.session.commit()
				return {'status':'ok'}
			except:
				return {'status':'error','message':'You have already added a question with that name.'}
		else:
			return {'status':'error','message':'One of the fields are blank.'}
	else:
		return {'status':'error','message':'One of the fields are blank.'}

@app.route('/editQuestion',  methods=['GET', 'POST', 'DELETE'])
def editQuestion():
	if(request.method == 'GET'):
		question = Question.query.filter_by(username=session['username'], quiz_name=session['quiz'], question_name=session['question']).one()
		response = {'name': question.question_name, 'questionType': question.question_type, 'correctAnswer': question.correct_answer, 'incorrectAnswer': question.answer1, 'incorrectAnswer2': question.answer2, 'incorrectAnswer3': question.answer3}
		return response
	elif(request.method == 'POST'):
		data = request.get_json()
		if (data.get('questionType') == 'Multiple Choice'):
			if(data.get('name') != '' and data.get('correctAnswer') != '' and data.get('incorrectAnswer') != '' and data.get('incorrectAnswer2') != '' and data.get('incorrectAnswer3') != ''):
				try:
					db.session.query(Question).filter(Question.username == session['username']).filter(Question.quiz_name == session['quiz']).filter(Question.question_name == session['question']).update({'question_name': data.get('name'), 'question_type': data.get('questionType'), 'correct_answer': data.get('correctAnswer'), 'answer1': data.get('incorrectAnswer'), 'answer2': data.get('incorrectAnswer2'), 'answer3': data.get('incorrectAnswer3')}, synchronize_session=False)
					db.session.commit()
					return {'status':'ok'}
				except:
					return {'status':'error','message':'You have already added a question with that name.'}
			else:
				return {'status':'error','message':'One of the fields are blank.'}
		elif (data.get('questionType') == 'True or False'):
			if(data.get('name') != '' and data.get('truthValue') != ''):
				try:
					db.session.query(Question).filter(Question.username == session['username']).filter(Question.quiz_name == session['quiz']).filter(Question.question_name == session['question']).update({'question_name': data.get('name'), 'question_type': data.get('questionType'), 'correct_answer': data.get('truthValue')}, synchronize_session=False)
					db.session.commit()
					return {'status':'ok'}
				except:
					return {'status':'error','message':'You have already added a question with that name.'}
			else:
				return {'status':'error','message':'One of the fields are blank.'}
		elif (data.get('questionType') == 'Short Answer'):
			if(data.get('name') != '' and data.get('correctAnswer') != ''):
				try:
					db.session.query(Question).filter(Question.username == session['username']).filter(Question.quiz_name == session['quiz']).filter(Question.question_name == session['question']).update({'question_name': data.get('name'), 'question_type': data.get('questionType'), 'correct_answer': data.get('correctAnswer')}, synchronize_session=False)
					db.session.commit()
					return {'status':'ok'}
				except:
					return {'status':'error','message':'You have already added a question with that name.'}
			else:
				return {'status':'error','message':'One of the fields are blank.'}
		else:
			return {'status':'error','message':'One of the fields are blank.'}
	elif(request.method == 'DELETE'):
		try:
			question = Question.query.filter_by(username=session['username'], quiz_name=session['quiz'], question_name=session['question']).one()
			db.session.delete(question)
			db.session.commit()
			return {'status':'ok'}
		except:
			return {'status': 'error', 'message': 'Something went wrong.'}
	else:
		return {'status':'error','message':'Invalid request method.'}

@app.route('/takeQuiz',  methods=['GET', 'POST'])
def takeQuiz():
	if(request.method == 'GET'):
		quizzes = Quiz.query.filter_by(username=session.get('username'))
		quiz_dicts = [
			{
				'name': quiz.quiz_name
			}
			for quiz in quizzes
		]
		return {'quizzes': quiz_dicts}
	elif(request.method == 'POST'):
		try:
			data = request.get_json()
			session['quiz'] = data.get('name')
			session['index'] = 0
			session['points'] = 0
			session['total'] = 0
			questions = Question.query.filter_by(username=session.get('username'), quiz_name = session.get('quiz')).all()
			questionList = []
			for question in questions:
				questionList.append({
					'username': question.username,
					'quiz_name': question.quiz_name,
					'question_name': question.question_name,
					'question_type': question.question_type,
					'correct_answer': question.correct_answer,
					'answer1': question.answer1,
					'answer2': question.answer2,
					'answer3': question.answer3
				})
			session['questions'] = questionList
			return {'status':'ok'}
		except:
			return {'status': 'error', 'message': 'Something went wrong.'}
	else:
		return {'status':'error','message':'Invalid request method.'}

@app.route('/answering',  methods=['GET', 'POST'])
def Answering():
	if(request.method == 'GET'):
		try:
			questions = session.get('questions')
			index = session.get('index')
			if(len(questions) == index):
				return {'status': 'done'}
			else:
				return {
					'name': questions[index].get('question_name'),
					'questionType': questions[index].get('question_type'),
					'correctAnswer': questions[index].get('correct_answer'),
					'incorrectAnswer': questions[index].get('answer1'),
					'incorrectAnswer2': questions[index].get('answer2'),
					'incorrectAnswer3': questions[index].get('answer3')
				}
		except:
			return {'status': 'error', 'message': 'Something went wrong.'}
	elif(request.method == 'POST'):
		try:
			data = request.get_json()
			points = session.get('points')
			total = session.get('total')
			answer = data.get('answer')
			questions = session.get('questions')
			index = session.get('index')
			if(answer == questions[index].get('correct_answer')):
				session['points'] = points + 1
			session['total'] = total + 1
			session['index'] = session.get('index') + 1
			index = session.get('index')
			if(len(questions) == index):
				return {'status': 'done'}
			return {
				'name': questions[index].get('question_name'),
				'questionType': questions[index].get('question_type'),
				'correctAnswer': questions[index].get('correct_answer'),
				'incorrectAnswer': questions[index].get('answer1'),
				'incorrectAnswer2': questions[index].get('answer2'),
				'incorrectAnswer3': questions[index].get('answer3')
			}
		except Exception as e:
			print(e)
			return {'status': 'error', 'message': 'Something went wrong.'}
	else:
		return {'status':'error','message':'Invalid request method.'}

@app.route('/end',  methods=['GET', 'POST'])
def End():
	if(request.method == 'GET'):
		try:
			return {'points': session.get('points'), 'total': session.get('total')}
		except:
			return {'status': 'error', 'message': 'Something went wrong.'}
	else:
		return {'status':'error','message':'Invalid request method.'}

def isValid(username, password):
	if(username != None):
		user = User.query.filter_by(username=username).one()
	else:
		user = None
	if (user is not None) and (user.password == password): # returns true if the information entered matches a user in the database
		return True
	else:
		return False

if __name__ == "__main__":
	with app.app_context():
		db.create_all()
	app.run(debug=True)