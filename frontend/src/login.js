import {useEffect, useState} from 'react';
import axios from "axios";
import {useNavigate} from 'react-router-dom';
import './App.css';

const baseUrl = "http://localhost:5000"

export function Login(){

	const [userValue, setUserValue] = useState('');

	const [passValue, setPassValue] = useState('');

	const navigate = useNavigate();

	const handleChange = (event) => {
		setUserValue(event.target.value);
	};

	const handlePassChange = (event) => {
		setPassValue(event.target.value);
	};

	const handleRedirect = () => {
		navigate('/createUser')
	};

	const handleSubmit = async (event) => {
		event.preventDefault();
		console.log(userValue);
		console.log(passValue);
        const formData = { username: userValue, password: passValue };
        try {
        	const response = await axios.post(baseUrl+'/login', formData, { withCredentials: true });
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
				    	<h2>Login</h2>
				        <div className="login">
					        <label htmlFor="username">Username</label>
					        <input 
                      			type="text"
                      			name="username"
                      			id="username"
								onChange={handleChange}
                    		/>
				        </div>
				        <div className="login">
					        <label htmlFor="password">Password</label>
					        <input
								type="password"
								name="password"
								id="password"
								onChange={handlePassChange}
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
						Create Account
					</button>
		    	</div>
    </div>
	);
}