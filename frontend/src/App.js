import './App.css';
import { HashRouter as BrowserRouter, Routes, Route } from 'react-router-dom'
import { Login } from './login'
import { CreateUser } from './createUser'
import { ChooseQuiz } from './chooseQuiz'
import { AddQuestion } from './addQuestion'
import { CreateQuiz } from './createQuiz'
import { EditQuestion } from './editQuestion'
import { EditQuiz } from './editQuiz'
import { Menu } from './menu'
import { TakeQuiz } from './takeQuiz'
import { Answering } from './answering'
import { End } from './end'

function App() {
	return(
		<div>
			<BrowserRouter>
				<Routes>
					<Route index element={<Login/>}/>
					<Route path="/login" element={<Login/>}/>
					<Route path="/createUser" element={<CreateUser/>}/>
					<Route path="/chooseQuiz" element={<ChooseQuiz/>}/>
					<Route path="/createQuiz" element={<CreateQuiz/>}/>
					<Route path="/editQuiz" element={<EditQuiz/>}/>
					<Route path="/editQuestion" element={<EditQuestion/>}/>
					<Route path="/addQuestion" element={<AddQuestion/>}/>
					<Route path="/menu" element={<Menu/>}/>
					<Route path="/takeQuiz" element={<TakeQuiz/>}/>
					<Route path="/answering" element={<Answering/>}/>
					<Route path="/end" element={<End/>}/>
				</Routes>
			</BrowserRouter>
		</div>
	);
}

export default App;
