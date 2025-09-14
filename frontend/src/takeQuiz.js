import {useEffect, useState} from 'react';
import axios from "axios";
import {useNavigate} from 'react-router-dom';
import './App.css';

const baseUrl = "http://127.0.0.1:5000"

export function TakeQuiz(){

	const [quizzes, setQuizzes] = useState([]);

	const navigate = useNavigate();

	useEffect(() => {
		const fetchData = async () => {
        try {
            const response = await axios.get(baseUrl + '/takeQuiz', { withCredentials: true });
            setQuizzes(response.data.quizzes);
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
        	const response = await axios.post(baseUrl+'/takeQuiz', formData, { withCredentials: true });
			if(response.data['status'] === 'error'){
				alert(response.data['message']);
			}
			else{
				navigate('/answering')
			}
        }
		catch (error) {
        	console.error('Error:', error);
		}
	};

	const menuRedirect = async () => {
		navigate('/menu')
	};

	return (
    <div className="App">
		<h1>Quiz!</h1>
		<div className = "main">
			<h2>Choose a Quiz</h2>
				{quizzes.map((quiz, index) => (
					<input
						id={index}
						type="button"
						name="submit"
						value={quiz['name']}
						className="submit"
						onClick = {handleClick}
					/>
				))}
			<button type="button" onClick={menuRedirect} className="submit">
				Back to Menu
			</button>
		</div>
    </div>
	);
}