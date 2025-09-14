import {useEffect, useState} from 'react';
import axios from "axios";
import {useNavigate} from 'react-router-dom';
import './App.css';

const baseUrl = "http://127.0.0.1:5000"

export function Answering(){

	const [name, setName] = useState('');

	const [questionType, setQuestionType] = useState('Short Answer');

	const [answers, setAnswers] = useState([]);

	const [answer, setAnswer] = useState('');

	const navigate = useNavigate();

	useEffect(() => {
		const fetchData = async () => {
			try {
				const response = await axios.get(baseUrl + '/answering', { withCredentials: true });
				if(response.data['status'] === 'error'){
					alert(response.data['message']);
				}
				else if(response.data['status'] === 'done'){
					navigate('/end');
				}
				else{
					setName(response.data.name);
					setQuestionType(response.data.questionType);
					if(response.data.questionType === 'True or False'){
						setAnswers(['True', 'False']);
					}
					else{
						const shuffledAnswers = shuffle([
							response.data.correctAnswer,
							response.data.incorrectAnswer,
							response.data.incorrectAnswer2,
							response.data.incorrectAnswer3
						]);
						setAnswers(shuffledAnswers);
					}
				}
			} catch (error) {
				console.error('Error:', error);
			}
		};
		fetchData();
	}, []);

	const handleAnswer = async (event) => {
		setAnswer(event.target.value)
	}

	const handleChoice = async (event) => {
		event.preventDefault();
        try {
			var formData = { answer: event.target.value };
			const response = await axios.post(baseUrl+'/answering', formData, { withCredentials: true });
			if(response.data['status'] === 'error'){
				alert(response.data['message']);
			}
			else if(response.data['status'] === 'done'){
				navigate('/end');
			}
			else{
				setName(response.data.name);
				setQuestionType(response.data.questionType);
				if(response.data.questionType === 'True or False'){
					setAnswers(['True', 'False']);
				}
				else{
					const shuffledAnswers = shuffle([
						response.data.correctAnswer,
						response.data.incorrectAnswer,
						response.data.incorrectAnswer2,
						response.data.incorrectAnswer3
					]);
					setAnswers(shuffledAnswers);
				}
			}
        }
		catch (error) {
        	console.error('Error:', error);
		}
	}

	const handleSubmit = async (event) => {
		event.preventDefault();
        try {
			var formData = { answer: answer };
			const response = await axios.post(baseUrl+'/answering', formData, { withCredentials: true });
			if(response.data['status'] === 'error'){
				alert(response.data['message']);
			}
			else if(response.data['status'] === 'done'){
				navigate('/end');
			}
			else{
				setName(response.data.name);
				setQuestionType(response.data.questionType);
				if(response.data.questionType === 'True or False'){
					setAnswers(['True', 'False']);
				}
				else{
					const shuffledAnswers = shuffle([
						response.data.correctAnswer,
						response.data.incorrectAnswer,
						response.data.incorrectAnswer2,
						response.data.incorrectAnswer3
					]);
					setAnswers(shuffledAnswers);
				}
			}
        }
		catch (error) {
        	console.error('Error:', error);
		}
    };

	function shuffle(array) {
		let currentIndex = array.length;
		
		// While there remain elements to shuffle...
		while (currentIndex != 0) {
			// Pick a remaining element...
			let randomIndex = Math.floor(Math.random() * currentIndex);
			currentIndex--;
			
			// And swap it with the current element.
			[array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
		}
		return array
	}

	return (
    <div className="App">
		<h1>Quiz!</h1>
			<h2>{name}</h2>
				<div className="main">
					<>
				    {questionType === "Multiple Choice" && (
						<>
						<input 
							type="button"
							name="answer1"
							id="answer1"
							onClick={handleChoice}
							value = {answers[0]}
						/>
						<input 
							type="button"
							name="answer2"
							id="answer2"
							onClick={handleChoice}
							value = {answers[1]}
						/>
						<input 
							type="button"
							name="answer3"
							id="answer3"
							onClick={handleChoice}
							value = {answers[2]}
						/>
						<input 
							type="button"
							name="answer4"
							id="answer4"
							onClick={handleChoice}
							value = {answers[3]}
						/>
						</>
					)}
					{questionType === "True or False" && (
						<>
						<input 
							type="button"
							name="true"
							id="true"
							onClick={handleChoice}
							value = {'True'}
						/>
						<input 
							type="button"
							name="false"
							id="false"
							onClick={handleChoice}
							value = {'False'}
						/>
						</>
					)}
					{questionType === "Short Answer" && (
						<>
						<input 
							type="text"
							name="answer"
							id="answer"
							onChange={handleAnswer}
						/>
						<input
							type="button"
							name="submit"
							id="submit"
							onClick={handleSubmit}
							value="Submit"
							className="submit"
						/>
						</>
					)}
					</>
				</div>
    </div>
	);
}