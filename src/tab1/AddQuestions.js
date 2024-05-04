import React, { useState } from 'react';
import InputField from '../custom-components/InputField';
import styled from 'styled-components';

const InputFieldContainer = styled.div`
  display: flex;
  justify-content: space-between;
`;

const AddQuestions = ({ form, handleInputChange }) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const handleNext = () => {
    if (currentIndex < form.numQuestions - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  return (
    <InputFieldContainer>
      {[...Array(form.numQuestions)].map((_, index) => (
        <InputField
          key={index}
          className={
            index === currentIndex ? 'input-field-num-questions' : 'hidden'
          }
          type="number"
          name={`question${index}`}
          placeholder={`Question ${index + 1}`}
          value={form[`question${index}`]}
          handleInputChange={handleInputChange}
        />
      ))}

      <button type="button" onClick={handlePrev}>
        Previous
      </button>
      <button type="button" onClick={handleNext}>
        Next
      </button>
    </InputFieldContainer>
  );
};

export default AddQuestions;
