import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSave } from '@fortawesome/free-solid-svg-icons';
import './Creation.css';
import InputField from '../custom-components/InputField';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import TestToast from '../toast-test';

const Creation = () => {
    const initialForm = {
        organization: '',
        subject: '',
        points: '',
        date: ''
    };
    
    const [form, setForm] = useState(initialForm);

    const [error, setError] = useState({
        organization: false,
        subject: false
    });

    const [savedData, setSavedData] = useState(null);

    const isFormValid = () => {
        return Object.values(form).every(x => x !== '' && x !== null && x !== undefined) && !Object.values(error).some(e => e);
    }

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        const isError = (name === 'organization' || name === 'subject') && (/^\d+$/.test(value) || value.length < 3);
    
        setForm(prevForm => ({
            ...prevForm,
            [name]: value
        }));
    
        setError(prevError => ({
            ...prevError,
            [name]: isError
        }));
    }

    const saveData = (event) => {
        event.preventDefault();
    
        // validate the form data
        const isError = Object.values(error).some(e => e);
        if (isError) {
            // show an error toast notification
            toast.error('There was an error in the form data.', {
                position: "bottom-center"
            });
            return;
        }
    
        // save the form data
        setSavedData(form);
    
        // show a success toast notification
        toast.success('Data saved successfully!', {
            position: "bottom-center"
        });
    }

    return (
        <div className="creation-container">
            <ToastContainer />
            <h1 className="h1-style">Test Details</h1>
            <form className="creation-form">
                <InputField 
                    type="text" 
                    name="organization" 
                    placeholder="Organization's Name" 
                    value={form.organization} 
                    error={error.organization} 
                    handleInputChange={handleInputChange} 
                />
                <InputField 
                    type="text" 
                    name="subject" 
                    placeholder="Test Subject" 
                    value={form.subject} 
                    error={error.subject} 
                    handleInputChange={handleInputChange} 
                />
                <InputField 
                    type="number" 
                    name="points" 
                    placeholder="Total Points" 
                    value={form.points} 
                    handleInputChange={handleInputChange} 
                />
                <InputField 
                    type="date" 
                    name="date" 
                    value={form.date} 
                    handleInputChange={handleInputChange} 
                />
                <button type="submit" className="creation-button" onClick={saveData}  disabled={!isFormValid()}>
                    <FontAwesomeIcon icon={faSave} /> Save
                </button>
            </form>
        </div>
    );
}
export default Creation