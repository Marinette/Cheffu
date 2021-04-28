import React from 'react';
import {
  BrowserRouter,
  Route,
  Switch
} from 'react-router-dom';
import './app.css';
import NavigationBar from './components/NavigationBar/NavigationBar';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage'
import RecipeDetails from './pages/RecipeDetails';

function App() {
  return (
    <div className="app">
      <div className='navbar'>
        <NavigationBar></NavigationBar>
      </div>
      <div className='content'>
        <BrowserRouter>
          <Switch>
            <Route path="/" component={HomePage} exact />
            <Route path="/recipe/:recipeID" component={RecipeDetails} />
            <Route path="/about" component={AboutPage} />
          </Switch>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default App;
