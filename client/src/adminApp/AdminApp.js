import React from "react";
import UserProfileCard from '../components/userProfileCard';
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

export default class AdminApp extends React.Component {
    constructor(props) {
        super(props);
    }
    render(){
        const { students } = this.props;

        return(
            <PageContainer>
                <CardContainer>
                    {students.map(({ name, image, id }) => (
                        <UserProfileCard 
                            editable={true} 
                            key={id} 
                            name={name} 
                            image={image} 
                        />
                    ))}   
                </CardContainer>
            </PageContainer>
        )
    }
}