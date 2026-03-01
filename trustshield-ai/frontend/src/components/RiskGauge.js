import React, { useMemo } from "react";

function RiskGauge({ score, level }) {
  
  const getColor = useMemo(() => {
    if (level === "Critical") return "#e74c3c";
    if (level === "High") return "#e67e22";
    if (level === "Medium") return "#f39c12";
    return "#27ae60";
  }, [level]);

  const displayScore = useMemo(() => (score * 100).toFixed(1), [score]);

  return (
    <div className="risk-gauge">
      <h3>Risk Assessment</h3>
      <div className="gauge-container" role="meter" aria-valuenow={score * 100} aria-valuemin="0" aria-valuemax="100" aria-label={`Risk score ${displayScore}%`}>
        <div 
          className="gauge-fill" 
          style={{ 
            width: `${score * 100}%`,
            backgroundColor: getColor,
            transition: 'width 0.6s cubic-bezier(0.4, 0, 0.2, 1), background-color 0.3s ease'
          }}
        />
      </div>
      <div className="risk-details">
        <p className="risk-score">Score: {displayScore}%</p>
        <p className="risk-level" style={{ color: getColor, fontWeight: 700 }}>
          Level: {level}
        </p>
      </div>
    </div>
  );
}

export default React.memo(RiskGauge);
