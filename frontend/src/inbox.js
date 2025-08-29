import {useEffect, useState} from 'react';
import axios from "axios";
import {useNavigate} from 'react-router-dom';
import './App.css';

const baseUrl = "http://localhost:5000"

export function Inbox(){

	const [mail, setMail] = useState([]);

	const navigate = useNavigate();

	useEffect(() => {
		const fetchData = async () => {
        try {
            const response = await axios.get(baseUrl + '/inbox', { withCredentials: true });
            setMail(response.data.mail);
        } catch (error) {
            console.error('Error:', error);
        }
		};
		fetchData();
	}, []);

	const handleAccept = async (event) => {
		event.preventDefault();
        const formData = { index: event.target.name };
        try {
        	const response = await axios.post(baseUrl+'/inbox', formData, { withCredentials: true });
			if(response.data['status'] === 'error'){
				alert(response.data['message']);
			}
			else{
				setMail(response.data.mail);
			}
        }
		catch (error) {
        	console.error('Error:', error);
		}
	};

	const handleDeny = async (event) => {
		event.preventDefault();
        const formData = { index: event.target.name };
        try {
        	const response = await axios.delete(baseUrl + '/inbox', { data: formData, withCredentials: true });
			if(response.data['status'] === 'error'){
				alert(response.data['message']);
			}
			else{
				setMail(response.data.mail);
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
			<h2>Inbox</h2>
				{mail.map((item, index) => (
					<div className = "inbox">
					<>
					<input
						type="button"
						name="submit"
						value={item['quiz_name']}
						className="submit"
					/>
					<input
						type="button"
						name={index}
						value='Accept'
						className="submit"
						onClick = {handleAccept}
					/>
					<input
						type="button"
						name={index}
						value='Deny'
						className="submit"
						onClick = {handleDeny}
					/>
					</>
					</div>
				))}
			<button type="button" onClick={menuRedirect} className="submit">
				Back to Menu
			</button>
		</div>
    </div>
	);
}