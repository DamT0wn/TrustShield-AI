import React from "react";

function TranscriptBox({ text, isLoading }) {
  return (
    <div className="card transcript-card">
      <div className="card-header">
        <h3>Live Call Transcript</h3>
        <span className={isLoading ? "status-dot live" : "status-dot idle"}>
          {isLoading ? "listening" : "ready"}
        </span>
      </div>
      <div className="transcript-body">
        <p>{text}</p>
      </div>
    </div>
  );
}

export default TranscriptBox;