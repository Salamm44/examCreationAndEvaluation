import React, { useState, useEffect, useCallback } from 'react';
import { faSave, faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { toast } from 'react-toastify';
import PropTypes from 'prop-types';
import useLocalStorage from './useLocalStorage';

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
  color: ${(props) => (props.validationmet ? 'green' : '#ccc')};
  margin: 0;
  text-align: left;
  display: flex;
  align-items: center;
`;

const StyledIcon = styled(FontAwesomeIcon)`
  margin-right: 10px;
  margin-left: 10px;
`;

const Line = styled.hr`
  color: #ccc;
  height: 2px;
  width: 70%;
  margin: 16px 0;
  border: none;
  background-color: #ccc;
`;

const QuestionForm = ({ numQuestions = 0, numAnswers = 0 }) => {

  const [questions, setQuestions] = useLocalStorage('questions', []);
  const [answers, setAnswers] = useLocalStorage('answers', []);

  useEffect(() => {
    const initialQuestions = Array.from({ length: numQuestions }, () => ({
      text: '',
      isCorrect: false,
    }));

    const initialAnswers = Array.from({ length: numQuestions }, () =>
      Array.from({ length: numAnswers }, () => ({
        text: '',
        isCorrect: false,
      })),
    );

    setQuestions(initialQuestions);
    setAnswers(initialAnswers);
  }, [numQuestions, numAnswers]);

  const [areQuestionsEntered, setAreQuestionsEntered] = useState(false);
  const [areAnswersEntered, setAreAnswersEntered] = useState(false);
  const [isCheckboxChecked, setIsCheckboxChecked] = useState(false);

  useEffect(() => {
    setAreQuestionsEntered(questions.every((question) => question.text));
  }, [questions]);

  useEffect(() => {
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
  }, [ answers]);

  const handleQuestionChange = useCallback((i, value) => {
    setQuestions((prevQuestions) => {
      const newQuestions = [...prevQuestions];
      newQuestions[i].text = value;
      return newQuestions;
    });
  }, []);

  const handleAnswerChange = useCallback((i, j, value, isCorrect) => {
    setAnswers((prevAnswers) => {
      const newAnswers = [...prevAnswers];
      newAnswers[i][j].text = value;
      newAnswers[i][j].isCorrect = isCorrect;
      return newAnswers;
    });
  }, []);

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

  const [showLoading, setShowLoading] = useState(false);

  useEffect(() => {
    setShowLoading(questions.length === 0);
  }, [questions]);

  const isDisabled = () => !areQuestionsEntered || !areAnswersEntered || !isCheckboxChecked || showLoading;

  return (
    <StyledForm onSubmit={handleSave}>
      {questions.length === 0 ? (
        <p>Loading...</p>
      ) : (
        questions && questions.map((question, qIndex) => (
          <>
            <React.Fragment key={`question-${qIndex}`}>
              <StyledQuestionBlock key={`question-block-${qIndex}`}>
                <StyledH3>Question {qIndex + 1}:</StyledH3>
                <StyledInput
                  type="text"
                  value={question.text}
                  onChange={(event) =>
                    handleQuestionChange(qIndex, event.target.value)
                  }
                  placeholder="Enter question"
                />
                {answers[qIndex] && answers[qIndex].map((answer, aIndex) => (
                  <React.Fragment key={`answer-${qIndex}-${aIndex}`}>
                    <StyledAnswerBlock key={`question-block-${qIndex}`}>
                      <StyledInput
                        type="text"
                        value={answer.text}
                        onChange={(event) =>
                          handleAnswerChange(
                            qIndex,
                            aIndex,
                            event.target.value,
                            answer.isCorrect,
                          )
                        }
                        placeholder="Enter answer"
                      />
                      <StyledCheckbox
                        checked={answer.isCorrect}
                        onChange={(event) =>
                          handleAnswerChange(
                            qIndex,
                            aIndex,
                            answer.text,
                            event.target.checked,
                          )
                        }
                      />
                    </StyledAnswerBlock>
                  </React.Fragment>
                ))}
              </StyledQuestionBlock>
            </React.Fragment>

            <StyledQuestionBlock>
              <div style={{ width: '100%', textAlign: 'left' }}>
                <StyledValidationRule
                  validationmet={areQuestionsEntered}
                >
                  <StyledIcon icon={areQuestionsEntered ? faCheck : faTimes} />{' '}
                  All questions must be entered.
                </StyledValidationRule>

                <StyledValidationRule
                  validationmet={areAnswersEntered}
                >
                  <StyledIcon icon={areAnswersEntered ? faCheck : faTimes} />{' '}
                  All answers must be entered.
                </StyledValidationRule>

                <StyledValidationRule
                  validationmet={isCheckboxChecked}
                >
                  <StyledIcon icon={isCheckboxChecked ? faCheck : faTimes} /> At
                  least one checkbox in each question must be checked.
                </StyledValidationRule>
              </div>
            </StyledQuestionBlock>

            <Line />
          </>
        ))
      )}

      <button
        type="submit"
        className="creation-button"
        disabled={isDisabled()}
      >
        <FontAwesomeIcon icon={faSave} /> Save
      </button>
    </StyledForm>
  );
};

QuestionForm.propTypes = {
  numQuestions: PropTypes.number.isRequired,
  numAnswers: PropTypes.number.isRequired,
};

export default QuestionForm;
