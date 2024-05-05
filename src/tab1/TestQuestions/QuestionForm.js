import React, { useState, useEffect } from 'react';
import { faSave, faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { toast } from 'react-toastify';

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
  display: flex;
  margin: 10px 0;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
  width: 100%;
  box-sizing: border-box;
`;

const StyledCheckbox = styled.input.attrs({ type: 'checkbox' })`
  width: 20px;
  height: 20px;
  margin: 10px;
  align-self: center;
`;

const StyledQuestionBlock = styled.div`
  width: 70%;
`;

const StyledAnswerBlock = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
`;

const StyledH3 = styled.h3`
  margin: 0px;
`;

const StyledValidationRule = styled.p`
  color: ${(props) => (props.isMet ? 'green' : '#ccc')};
  margin: 0;
  text-align: left;
  display: flex;
  align-items: center;
`;

const StyledIcon = styled(FontAwesomeIcon)`
  margin-right: 10px;
  margin-left: 10px;
`;

const QuestionForm = ({ numQuestions = 0, numAnswers = 0 }) => {
  const [questions, setQuestions] = useState(Array(numQuestions).fill(''));
  const [answers, setAnswers] = useState(
    Array(numQuestions).fill(
      Array(numAnswers).fill({ text: '', isCorrect: false }),
    ),
  );

  useEffect(() => {
    setQuestions(Array(numQuestions).fill(''));
    setAnswers(
      Array(numQuestions).fill(
        Array(numAnswers).fill({ text: '', isCorrect: false }),
      ),
    );
  }, [numQuestions, numAnswers]);

  const [areQuestionsEntered, setAreQuestionsEntered] = useState(false);
  const [areAnswersEntered, setAreAnswersEntered] = useState(false);
  const [isCheckboxChecked, setIsCheckboxChecked] = useState(false);

  useEffect(() => {
    setAreQuestionsEntered(questions.every((question) => question));
    setAreAnswersEntered(
      answers.every((answerBlock) =>
        answerBlock.every((answer) => answer.text),
      ),
    );
    setIsCheckboxChecked(
      answers.every((answerBlock) =>
        answerBlock.some((answer) => answer.isCorrect),
      ),
    );
  }, [questions, answers]);

  const handleQuestionChange = (index, newQuestion) => {
    setQuestions(
      questions.map((question, i) => (i === index ? newQuestion : question)),
    );
  };

  const handleAnswerChange = (
    questionIndex,
    answerIndex,
    newText,
    newIsCorrect,
  ) => {
    setAnswers(
      answers.map((questionAnswers, i) =>
        i === questionIndex
          ? questionAnswers.map((answer, j) =>
              j === answerIndex
                ? { text: newText, isCorrect: newIsCorrect }
                : answer,
            )
          : questionAnswers,
      ),
    );
  };

  const handleSave = (event) => {
    event.preventDefault();
  
    // Your existing form submission logic here...
  
    // Convert the questions and answers arrays to JSON strings
    const questionsJSON = JSON.stringify(questions);
    const answersJSON = JSON.stringify(answers);
  
    // Save the JSON strings to localStorage
    localStorage.setItem('questions', questionsJSON);
    localStorage.setItem('answers', answersJSON);
  
    // Show a success message
    toast.success('Questions and answers saved successfully!');
  };

  return (
    <StyledForm onSubmit={handleSave}>
      {questions.map((question, i) => (
        <StyledQuestionBlock key={i}>
          <StyledH3>Question {i + 1}:</StyledH3>
          <StyledInput
            type="text"
            value={question}
            onChange={(event) => handleQuestionChange(i, event.target.value)}
            placeholder="Enter question"
          />
          {answers[i].map((answer, j) => (
            <StyledAnswerBlock key={j}>
              <StyledInput
                type="text"
                value={answer.text}
                onChange={(event) =>
                  handleAnswerChange(i, j, event.target.value, answer.isCorrect)
                }
                placeholder="Enter answer"
              />
              <StyledCheckbox
                checked={answer.isCorrect}
                onChange={(event) =>
                  handleAnswerChange(i, j, answer.text, event.target.checked)
                }
              />
            </StyledAnswerBlock>
          ))}
        </StyledQuestionBlock>
      ))}

      <StyledQuestionBlock>
        <div style={{ width: '100%', textAlign: 'left' }}>
          <StyledValidationRule isMet={areQuestionsEntered}>
            <StyledIcon icon={areQuestionsEntered ? faCheck : faTimes} />{' '}
            All questions must be entered.
          </StyledValidationRule>

          <StyledValidationRule isMet={areAnswersEntered}>
            <StyledIcon icon={areAnswersEntered ? faCheck : faTimes} /> All
            answers must be entered.
          </StyledValidationRule>

          <StyledValidationRule isMet={isCheckboxChecked}>
            <StyledIcon icon={isCheckboxChecked ? faCheck : faTimes} /> At
            least one checkbox in each question must be checked.
          </StyledValidationRule>
        </div>
      </StyledQuestionBlock>

      <button
        type="submit"
        className="creation-button"
        disabled={
          !areQuestionsEntered || !areAnswersEntered || !isCheckboxChecked
        }
      >
        <FontAwesomeIcon icon={faSave} /> Save
      </button>
    </StyledForm>
  );
};

export default QuestionForm;
