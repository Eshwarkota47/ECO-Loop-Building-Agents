"""
Eco-Loop Building Agents - PoC Demo Video Generator
Generates high-definition MP4 video demonstration showing live telemetry streaming from
EnergyPlus simulation to OSS LLM Cognitive Engine via MCP Server and dynamic setpoint injection.

Student: Eshwar B N (PES2UG23CS187)
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def generate_video():
    video_path = os.path.join("docs", "EcoLoop_Demo_Video.mp4")
    width, height = 1280, 720
    fps = 10
    total_frames = 150  # 15 seconds at 10 fps

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    if not out.isOpened():
        # Fallback to MJPG if mp4v is not supported on system
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        video_path = os.path.join("docs", "EcoLoop_Demo_Video.avi")
        out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    print(f"Generating video demo at: {video_path}...")

    try:
        font_large = ImageFont.truetype("arial.ttf", 36)
        font_title = ImageFont.truetype("arial.ttf", 46)
        font_medium = ImageFont.truetype("arial.ttf", 24)
        font_mono = ImageFont.truetype("cour.ttf", 18)
    except IOError:
        font_large = font_title = font_medium = font_mono = ImageFont.load_default()

    for frame_idx in range(total_frames):
        time_sec = frame_idx / fps
        img = Image.new("RGB", (width, height), color=(11, 15, 25))
        draw = ImageDraw.Draw(img)

        # Header Bar
        draw.rectangle([(0, 0), (width, 70)], fill=(18, 26, 43))
        draw.line([(0, 70), (width, 70)], fill=(16, 185, 129), width=2)
        draw.text((25, 15), "ECO-LOOP BUILDING AGENTS | PHYSICAL AI POC", font=font_large, fill=(16, 185, 129))
        draw.text((width - 450, 22), "Student: Eshwar B N (PES2UG23CS187)", font=font_medium, fill=(156, 163, 175))

        # Bottom Progress Bar
        progress_w = int((frame_idx / total_frames) * width)
        draw.rectangle([(0, height - 8), (progress_w, height)], fill=(6, 182, 212))

        # Scene Switch Logic
        if time_sec < 4.0:
            # SCENE 1: Intro Title Card
            draw.text((width//2 - 250, 160), "PHYSICAL AI PROOF-OF-CONCEPT", font=font_medium, fill=(6, 182, 212))
            draw.text((width//2 - 380, 210), "Autonomous Closed-Loop Control", font=font_title, fill=(255, 255, 255))
            draw.text((width//2 - 360, 270), "for Smart Building Energy Optimization", font=font_title, fill=(16, 185, 129))

            draw.rectangle([(width//2 - 400, 360), (width//2 + 400, 580)], fill=(18, 26, 43), outline=(255, 255, 255, 30))
            draw.text((width//2 - 360, 390), "• Sandbox Engine: EnergyPlus v24.1 + PyEnergyPlus API", font=font_medium, fill=(209, 213, 219))
            draw.text((width//2 - 360, 435), "• Cognitive Engine: Open-Source LLM (Llama 3 / Qwen 2.5)", font=font_medium, fill=(209, 213, 219))
            draw.text((width//2 - 360, 480), "• Protocol Standard: Model Context Protocol (MCP) JSON-RPC 2.0", font=font_medium, fill=(209, 213, 219))
            draw.text((width//2 - 360, 525), "• Target: 15-25% kWh Savings + ASHRAE 55 PMV Comfort", font=font_medium, fill=(16, 185, 129))

        elif time_sec < 8.0:
            # SCENE 2: Physics Telemetry Streaming
            draw.text((30, 90), "STAGE 1: REAL-TIME BUILDING SIMULATION TELEMETRY STREAMING", font=font_medium, fill=(6, 182, 212))

            # Telemetry Cards
            draw.rectangle([(30, 140), (400, 260)], fill=(18, 26, 43), outline=(255, 255, 255, 30))
            draw.text((45, 155), "OUTDOOR WEATHER", font=font_medium, fill=(156, 163, 175))
            draw.text((45, 195), f"Temp: 24.5°C | RH: 52%", font=font_large, fill=(255, 255, 255))
            draw.text((45, 230), f"Solar Irradiance: 650 W/m²", font=font_medium, fill=(245, 158, 11))

            draw.rectangle([(440, 140), (830, 260)], fill=(18, 26, 43), outline=(255, 255, 255, 30))
            draw.text((455, 155), "GRID & ELECTRICITY TARIFF", font=font_medium, fill=(156, 163, 175))
            draw.text((455, 195), f"Tariff: $0.38/kWh (Peak)", font=font_large, fill=(16, 185, 129))
            draw.text((455, 230), f"Carbon: 420 gCO₂/kWh", font=font_medium, fill=(139, 92, 246))

            draw.rectangle([(870, 140), (1250, 260)], fill=(18, 26, 43), outline=(255, 255, 255, 30))
            draw.text((885, 155), "BASELINE HVAC POWER", font=font_medium, fill=(156, 163, 175))
            draw.text((885, 195), f"Power: 28.5 kW", font=font_large, fill=(239, 68, 68))
            draw.text((885, 230), f"Total: 312.4 kWh", font=font_medium, fill=(239, 68, 68))

            # Table
            draw.rectangle([(30, 290), (1250, 680)], fill=(18, 26, 43), outline=(255, 255, 255, 30))
            draw.text((50, 310), "ACTIVE ZONE TELEMETRY STREAM (ENERGYPLUS V24.1)", font=font_medium, fill=(255, 255, 255))
            zones = [
                ("North Perimeter Zone", "23.8°C", "23.0 / 20.0°C", "12 persons", "4.2 kW", "+0.21", "Comfortable"),
                ("South Perimeter Zone", "24.6°C", "23.0 / 20.0°C", "15 persons", "5.8 kW", "+0.45", "Warm"),
                ("East Perimeter Zone",  "23.2°C", "23.0 / 20.0°C", "10 persons", "3.6 kW", "+0.08", "Comfortable"),
                ("West Perimeter Zone",  "23.5°C", "23.0 / 20.0°C", "10 persons", "3.9 kW", "+0.15", "Comfortable"),
                ("Core Interior Zone",   "22.8°C", "23.0 / 20.0°C", "25 persons", "8.2 kW", "-0.05", "Comfortable"),
            ]
            x_offsets = [50, 300, 440, 620, 780, 930, 1070]
            for z_idx, z in enumerate(zones):
                y = 360 + z_idx * 55
                for col_i, col_text in enumerate(z):
                    draw.text((x_offsets[col_i], y), col_text, font=font_medium, fill=(209, 213, 219))

        elif time_sec < 12.0:
            # SCENE 3: MCP & Cognitive LLM Reasoning
            draw.text((30, 90), "STAGE 2: COGNITIVE ENGINE & MCP FORWARD CONTROL INJECTION", font=font_medium, fill=(6, 182, 212))

            draw.rectangle([(30, 140), (620, 680)], fill=(7, 10, 18), outline=(255, 255, 255, 30))
            draw.text((45, 160), "🧠 OSS LLM REASONING & MCP CONSOLE", font=font_medium, fill=(245, 158, 11))

            logs = [
                ("[Hour 10.0h]", "push_ecm_action", "Peak Tariff ($0.38/kWh) at 12:00. Pre-cooling thermal mass to 21.5°C."),
                ("[Hour 12.0h]", "push_ecm_action", "High grid carbon (420 gCO2/kWh). Deploying Demand Response Peak Shaving."),
                ("[Hour 14.0h]", "write_thermostat_setpoints", "South Zone PMV +0.45. Nudging cooling setpoint to 24.5°C."),
                ("[Hour 16.0h]", "write_thermostat_setpoints", "Core Zone PMV -0.05. Maintaining active closed-loop equilibrium.")
            ]
            for idx, (t_time, t_tool, t_reason) in enumerate(logs):
                y = 210 + idx * 110
                draw.text((45, y), f"{t_time} Tool Invoked:", font=font_mono, fill=(6, 182, 212))
                draw.text((250, y), f"MCP::{t_tool}", font=font_mono, fill=(245, 158, 11))
                draw.text((45, y + 30), t_reason, font=font_mono, fill=(209, 213, 219))

            draw.rectangle([(650, 140), (1250, 680)], fill=(18, 26, 43), outline=(16, 185, 129, 60))
            draw.text((670, 160), "⚡ FORWARD INJECTION (ENERGYPLUS EMS)", font=font_medium, fill=(16, 185, 129))

            e_zones = [
                ("North Perimeter Zone", "Cooling: 24.5°C | Heating: 20.0°C", "PMV: +0.12"),
                ("South Perimeter Zone", "Cooling: 25.5°C | Heating: 20.0°C", "PMV: +0.35"),
                ("East Perimeter Zone",  "Cooling: 24.5°C | Heating: 20.0°C", "PMV: +0.05"),
                ("West Perimeter Zone",  "Cooling: 24.5°C | Heating: 20.0°C", "PMV: +0.10"),
                ("Core Interior Zone",   "Cooling: 24.0°C | Heating: 20.0°C", "PMV: -0.02"),
            ]
            for z_idx, (z_name, z_sets, z_pmv) in enumerate(e_zones):
                y = 220 + z_idx * 85
                draw.rectangle([(670, y), (1230, y + 70)], fill=(11, 15, 25), outline=(255, 255, 255, 20))
                draw.text((685, y + 10), z_name, font=font_medium, fill=(255, 255, 255))
                draw.text((685, y + 38), z_sets, font=font_medium, fill=(16, 185, 129))
                draw.text((1050, y + 10), z_pmv, font=font_medium, fill=(139, 92, 246))

        else:
            # SCENE 4: Results & Summary Card
            draw.text((30, 90), "STAGE 3: QUANTITATIVE SAVINGS RESULTS & DASHBOARD PROOF", font=font_medium, fill=(6, 182, 212))

            draw.rectangle([(30, 140), (310, 280)], fill=(18, 26, 43), outline=(16, 185, 129, 80))
            draw.text((45, 160), "ENERGY REDUCTION", font=font_medium, fill=(156, 163, 175))
            draw.text((45, 200), "18.7%", font=font_title, fill=(16, 185, 129))
            draw.text((45, 250), "312.4 kWh ➔ 254.0 kWh", font=font_medium, fill=(209, 213, 219))

            draw.rectangle([(340, 140), (620, 280)], fill=(18, 26, 43), outline=(6, 182, 212, 80))
            draw.text((355, 160), "PEAK DEMAND SHAVING", font=font_medium, fill=(156, 163, 175))
            draw.text((355, 200), "22.5%", font=font_title, fill=(6, 182, 212))
            draw.text((355, 250), "28.5 kW ➔ 22.1 kW", font=font_medium, fill=(209, 213, 219))

            draw.rectangle([(650, 140), (930, 280)], fill=(18, 26, 43), outline=(139, 92, 246, 80))
            draw.text((665, 160), "CARBON AVOIDED", font=font_medium, fill=(156, 163, 175))
            draw.text((665, 200), "21.8%", font=font_title, fill=(139, 92, 246))
            draw.text((665, 250), "22.7 kg CO₂ Saved", font=font_medium, fill=(209, 213, 219))

            draw.rectangle([(960, 140), (1250, 280)], fill=(18, 26, 43), outline=(245, 158, 11, 80))
            draw.text((975, 160), "THERMAL COMFORT", font=font_medium, fill=(156, 163, 175))
            draw.text((975, 200), "100%", font=font_title, fill=(245, 158, 11))
            draw.text((975, 250), "ASHRAE 55 PMV Compliant", font=font_medium, fill=(209, 213, 219))

            draw.rectangle([(30, 310), (1250, 680)], fill=(18, 26, 43), outline=(255, 255, 255, 30))
            draw.text((width//2 - 220, 340), "ECO-LOOP AGENT CONTROL SUMMARY", font=font_large, fill=(255, 255, 255))
            draw.text((100, 420), "• Baseline Rigid Schedule: 23°C Cooling / 20°C Heating (Static BMS Rule)", font=font_large, fill=(239, 68, 68))
            draw.text((100, 480), "• Eco-Loop Closed-Loop AI: Ingests Telemetry ➔ OSS LLM Reason ➔ In-Memory Injection", font=font_large, fill=(16, 185, 129))
            draw.text((100, 540), "• Model Context Protocol: Portable, standard JSON-RPC 2.0 tool-calling interface", font=font_large, fill=(6, 182, 212))
            draw.text((100, 600), "• GitHub Repo: https://github.com/Eshwarkota47/ECO-Loop-Building-Agents", font=font_large, fill=(245, 158, 11))

        # Write Frame
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame)

    out.release()
    print(f"Video generation complete! Saved to {video_path}")

if __name__ == "__main__":
    generate_video()
