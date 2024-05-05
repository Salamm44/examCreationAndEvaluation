import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import QuestionForm from './TestQuestions/QuestionForm';

const StyledDiv = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  font-family: 'Helvetica Neue', Arial, sans-serif;
`;

// const StyledRowDiv = styled.div`
//   display: flex;
//   flex-direction: row;
//   justify-content: center
//   width: 100%;
// `;

const StyledP = styled.p`
  font-size: 20px;
  color: #333;
  margin-top: 0px;
  margin-bottom: 20px;
  margin-right: 20px;
  padding: 10px;
  border-radius: 5px;
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  width: 150px;
  &:hover {
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
  }
`;

const TestQuestions = () => {
  const [numQuestions, setNumQuestions] = useState(0); // State for number of questions
  const [numAnswers, setNumAnswers] = useState(0); // State for number of answers

  // Use useEffect to retrieve numQuestions and numAnswers from localStorage when the component mounts
  useEffect(() => {
    const storedForm = JSON.parse(localStorage.getItem('form'));
    if (storedForm) {
      if (!isNaN(Number(storedForm.numQuestions))) {
        setNumQuestions(Number(storedForm.numQuestions));
      }

      if (!isNaN(Number(storedForm.numAnswers))) {
        setNumAnswers(Number(storedForm.numAnswers));
      }
    }
  }, []);

  return (
    <StyledDiv>
      {/* <StyledRowDiv>
        <StyledP>Questions: {numQuestions}</StyledP>
        <StyledP>Answers: {numAnswers}</StyledP>
      </StyledRowDiv> */}
      <QuestionForm numQuestions={numQuestions} numAnswers={numAnswers} />
    </StyledDiv>
  );
};

export default TestQuestions;
