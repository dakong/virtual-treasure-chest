import React from "react";
import styled from 'styled-components';
import { useLocation } from 'react-router-dom';

const InputField = styled.input`
    font-size: 6rem;
    border: none;
    border-bottom: solid 4px black;
    width: 150px;
    text-align: center;
    margin: 16px;
`;

const Key = styled.button`
    cursor: pointer;
    min-width: 150px;
    min-height: 150px;
    border-radius: 150px;
    border: solid 4px black;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3.5rem;

    &:hover {
        background-color: #FFFFFF;
    }
`;

const Row = styled.div`
    display: flex;
    flex-direction: row;
    justify-content: ${props => props['justify-content'] || 'space-around'};
    margin: 32px auto;
`;

const NumberPadContainer = styled.div`
    padding: 16px;
    max-width: 679px;
    margin: auto;
`;
function useQuery() {
    return new URLSearchParams(useLocation().search);
}
function Passcode({ enteredPasscode = [], onKeyClick = () => {} }) {
    let id = useQuery().get('id');

    const onNumberPadClick = (e) => {
        if (e.target.tagName === 'BUTTON') {
            onKeyClick(id, e.target.value)
        }
    }
    
    return (
        <React.Fragment>
            <NumberPadContainer onClick={onNumberPadClick}>
                <Row justify-content="center">
                    <InputField 
                        type="number"
                        value={enteredPasscode[0]}
                        readOnly 
                    />
                    <InputField 
                        type="number" 
                        value={enteredPasscode[1]}
                        readOnly 
                    />
                </Row>
                <Row>
                    <Key value={1}>1</Key>
                    <Key value={2}>2</Key>
                    <Key value={3}>3</Key>
                </Row>
                <Row>
                    <Key value={4}>4</Key>
                    <Key value={5}>5</Key>
                    <Key value={6}>6</Key>
                </Row>
                <Row>
                    <Key value={7}>7</Key>
                    <Key value={8}>8</Key>
                    <Key value={9}>9</Key>
                </Row>
                <Row>
                    <Key value={0}>0</Key>
                </Row>
            </NumberPadContainer>
        </React.Fragment>
    );
}

export default Passcode;