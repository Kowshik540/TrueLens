import { useState, useEffect } from "react";

const styles = `
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg:        #08080F;
    --bg2:       #0F0F1C;
    --bg3:       #161625;
    --red:       #E63946;
    --gold:      #F4A261;
    --teal:      #2EC4B6;
    --yellow:    #FFB703;
    --white:     #F0F0F5;
    --gray:      #6B6B88;
    --border:    #1E1E32;
  }

  body {
    background: var(--bg);
    color: var(--white);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
  }

  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
      0deg, transparent, transparent 2px,
      rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px
    );
    pointer-events: none;
    z-index: 9999;
  }

  .app { max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }

  .header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    margin-bottom: 3rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
  }

  .logo { display: flex; flex-direction: column; gap: 0; }

  .logo-true {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4.5rem; line-height: 0.9;
    color: var(--white); letter-spacing: 2px;
  }

  .logo-lens {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4.5rem; line-height: 0.9;
    color: var(--red); letter-spacing: 2px;
  }

  .logo-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem; color: var(--gray);
    letter-spacing: 3px; text-transform: uppercase; margin-top: 0.5rem;
  }

  .domain-badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem; color: var(--gold);
    border: 1px solid var(--gold);
    padding: 0.35rem 0.7rem;
    letter-spacing: 2px; text-transform: uppercase; opacity: 0.8;
  }

  .input-section { margin-bottom: 2.5rem; }

  .input-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem; letter-spacing: 3px;
    color: var(--gray); text-transform: uppercase;
    margin-bottom: 0.75rem;
    display: flex; align-items: center; gap: 0.5rem;
  }

  .input-label::before {
    content: ''; display: inline-block;
    width: 8px; height: 8px; background: var(--red);
  }

  .tab-row { display: flex; gap: 0; margin-bottom: 0; }

  .tab {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem; letter-spacing: 2px;
    padding: 0.5rem 1.2rem;
    background: var(--bg2); color: var(--gray);
    border: 1px solid var(--border);
    cursor: pointer; transition: all 0.15s; text-transform: uppercase;
  }

  .tab:first-child { border-right: none; }

  .tab.active { background: var(--red); color: var(--white); border-color: var(--red); }

  textarea, input[type="text"] {
    width: 100%;
    background: var(--bg2);
    border: 1px solid var(--border);
    border-top: 2px solid var(--red);
    color: var(--white);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    padding: 1rem 1.2rem;
    outline: none; resize: none;
    transition: border-color 0.2s; line-height: 1.6;
  }

  textarea { height: 140px; }
  input[type="text"] { height: 52px; }

  textarea:focus, input[type="text"]:focus {
    border-color: var(--red); background: var(--bg3);
  }

  textarea::placeholder, input::placeholder { color: var(--gray); opacity: 0.5; }

  .analyze-btn {
    width: 100%; margin-top: 0.75rem; padding: 1rem;
    background: var(--red); color: var(--white); border: none;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.3rem; letter-spacing: 4px;
    cursor: pointer; transition: all 0.2s;
    display: flex; align-items: center; justify-content: center; gap: 0.75rem;
  }

  .analyze-btn:hover:not(:disabled) { background: #FF4655; transform: translateY(-1px); }
  .analyze-btn:disabled { background: var(--bg3); color: var(--gray); cursor: not-allowed; }

  .btn-dot {
    width: 8px; height: 8px;
    background: var(--white); border-radius: 50%;
    animation: pulse 1s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.8); }
  }

  .detectives-section { margin-bottom: 2.5rem; }

  .section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem; letter-spacing: 3px;
    color: var(--gray); text-transform: uppercase;
    margin-bottom: 1rem;
    display: flex; align-items: center; gap: 0.5rem;
  }

  .section-label::before {
    content: ''; display: inline-block;
    width: 8px; height: 8px; background: var(--teal);
  }

  .detectives-grid { display: flex; flex-direction: column; gap: 0.5rem; }

  .detective-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--border);
    padding: 1rem 1.2rem;
    display: flex; align-items: center; gap: 1rem;
    transition: all 0.3s ease;
    position: relative; overflow: hidden;
  }

  .detective-card.idle    { border-left-color: var(--border); }
  .detective-card.working { border-left-color: var(--gold); background: var(--bg3); animation: cardPulse 1.5s ease-in-out infinite; }
  .detective-card.done    { border-left-color: var(--teal); }
  .detective-card.flagged { border-left-color: var(--red); }

  @keyframes cardPulse {
    0%, 100% { box-shadow: 0 0 0 rgba(244,162,97,0); }
    50%       { box-shadow: 0 0 15px rgba(244,162,97,0.1); }
  }

  .detective-card.working::after {
    content: ''; position: absolute; left: 0; top: 0;
    height: 100%; width: 40%;
    background: linear-gradient(90deg, transparent, rgba(244,162,97,0.05), transparent);
    animation: shimmer 1.5s infinite;
  }

  @keyframes shimmer {
    0%   { transform: translateX(-100%); }
    100% { transform: translateX(350%); }
  }

  .detective-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem; line-height: 1;
    color: var(--border); min-width: 2.5rem; transition: color 0.3s;
  }

  .detective-card.working .detective-num { color: var(--gold); }
  .detective-card.done    .detective-num { color: var(--teal); }
  .detective-card.flagged .detective-num { color: var(--red); }

  .detective-info { flex: 1; }

  .detective-name {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem; font-weight: 600;
    letter-spacing: 1px; color: var(--white); margin-bottom: 0.2rem;
  }

  .detective-status {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem; color: var(--gray); letter-spacing: 1px;
  }

  .detective-card.working .detective-status { color: var(--gold); }
  .detective-card.done    .detective-status { color: var(--teal); }
  .detective-card.flagged .detective-status { color: var(--red); }

  .detective-icon { font-size: 1.1rem; min-width: 1.5rem; text-align: center; }

  .verdict-section { animation: fadeUp 0.6s ease forwards; }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .verdict-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.5rem 1.5rem 1.2rem;
    background: var(--bg2);
    border: 1px solid var(--border); border-bottom: none;
    border-top: 3px solid var(--red);
  }

  .verdict-header.real       { border-top-color: var(--teal); }
  .verdict-header.misleading { border-top-color: var(--yellow); }
  .verdict-header.fake       { border-top-color: var(--red); }

  .verdict-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem; letter-spacing: 3px;
    color: var(--gray); text-transform: uppercase; margin-bottom: 0.4rem;
  }

  .verdict-text {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem; line-height: 1; letter-spacing: 2px;
  }

  .verdict-text.real       { color: var(--teal); }
  .verdict-text.misleading { color: var(--yellow); }
  .verdict-text.fake       { color: var(--red); }

  .score-display { text-align: right; }

  .score-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem; line-height: 1; color: var(--white);
  }

  .score-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem; color: var(--gray);
    letter-spacing: 2px; text-transform: uppercase;
  }

  .score-bar-wrap {
    background: var(--bg2);
    border: 1px solid var(--border); border-top: none; border-bottom: none;
    height: 6px;
  }

  .score-bar-track { height: 6px; background: var(--bg3); width: 100%; }

  .score-bar-fill { height: 100%; transition: width 1.5s cubic-bezier(0.4,0,0.2,1); }

  .evidence-grid {
    background: var(--bg2);
    border: 1px solid var(--border); border-top: none;
    display: grid; grid-template-columns: repeat(3, 1fr);
  }

  .evidence-cell { padding: 1.2rem 1.5rem; border-right: 1px solid var(--border); }
  .evidence-cell:last-child { border-right: none; }

  .evidence-cell-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem; letter-spacing: 3px;
    color: var(--gray); text-transform: uppercase; margin-bottom: 0.4rem;
  }

  .evidence-cell-score { font-family: 'Bebas Neue', sans-serif; font-size: 2rem; line-height: 1; margin-bottom: 0.2rem; }
  .evidence-cell-max   { font-family: 'IBM Plex Mono', monospace; font-size: 0.6rem; color: var(--gray); }

  .flags-box {
    background: var(--bg2);
    border: 1px solid var(--border); border-top: none; padding: 1.5rem;
  }

  .flags-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem; letter-spacing: 3px;
    color: var(--gray); text-transform: uppercase; margin-bottom: 0.75rem;
  }

  .flag-item {
    display: flex; align-items: flex-start; gap: 0.6rem; margin-bottom: 0.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem; color: var(--white); opacity: 0.8; line-height: 1.5;
  }

  .flag-dot { width: 6px; height: 6px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
  .flag-dot.red  { background: var(--red); }
  .flag-dot.gold { background: var(--gold); }
  .flag-dot.teal { background: var(--teal); }

  .explanation-box {
    background: var(--bg2);
    border: 1px solid var(--border); border-top: none; padding: 1.5rem;
  }

  .explanation-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem; letter-spacing: 3px;
    color: var(--gray); text-transform: uppercase; margin-bottom: 0.75rem;
  }

  .explanation-text {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem; color: var(--white); line-height: 1.7; opacity: 0.85;
  }

  .reset-btn {
    width: 100%; margin-top: 1rem; padding: 0.75rem;
    background: transparent; color: var(--gray);
    border: 1px solid var(--border);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem; letter-spacing: 3px;
    cursor: pointer; text-transform: uppercase; transition: all 0.2s;
  }

  .reset-btn:hover { border-color: var(--gray); color: var(--white); }

  .error-box {
    background: rgba(230,57,70,0.08);
    border: 1px solid var(--red); padding: 1rem 1.2rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem; color: var(--red); margin-top: 0.75rem;
  }
`;

