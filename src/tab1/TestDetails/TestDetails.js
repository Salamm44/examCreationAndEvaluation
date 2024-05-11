import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSave, faEdit, faRedo } from '@fortawesome/free-solid-svg-icons';
import './TestDetails.css';
import InputField from '../../custom-components/InputField';
import 'react-toastify/dist/ReactToastify.css';
import { isFormEmpty } from '../../utils/checkFormEmpty';
import styled from 'styled-components';
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
  height: 480px;
  margin: auto;
  margin-top: 20px;
`;

const TestDetails = () => {
  // initialize form state with data from local storage
  const [form, setForm] = useState(() => {
    const initialForm = {
      organization: localStorage.getItem('organization') || '',
      subject: localStorage.getItem('subject') || '',
      points: localStorage.getItem('points') || '',
      date: localStorage.getItem('date') || '',
      numQuestions: localStorage.getItem('numQuestions') || '',
      numAnswers: localStorage.getItem('numAnswers') || '',
    };

    const savedForm = localStorage.getItem('form');
    return savedForm ? JSON.parse(savedForm) : initialForm;
  });

  // Check if the form is empty
  const formIsEmpty = isFormEmpty(form);

  const [error, setError] = useState({
    organization: false,
    subject: false,
    numQuestions: false,
    numAnswers: false,
    date: false,
  });

  // initialize isSaved state with data from local storage
  const [isSaved, setIsSaved] = useState(() => {
    const saved = localStorage.getItem('isSaved');
    return saved ? JSON.parse(saved) : false;
  });

  const [buttonTitle, setButtonTitle] = useState(
    localStorage.getItem('formValues') ? 'Update' : 'Save',
  );

  useEffect(() => {
    setButtonTitle(isFormValid() ? 'Update' : 'Save');
  }, [form, error]);

const isFormValid = () => {
    const isOrganizationValid = isNaN(form.organization);
    const isSubjectValid = isNaN(form.subject);
    const isPointsValid = !isNaN(form.points) && form.points > 0;
    const isDateValid = form.date !== '';
    const isNumQuestionsValid = !isNaN(form.numQuestions) && form.numQuestions > 0;
    const isNumAnswersValid = !isNaN(form.numAnswers) && form.numAnswers > 0;

    const areFieldsFilled = Object.values(form).every(
        (x) => x !== '' && x !== null && x !== undefined,
    );

    const noErrors = !Object.values(error).some((e) => e);

    return isOrganizationValid && isSubjectValid && isPointsValid && isDateValid && isNumQuestionsValid && isNumAnswersValid && areFieldsFilled && noErrors;
};

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setForm((prevForm) => ({ ...prevForm, [name]: value })); // set the form field value to the input value

    let isError = isFieldInvalid(name, value); // check if the field is invalid

    setError((prevError) => {
      const newError = {
        ...prevError,
        [name]: isError,
      };
      return newError;
    });
  };

  const isFieldInvalid = (name, value) => {
    let isError = false;

    // Check if the value is empty
    isError = value === '';

    return isError;
  };

  const handleSave = (event) => {
    event.preventDefault();

    // validate the form data
    const isError = Object.values(error).some((e) => e);
    if (isError) {
      toast.error('There was an error in the form data.', {
        position: 'bottom-center',
      });
      return;
    }

    // Update localStorage with the form data
    localStorage.setItem('form', JSON.stringify(form));

    // save the isSaved state
    localStorage.setItem('isSaved', true);
    setIsSaved(true);

    // show a proper toast notification
    const successMessage =
      buttonTitle === 'Save'
        ? 'Data saved successfully!'
        : 'Data updated successfully!';
    toast.success(successMessage, {
      position: 'bottom-center',
      autoClose: 1000,
      onClose: () => {
        setIsSaved(true);
        setButtonTitle('Update');
      },
    });
  };

  // Add this function to handle the reset action
  const resetForm = () => {
    // Define the empty form
    const emptyForm = {
      organization: '',
      subject: '',
      points: '',
      date: '',
      numQuestions: '',
      numAnswers: '',
    };

    // Reset the form state
    setForm(emptyForm);

    // Reset the error state
    setError({
      organization: false,
      subject: false,
      numQuestions: false,
      numAnswers: false,
    });

    // Remove the form data from local storage
    localStorage.removeItem('form');

    // reset the isSaved state
    localStorage.setItem('isSaved', false);
    setIsSaved(false);
  };

  
  return (
    <>
      <StyledForm>
        <div className="creation-container">
          <InputField
            type="text"
            name="organization"
            placeholder="Enter organization"
            initialValue={form.organization}
            propValue={form.organization}
            error={error.organization}
            handleInputChange={handleInputChange}
          />
          <InputField
            type="text"
            name="subject"
            placeholder="Enter Test Subject"
            initialValue={form.subject}
            propValue={form.subject}
            error={error.subject}
            handleInputChange={handleInputChange}
          />
          <InputField
            type="number"
            name="points"
            placeholder="Enter the Total Points"
            initialValue={form.points}
            propValue={form.points}
            handleInputChange={handleInputChange}
          />
          <InputField
            type="date"
            name="date"
            placeholder="Enter Date"
            initialValue={form.date}
            propValue={form.date}
            handleInputChange={handleInputChange}
          />

          <InputField
            className="input-field-num-qurestions"
            type="number"
            name="numQuestions"
            placeholder="Number of Questions"
            initialValue={form.numQuestions}
            propValue={form.numQuestions}
            handleInputChange={handleInputChange}
            disabled={isSaved}
            hint="Update question count on Test Questions page"
          />

          <InputField
            className="input-field-num-answers"
            type="number"
            name="numAnswers"
            placeholder="Number of Answers"
            initialValue={form.numAnswers}
            propValue={form.numAnswers}
            handleInputChange={handleInputChange}
            disabled={isSaved}
            hint="Update answer count on Test Questions page"
          />

          <div className="control-buttons-container">
            <button
              type="button"
              className="creation-button reset-button"
              onClick={resetForm}
            >
              <FontAwesomeIcon icon={faRedo} /> Reset
            </button>

            <button
              type="submit"
              className="creation-button"
              onClick={handleSave}
              disabled={!isFormValid() || formIsEmpty}
            >
              <FontAwesomeIcon icon={isSaved ? faEdit : faSave} />{' '}
              {isSaved ? 'Update' : 'Save'}
            </button>
          </div>
        </div>
      </StyledForm>
    </>
  );
};

export default TestDetails;
