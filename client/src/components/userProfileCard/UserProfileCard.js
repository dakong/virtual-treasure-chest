import React from "react";

function UserProfileCard({ name }) {
    console.log(name);
    return (
        <div>
            <p>{name}</p>
        </div>
    );
}

export default UserProfileCard;