// ─── Mock API (swap with real backend later) ──────────────────
async function analyzeArticle(inputType, content) {
  const res = await fetch("http://localhost:8000/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input_type: inputType, content })
  });
  return res.json();
}

// ─── Detective Config ─────────────────────────────────────────
const DETECTIVES = [
  { num: "01", name: "Claim Extractor",  icon: "🔍", desc: "Extracting verifiable claims from article" },
  { num: "02", name: "Fact Verifier",    icon: "🌐", desc: "Searching trusted sources for each claim" },
  { num: "03", name: "Image Forensics",  icon: "🖼",  desc: "Scraping and analyzing image metadata" },
  { num: "04", name: "Language Analyst", icon: "📝", desc: "Scanning writing for manipulation patterns" },
  { num: "05", name: "Judge",            icon: "⚖️", desc: "Weighing all evidence for final verdict" },
];

// ─── DetectiveCard ────────────────────────────────────────────
function DetectiveCard({ detective, status }) {
  const statusText = {
    idle:    "Waiting...",
    working: detective.desc + "...",
    done:    "Complete",
    flagged: "Issues found",
  };

  return (
    <div className={`detective-card ${status}`}>
      <div className="detective-num">{detective.num}</div>
      <div className="detective-info">
        <div className="detective-name">{detective.name}</div>
        <div className="detective-status">{statusText[status]}</div>
      </div>
      <div className="detective-icon">{detective.icon}</div>
    </div>
  );
}

