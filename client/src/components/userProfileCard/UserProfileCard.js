import React from "react";
import isFunction from 'lodash/isFunction';
import isNil from 'lodash/isNil';

import styled from 'styled-components';

const Card = styled.div.attrs(props => ({
    clickable: props.clickable
}))`
    width: 250px;
    border: solid 1px #576675;
    border-radius: 4px;
    position:relative;
    cursor: ${props => props.clickable ? 'pointer' : 'default'};
    background-color: #FFFFFF;

    &:hover {
        background-color: ${props => props.clickable ? '#C0C0C0' : '#FFFFFF'};
    }
`;

const Input = styled.input`
    margin: 16px auto;
    display: block;
`;

const Heading = styled.h1`
    font-size: 1.5rem;
    text-align: center;
    margin: 16px auto;
    width: 100%;
`;

const ProfileImage = styled.img`
    max-width: 100%;
    height: 'auto';
    max-height: 250px;
`;

function UserProfileCard({ name, image, points, onInputChangedFn, clickable = false }) {
    const hasOnChangeFn = isFunction(onInputChangedFn);

    return (
        <Card clickable={clickable}>
            {!isNil(points) && (<Input type="number" value={points} onChange={(e) => hasOnChangeFn ? onInputChangedFn(e) : () => {}}/>)}
            <ProfileImage src={image}></ProfileImage>
            <Heading>{name}</Heading>
        </Card>
    );
}

export default UserProfileCard;