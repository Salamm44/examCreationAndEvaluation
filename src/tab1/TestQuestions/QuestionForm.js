import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSave } from '@fortawesome/free-solid-svg-icons';
import styled from 'styled-components';
import AnswerOption from './AnswerOption';

const StyledTable = styled.table`
  width: auto;
  border-collapse: collapse;
  border-spacing: 0 10px;
  font-family: Arial, sans-serif;
`;

const StyledTableRow = styled.tr`
  width: 100%;
  border-bottom: 1px solid #ddd;
  margin: 10px 0;
  &:nth-child(even) {
    background-color: #f2f2f2;
  }
`;

const StyledTableData = styled.td`
  padding: 8px;
  text-align: left;
`;

const StyledTableHeader = styled.th`
  padding: 10px;
  text-align: left;
  background-color: #d3d3d3;
`;

const StyledForm = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.2);
  width: 50%;
  height: auto;
  margin: auto;
`;

const StyledInput = styled.input`
  margin: 10px 0;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
  width: 100%;
  box-sizing: border-box;
`;

const QuestionBlock = styled.div`
  width: 100%;
  margin-bottom: 10px;
`;

const QuestionForm = ({ numQuestions, numAnswers }) => {
  const [question, setQuestion] = useState(''); // State for the question

  const answerOptions = [];
  for (let i = 0; i < numAnswers; i++) {
    answerOptions.push(<AnswerOption key={i} index={i} />);
  }

  // Function to handle the form submission
  const handleSubmit = (event) => {
    event.preventDefault();
    // TODO: Handle the form submission
  };

  const questionComponents = [];
  for (let i = 0; i < numQuestions; i++) {
    const answerComponents = [];
    for (let j = 0; j < numAnswers; j++) {
      answerComponents.push(
        <StyledTableRow key={`${i}-${j}`}>
          <StyledTableData>{`Answer ${j + 1}`}</StyledTableData>
          <StyledTableData>
            <AnswerOption index={j} />
          </StyledTableData>
        </StyledTableRow>,
      );
    }

    questionComponents.push(
      <QuestionBlock key={i}>
        <StyledTableRow>
          <StyledTableHeader>Question {i + 1}:</StyledTableHeader>
          <StyledTableHeader>
            <StyledInput
              type="text"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
            />
          </StyledTableHeader>
        </StyledTableRow>
        {answerComponents}
      </QuestionBlock>,
    );
  }

  return (
    <StyledForm onSubmit={handleSubmit}>
      <StyledTable>{questionComponents}</StyledTable>
      <button type="submit" className="creation-button">
        <FontAwesomeIcon icon={faSave} /> Save
      </button>
    </StyledForm>
  );
};

export default QuestionForm;
