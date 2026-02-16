import React from "react";

function RiskGauge({ score, level }) {
  
  const getColor = () => {
    if (level === "Critical") return "#e74c3c";
    if (level === "High") return "#e67e22";
    if (level === "Medium") return "#f39c12";
    return "#27ae60";
  };

  return (
    <div className="risk-gauge">
      <h3>Risk Assessment</h3>
      <div className="gauge-container">
        <div 
          className="gauge-fill" 
          style={{ 
            width: `${score * 100}%`,
            backgroundColor: getColor()
          }}
        />
      </div>
      <div className="risk-details">
        <p className="risk-score">Score: {(score * 100).toFixed(1)}%</p>
        <p className="risk-level" style={{ color: getColor() }}>
          Level: {level}
        </p>
      </div>
    </div>
  );
}

export default RiskGauge;
