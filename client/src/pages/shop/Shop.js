import React from "react";
import groupBy from 'lodash/groupBy';

import styled from 'styled-components';

import { studentLogout } from '../../services/student';
import { purchaseItem } from '../../services/treasureItem';

function groupByCost(items) {
    return Object.entries(groupBy(items, 'cost')).sort((a,b) => a[0] - b[0]);
}

const Card = styled.div`
    border: solid 2px #008080;
    border-radius: 8px;
    width: 250px;
    max-height: 500px;
    margin: 16px;
    padding: 8px;
`;

const CardContainer = styled.div`
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    margin: 16px auto;
    justify-content: center;
`;

const CardTitle = styled.h1`
    font-size: 1.5rem;
    margin: 8px 0;
`;

const CardSubTitle = styled.h2`
    font-size: 1rem;
    margin: 4px 0;
`;

const CardButton = styled.button`
    width: 100%;
    background-color: #66b2b2;
    border: solid 1px #004c4c;
    padding: 8px;
    font-size: 1.5rem;
    border-radius: 4px;
    color: #ffffff;
`;

const CardImage = styled.img`
    height: 200px;
    width: 200px;
`;
class Shop extends React.Component {
    constructor(props) {
        super(props);
        this.onLogout = this.onLogout.bind(this);
        this.canPurchase = this.canPurchase.bind(this);
    }

    async onLogout () {
        const result = await studentLogout();

        if (result.status === 'success') {
            this.props.history.replace('/');
            this.props.onLogout();
        }
    }

    canPurchase(costOfItem) {
        const { currentStudent } = this.props;
        return currentStudent.points >= costOfItem;
    }

    render() {
        const { currentStudent, treasureItems } = this.props;
        const groupedItems = groupByCost(treasureItems);
        return (
            <React.Fragment>
                <button onClick={this.onLogout}>Logout</button>
                <h1>{`Hey ${currentStudent.name}, you currently have ${currentStudent.points} points!`}</h1>
                <h2>Treasure items</h2>
                    {groupedItems.map(([cost, items]) => (
                        <React.Fragment>
                            <h1>{`Items for ${cost} dollars`}</h1>
                            <CardContainer>
                                {items.map(({id, cost, name, quantity}) => (
                                    <Card>
                                        <CardImage alt={`${name} image`}></CardImage>
                                        <CardTitle>{name}</CardTitle>
                                        <CardSubTitle>{`Price: $${cost}`}</CardSubTitle>
                                        <CardSubTitle>{`Quantity: ${quantity}`}</CardSubTitle>
                                        {this.canPurchase(cost) && (
                                            <CardButton onClick={() => purchaseItem(currentStudent.id, id)}>
                                                Buy
                                            </CardButton>
                                        )}
                                    </Card>
                                ))}
                            </CardContainer>
                        </React.Fragment>
                ))}
            </React.Fragment>
        )
    }
};
export default Shop;