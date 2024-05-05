import React from 'react';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye } from '@fortawesome/free-solid-svg-icons';

const StyledDiv = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  font-family: 'Helvetica Neue', Arial, sans-serif;
`;

const StyledButton = styled.button`
  background-color: #4caf50;
  border: none;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  white-space: nowrap; // This will prevent the text from wrapping to the next line
  overflow: hidden; // This will hide any text that overflows the button
  text-overflow: ellipsis; // This will add an ellipsis (...) to any text that overflows the button
  display: inline-block; // This will make the button only as wide as its content
`;

const StyledForm = styled.form`
  display: flex;
  flex-direction: column;
  justify-content: center; 
  align-items: center;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.2);
  width: 50%;
  height: 480px;
  margin: auto;
`;

const PreviewPDF = () => {
  return (
    <StyledDiv>
      <StyledForm>
        <StyledButton>
          <span style={{ marginRight: '8px' }}>
            <FontAwesomeIcon icon={faEye} />
          </span>
          Preview PDF
        </StyledButton>
      </StyledForm>
    </StyledDiv>
  );
};

export default PreviewPDF;
