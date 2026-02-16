import React from "react";

function AlertPanel({ alerts }) {
  return (
    <div className="card alert-panel">
      <h3>Security Alerts</h3>
      {alerts.length === 0 ? (
        <p className="no-alerts">No alerts at this time</p>
      ) : (
        <ul className="alert-list">
          {alerts.map((alert, index) => (
            <li key={index} className="alert-item">
              {alert}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default AlertPanel;
