import {useEffect, useState} from 'react';
import axios from "axios";
import {useNavigate} from 'react-router-dom';
import './App.css';

const baseUrl = "http://localhost:5000"

export function CreateQuiz(){

	const [name, setName] = useState('');

	const navigate = useNavigate();

	const handleChange = (event) => {
		setName(event.target.value);
	};

	const handleSubmit = async (event) => {
		event.preventDefault();
        const formData = { name: name };
        try {
        	const response = await axios.post(baseUrl+'/createQuiz', formData, { withCredentials: true });
			if(response.data['status'] === 'error'){
				alert(response.data['message']);
			}
			else{
				navigate('/editQuiz');
			}
        }
		catch (error) {
        	console.error('Error:', error);
		}
    };

	return (
    <div className="App">
		<h1>Quiz!</h1>
			<h2>Create a Quiz</h2>
			<form onSubmit={handleSubmit}>
				<div className="main">
					<label htmlFor="name">Quiz Name</label>
					    <input 
							type="text"
							name="name"
							id="name"
							onChange={handleChange}
						/>
				        <input
							id = "button"
							type="submit"
							name="submit"
							value="Submit"
							className="submit"
						/>
				</div>
			</form>
    </div>
	);
}