import React from "react";
import styled from 'styled-components';
import { Link } from 'react-router-dom';
import NumberPad from '../../components/numberPad';

const PageContainer = styled.div`
    max-width: 960px;
    margin-left: auto;
    margin-right: auto;
`;

function Passcode({ clearPasscode, enteredPasscode, onKeyPadClick }) {
    
    return (
        <PageContainer>
            <section>
                <Link to='/' onClick={clearPasscode}>Back</Link>
                <h1>Enter your 2 digit passcode below</h1>
            </section>
            <NumberPad 
                enteredPasscode={enteredPasscode}
                onKeyClick={onKeyPadClick}
            />
        </PageContainer>
    );
}

export default Passcode;