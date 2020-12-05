import React from "react";
import styled from 'styled-components';
import { Link, withRouter } from 'react-router-dom';

import { verifyStudent } from '../../services/student';
import NumberPad from '../../components/numberPad';

const PageContainer = styled.div`
    max-width: 960px;
    margin-left: auto;
    margin-right: auto;
`;

class Passcode extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            enteredPasscode: [],
            isVerifyingPasscode: false,
            failedPasscode: false,
            validatedPasscode: false,
        }

        this.clearPasscode = this.clearPasscode.bind(this);
        this.onKeyPadClick = this.onKeyPadClick.bind(this);
    }

    clearPasscode() {
        this.setState({
            enteredPasscode: []
        });
    }
    
    async onKeyPadClick(id, value) {
        const { enteredPasscode, isVerifyingPasscode } = this.state;

        if (isVerifyingPasscode) return;

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
            this.setState({ isVerifyingPasscode: true });
            let result = await verifyStudent({ userID: id, passcode: newPasscode.join('') });
            
            this.setState({
                isVerifyingPasscode: false, 
                failedPasscode: result.status === 'fail',
                validatedPasscode: result.status === 'success',
                enteredPasscode: [] 
            });
            console.log(result)
            if (result.status === 'success') {
                let {history} = this.props;
                console.log(history)
                console.log('updating history')
                history.replace('/shop');
            }
        }
    }

    render() {
        const { enteredPasscode } = this.state;
        return (
            <PageContainer>
                <section>
                    <Link to='/' onClick={this.clearPasscode}>Back</Link>
                    <h1>Enter your 2 digit passcode below</h1>
                </section>
                <NumberPad 
                    enteredPasscode={enteredPasscode}
                    onKeyClick={this.onKeyPadClick}
                />
            </PageContainer>
        );
    }
};

export default withRouter(Passcode);