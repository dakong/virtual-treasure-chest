import React from "react";
import groupBy from 'lodash/groupBy';

import styled from 'styled-components';

import { studentLogout } from '../../services/student';

function groupByCost(items) {
    return Object.entries(groupBy(items, 'cost')).sort((a,b) => a[0] - b[0]);
}

const Page = styled.div`
    margin: 16px;
`;

const PriceLabel = styled.h1`
`;

const Card = styled.div`
    border: solid 4px #a5dede;
    border-radius: 8px;
    width: 250px;
    max-height: 500px;
    padding: 8px;
`;

const CardContainer = styled.div`
    display: grid;
    grid-template-columns: repeat(auto-fit, 250px);
    grid-template-rows: repeat(3, auto-fit);
    gap: 16px;
    margin: 16px auto;

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
    cursor: pointer;
    width: 100%;
    background-color: #46d7ba;
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
        const { currentStudent, treasureItems, onPurchase } = this.props;
        const groupedItems = groupByCost(treasureItems);
        return (
            <React.Fragment>
                <button onClick={this.onLogout}>Logout</button>
                <Page>
                    <h1>{`Hey ${currentStudent.name}, you currently have ${currentStudent.points} points!`}</h1>
                    {groupedItems.map(([cost, items]) => (
                        <React.Fragment>
                            <PriceLabel>{`$${cost}`}</PriceLabel>
                            <CardContainer>
                                {items.map(({id, cost, name, quantity, image_path}) => (
                                    <Card>
                                        <CardImage alt={`${name} image`} src={image_path}></CardImage>
                                        <CardTitle>{name}</CardTitle>
                                        <CardSubTitle>{`Price: $${cost}`}</CardSubTitle>
                                        <CardSubTitle>{`Quantity: ${quantity}`}</CardSubTitle>
                                        {this.canPurchase(cost) && (
                                            <CardButton onClick={() => onPurchase(currentStudent.id, id)}>
                                                Buy
                                            </CardButton>
                                        )}
                                    </Card>
                                ))}
                            </CardContainer>
                        </React.Fragment>
                    ))}
                </Page>
            </React.Fragment>
        );
    }
};
export default Shop;