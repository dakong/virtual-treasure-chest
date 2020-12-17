import React from 'react';
import groupBy from 'lodash/groupBy';
import styled from 'styled-components';

import Card from '../../components/card';

function groupByCost(items) {
    return Object.entries(groupBy(items, 'cost')).sort((a,b) => a[0] - b[0]);
}

const Page = styled.div`
    margin: 16px;
`;

const PriceLabel = styled.h1``;

const Container = styled.div`
    display: grid;
    grid-template-columns: repeat(auto-fit, 275px);
    grid-template-rows: repeat(3, auto-fit);
    gap: 32px;
    margin: 16px auto;
`;

class Shop extends React.PureComponent {
    constructor(props) {
        super(props);
        this.canPurchase = this.canPurchase.bind(this);
    }

    canPurchase(costOfItem, quantity) {
        const { currentStudent } = this.props;
        return currentStudent.points >= costOfItem && quantity > 0;
    }

    render() {
        const { currentStudent, treasureItems, onSelectItem, onLogout } = this.props;
        const groupedItems = groupByCost(treasureItems);
        return (
            <React.Fragment>
                <button onClick={onLogout}>Logout</button>
                <Page>
                    <h1>{`Hey ${currentStudent.name}, you currently have ${currentStudent.points} points!`}</h1>
                    {groupedItems.map(([cost, items], idx) => (
                        <React.Fragment key={`group_${idx}`}>
                            <PriceLabel>{`$${cost}`}</PriceLabel>
                            <Container>
                                {items.map(({id, cost, description, name, quantity, image_path}) => (
                                    <Card

                                        key={`card_${id}`}
                                        cardActionLabel="Buy"
                                        imageAlt={`${name} image`}
                                        imageSrc={image_path}
                                        onCardActionClick={() => onSelectItem({id, cost, description, name, quantity, image_path})}
                                        showButton={this.canPurchase(cost, quantity)}
                                        subTitlePrimary={`Price: $${cost}`}
                                        subTitleSecondary={`Quantity: ${quantity}`}
                                        title={name}
                                    />
                                ))}
                            </Container>
                        </React.Fragment>
                    ))}
                </Page>
            </React.Fragment>
        );
    }
};
export default Shop;