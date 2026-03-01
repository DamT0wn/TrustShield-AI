import React from "react";

function TranscriptBox({ text, isLoading, analysisStage }) {
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

  return (
    <div className="card transcript-card">
      <div className="card-header">
        <h3>Live Call Transcript</h3>
        <span className={getStatusClass()}>
          {getStatusText()}
        </span>
      </div>
      <div className="transcript-body">
        <p className={analysisStage === "transcribing" ? "typing-effect" : ""}>
          {text}
        </p>
      </div>
    </div>
  );
}

export default TranscriptBox;