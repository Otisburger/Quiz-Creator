import {useEffect, useState} from 'react';
import axios from "axios";
import {useNavigate} from 'react-router-dom';
import './App.css';

const baseUrl = "http://127.0.0.1:5000"

export function End(){

	const [points, setPoints] = useState(0);

	const [total, setTotal] = useState(0);

	const navigate = useNavigate();

	useEffect(() => {
		const fetchData = async () => {
        try {
            const response = await axios.get(baseUrl + '/end', { withCredentials: true });
            setPoints(response.data.points);
			setTotal(response.data.total);
        } catch (error) {
            console.error('Error:', error);
        }
		};
		fetchData();
	}, []);

	const handleRedirect = () => {
		navigate('/takeQuiz')
	};

	const handleMenu = () => {
		navigate('/menu')
	};

	return (
    <div className="App">
		    <h1>Quiz!</h1>
		    <div className = "main">
				<h2>Quiz Completed!</h2>
				<p>
					You answered {points} out of {total} questions correctly!
				</p>
			    <button type="button" onClick={handleRedirect} className="submit">
					Take Another Quiz
				</button>
			    <button type="button" onClick={handleMenu} className="submit">
					Back to Menu
				</button>
		    </div>
    </div>
	);
}