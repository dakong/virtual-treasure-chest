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
    const { 
      authenticated,
      students, 
      currentStudent,
      treasureItems
    } = this.props;

    const ShopWithProps = () => {
      return (
        <Shop 
          treasureItems={treasureItems} 
          currentStudent={currentStudent}
        />
      );
    };

    const PublicPage = () => {
      return (
        <Router>
          <Switch>
              <Route path="/passcode" component={Passcode}>
              </Route>
              <Route path="/shop" component={ShopWithProps}>
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