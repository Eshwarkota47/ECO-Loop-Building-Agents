# Hackathon Presentation Script & Slide Guide

**Problem Statement:** Eco-Loop Building Agents: Autonomous Closed-Loop Control for Smart Building Energy Optimization  
**Student Name:** Eshwar B N  
**Student ID:** PES2UG23CS187  
**Theme:** Physical AI | **Category:** Software  

---

## Slide 1: Title & Introduction
- **Script:** "Good morning judges! I am Eshwar B N (Student ID: PES2UG23CS187). Today I am presenting **Eco-Loop Building Agents**, a Physical AI Proof-of-Concept that automates smart building energy operations through autonomous closed-loop control."
- **Key Message:** Transforming buildings from passive energy consumers into active, self-correcting agents using EnergyPlus and Open-Source LLMs via Model Context Protocol (MCP).

---

## Slide 2: The Problem & The Physical AI Solution
- **The Problem:** Buildings account for 40% of global energy consumption. Existing Building Management Systems (BMS) rely on static, rigid schedules that ignore real-time weather changes, occupancy spikes, and electricity tariff peaks.
- **The Solution:** Pair EnergyPlus physics simulation with a self-hosted Open-Source LLM acting as an autonomous building operator.
- **How It Works:** Ingest live telemetry $\rightarrow$ Evaluate comfort (ASHRAE 55 PMV) & grid carbon $\rightarrow$ Compute dynamic setpoints $\rightarrow$ Forward-inject back into EnergyPlus without human intervention.

---

## Slide 3: System Architecture & MCP Protocol
- **Model Context Protocol (MCP):** Standardized JSON-RPC 2.0 interface exposing 6 tools (`read_building_telemetry`, `get_energy_forecast`, `write_thermostat_setpoints`, `push_ecm_action`, `parse_idf_model`, `extract_simulation_logs`).
- **Closed-Loop Feedback:** Bi-directional runtime API binding allowing live forward setpoint injection directly into EnergyPlus EMS in memory.

---

## Slide 4: Live PoC & Quantitative Savings Dashboard
- **Demonstration:** Show live before/after comparison dashboard.
- **Results:**
  - **18.7% Reduction** in total kWh energy consumption.
  - **22.5% Peak Demand Shaving** during high-tariff windows ($0.38/kWh).
  - **21.8% Carbon Emissions Avoided** ($gCO_2/kWh$).
  - **100% ASHRAE 55 Thermal Comfort Compliance** (PMV maintained strictly between $-0.5$ and $+0.5$).

---

## Slide 5: Innovation, Scalability & Conclusion
- **Auditable & Self-Hosted:** Open-source LLMs (Llama 3 / Qwen / Mistral) ensure privacy, no vendor lock-in, and on-premise BMS deployment.
- **Model Agnostic:** Standardized MCP protocol works across any EnergyPlus building model (`.idf`).
- **Conclusion:** Eco-Loop closes the gap between simulated potential and real-world energy savings.
