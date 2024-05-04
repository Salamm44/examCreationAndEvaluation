import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faChevronLeft,
  faChevronRight,
} from '@fortawesome/free-solid-svg-icons';
import Creation from './tab1/Creation';

const tabs = ['Test details', 'Test Questions', 'Preview PDF', 'Generate PDF'];

const Tab1 = () => {
  const [activePoint, setActivePoint] = useState(tabs[0]);
  const [visitedPoints, setVisitedPoints] = useState([]);

  const goRight = () => {
    const currentIndex = tabs.indexOf(activePoint);
    if (currentIndex < tabs.length - 1) {
      if (!visitedPoints.includes(activePoint)) {
        setVisitedPoints((prevVisitedPoints) => [
          ...prevVisitedPoints,
          activePoint,
        ]);
      }
      const nextPoint = tabs[currentIndex + 1];
      setActivePoint(nextPoint);
    }
  };

  const goLeft = () => {
    const currentIndex = tabs.indexOf(activePoint);
    if (currentIndex > 0) {
      if (!visitedPoints.includes(activePoint)) {
        setVisitedPoints((prevVisitedPoints) => [
          ...prevVisitedPoints,
          activePoint,
        ]);
      }
      setActivePoint(tabs[currentIndex - 1]);
    }
  };

  return (
    <>
      <div className="progress-container">
        <div className="arrow left-arrow" onClick={goLeft}>
          <FontAwesomeIcon icon={faChevronLeft} />
        </div>
        <div className="progress-line">
          {tabs.map((point) => (
            <div
              key={point}
              className={`progress-step ${
                activePoint === point ? 'active' : ''
              }`}
              onClick={() => {
                if (!visitedPoints.includes(activePoint)) {
                  setVisitedPoints((prevVisitedPoints) => [
                    ...prevVisitedPoints,
                    activePoint,
                  ]);
                }
                setActivePoint(point);
              }}
            >
              {(activePoint === point || visitedPoints.includes(point)) && (
                <div>{point}</div>
              )}
            </div>
          ))}
        </div>
        <div className="arrow right-arrow" onClick={goRight}>
          <FontAwesomeIcon icon={faChevronRight} />
        </div>
      </div>
      {activePoint === 'Test details' && <Creation />}
    </>
  );
};

export default Tab1;
