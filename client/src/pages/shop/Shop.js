import React from "react";
import { withRouter } from 'react-router-dom';

import { studentLogout } from '../../services/student';
class Shop extends React.Component {
    constructor(props) {
        super(props);
        this.onLogout = this.onLogout.bind(this);
    }

    async onLogout () {
        const result = await studentLogout();

        if (result.status === 'success') {
            const { history } = this.props;
            history.replace('/');
        }
    }

    render() {
        const { currentStudent, treasureItems } = this.props;
        return (
            <React.Fragment>
                <button onClick={this.onLogout}>Logout</button>
                <h1> Welcome to the shop!</h1>

                <h2>Current student</h2>
                <code>{JSON.stringify(currentStudent)}</code>

                <h2>Treasure items</h2>
                <ul>
                    {treasureItems.map(({id, cost, name, quantity}) => (
                        <li key={id}>
                            <span>{name}, {quantity}</span>
                        </li>
                    ))}
                </ul>
            </React.Fragment>
        )
    }
};
export default Shop;