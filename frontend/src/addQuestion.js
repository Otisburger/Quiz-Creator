import {useEffect, useState} from 'react';
import axios from "axios";
import {useNavigate} from 'react-router-dom';
import './App.css';

const baseUrl = "http://localhost:5000"

export function AddQuestion(){

	const [name, setName] = useState('');

	const [questionType, setQuestionType] = useState('Multiple Choice');

	const [correctAnswer, setCorrectAnswer] = useState('');

	const [incorrectAnswer, setIncorrectAnswer] = useState('');

	const [incorrectAnswer2, setIncorrectAnswer2] = useState('');

	const [incorrectAnswer3, setIncorrectAnswer3] = useState('');

	const [truthValue, setTruthValue] = useState('True');

	const navigate = useNavigate();

	const handleName = (event) => {
		setName(event.target.value);
	};

	const handleChange = (event) => {
		setQuestionType(event.target.value);
	};

	const handleCorrectAnswer = (event) => {
		setCorrectAnswer(event.target.value);
	};

	const handleIncorrectAnswer = (event) => {
		setIncorrectAnswer(event.target.value);
	};

	const handleIncorrectAnswer2 = (event) => {
		setIncorrectAnswer2(event.target.value);
	};

	const handleIncorrectAnswer3 = (event) => {
		setIncorrectAnswer3(event.target.value);
	};

	const handleTruthValue = (event) => {
		setTruthValue(event.target.value);
	};

	const handleSubmit = async (event) => {
		event.preventDefault();
        try {
			if(questionType === 'Multiple Choice'){
				var formData = { name: name, questionType: questionType, correctAnswer: correctAnswer, incorrectAnswer: incorrectAnswer, incorrectAnswer2: incorrectAnswer2, incorrectAnswer3: incorrectAnswer3 };
			}
			else if(questionType === 'True or False'){
				var formData = { name: name, questionType: questionType, truthValue: truthValue }
			}
			else{
				var formData = { name: name, questionType: questionType, correctAnswer: correctAnswer }
			}
        	const response = await axios.post(baseUrl+'/addQuestion', formData, { withCredentials: true });
			if(response.data['status'] === 'error'){
				alert(response.data['message']);
			}
			else{
				navigate('/editQuiz')
			}
        }
		catch (error) {
        	console.error('Error:', error);
		}
    };

	return (
  <div className="App">
    <h1>Quiz!</h1>
    <h2>Add a Question</h2>
    <form onSubmit={handleSubmit}>
      <div className="main">
        <>
        <label htmlFor="name">Question</label>
        <input 
          type="text"
          name="name"
          id="name"
          onChange={handleName}
        />
        <label>
          Pick a Question Type
          <select name="selectedType" onChange={handleChange}>
            <option value="Multiple Choice">Multiple Choice</option>
            <option value="True or False">True or False</option>
            <option value="Short Answer">Short Answer</option>
          </select>
        </label>

        {questionType === "Multiple Choice" && (
          <>
            <label htmlFor="correctAnswer">Correct Answer</label>
            <input 
              type="text"
              name="correctAnswer"
              id="correctAnswer"
              onChange={handleCorrectAnswer}
            />
            <label htmlFor="incorrectAnswer">Incorrect Answer</label>
            <input 
              type="text"
              name="incorrectAnswer"
              id="incorrectAnswer"
              onChange={handleIncorrectAnswer}
            />
            <label htmlFor="incorrectAnswer2">Incorrect Answer</label>
            <input 
              type="text"
              name="incorrectAnswer2"
              id="incorrectAnswer2"
              onChange={handleIncorrectAnswer2}
            />
            <label htmlFor="incorrectAnswer3">Incorrect Answer</label>
            <input 
              type="text"
              name="incorrectAnswer3"
              id="incorrectAnswer3"
              onChange={handleIncorrectAnswer3}
            />
          </>
        )}

        {questionType === "True or False" && (
          <>
          <label>
            True or False:
            <select name="trueOrFalse" onChange={handleTruthValue}>
              <option value="True">True</option>
              <option value="False">False</option>
            </select>
          </label>
          </>
        )}

        {questionType === "Short Answer" && (
          <>
            <label htmlFor="correctAnswer">Correct Answer</label>
            <input 
              type="text"
              name="correctAnswer"
              id="correctAnswer"
              onChange={handleCorrectAnswer}
            />
          </>
        )}
        <input
          id = "button"
          type="submit"
          name="submit"
          value="Submit"
          className="submit"
        />
        </>
      </div>
    </form>
  </div>
);
}