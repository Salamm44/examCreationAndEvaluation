import React, { useState } from 'react';
import styled from 'styled-components';

const StyledInput = styled.input`
  margin: 10px 0;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
  width: 100%;
`;

const StyledCheckbox = styled.input.attrs({ type: 'checkbox' })`
  width: 20px;
  height: 20px;
  margin: 10px;
`;

const AnswerOption = ({ index }) => {
    const [answer, setAnswer] = useState(''); // State for the answer
    const [isCorrect, setIsCorrect] = useState(false); // State for the checkbox
    const [isInvalid, setIsInvalid] = useState(false); // State for invalid fields
  
    const handleInputChange = (event) => {
      const newAnswer = event.target.value;
      setAnswer(newAnswer);
  
      if (newAnswer.trim() === '') {
        setIsInvalid(true);
      } else {
        setIsInvalid(false);
      }
    };
  
    return (
      <div style={{ display: 'flex', alignItems: 'center', width: '100%' }}>
        <label style={{ display: 'flex', width: '100%' }}>
          <StyledInput
            type="text"
            value={answer}
            onChange={handleInputChange}
            style={isInvalid ? { borderColor: 'red' } : {}}
          />
        </label>
        <label>
          <StyledCheckbox
            onChange={(event) => setIsCorrect(event.target.checked)}
          />
        </label>
      </div>
    );
  };
  

export default AnswerOption;
