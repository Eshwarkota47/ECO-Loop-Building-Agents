"""
Eco-Loop Building Agents - Master Demonstration Launcher
Executes baseline vs. Eco-Loop AI closed-loop simulation cycle, prints quantitative
savings metrics, and starts the live web dashboard server.

Student: Eshwar B N (ID: PES2UG23CS187)
"""

import sys
import os
import uvicorn

# Add project root directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.orchestrator import ClosedLoopOrchestrator

def main():
    print("==========================================================================")
    print("            ECO-LOOP BUILDING AGENTS: PHYSICAL AI PO-C LAUNCHER            ")
    print("==========================================================================")
    print("\n[Dashboard Server] Starting Live Dashboard on http://127.0.0.1:8000 ...")

    from dashboard.server import app
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
