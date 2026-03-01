import React, { useState, useCallback, useEffect, useRef } from "react";

function TranscriptBox({ text, isLoading, analysisStage }) {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);
  const utteranceRef = useRef(null);

  // Check if speech synthesis is supported
  useEffect(() => {
    if ('speechSynthesis' in window) {
      setSpeechSupported(true);
    }
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const getStatusText = () => {
    if (analysisStage === "transcribing") return "🎙️ transcribing";
    if (analysisStage === "analyzing") return "🤖 analyzing";
    if (analysisStage === "complete") return "✅ complete";
    if (isLoading) return "⏳ processing";
    return "ready";
  };

  const getStatusClass = () => {
    if (analysisStage === "transcribing" || analysisStage === "analyzing") return "status-dot live";
    if (analysisStage === "complete") return "status-dot complete";
    if (isLoading) return "status-dot live";
    return "status-dot idle";
  };

  const handleSpeak = useCallback(() => {
    if (!speechSupported || !text || text.includes("Click 'Run Analysis'")) {
      return;
    }

    // If already speaking, stop
    if (isSpeaking && !isPaused) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      setIsPaused(false);
      return;
    }

    // If paused, resume
    if (isPaused) {
      window.speechSynthesis.resume();
      setIsPaused(false);
      return;
    }

    // Start new speech
    const utterance = new SpeechSynthesisUtterance(text);
    utteranceRef.current = utterance;

    // Configure voice settings
    utterance.rate = 1.0; // Normal speed
    utterance.pitch = 1.0; // Normal pitch
    utterance.volume = 1.0; // Full volume

    // Event handlers
    utterance.onstart = () => {
      setIsSpeaking(true);
      setIsPaused(false);
    };

    utterance.onend = () => {
      setIsSpeaking(false);
      setIsPaused(false);
    };

    utterance.onerror = (event) => {
      console.error('Speech synthesis error:', event);
      setIsSpeaking(false);
      setIsPaused(false);
    };

    // Speak
    window.speechSynthesis.speak(utterance);
  }, [text, isSpeaking, isPaused, speechSupported]);

  const handlePause = useCallback(() => {
    if (isSpeaking && !isPaused) {
      window.speechSynthesis.pause();
      setIsPaused(true);
    }
  }, [isSpeaking, isPaused]);

  const handleStop = useCallback(() => {
    window.speechSynthesis.cancel();
    setIsSpeaking(false);
    setIsPaused(false);
  }, []);

  const hasValidText = text && !text.includes("Click 'Run Analysis'") && !text.includes("🎙️ Listening");

  return (
    <div className="card transcript-card">
      <div className="card-header">
        <h3>Live Call Transcript</h3>
        <div className="transcript-controls">
          {speechSupported && hasValidText && (
            <div className="tts-controls">
              <button
                className={`tts-button ${isSpeaking ? 'speaking' : ''}`}
                onClick={handleSpeak}
                disabled={isLoading}
                title={isSpeaking && !isPaused ? "Stop speaking" : isPaused ? "Resume speaking" : "Listen to transcript"}
                aria-label={isSpeaking && !isPaused ? "Stop speaking" : isPaused ? "Resume speaking" : "Listen to transcript"}
              >
                {isSpeaking && !isPaused ? (
                  <>
                    <span className="tts-icon">🔊</span>
                    <span className="tts-label">Stop</span>
                  </>
                ) : isPaused ? (
                  <>
                    <span className="tts-icon">▶️</span>
                    <span className="tts-label">Resume</span>
                  </>
                ) : (
                  <>
                    <span className="tts-icon">🔊</span>
                    <span className="tts-label">Listen</span>
                  </>
                )}
              </button>
              {isSpeaking && !isPaused && (
                <button
                  className="tts-button tts-pause"
                  onClick={handlePause}
                  title="Pause speaking"
                  aria-label="Pause speaking"
                >
                  <span className="tts-icon">⏸️</span>
                  <span className="tts-label">Pause</span>
                </button>
              )}
            </div>
          )}
          <span className={getStatusClass()}>
            {getStatusText()}
          </span>
        </div>
      </div>
      <div className="transcript-body">
        <p className={analysisStage === "transcribing" ? "typing-effect" : ""}>
          {text}
        </p>
        {isSpeaking && (
          <div className="speaking-indicator">
            <div className="sound-wave">
              <span></span>
              <span></span>
              <span></span>
              <span></span>
              <span></span>
            </div>
            <span className="speaking-text">Speaking...</span>
          </div>
        )}
      </div>
    </div>
  );
}

export default React.memo(TranscriptBox);