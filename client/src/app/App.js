import React from "react";

import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";

import { fetchTreasureItems } from '../services/treasureItem';
import { fetchStudent } from '../services/student';

import Passcode from '../pages/passcode';
import Welcome from '../pages/welcome';
import Shop from '../pages/shop';

class App extends React.Component {
  constructor(props) {
    super(props);

    // Note this is usually an anti-pattern, but in this case it's okay. Properties coming into
    // this component is used as seed data. We do not expect props to ever change for this component.
    this.state = {
      students: props.students,
      currentStudent: props.currentStudent,
      treasureItems: props.treasureItems
    }

    this.fetchShopItemsAndCurrentStudent = this.fetchShopItemsAndCurrentStudent.bind(this);
    this.clearSessionData = this.clearSessionData.bind(this);
  }

  async fetchShopItemsAndCurrentStudent(studentId) {
    try {
      const [ treasureItemResult, currentStudentResult ] = await Promise.all([
        fetchTreasureItems(),
        fetchStudent(studentId)
      ]);

      this.setState({ 
        treasureItems: treasureItemResult.data.treasureItems,
        currentStudent: currentStudentResult.data.student
      });
    } catch(e) {
      console.log('an error occurred: ', e);
    }
  }

  clearSessionData() {
    this.setState({
      currentStudent: {},
      treasureItems: []
    });
  }

  render() {
    const { 
      authenticated,
      students, 
      currentStudent,
      treasureItems
    } = this.state;

    const ShopWithProps = ({ history }) => {
      return (
        <Shop 
          history={history}
          treasureItems={treasureItems} 
          currentStudent={currentStudent}
          onLogout={this.clearSessionData}
        />
      );
    };

    const PasscodeWithProps = ({ history }) => {
      return (
        <Passcode 
          history={history}
          onSuccess={this.fetchShopItemsAndCurrentStudent}
        />
      );
    };

    return (
      <React.Fragment>
        <Router>
          <Switch>
              <Route path="/passcode" component={PasscodeWithProps}>
              </Route>
              <Route path="/shop" component={ShopWithProps}>
              </Route>
              <Route path="/">
                <Welcome users={students} />
              </Route>
          </Switch>
        </Router>
      </React.Fragment>
    );
  }
}

export default App;