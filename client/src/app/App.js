import React from "react";

import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";

import Passcode from '../pages/passcode';
import Welcome from '../pages/welcome';
import Shop from '../pages/shop';

class App extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { students, authenticated } = this.props;

    const PublicPage = () => {
      return (
        <Router>
          <Switch>
              <Route path="/passcode" component={Passcode}>
              </Route>
              <Route path="/shop" component={Shop}>
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

export default App;