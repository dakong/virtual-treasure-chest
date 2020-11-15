import React from "react";
import UserProfileCard from '../../components/userProfileCard';

function Welcome({ users }) {
    console.log(users)
    return (
        <React.Fragment>
            <section>
                <h1>Welcome to Ms.Chang's Virtual Classroom Store</h1>
                <p>Please select your name below to get started.</p>
            </section>
            <section>
                {users.map(({ name }) => <UserProfileCard name={name} />)}
            </section>
        </React.Fragment>
    );
}

export default Welcome;