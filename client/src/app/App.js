import React from "react";

import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";

import Passcode from '../pages/passcode';
import Welcome from '../pages/welcome';
export default class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      enteredPasscode: [],
    }
    this.clearPasscode = this.clearPasscode.bind(this);
    this.onKeyPadClick = this.onKeyPadClick.bind(this);
  }

  clearPasscode() {
    this.setState({
      enteredPasscode: []
    });
  }

  onKeyPadClick(id, value) {
    const { enteredPasscode } = this.state;
    let newPasscode = enteredPasscode;
    if (enteredPasscode.length < 2) {
      newPasscode = [...enteredPasscode, value];
      this.setState({
        enteredPasscode: newPasscode
      });
    } 
    
    if (newPasscode.length === 2) {
      // Passcode is filled, let's make a call to validate the student
      console.log( `validate student id: ${id}, with passcode: ${newPasscode.join('')}`);
    }
  }

  render() {
    const { students } = this.props;
    const { enteredPasscode } = this.state

    const PublicPage = () => {
      return (
        <Router>
          <Switch>
              <Route path="/passcode">
                <Passcode 
                  clearPasscode={this.clearPasscode}
                  enteredPasscode={enteredPasscode} 
                  onKeyPadClick={this.onKeyPadClick} 
                />
              </Route>
              <Route path="/">
                <Welcome users={students} />
              </Route>
          </Switch>
        </Router>
      )
    };

    return (
      <React.Fragment>
        <PublicPage />
      </React.Fragment>
    );
  }
}