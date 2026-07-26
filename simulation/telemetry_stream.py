"""
Telemetry Stream Module
Collects, aggregates, and stores baseline vs. Eco-Loop AI control simulation history
for real-time dashboard streaming and quantitative metrics calculation.
"""

from typing import Dict, List, Any

class TelemetryCollector:
    """Manages telemetry historical logs for Baseline and Eco-Loop AI runs."""
    def __init__(self):
        self.baseline_history: List[Dict[str, Any]] = []
        self.ecoloop_history: List[Dict[str, Any]] = []
        self.agent_thought_logs: List[Dict[str, Any]] = []

    def log_step(self, is_baseline: bool, step_data: Dict[str, Any]):
        """Logs a simulation timestep frame."""
        if is_baseline:
            self.baseline_history.append(step_data)
        else:
            self.ecoloop_history.append(step_data)

    def log_agent_thought(self, timestamp_hour: float, thought: str, action: str, tool_used: str):
        """Logs cognitive agent reasoning step for the dashboard console."""
        self.agent_thought_logs.append({
            "hour": round(timestamp_hour, 2),
            "thought": thought,
            "action": action,
            "tool_used": tool_used
        })

    def get_quantitative_summary(self) -> Dict[str, Any]:
        """Calculates precise baseline vs. Eco-Loop savings percentages."""
        if not self.baseline_history or not self.ecoloop_history:
            return {
                "kwh_baseline": 0.0,
                "kwh_ecoloop": 0.0,
                "kwh_savings_pct": 0.0,
                "peak_kw_baseline": 0.0,
                "peak_kw_ecoloop": 0.0,
                "peak_shaving_pct": 0.0,
                "carbon_baseline_kg": 0.0,
                "carbon_ecoloop_kg": 0.0,
                "carbon_reduction_pct": 0.0,
                "discomfort_hours_baseline": 0.0,
                "discomfort_hours_ecoloop": 0.0
            }

        b_last = self.baseline_history[-1]
        e_last = self.ecoloop_history[-1]

        b_kwh = b_last["total_kwh_consumed"]
        e_kwh = e_last["total_kwh_consumed"]
        kwh_savings = ((b_kwh - e_kwh) / b_kwh * 100.0) if b_kwh > 0 else 0.0

        b_peak = max(h["total_hvac_power_kw"] for h in self.baseline_history)
        e_peak = max(h["total_hvac_power_kw"] for h in self.ecoloop_history)
        peak_shaving = ((b_peak - e_peak) / b_peak * 100.0) if b_peak > 0 else 0.0

        b_carbon = b_last["carbon_emissions_kg"]
        e_carbon = e_last["carbon_emissions_kg"]
        carbon_savings = ((b_carbon - e_carbon) / b_carbon * 100.0) if b_carbon > 0 else 0.0

        return {
            "kwh_baseline": b_kwh,
            "kwh_ecoloop": e_kwh,
            "kwh_savings_pct": round(kwh_savings, 1),
            "peak_kw_baseline": b_peak,
            "peak_kw_ecoloop": e_peak,
            "peak_shaving_pct": round(peak_shaving, 1),
            "carbon_baseline_kg": b_carbon,
            "carbon_ecoloop_kg": e_carbon,
            "carbon_reduction_pct": round(carbon_savings, 1),
            "discomfort_hours_baseline": b_last["discomfort_hours"],
            "discomfort_hours_ecoloop": e_last["discomfort_hours"]
        }
