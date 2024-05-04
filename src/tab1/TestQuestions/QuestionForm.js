import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSave } from '@fortawesome/free-solid-svg-icons';
import styled from 'styled-components';
import AnswerOption from './AnswerOption';

const StyledForm = styled.form`
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.2);
    width: 50%;
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

const StyledDiv = styled.div`
    width: 70%;
`;

const StyledH3 = styled.h3`
    margin-top: 0px;
`;
const QuestionForm = ({ numQuestions, numAnswers }) => {
    const [questions, setQuestions] = useState(Array(numQuestions).fill(''));

    const handleQuestionChange = (index, newQuestion) => {
        setQuestions(questions.map((question, i) => i === index ? newQuestion : question));
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        // TODO: Handle the form submission
    };

    return (
        <StyledForm onSubmit={handleSubmit}>
            {questions.map((question, i) => (
                <StyledDiv key={i}>
                    <StyledH3>Question {i + 1}:</StyledH3>
                    <StyledInput
                        type="text"
                        value={question}
                        onChange={(event) => handleQuestionChange(i, event.target.value)}
                        placeholder="Enter question"
                    />
                    {[...Array(numAnswers)].map((_, j) => (
                        <AnswerOption key={j} index={j} />
                    ))}
                </StyledDiv>
            ))}
            <button type="submit" className="creation-button">
                <FontAwesomeIcon icon={faSave} /> Save
            </button>
        </StyledForm>
    );
};

export default QuestionForm;
