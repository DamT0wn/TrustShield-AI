import React, { useState } from "react";
import axios from "axios";

import TranscriptBox from "./components/TranscriptBox";
import RiskGauge from "./components/RiskGauge";
import AlertPanel from "./components/AlertPanel";

import "./App.css";

function App() {

  // ---------------- STATE MANAGEMENT ----------------

  const [transcript, setTranscript] = useState(
    "Caller is requesting an urgent wire transfer and asks to bypass standard verification steps."
  );
  const [fraudScore, setFraudScore] = useState(0.32);
  const [riskLevel, setRiskLevel] = useState("Medium");
  const [alerts, setAlerts] = useState([
    "Unverified recipient added within last 24 hours",
    "Voice pattern matches prior scam script"
  ]);
  const [isLoading, setIsLoading] = useState(false);

  // ---------------- API BASE URL ----------------

  const API_URL = "http://127.0.0.1:8000";

  // ---------------- FETCH FRAUD ANALYSIS ----------------

  const runFraudAnalysis = async () => {
    setIsLoading(true);

    try {
      const [callRes, txRes, finalRes] = await Promise.all([
        axios.post(`${API_URL}/analyze-call`),
        axios.post(`${API_URL}/transaction-risk`),
        axios.post(`${API_URL}/final-risk`)
      ]);

      const nextTranscript = callRes.data?.transcript || transcript;
      const nextFraud = callRes.data?.fraud_probability ?? finalRes.data?.risk_score ?? 0;
      const nextLevel = finalRes.data?.risk_level || "Low";
      const nextAlerts = [];

      if (txRes.data?.transaction_flag === -1) {
        nextAlerts.push("Anomalous transaction behavior detected");
      }

      if (nextFraud >= 0.7) {
        nextAlerts.push("High voice fraud probability detected");
      }

      if (nextLevel === "Critical") {
        nextAlerts.push("Fraud detected - auto block engaged");
      }

      setTranscript(nextTranscript);
      setFraudScore(nextFraud);
      setRiskLevel(nextLevel);
      setAlerts(nextAlerts.length > 0 ? nextAlerts : ["Monitoring - no active alerts"]);
    } catch (err) {
      console.error("API Error:", err);
      setAlerts(["Backend unreachable - showing sample data"]);
    } finally {
      setIsLoading(false);
    }
  };

  // ---------------- UI RENDER ----------------

  return (

    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">TrustShield AI</p>
          <h1>Fraud Protection Dashboard</h1>
          <p className="subtitle">
            Real-time signal fusion across voice, transaction, and behavioral risk.
          </p>
        </div>
        <div className="hero-actions">
          <button
            className="run-button"
            onClick={runFraudAnalysis}
            disabled={isLoading}
          >
            {isLoading ? "Analyzing..." : "Run Analysis"}
          </button>
          <div className="status-pill">
            Live API: {API_URL}
          </div>
        </div>
      </header>

      <section className="grid">
        <TranscriptBox text={transcript} isLoading={isLoading} />

        <div className="card score-card">
          <RiskGauge score={fraudScore} level={riskLevel} />
        </div>

        <div className="card risk-banner">
          <div>
            <p className="label">Current Risk Level</p>
            <h2>{riskLevel}</h2>
          </div>
          <div className="risk-score-chip">
            {(fraudScore * 100).toFixed(1)}%
          </div>
        </div>

        <AlertPanel alerts={alerts} />
      </section>
    </div>

  );
}

export default App;