// ─── VerdictPanel ─────────────────────────────────────────────
function VerdictPanel({ result, onReset }) {
  const [displayScore, setDisplayScore] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => setDisplayScore(result.total_score), 300);
    return () => clearTimeout(timer);
  }, [result.total_score]);

  const verdictClass = result.verdict_type;

  const scoreColor = {
    real:       "#2EC4B6",
    misleading: "#FFB703",
    fake:       "#E63946",
  }[verdictClass];

  return (
    <div className="verdict-section">
      <div className={`verdict-header ${verdictClass}`}>
        <div>
          <div className="verdict-label">Final Verdict</div>
          <div className={`verdict-text ${verdictClass}`}>{result.verdict}</div>
        </div>
        <div className="score-display">
          <div className="score-num">{displayScore}</div>
          <div className="score-label">/ 100 Score</div>
        </div>
      </div>

      <div className="score-bar-wrap">
        <div className="score-bar-track">
          <div className="score-bar-fill" style={{ width: `${displayScore}%`, background: scoreColor }} />
        </div>
      </div>

      <div className="evidence-grid">
        {[
          { label: "Fact Check",      score: result.fact_check_score, max: 40, color: "#F4A261" },
          { label: "Image Forensics", score: result.image_score,       max: 30, color: "#E63946" },
          { label: "Language",        score: result.language_score,    max: 30, color: "#2EC4B6" },
        ].map(e => (
          <div className="evidence-cell" key={e.label}>
            <div className="evidence-cell-label">{e.label}</div>
            <div className="evidence-cell-score" style={{ color: e.color }}>{e.score}</div>
            <div className="evidence-cell-max">out of {e.max} pts</div>
          </div>
        ))}
      </div>

      <div className="flags-box">
        <div className="flags-label">Evidence Found</div>
        {result.flags.map((f, i) => (
          <div className="flag-item" key={i}>
            <div className={`flag-dot ${f.type}`} />
            {f.text}
          </div>
        ))}
      </div>

      <div className="explanation-box">
        <div className="explanation-label">Verdict Explanation</div>
        <div className="explanation-text">{result.explanation}</div>
      </div>

      <button className="reset-btn" onClick={onReset}>
        ↩ Investigate Another Article
      </button>
    </div>
  );
}

