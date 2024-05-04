import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSave, faEdit, faRedo } from '@fortawesome/free-solid-svg-icons';
import './TestDetails.css';
import InputField from '../custom-components/InputField';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import AddQuestions from './TestQuestions';
import { isFormEmpty } from '../utils/checkFormEmpty';

const TestDetails = () => {
  const initialForm = {
    organization: localStorage.getItem('organization') || '',
    subject: localStorage.getItem('subject') || '',
    points: localStorage.getItem('points') || '',
    date: localStorage.getItem('date') || '',
    numQuestions: localStorage.getItem('numQuestions') || '',
    numAnswers: localStorage.getItem('numAnswers') || '',
  };

  // initialize form state with data from local storage
  const [form, setForm] = useState(() => {
    const savedForm = localStorage.getItem('form');
    if (savedForm) {
      return JSON.parse(savedForm);
    } else {
      return initialForm;
    }
  });
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

  const [savedData, setSavedData] = useState(null);
  const [buttonTitle, setButtonTitle] = useState(
    localStorage.getItem('formValues') ? 'Update' : 'Save',
  );

  const isFormValid = () => {
    return (
      Object.values(form).every(
        (x) => x !== '' && x !== null && x !== undefined,
      ) && !Object.values(error).some((e) => e)
    );
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    let isError =
      (name === 'organization' || name === 'subject') &&
      (/^\d+$/.test(value) || value.length < 3);

      if (name === 'date') {
        isError = value === '' || value === 'tt.mm.jjjj'; // date should not be empty or placeholder
        if (!isError) {
          const date = new Date(value);
          const now = new Date();
          isError = date < now; // date should not be in the past
        }
      }

    setForm((prevForm) => ({
      ...prevForm,
      [name]: value,
    }));

    setError((prevError) => ({
      ...prevError,
      [name]: isError,
    }));
  };

  const saveData = (event) => {
    event.preventDefault();

    // validate the form data
    const isError = Object.values(error).some((e) => e);
    if (isError) {
      // show an error toast notification
      toast.error('There was an error in the form data.', {
        position: 'bottom-center',
      });
      return;
    }

    // save the form data
    setSavedData(form);

    // save the isSaved state
    localStorage.setItem('isSaved', true);
    setIsSaved(true);

    // show a proper toast notification
    if (buttonTitle === 'Save') {
      toast.success('Data saved successfully!', {
        position: 'bottom-center',
        autoClose: 1000,
        onClose: () => {
          setIsSaved(true);
          setButtonTitle('Update');
        },
      });
    } else {
      toast.warn('Data updated successfully!', {
        position: 'bottom-center',
        autoClose: 1000,
        onClose: () => {
          setIsSaved(true);
          setButtonTitle('Update');
        },
      });
    }
  };

  // save form data in local storage when form state changes
  useEffect(() => {
    localStorage.setItem('form', JSON.stringify(form));
  }, [form]);

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

  const formIsEmpty = isFormEmpty(form);

  return (
    <div className="creation-container">
      <ToastContainer />
      <h1 className="h1-style">Test Details</h1>
      <form className="creation-form">
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
          placeholder="Test Subject"
          initialValue={form.subject}
          propValue={form.subject}
          error={error.subject}
          handleInputChange={handleInputChange}
        />
        <InputField
          type="number"
          name="points"
          placeholder="Total Points"
          initialValue={form.points}
          propValue={form.points}
          handleInputChange={handleInputChange}
        />
        <InputField
          type="date"
          name="date"
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
        />

        <InputField
          className="input-field-num-answers"
          type="number"
          name="numAnswers"
          placeholder="Number of Answers"
          initialValue={form.numAnswers}
          propValue={form.numAnswers}
          handleInputChange={handleInputChange}
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
            onClick={saveData}
            disabled={!isFormValid() || (isSaved && formIsEmpty)}
          >
            <FontAwesomeIcon icon={isSaved ? faEdit : faSave} />{' '}
            {isSaved ? 'Update' : 'Save'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TestDetails;
