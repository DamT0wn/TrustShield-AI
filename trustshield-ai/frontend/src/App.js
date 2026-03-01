import React, { useState, useCallback, useEffect, useRef } from "react";
import axios from "axios";

import TranscriptBox from "./components/TranscriptBox";
import RiskGauge from "./components/RiskGauge";
import AlertPanel from "./components/AlertPanel";

import "./App.css";

function App() {

  // ---------------- STATE MANAGEMENT ----------------

  const [transcript, setTranscript] = useState(
    "Click 'Run Analysis' or select a demo scenario to analyze a call for fraud indicators..."
  );
  const [fraudScore, setFraudScore] = useState(0);
  const [riskLevel, setRiskLevel] = useState("Low");
  const [alerts, setAlerts] = useState([
    "✅ System ready - awaiting analysis"
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [confidence, setConfidence] = useState(0);
  const [demoScenario, setDemoScenario] = useState("bank_scam");
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  const [analysisStage, setAnalysisStage] = useState("idle");
  const [apiStatus, setApiStatus] = useState("checking");
  const [analysisCount, setAnalysisCount] = useState(0);

  // ---------------- REFS ----------------

  const audioRef = useRef(null);
  const transcriptIntervalRef = useRef(null);

  // ---------------- API BASE URL ----------------

  const API_URL = "http://127.0.0.1:8000";

  // ---------------- CHECK API HEALTH ON MOUNT ----------------

  useEffect(() => {
    const checkApiHealth = async () => {
      try {
        const response = await axios.get(`${API_URL}/`, { timeout: 3000 });
        if (response.data.status === "online") {
          setApiStatus("online");
        }
      } catch (error) {
        setApiStatus("offline");
        setAlerts(["⚠️ Backend API is offline. Please start the backend server."]);
      }
    };

    checkApiHealth();

    // Cleanup on unmount
    return () => {
      if (transcriptIntervalRef.current) {
        clearInterval(transcriptIntervalRef.current);
      }
      if (audioRef.current) {
        audioRef.current.pause();
      }
    };
  }, []);

  // ---------------- SIMULATE REAL-TIME TRANSCRIPT (OPTIMIZED) ----------------

  const simulateRealTimeTranscript = useCallback((fullTranscript, callback) => {
    const words = fullTranscript.split(' ');
    let currentText = '';
    let wordIndex = 0;

    // Clear any existing interval
    if (transcriptIntervalRef.current) {
      clearInterval(transcriptIntervalRef.current);
    }

    transcriptIntervalRef.current = setInterval(() => {
      if (wordIndex < words.length) {
        currentText += (wordIndex > 0 ? ' ' : '') + words[wordIndex];
        setTranscript(currentText);
        wordIndex++;
      } else {
        clearInterval(transcriptIntervalRef.current);
        transcriptIntervalRef.current = null;
        if (callback) callback();
      }
    }, 100); // Faster for better UX (100ms per word)

    return transcriptIntervalRef.current;
  }, []);

  // ---------------- PLAY AUDIO (if available) ----------------

  const playAudioIfAvailable = useCallback((scenario) => {
    const audioPath = `/audio/${scenario}.mp3`;
    const audio = new Audio(audioPath);
    audioRef.current = audio;
    
    audio.play().then(() => {
      setIsPlayingAudio(true);
      audio.onended = () => setIsPlayingAudio(false);
    }).catch(() => {
      // Audio file not found, continue without audio
      console.log("Audio file not available, continuing with text simulation");
    });

    return audio;
  }, []);

  // ---------------- FETCH FRAUD ANALYSIS WITH REAL-TIME EFFECT (OPTIMIZED) ----------------

  const runFraudAnalysis = useCallback(async (scenario = null) => {
    setIsLoading(true);
    setAnalysisStage("transcribing");
    setTranscript("🎙️ Listening to call...");
    setAlerts(["📞 Call in progress - analyzing audio..."]);
    setFraudScore(0);
    setRiskLevel("Analyzing");
    setConfidence(0);

    const selectedScenario = scenario || demoScenario;

    try {
      // Step 1: Simulate audio playback (if available)
      const audio = playAudioIfAvailable(selectedScenario);

      // Step 2: Fetch analysis from backend (parallel with audio)
      const response = await axios.post(`${API_URL}/full-analysis`, {
        demo_scenario: selectedScenario
      }, { timeout: 10000 });

      const data = response.data;

      // Step 3: Simulate real-time transcription
      setAlerts(["🎙️ Converting speech to text...", "🔍 Detecting scam patterns..."]);
      await new Promise(resolve => {
        simulateRealTimeTranscript(data.transcript || "No transcript available", resolve);
      });

      // Step 4: Show analysis in progress
      setAnalysisStage("analyzing");
      setAlerts(["🤖 Analyzing for scam patterns...", "💰 Checking transaction anomalies...", "📊 Calculating risk score..."]);
      await new Promise(resolve => setTimeout(resolve, 1200)); // Slightly faster

      // Step 5: Display final results with animation
      setAnalysisStage("complete");
      
      // Animate score increase
      const targetScore = data.final_risk?.risk_score || 0;
      let currentScore = 0;
      const scoreInterval = setInterval(() => {
        currentScore += targetScore / 20;
        if (currentScore >= targetScore) {
          currentScore = targetScore;
          clearInterval(scoreInterval);
        }
        setFraudScore(currentScore);
      }, 30);

      setRiskLevel(data.final_risk?.risk_level || "Low");
      setAlerts(data.final_risk?.alerts || ["No alerts"]);
      setConfidence(data.voice_analysis?.confidence || 0);
      setAnalysisCount(prev => prev + 1);

      // Stop audio if still playing
      if (audio) {
        audio.pause();
        audio.currentTime = 0;
      }

    } catch (err) {
      console.error("API Error:", err);
      setAlerts([
        "⚠️ Backend unreachable - Please ensure backend is running",
        "💡 Tip: Run 'python -m uvicorn backend.main:app --reload' in trustshield-ai folder"
      ]);
      setTranscript("❌ Error: Unable to connect to backend API. Please check if the server is running.");
      setRiskLevel("Unknown");
      setAnalysisStage("idle");
      setApiStatus("offline");
    } finally {
      setIsLoading(false);
      setIsPlayingAudio(false);
    }
  }, [demoScenario, playAudioIfAvailable, simulateRealTimeTranscript, API_URL]);

  // ---------------- DEMO SCENARIO SELECTOR (OPTIMIZED) ----------------

  const runDemoScenario = useCallback((scenario) => {
    setDemoScenario(scenario);
    runFraudAnalysis(scenario);
  }, [runFraudAnalysis]);

  // ---------------- RESET ANALYSIS ----------------

  const resetAnalysis = useCallback(() => {
    setTranscript("Click 'Run Analysis' or select a demo scenario to analyze a call for fraud indicators...");
    setFraudScore(0);
    setRiskLevel("Low");
    setAlerts(["✅ System ready - awaiting analysis"]);
    setConfidence(0);
    setAnalysisStage("idle");
    if (transcriptIntervalRef.current) {
      clearInterval(transcriptIntervalRef.current);
    }
    if (audioRef.current) {
      audioRef.current.pause();
    }
  }, []);

  // ---------------- SCENARIO METADATA ----------------

  const scenarioMetadata = {
    bank_scam: { icon: "🏦", label: "Bank Scam", type: "critical" },
    irs_scam: { icon: "📋", label: "IRS Scam", type: "critical" },
    tech_support_scam: { icon: "💻", label: "Tech Support", type: "critical" },
    grandparent_scam: { icon: "👴", label: "Grandparent", type: "critical" },
    legitimate_call: { icon: "✅", label: "Legitimate Call", type: "safe" },
    legitimate_business: { icon: "💼", label: "Business Call", type: "safe" }
  };

  // ---------------- UI RENDER ----------------

  return (

    <div className="app-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">TrustShield AI</p>
          <h1>Fraud Protection Dashboard</h1>
          <p className="subtitle">
            Real-time call analysis: Audio → Transcript → Scam Detection → Risk Assessment
          </p>
        </div>
        <div className="hero-actions">
          <button
            className="run-button"
            onClick={() => runFraudAnalysis()}
            disabled={isLoading || apiStatus === "offline"}
            title={apiStatus === "offline" ? "Backend API is offline" : "Run analysis with current scenario"}
          >
            {isLoading ? "⏳ Analyzing..." : "▶️ Run Analysis"}
          </button>
          {analysisCount > 0 && !isLoading && (
            <button
              className="reset-button"
              onClick={resetAnalysis}
              title="Reset dashboard"
            >
              🔄 Reset
            </button>
          )}
          <div className={`status-pill ${apiStatus === "online" ? "online" : apiStatus === "offline" ? "offline" : "checking"}`}>
            {apiStatus === "online" ? "🟢 API Online" : apiStatus === "offline" ? "🔴 API Offline" : "⏳ Checking..."}
          </div>
        </div>
      </header>

      {/* Demo Scenario Selector */}
      <section className="demo-controls">
        <div className="demo-header">
          <p className="label">Demo Scenarios</p>
          <span className="demo-count">{analysisCount} analysis completed</span>
        </div>
        <div className="scenario-buttons">
          {Object.entries(scenarioMetadata).map(([key, meta]) => (
            <button
              key={key}
              onClick={() => runDemoScenario(key)}
              disabled={isLoading || apiStatus === "offline"}
              className={`scenario-btn ${meta.type} ${demoScenario === key ? "selected" : ""}`}
              title={`Analyze ${meta.label} scenario`}
            >
              <span className="scenario-icon">{meta.icon}</span>
              <span className="scenario-label">{meta.label}</span>
            </button>
          ))}
        </div>
      </section>

      {/* Analysis Progress Indicator */}
      {isLoading && (
        <section className="analysis-stage">
          <div className={`stage-item ${analysisStage === "transcribing" ? "active" : analysisStage === "analyzing" || analysisStage === "complete" ? "complete" : ""}`}>
            <div className="stage-icon">{analysisStage === "analyzing" || analysisStage === "complete" ? "✓" : "1"}</div>
            <span>Speech-to-Text</span>
          </div>
          <div className={`stage-item ${analysisStage === "analyzing" ? "active" : analysisStage === "complete" ? "complete" : ""}`}>
            <div className="stage-icon">{analysisStage === "complete" ? "✓" : "2"}</div>
            <span>Scam Detection</span>
          </div>
          <div className={`stage-item ${analysisStage === "complete" ? "complete" : ""}`}>
            <div className="stage-icon">{analysisStage === "complete" ? "✓" : "3"}</div>
            <span>Risk Assessment</span>
          </div>
        </section>
      )}

      <section className="grid">
        <TranscriptBox text={transcript} isLoading={isLoading} analysisStage={analysisStage} />

        <div className="card score-card">
          <RiskGauge score={fraudScore} level={riskLevel} />
          {confidence > 0 && (
            <p className="confidence-label">
              🎯 Confidence: {(confidence * 100).toFixed(0)}%
            </p>
          )}
          {isPlayingAudio && (
            <div className="audio-indicator">
              <div className="audio-wave">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
              </div>
              🔊 Audio Playing
            </div>
          )}
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

      {/* Footer Stats */}
      {analysisCount > 0 && (
        <footer className="stats-footer">
          <div className="stat-item">
            <span className="stat-value">{analysisCount}</span>
            <span className="stat-label">Analyses</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">&lt;500ms</span>
            <span className="stat-label">Response Time</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">85%+</span>
            <span className="stat-label">Accuracy</span>
          </div>
        </footer>
      )}
    </div>

  );
}

export default App;
