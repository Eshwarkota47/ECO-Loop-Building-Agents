"""
Closed-Loop Orchestration Engine
Coordinates the continuous feedback loop between EnergyPlus, MCP Server,
Cognitive LLM Engine, and Telemetry Collectors.
"""

import time
import json
from typing import Dict, Any
from simulation.building_physics import BuildingPhysicsEngine
from simulation.telemetry_stream import TelemetryCollector
from mcp_server.server import MCPServer
from agent.llm_brain import CognitiveLLMBrain

class ClosedLoopOrchestrator:
    """Manages full closed-loop simulation runs for Baseline vs. Eco-Loop AI agent."""

    def __init__(self):
        self.collector = TelemetryCollector()
        self.brain = CognitiveLLMBrain()

    def run_full_24h_cycle(self) -> Dict[str, Any]:
        """Runs a complete 24-hour simulation cycle for both Baseline and Eco-Loop AI."""
        print("================================================================")
        print("  ECO-LOOP BUILDING AGENTS: EXECUTING 24-HOUR CLOSED-LOOP RUN")
        print("================================================================")

        # ------------------------------------------------------------------
        # PHASE 1: Run Baseline Building Simulation (Rigid Static Schedule)
        # ------------------------------------------------------------------
        print("\n[1/2] Simulating Baseline Building (Rigid 23°C/20°C Schedule)...")
        baseline_sim = BuildingPhysicsEngine()
        for ts in range(96):  # 96 x 15-min steps = 24 hours
            step_data = baseline_sim.step_simulation()
            self.collector.log_step(is_baseline=True, step_data=step_data)

        # ------------------------------------------------------------------
        # PHASE 2: Run Eco-Loop Building Simulation (Autonomous AI Agent)
        # ------------------------------------------------------------------
        print("[2/2] Simulating Eco-Loop Building (Autonomous OSS LLM + MCP Control)...")
        ecoloop_sim = BuildingPhysicsEngine()
        mcp_server = MCPServer(ecoloop_sim)

        for ts in range(96):  # 96 x 15-min steps = 24 hours
            # 1. EnergyPlus Telemetry Feedback via MCP
            read_req = json.dumps({
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {"name": "read_building_telemetry", "arguments": {}},
                "id": 10
            })
            res_json = json.loads(mcp_server.handle_json_rpc_request(read_req))
            step_data = res_json["result"]["data"]

            # 2. Get Forecast via MCP
            fc_req = json.dumps({
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {"name": "get_energy_forecast", "arguments": {}},
                "id": 11
            })
            fc_res = json.loads(mcp_server.handle_json_rpc_request(fc_req))
            forecast = fc_res["result"].get("forecast", [])

            # 3. LLM Cognitive Engine Reasoning
            decision = self.brain.evaluate_state_and_decide(step_data, forecast)

            # 4. MCP Forward Control Injection
            action = decision.get("action_name")
            args = decision.get("tool_args", {})
            reasoning = decision.get("reasoning", "")

            if action and action != "read_building_telemetry":
                call_req = json.dumps({
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {"name": action, "arguments": args},
                    "id": 12
                })
                mcp_server.handle_json_rpc_request(call_req)

            # Log thought to collector
            self.collector.log_agent_thought(
                timestamp_hour=step_data["hour"],
                thought=reasoning,
                action=action or "monitor",
                tool_used=action or "read_building_telemetry"
            )

            # Log step telemetry
            self.collector.log_step(is_baseline=False, step_data=step_data)

        # Calculate final summary
        summary = self.collector.get_quantitative_summary()
        print("\n================================================================")
        print("                 QUANTITATIVE SAVINGS SUMMARY                   ")
        print("================================================================")
        print(f" Baseline Total Consumption  : {summary['kwh_baseline']:.2f} kWh")
        print(f" Eco-Loop Total Consumption : {summary['kwh_ecoloop']:.2f} kWh")
        print(f" >>> TOTAL ENERGY SAVED     : {summary['kwh_savings_pct']:.1f}% <<<")
        print(f" Peak Demand Shaving        : {summary['peak_shaving_pct']:.1f}% ({summary['peak_kw_baseline']:.1f} kW -> {summary['peak_kw_ecoloop']:.1f} kW)")
        print(f" Carbon Emissions Avoided   : {summary['carbon_reduction_pct']:.1f}% ({summary['carbon_baseline_kg']:.1f} kg -> {summary['carbon_ecoloop_kg']:.1f} kg)")
        print(f" Discomfort Hours (PMV)     : Baseline={summary['discomfort_hours_baseline']:.1f}h | Eco-Loop={summary['discomfort_hours_ecoloop']:.1f}h")
        print("================================================================")

        return summary
