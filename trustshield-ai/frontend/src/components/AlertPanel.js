import React, { useMemo } from "react";

function AlertPanel({ alerts }) {
  const hasAlerts = useMemo(() => alerts && alerts.length > 0, [alerts]);

  // Categorize alerts by severity
  const categorizedAlerts = useMemo(() => {
    if (!hasAlerts) return [];
    
    return alerts.map(alert => {
      const alertLower = alert.toLowerCase();
      let severity = 'info';
      let icon = '📋';
      
      if (alertLower.includes('critical') || alertLower.includes('🚨')) {
        severity = 'critical';
        icon = '🚨';
      } else if (alertLower.includes('alert') || alertLower.includes('warning') || alertLower.includes('💳')) {
        severity = 'warning';
        icon = '⚠️';
      } else if (alertLower.includes('voice') || alertLower.includes('📞')) {
        severity = 'voice';
        icon = '📞';
      } else if (alertLower.includes('analyzed') || alertLower.includes('📁')) {
        severity = 'success';
        icon = '✅';
      } else if (alert.includes('✅')) {
        severity = 'success';
        icon = '✅';
      }
      
      return { text: alert, severity, icon };
    });
  }, [alerts, hasAlerts]);

  return (
    <div className="card alert-panel">
      <div className="alert-panel-header">
        <h3>Security Alerts</h3>
        {hasAlerts && (
          <span className="alert-count" aria-label={`${alerts.length} alerts`}>
            {alerts.length}
          </span>
        )}
      </div>
      {!hasAlerts ? (
        <div className="no-alerts-container" role="status">
          <span className="no-alerts-icon">🛡️</span>
          <p className="no-alerts">All systems secure</p>
          <p className="no-alerts-subtitle">No threats detected</p>
        </div>
      ) : (
        <ul className="alert-list" role="list" aria-label="Security alerts">
          {categorizedAlerts.map((alert, index) => (
            <li 
              key={`${index}-${alert.text.substring(0, 20)}`} 
              className={`alert-item alert-${alert.severity}`}
              role="listitem"
            >
              <span className="alert-icon" aria-hidden="true">{alert.icon}</span>
              <span className="alert-text">{alert.text}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default React.memo(AlertPanel);
