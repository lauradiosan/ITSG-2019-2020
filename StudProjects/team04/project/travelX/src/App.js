import React, { Component } from 'react';
import { BrowserRouter, Route } from 'react-router-dom';
import ChatPage from "./views/ChatPage";

import './App.scss';
import 'antd/dist/antd.css';

class App extends Component {
  componentWillMount() { }

  render() {
    return (
      <div className="App">
        <BrowserRouter>
          <div className="app-content">
            <Route exact path="/" component={ChatPage} />
          </div>
        </BrowserRouter>
      </div>
    );
  }
}

export default App;