// ─── Main App ─────────────────────────────────────────────────
export default function TrueLens() {
  const [tab, setTab]                         = useState("text");
  const [input, setInput]                     = useState("");
  const [phase, setPhase]                     = useState("idle");
  const [detectiveStates, setDetectiveStates] = useState(DETECTIVES.map(() => "idle"));
  const [result, setResult]                   = useState(null);
  const [error, setError]                     = useState("");

  const runDetectives = async () => {
    const delays = [800, 1600, 2400, 3200, 3800];
    for (let i = 0; i < DETECTIVES.length; i++) {
      await new Promise(r => setTimeout(r, delays[i]));
      setDetectiveStates(prev => {
        const next = [...prev];
        if (i > 0) next[i - 1] = "done";
        next[i] = "working";
        return next;
      });
    }
    await new Promise(r => setTimeout(r, 600));
    setDetectiveStates(DETECTIVES.map(() => "done"));
  };

  const handleAnalyze = async () => {
    if (!input.trim()) return;
    setError("");
    setPhase("analyzing");
    setDetectiveStates(DETECTIVES.map(() => "idle"));
    setResult(null);

    try {
      const [apiResult] = await Promise.all([
        analyzeArticle(tab, input.trim()),
        runDetectives(),
      ]);

      setDetectiveStates(prev => {
        const next = [...prev];
        if (apiResult.fact_check_score < 20) next[1] = "flagged";
        if (apiResult.image_score       < 15) next[2] = "flagged";
        if (apiResult.language_score    < 15) next[3] = "flagged";
        next[4] = "flagged";
        return next;
      });

      setResult(apiResult);
      setPhase("done");
    } catch (err) {
      setError("Connection failed. Make sure the backend server is running on port 8000.");
      setPhase("idle");
      setDetectiveStates(DETECTIVES.map(() => "idle"));
    }
  };

  const handleReset = () => {
    setPhase("idle");
    setInput("");
    setResult(null);
    setError("");
    setDetectiveStates(DETECTIVES.map(() => "idle"));
  };

  const isAnalyzing = phase === "analyzing";
  const isDone      = phase === "done";

  return (
    <>
      <style>{styles}</style>
      <div className="app">

        <header className="header">
          <div className="logo">
            <div>
              <span className="logo-true">TRUE</span>
              <span className="logo-lens">LENS</span>
            </div>
            <div className="logo-tag">Fake News Forensics Agent</div>
          </div>
          {/* <div className="domain-badge">Agentic AI · Domain 5.1</div> */}
        </header>

        {!isDone && (
          <div className="input-section">
            <div className="input-label">Submit for Investigation</div>
            <div className="tab-row">
              <button className={`tab ${tab === "text" ? "active" : ""}`} onClick={() => setTab("text")}>
                Article Text
              </button>
              <button className={`tab ${tab === "url" ? "active" : ""}`} onClick={() => setTab("url")}>
                Article URL
              </button>
            </div>

            {tab === "text" ? (
              <textarea
                placeholder="Paste the full article text here..."
                value={input}
                onChange={e => setInput(e.target.value)}
                disabled={isAnalyzing}
              />
            ) : (
              <input
                type="text"
                placeholder="https://example.com/article"
                value={input}
                onChange={e => setInput(e.target.value)}
                disabled={isAnalyzing}
              />
            )}

            {error && <div className="error-box">⚠ {error}</div>}

            <button
              className="analyze-btn"
              onClick={handleAnalyze}
              disabled={isAnalyzing || !input.trim()}
            >
              {isAnalyzing
                ? <><div className="btn-dot" /> Investigating...</>
                : "Begin Investigation"
              }
            </button>
          </div>
        )}

        {(isAnalyzing || isDone) && (
          <div className="detectives-section">
            <div className="section-label">Investigation Pipeline</div>
            <div className="detectives-grid">
              {DETECTIVES.map((d, i) => (
                <DetectiveCard key={d.num} detective={d} status={detectiveStates[i]} />
              ))}
            </div>
          </div>
        )}

        {isDone && result && (
          <VerdictPanel result={result} onReset={handleReset} />
        )}

      </div>
    </>
  );
}
