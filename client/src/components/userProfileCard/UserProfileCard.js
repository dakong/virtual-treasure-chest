import React from "react";
import styled from 'styled-components';

const Card = styled.div`
    width: 250px;
    border: solid 1px #576675;
    border-radius: 4px;
    position:relative;
    cursor: pointer;
    background-color: #FFFFFF;

    &:hover {
        background-color: #C0C0C0;
    }
    
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
`;

function UserProfileCard({ name, image }) {
    return (
        <Card>
            <ProfileImage src={image}></ProfileImage>
            <Heading>{name}</Heading>
        </Card>
    );
}

export default UserProfileCard;