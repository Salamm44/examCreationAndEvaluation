import React, { useState, useEffect } from 'react';
import QuestionForm from './TestQuestions/QuestionForm';

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
    <div>
      <p>Number of questions: {numQuestions}</p>
      <p>Number of answers: {numAnswers}</p>
      <QuestionForm numQuestions={numQuestions} numAnswers={numAnswers}/>
    </div>
  );
}

export default TestQuestions;