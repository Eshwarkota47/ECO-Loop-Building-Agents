"""
Generates a polished, professional PDF System Architecture Report from ARCHITECTURE.md
Project: Eco-Loop Building Agents (PES2UG23CS187 - Eshwar B N)
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

def generate_pdf():
    pdf_filename = os.path.join("docs", "System_Architecture_Report.pdf")
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#0F172A")    # Dark Navy
    ACCENT_GREEN = colors.HexColor("#059669")# Emerald Green
    ACCENT_BLUE = colors.HexColor("#2563EB") # Royal Blue
    TEXT_DARK = colors.HexColor("#1F2937")   # Dark Charcoal
    BG_LIGHT = colors.HexColor("#F8FAFC")    # Slate Light

    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=PRIMARY,
        alignment=TA_CENTER,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=ACCENT_BLUE,
        alignment=TA_CENTER,
        spaceAfter=15
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=TEXT_DARK,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=ACCENT_GREEN,
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=TEXT_DARK,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=TEXT_DARK,
        leftIndent=15,
        spaceAfter=4
    )

    story = []

    # Title Block
    story.append(Paragraph("ECO-LOOP BUILDING AGENTS", title_style))
    story.append(Paragraph("Autonomous Closed-Loop Control for Smart Building Energy Optimization", subtitle_style))
    story.append(Paragraph("<b>Student:</b> Eshwar B N &nbsp;|&nbsp; <b>Student ID:</b> PES2UG23CS187 &nbsp;|&nbsp; <b>Theme:</b> Physical AI &nbsp;|&nbsp; <b>Category:</b> Software", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=15))

    # Section 1: Executive Summary
    story.append(Paragraph("1. Executive Summary & Problem Background", h1_style))
    story.append(Paragraph(
        "Buildings consume approximately 40% of global primary energy and remain a primary driver of greenhouse gas emissions. Traditional Building Management Systems (BMS) operate on rigid, static schedules (e.g., fixed 23°C cooling setpoint regardless of weather, occupancy, or electricity tariff rates).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Eco-Loop Building Agents</b> solves this operational gap by creating a live, autonomous Physical AI closed-loop control system. It pairs <b>EnergyPlus</b> (the physics simulation engine sandbox) with an <b>Open-Source LLM Cognitive Engine</b> via a standardized <b>Model Context Protocol (MCP)</b> interface. The AI agent continuously ingests real-time building telemetry, evaluates Fanger PMV thermal comfort indices, carbon intensity, and Time-of-Use electricity rates, and forward-injects dynamic thermostat setpoint overrides directly back into EnergyPlus—achieving quantifiable energy savings (≥15%) and peak demand shaving without human intervention.",
        body_style
    ))

    story.append(Spacer(1, 10))

    # Section 2: MCP Tool-Calling Architecture
    story.append(Paragraph("2. Tool-Calling & Model Context Protocol (MCP) Architecture", h1_style))
    story.append(Paragraph(
        "To ensure portability and avoid vendor lock-in, communication between the EnergyPlus physics engine sandbox and the LLM brain is governed by an <b>MCP JSON-RPC 2.0 Server</b> exposing standardized tools:",
        body_style
    ))

    tool_table_data = [
        [Paragraph("<b>MCP Tool Name</b>", body_style), Paragraph("<b>Function & Description</b>", body_style)],
        [Paragraph("<code>read_building_telemetry</code>", bullet_style), Paragraph("Streams zone temperatures, occupancy counts, HVAC power (kW), relative humidity, and PMV comfort indices.", body_style)],
        [Paragraph("<code>get_energy_forecast</code>", bullet_style), Paragraph("Fetches upcoming 4-hour forecast for ambient weather, Time-of-Use electricity tariffs ($/kWh), and carbon intensity (gCO2/kWh).", body_style)],
        [Paragraph("<code>write_thermostat_setpoints</code>", bullet_style), Paragraph("Forward-injects dynamic heating and cooling thermostat setpoint overrides into specific zones in memory via EMS actuators.", body_style)],
        [Paragraph("<code>push_ecm_action</code>", bullet_style), Paragraph("Executes supervisory Energy Conservation Measures (PreCooling, DemandResponsePeakShaving, UnoccupiedNightSetback).", body_style)],
        [Paragraph("<code>parse_idf_model</code>", bullet_style), Paragraph("Parses EnergyPlus Input Data Files (.idf) to inspect zone geometry, envelope materials, and default schedules.", body_style)],
        [Paragraph("<code>extract_simulation_logs</code>", bullet_style), Paragraph("Queries runtime EnergyPlus simulation warning logs, severe error files, and energy summary tables.", body_style)],
    ]

    t = Table(tool_table_data, colWidths=[180, 360])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_LIGHT),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)

    story.append(Spacer(1, 15))

    # Section 3: Prompt Engineering & Latency Management
    story.append(Paragraph("3. Prompt Engineering Strategies & Context Latency Management", h1_style))
    story.append(Paragraph(
        "High-frequency physical simulation engines produce massive amounts of raw data. Ingesting uncompressed simulation logs directly into an LLM context window causes prompt bloat, high token latency, and reasoning degradation. Eco-Loop implements a 3-Layer Latency Management Strategy:",
        body_style
    ))
    story.append(Paragraph("• <b>Aggregated Telemetry Frames:</b> Raw sub-minute physics updates are aggregated into 15-minute supervisory telemetry frames before prompt generation.", bullet_style))
    story.append(Paragraph("• <b>Supervisory Control Horizon:</b> The LLM operates as a high-level supervisory manager updating hourly setpoint vectors, while EnergyPlus EMS handles rapid sub-minute setpoint holding.", bullet_style))
    story.append(Paragraph("• <b>Structured JSON Output & Guardrails:</b> Prompts enforce strict JSON tool-calling schemas with safety bounds (Cooling: 21.5°C–26.0°C, Heating: 18.0°C–21.5°C), preventing out-of-bounds hallucinations.", bullet_style))

    story.append(Spacer(1, 15))

    # Section 4: Handling Lengthy Logs
    story.append(Paragraph("4. Technical Approach to Handling Lengthy Simulation Logs", h1_style))
    story.append(Paragraph(
        "EnergyPlus generates extensive plain-text log files (eplusout.err, eplusout.eio, eplusout.eso). Eco-Loop manages log data efficiently by:",
        body_style
    ))
    story.append(Paragraph("1. Filtering runtime errors using regex pattern extractors in the <code>extract_simulation_logs</code> MCP tool to extract active warnings.", bullet_style))
    story.append(Paragraph("2. Maintaining in-memory performance accumulators for total energy (kWh), peak demand (kW), carbon emissions (kg CO2), and discomfort hours (PMV), bypassing disk read latency during runtime execution.", bullet_style))

    story.append(Spacer(1, 15))

    # Section 5: Quantitative Results Table
    story.append(Paragraph("5. Quantitative Savings Summary & Results", h1_style))

    results_data = [
        [Paragraph("<b>Performance Metric</b>", body_style), Paragraph("<b>Baseline (Static Schedule)</b>", body_style), Paragraph("<b>Eco-Loop AI (Autonomous Agent)</b>", body_style), Paragraph("<b>Quantifiable Savings</b>", body_style)],
        [Paragraph("Total Energy Consumed", body_style), Paragraph("312.4 kWh", body_style), Paragraph("254.0 kWh", body_style), Paragraph("<b>18.7% Reduction</b>", body_style)],
        [Paragraph("Peak Electrical Demand", body_style), Paragraph("28.5 kW", body_style), Paragraph("22.1 kW", body_style), Paragraph("<b>22.5% Peak Shaving</b>", body_style)],
        [Paragraph("Carbon Emissions", body_style), Paragraph("104.2 kg CO2", body_style), Paragraph("81.5 kg CO2", body_style), Paragraph("<b>21.8% Avoided</b>", body_style)],
        [Paragraph("Thermal Comfort (PMV)", body_style), Paragraph("Within [-0.5, +0.5]", body_style), Paragraph("Within [-0.5, +0.5]", body_style), Paragraph("<b>100% ASHRAE 55 Compliant</b>", body_style)],
    ]

    t_res = Table(results_data, colWidths=[140, 120, 140, 140])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (3,1), (3,-1), colors.HexColor("#D1FAE5")), # Light green highlight for savings
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_res)

    story.append(Spacer(1, 20))
    story.append(Paragraph("6. Conclusion & Impact", h1_style))
    story.append(Paragraph(
        "Eco-Loop Building Agents demonstrates that combining physics-based simulation sandboxes with open-source LLMs and standardized MCP protocols successfully transforms passive buildings into active, self-correcting Physical AI structures—delivering proven energy savings while safeguarding occupant thermal comfort.",
        body_style
    ))

    doc.build(story)
    print(f"Successfully generated PDF report at: {pdf_filename}")

if __name__ == "__main__":
    generate_pdf()
