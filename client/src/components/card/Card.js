import React from 'react';
import styled from 'styled-components';

const CardContainer = styled.div`
    border: solid 4px #a5dede;
    border-radius: 8px;
    width: 275px;
    max-height: 500px;
    padding: 8px;
    box-sizing: border-box;
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

const Card = ({
  cardActionLabel = '',
  imageAlt = '',
  imageSrc = '',
  onCardActionClick = () => {},
  showButton = true,
  subTitlePrimary = '',
  subTitleSecondary = '',
  title = '',
}) => (
  <CardContainer>
      <CardImage alt={imageAlt} src={imageSrc}></CardImage>
      <CardTitle>{title}</CardTitle>
      <CardSubTitle>{subTitlePrimary}</CardSubTitle>
      <CardSubTitle>{subTitleSecondary}</CardSubTitle>
      {showButton && (
          <CardButton onClick={onCardActionClick}>
              {cardActionLabel}
          </CardButton>
      )}
  </CardContainer>
);

export default Card;