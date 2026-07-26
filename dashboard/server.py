"""
Quantitative Savings Dashboard & Telemetry API Server
Serves static dashboard UI and provides REST / WebSocket telemetry streams
comparing Baseline operation against Eco-Loop AI closed-loop strategy.
"""

import os
import sys

# Ensure root directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse

from agent.orchestrator import ClosedLoopOrchestrator

app = FastAPI(title="Eco-Loop Building Agents Dashboard", version="1.0.0")

# Global Orchestrator & Telemetry Cache
orchestrator = ClosedLoopOrchestrator()
simulation_results = None

@app.get("/api/telemetry")
def get_telemetry_data():
    """Returns baseline history, ecoloop history, agent thoughts, and quantitative summary."""
    global simulation_results
    if not orchestrator.collector.baseline_history:
        simulation_results = orchestrator.run_full_24h_cycle()
    return {
        "summary": orchestrator.collector.get_quantitative_summary(),
        "baseline_history": orchestrator.collector.baseline_history,
        "ecoloop_history": orchestrator.collector.ecoloop_history,
        "agent_thoughts": orchestrator.collector.agent_thought_logs
    }

@app.post("/api/run-simulation")
def trigger_simulation():
    """Triggers a fresh 24-hour closed-loop simulation run."""
    global simulation_results
    orchestrator.collector.baseline_history.clear()
    orchestrator.collector.ecoloop_history.clear()
    orchestrator.collector.agent_thought_logs.clear()
    simulation_results = orchestrator.run_full_24h_cycle()
    return {"status": "success", "summary": simulation_results}

@app.get("/")
def read_root():
    """Serves main dashboard UI."""
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return HTMLResponse("<h1>Eco-Loop Building Agents Dashboard API</h1>")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
