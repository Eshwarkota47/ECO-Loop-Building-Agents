"""
Thermal Comfort Module - Fanger's PMV and PPD Model (ASHRAE 55 Standard)
Calculates Predicted Mean Vote (PMV) and Predicted Percentage Dissatisfied (PPD)
for indoor thermal comfort analysis.
"""

import math

def calculate_pmv_ppd(
    ta: float,          # Air temperature (°C)
    tr: float = None,   # Mean radiant temperature (°C), defaults to ta if None
    vel: float = 0.1,   # Relative air velocity (m/s)
    rh: float = 50.0,   # Relative humidity (%)
    met: float = 1.2,   # Metabolic rate (met) (1.2 met = typical office work)
    clo: float = 0.7    # Clothing insulation (clo) (0.7 clo = light clothing)
) -> dict:
    """
    Computes Fanger's PMV [-3 (very cold) to +3 (very hot)] and PPD [%].
    Target PMV range for comfort is [-0.5, +0.5].
    """
    if tr is None:
        tr = ta

    # Constants & Conversion factors
    pa = rh * 10.0 * math.exp(16.6536 - 4030.183 / (ta + 235.0)) # Water vapor pressure (Pa)
    icl = 0.155 * clo  # Thermal resistance of clothing (m2 K/W)
    m = met * 58.15     # Metabolic rate (W/m2)
    w = 0.0             # External work (assumed 0)
    mw = m - w          # Heat production

    # Clothing surface temperature iteration setup
    if icl <= 0.078:
        fcl = 1.0 + 1.29 * icl
    else:
        fcl = 1.05 + 0.645 * icl

    hcf = 12.1 * math.sqrt(vel)
    taa = ta + 273.15
    tra = tr + 273.15

    # Iterative calculation of clothing surface temperature (tcl)
    tcla = taa + (35.5 - ta) / (3.5 * (icl + 0.1))
    tcl = tcla - 273.15
    p1 = icl * fcl
    p2 = p1 * 3.96
    p3 = p1 * 100.0
    p4 = p1 * taa
    p5 = 308.7 - 0.028 * mw + p2 * math.pow(tra / 100.0, 4)

    xn = tcla / 100.0
    xf = xn
    eps = 0.0001
    hc = 0.0
    iter_count = 0

    while iter_count < 150:
        xf = (xf + xn) / 2.0
        hcn = 2.38 * math.pow(abs(100.0 * xf - taa), 0.25)
        if hcf > hcn:
            hc = hcf
        else:
            hc = hcn

        xn = (p5 + p4 * hc - p2 * math.pow(xf, 4)) / (100.0 + p3 * hc)
        if abs(xn - xf) < eps:
            break
        iter_count += 1

    tcl = 100.0 * xn - 273.15

    # Heat loss components
    hl1 = 3.05 * 0.001 * (5733.0 - 6.99 * mw - pa)  # Skin diff. vapor loss
    hl2 = 0.42 * (mw - 58.15) if mw > 58.15 else 0.0  # Sweating loss
    hl3 = 1.7 * 0.00001 * m * (5867.0 - pa)           # Latent respiration loss
    hl4 = 0.0014 * m * (34.0 - ta)                    # Dry respiration loss
    hl5 = 3.96 * fcl * (math.pow(xn, 4) - math.pow(tra / 100.0, 4)) # Radiation loss
    hl6 = fcl * hc * (tcl - ta)                        # Convection loss

    # Total thermal load
    ts = 0.303 * math.exp(-0.036 * m) + 0.028
    pmv = ts * (mw - hl1 - hl2 - hl3 - hl4 - hl5 - hl6)

    # Clamp PMV to standard [-3.0, +3.0] scale
    pmv = max(-3.0, min(3.0, round(pmv, 2)))

    # Calculate PPD (Predicted Percentage Dissatisfied)
    ppd = 100.0 - 95.0 * math.exp(-0.03353 * math.pow(pmv, 4) - 0.2179 * math.pow(pmv, 2))
    ppd = min(99.0, max(5.0, round(ppd, 1)))

    return {
        "pmv": pmv,
        "ppd": ppd,
        "comfort_status": "Comfortable" if -0.5 <= pmv <= 0.5 else ("Too Cold" if pmv < -0.5 else "Too Hot"),
        "in_comfort_zone": -0.5 <= pmv <= 0.5
    }
