import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronLeft, faChevronRight } from '@fortawesome/free-solid-svg-icons';
import Creation from './tab1/Creation'; 

const tabs = ['Creation', 'Modify', 'Preview PDF', 'Generate PDF'];

const Tab1 = () => {
  const [activePoint, setActivePoint] = useState(tabs[0]);

  const goLeft = () => {
    const currentIndex = tabs.indexOf(activePoint);
    if (currentIndex > 0) {
      setActivePoint(tabs[currentIndex - 1]);
    }
  };

  const goRight = () => {
    const currentIndex = tabs.indexOf(activePoint);
    if (currentIndex < tabs.length - 1) {
      setActivePoint(tabs[currentIndex + 1]);
    }
  };

  return (
    <>
      <div className="progress-container">
        <div className="arrow left-arrow" onClick={goLeft}><FontAwesomeIcon icon={faChevronLeft} /></div>
        <div className="progress-line">
          {tabs.map(point => (
            <div
              key={point}
              className={`progress-step ${activePoint === point ? 'active' : ''}`}
              onClick={() => setActivePoint(point)}
            >
              {activePoint === point && <div>{point}</div>}
            </div>
          ))}
        </div>
        <div className="arrow right-arrow" onClick={goRight}><FontAwesomeIcon icon={faChevronRight} /></div>
      </div>
      {activePoint === 'Creation' && <Creation />}
    </>
  );
}

export default Tab1;
