import React from 'react';
import styled from 'styled-components';

const Image = styled.img`
  width: 300px;
  height: 300px;
  margin: 16px auto;
  display: block;
`;

const ButtonGroup = styled.div`
  display: flex;
  justify-content: center;
`;

const Button = styled.button`
  cursor: pointer;
  width: 200px;
  padding: 8px 16px;
  margin: 8px 16px;
  font-size: 1.5rem;
`;

const ItemModal = ({
  description,
  imageAlt,
  imageSrc,
  onPrimaryButtonClick,
  onSecondaryButtonClick,
  primaryButtonLabel,
  secondaryButtonLabel,
  subTitlePrimary,
  subTitleSecondary,
  title,
}) => (
  <div>
    <Image src={imageSrc} alt ={imageAlt} />
    <p>Do you want to buy <b>{title}</b> for <b>${subTitlePrimary}</b>?</p>
    <ButtonGroup>
      <Button onClick={onPrimaryButtonClick}>{primaryButtonLabel}</Button>
      <Button onClick={onSecondaryButtonClick}>{secondaryButtonLabel}</Button>
    </ButtonGroup>
  </div>
);

export default ItemModal;