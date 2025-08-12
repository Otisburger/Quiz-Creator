import {useEffect, useState} from 'react';
import axios from "axios";
import {useNavigate} from 'react-router-dom';
import './App.css';

const baseUrl = "http://localhost:5000"

export function EditQuiz(){

	const [questions, setQuestions] = useState([]);

	const navigate = useNavigate();

	useEffect(() => {
		const fetchData = async () => {
			try {
				const response = await axios.get(baseUrl + '/editQuiz', { withCredentials: true });
				setQuestions(response.data.names);
			} catch (error) {
				console.error('Error:', error);
			}
		};
		fetchData();
	}, []);

	const handleClick = async (event) => {
		event.preventDefault();
        const formData = { name: event.target.value };
        try {
        	const response = await axios.post(baseUrl+'/editQuiz', formData, { withCredentials: true });
			if(response.data['status'] === 'error'){
				alert(response.data['message']);
			}
			else{
				navigate('/editQuestion')
			}
        }
		catch (error) {
        	console.error('Error:', error);
		}
	};

	const handleRedirect = async () => {
		navigate('/addQuestion')
	};

	const handleDelete = async () => {
		const response = await axios.delete(baseUrl+'/editQuiz', { withCredentials: true });
		if(response.data['status'] === 'error'){
			alert(response.data['message']);
		}
		else{
			navigate('/chooseQuiz')
		}
	};

	const menuRedirect = async () => {
		navigate('/menu')
	};

	return (
    <div className="App">
		<h1>Quiz!</h1>
		<div className = "main">
			<h2>Choose a Question to Edit</h2>
				{questions.map((question, index) => (
					<input
						id={index}
						type="button"
						name="submit"
						value={question['name']}
						className="submit"
						onClick = {handleClick}
					/>
				))}
				<button type="button" onClick={handleRedirect} className="submit">
					Add a Question
				</button>
				<button type="button" onClick={handleDelete} className="submit">
					Delete Quiz
				</button>
				<button type="button" onClick={menuRedirect} className="submit">
					Back to Menu
				</button>
		</div>
    </div>
	);
}