import React, { useEffect, useState } from "react";

interface CircularProgressBarProps {
  maxValue: number;
  currentValue: number;
  size: number;
}

const CircularProgressBar: React.FC<CircularProgressBarProps> = ({ maxValue, currentValue, size }) => {
  const [progress, setProgress] = useState(0);
  const [displayValue, setDisplayValue] = useState(0);

  useEffect(() => {
    let start = displayValue;
    const end = (currentValue / maxValue) * 100;
    const duration = 1000;
    const stepTime = Math.abs(Math.floor(duration / Math.abs(end - start)));
    const timer = setInterval(() => {
      if (start < end) {
        start += 1;
      } else {
        start -= 1;
      }
      setProgress(start);
      setDisplayValue(Math.round((start / 100) * maxValue));
      if (start === end) {
        clearInterval(timer);
      }
    }, stepTime);

    return () => clearInterval(timer);
  }, [currentValue, maxValue]);

  const radius = 50;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (currentValue / 100) * circumference;

  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox="0 0 120 120" className="transform -rotate-90">
        <circle cx="60" cy="60" r={radius} stroke="rgb(209, 213, 219)" strokeWidth="10" fill="transparent" />
        <circle cx="60" cy="60" r={radius} stroke="rgb(59, 130, 246)" strokeWidth="10" fill="transparent" strokeDasharray={circumference} strokeDashoffset={offset} style={{ transition: "stroke-dashoffset 0.5s ease" }} />
      </svg>
      <div className="absolute text-xl font-bold" style={{ fontSize: size / 5 }}>
        {displayValue}
      </div>
    </div>
  );
};

export default CircularProgressBar;
