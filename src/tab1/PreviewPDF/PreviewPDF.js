import React, { useState } from 'react';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye } from '@fortawesome/free-solid-svg-icons';
import { jsPDF } from 'jspdf';
import { GlobalWorkerOptions } from 'pdfjs-dist';
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker.entry';
import useLocalStorage from '../TestQuestions/useLocalStorage';

GlobalWorkerOptions.workerSrc = pdfjsWorker;

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
  white-space: nowrap; 
  overflow: hidden; 
  text-overflow: ellipsis; 
  display: inline-block; 

  &:disabled {
    background-color: gray;
    cursor: not-allowed;
  }
`;

const StyledBlock = styled.div`
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
  const [pdfBlob, setPdfBlob] = useState(null);
  const [questions, setQuestions] = useLocalStorage('questions', []);
  const [answers, serAnswers] = useLocalStorage('answers', []);
  const isPreviewDisabled = () =>  questions.length === 0 || answers.length === 0;

  const generatePDF = async () => {

    const testDetails = JSON.parse(localStorage.getItem('form'));

    const doc = new jsPDF();

    // Set the text color to light gray and the size to 10
    doc.setTextColor(169, 169, 169); // RGB value for light gray
    doc.setFontSize(12);

    // Add the form values to the PDF
    let y = 10; // Initialize y
    const keys = Object.keys(testDetails).slice(0, -2); // Get all keys except the last two
    keys.forEach((key) => {
      doc.text(`${key}: ${testDetails[key]}`, 5, y);
      y += 5;
    });

    // Reset the text color to black and the size to 12
    doc.setTextColor(0, 0, 0); // RGB value for black
    doc.setFontSize(12);

    // Add a space before the questions and answers
    y += 10;

    questions.forEach((question, index) => {
      // Ensure the question is a string
      const questionText = question.text ? question.text : question;
      if (typeof questionText !== 'string') {
        console.error('Question is not a string:', question);
        return;
      }
    
      const pageWidth = doc.internal.pageSize.getWidth();
      const textWidth = doc.getStringUnitWidth(questionText) * doc.internal.getFontSize() / doc.internal.scaleFactor;
      const textX = 10;
      doc.text(questionText, textX, y);
      y += 10; // Increase the y-coordinate by 10 for each question
    
      answers[index].forEach((answer) => {
        // Check if answer is an object and has a text property
        if (typeof answer === 'object' && answer.text) {
          // Draw an empty checkbox before the answer
          doc.rect(15, y - 3, 3, 3);
          doc.text(answer.text, 20, y); // Indent the answer
          y += 5; // Increase the y-coordinate by 5 for each answer
        } else {
          console.error('Answer is not a string:', answer);
        }
      });
    });

    // Stop download a file
    //doc.save('test.pdf');

    // Generate the PDF as a Blob instead of saving it
    const blob = new Blob([doc.output('arraybuffer')], { type: 'application/pdf' });
    

    // Create a URL from the Blob
    const url = URL.createObjectURL(blob);

    // Add #toolbar=0 to the URL to hide the toolbar
    const urlWithNoToolbar = url + '#toolbar=1';

    // Store the Blob in the component's state
    setPdfBlob(urlWithNoToolbar);
  };

  return (
    <StyledDiv>
      <StyledBlock>
      {pdfBlob ? (
        // If the PDF has been generated, display it
        <iframe src={pdfBlob} type="application/pdf" width="100%" height="600px" />
      ) : (
        <>
        {isPreviewDisabled() && <p style={{ color: 'red' }}>Please fill out all questions to enable PDF preview</p>}
        <StyledButton onClick={generatePDF} disabled={isPreviewDisabled()}>
          <span style={{ marginRight: '8px' }}>
            <FontAwesomeIcon icon={faEye} />
          </span>
          Preview PDF
        </StyledButton>
        </>
      )}
      </StyledBlock>
    </StyledDiv>
  );
};

export default PreviewPDF;
