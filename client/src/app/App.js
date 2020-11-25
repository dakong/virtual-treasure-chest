import React from "react";
import isEmpty from "lodash/isEmpty";

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useRouteMatch,
  useParams,
  useHistory
} from "react-router-dom";
import Welcome from '../pages/welcome';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    
    this.state = {
      categories: [{label: 'Stickers', id: 1}, {label: 'Snacks', id: 2}, {label: 'Toys', id: 3}],
    }
  }

  render() {
    const { students, authenticated } = this.props;
    const { categories } = this.state
    return (
      <React.Fragment>
        { !authenticated ? (
          <Router>
            <div>
              <Switch>
                <Route path="/treasure-chest">
                  <TreasureChest tabs={categories}/>
                </Route>
              </Switch>
            </div>
          </Router>
        ) : <Welcome users={students} />}
        
      </React.Fragment>
    );
  }
}

function TreasureChest({tabs}) {
  let match = useRouteMatch();

  return (
    <div>
      <h2>Topics</h2>

      <ul>
        {tabs.map(({label, id}) => (
          <li key={id}>
            <Link to={`${match.url}/${label}`}>{label}</Link>
          </li>
        ))}
      </ul>

      {/* The Topics page has its own <Switch> with more routes
          that build on the /topics URL path. You can think of the
          2nd <Route> here as an "index" page for all topics, or
          the page that is shown when no topic is selected */}
      <Switch>
        <Route path={`${match.path}/:topicId`}>
          <Topic />
        </Route>
      </Switch>
    </div>
  );
}

function Topic() {
  let { topicId } = useParams();
  return <h3>Requested topic ID: {topicId}</h3>;
}