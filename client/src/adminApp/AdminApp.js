import React from "react";
import styled from 'styled-components';

import UserProfileCard from '../components/userProfileCard';
import { updateStudent } from '../services/student';

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
        this.onCardInputChanged = this.onCardInputChanged.bind(this);
        this.state = {
            students: props.students
        }
    }

    onCardInputChanged (id) {
        return (e) => {
            const {students} = this.state;
            const {value} = e.target;
            const studentsWithUpdatedPoints = students.map(student => {
                return student.id === id ? { ...student, points: value } : student;
            });
            
            // make call to students api to update points.
            // Do we want to do a write through?
            this.setState({ students: studentsWithUpdatedPoints })
            updateStudent({ id, points: value }).then((result => console.log(result)));

        }
    }

    render(){
        const { students } = this.state;

        return(
            <PageContainer>
                <CardContainer>
                    {students.map(({ name, image, id, points }) => (
                        <UserProfileCard 
                            editable={true} 
                            key={id} 
                            name={name} 
                            image={image} 
                            points={points}
                            onInputChangedFn={this.onCardInputChanged(id)}
                        />
                    ))}   
                </CardContainer>
            </PageContainer>
        )
    }
}