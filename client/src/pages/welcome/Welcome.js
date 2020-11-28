import React from "react";
import UserProfileCard from '../../components/userProfileCard';
import styled from 'styled-components';

const PageContainer = styled.div`
    max-width: 960px;
    margin-left: auto;
    margin-right: auto;
`;
const CardContainer = styled.section`
    max-width: 960px;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, max-content));
    gap: 16px;
    justify-content: space-evenly;
`;

function Welcome({ users }) {
    return (
        <PageContainer>
            <section>
                <h1>Welcome to Ms.Chang's Virtual Classroom Store</h1>
                <p>Please select your name below to get started.</p>
            </section>
            <CardContainer>
                {users.map(({ name, image, id }) => <UserProfileCard clickable key={id} name={name} image={image}/>)}
            </CardContainer>
        </PageContainer>
    );
}

export default Welcome;