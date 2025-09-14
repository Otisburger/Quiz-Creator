import {useEffect, useState} from 'react';
import axios from "axios";
import {useNavigate} from 'react-router-dom';
import './App.css';

const baseUrl = "http://127.0.0.1:5000"

export function Send(){

	const [sendValue, setSendValue] = useState('');

	const [quizValue, setQuizValue] = useState('');

	const navigate = useNavigate();

	const handleSendChange = (event) => {
		setSendValue(event.target.value);
	};

	const handleQuizChange = (event) => {
		setQuizValue(event.target.value);
	};

	const handleRedirect = () => {
		navigate('/menu')
	};

	const handleSubmit = async (event) => {
		event.preventDefault();
        const formData = { send: sendValue, quiz: quizValue };
        try {
        	const response = await axios.post(baseUrl+'/send', formData, { withCredentials: true });
			if(response.data['status'] === 'error'){
				alert(response.data['message']);
			}
			else{
				navigate('/menu')
			}
        }
		catch (error) {
        	console.error('Error:', error);
		}
    };

	return (
    <div className="App">
		    <h1>Quiz!</h1>
		    	<div className = "main">
			    	<form onSubmit={handleSubmit}>
				    	<h2>Send a Quiz</h2>
				        <div className="login">
					        <label htmlFor="send">Send to</label>
					        <input 
                      			type="text"
                      			name="send"
                      			id="send"
								onChange={handleSendChange}
                    		/>
				        </div>
				        <div className="login">
					        <label htmlFor="quiz">Quiz Name</label>
					        <input
								type="text"
								name="quiz"
								id="quiz"
								onChange={handleQuizChange}
							/>
				        </div>
				        <input
							id = "button"
							type="submit"
							name="submit"
							value="Submit"
							className="submit"
						/>
			    	</form>
			    	<button type="button" onClick={handleRedirect} className="submit">
						Back to Menu
					</button>
		    	</div>
    </div>
	);
}