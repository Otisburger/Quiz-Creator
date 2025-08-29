import {useEffect, useState} from 'react';
import {useNavigate} from 'react-router-dom';
import './App.css';

const baseUrl = "http://localhost:5000"

export function Menu(){

	const navigate = useNavigate();

	const handleTake = () => {
		navigate('/takeQuiz')
	};

	const handleCreate = () => {
		navigate('/createQuiz')
	};

	const handleEdit = () => {
		navigate('/chooseQuiz')
	};

	const handleLogin = () => {
		navigate('/login')
	};

	const handleSend = () => {
		navigate('/send')
	};

	const handleInbox = () => {
		navigate('/inbox')
	};

	return (
	<div className="App">
		<h1>Quiz!</h1>
		<div className = "menu">
			<h2>Menu</h2>
			<button type="button" onClick={handleTake} className="submit">
				Take a Quiz
			</button>
			<button type="button" onClick={handleCreate} className="submit">
				Create a Quiz
			</button>
			<button type="button" onClick={handleEdit} className="submit">
				Edit a Quiz
			</button>
			<button type="button" onClick={handleSend} className="submit">
				Send a Quiz
			</button>
			<button type="button" onClick={handleInbox} className="submit">
				Inbox
			</button>
			<button type="button" onClick={handleLogin} className="submit">
				Back to Login
			</button>
		</div>
	</div>
	);
}