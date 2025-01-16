import React, { useEffect, useState } from "react";

interface CircularProgressBarProps {
  maxValue: number;
  currentValue: number;
  size: number;
}

const CircularProgressBar = ({ maxValue, currentValue, size }: CircularProgressBarProps) => {
  const [progress, setProgress] = useState(0);
  const [displayValue, setDisplayValue] = useState(0);

  // 進捗に応じた色を返す関数
  const getProgressColor = (value: number) => {
    const percentage = (value / maxValue) * 100;
    if (percentage <= 50) {
      return "rgb(239, 68, 68)";
    } else if (percentage <= 75) {
      return "rgb(234, 179, 8)";
    } else if(percentage <= 90) {
      return "rgb(34, 197, 94)";
    }
  };

  useEffect(() => {
    let start = progress;
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
  }, [currentValue, maxValue, progress, displayValue]);

  const radius = 50;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (progress / 100) * circumference;

  const textColor = getProgressColor(currentValue);

  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox="0 0 120 120" className="transform -rotate-90">
        <circle cx="60" cy="60" r={radius} stroke="rgb(209, 213, 219)" strokeWidth="10" fill="transparent" />
        <circle
          cx="60"
          cy="60"
          r={radius}
          stroke={getProgressColor(currentValue)}
          strokeWidth="10"
          fill="transparent"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{
            transition: "stroke-dashoffset 0.5s ease, stroke 0.5s ease",
          }}
        />
      </svg>
      <div
        className="absolute font-bold"
        style={{
          fontSize: size / 5,
          color: textColor,
          transition: "color 0.5s ease",
        }}
      >
        {displayValue}
      </div>
    </div>
  );
};

export default CircularProgressBar;
