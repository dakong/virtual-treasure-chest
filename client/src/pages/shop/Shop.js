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
        return (
            <React.Fragment>
                <button onClick={this.onLogout}>Logout</button>
                <h1> Welcome to the shop!</h1>
            </React.Fragment>
        )
    }
};
export default Shop;