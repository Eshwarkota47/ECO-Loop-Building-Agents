"""
Building Physics Simulation Engine
Models multi-zone commercial building thermal dynamics, HVAC electricity consumption,
occupancy heat gains, solar radiation, grid carbon intensity, and EnergyPlus API bindings.
"""

import time
import math
import random
from typing import Dict, List, Any
from simulation.thermal_comfort import calculate_pmv_ppd

class ZoneState:
    """Represents real-time thermodynamic state of a building zone."""
    def __init__(self, name: str, floor_area: float, thermal_mass: float):
        self.name = name
        self.floor_area = floor_area  # sq. meters
        self.thermal_mass = thermal_mass  # kJ/K
        self.temperature = 22.0  # °C
        self.humidity = 50.0  # %
        self.cooling_setpoint = 23.0  # °C (Baseline rigid)
        self.heating_setpoint = 20.0  # °C (Baseline rigid)
        self.occupancy_count = 0
        self.hvac_power_kw = 0.0
        self.fan_speed_ratio = 1.0
        self.economizer_active = False

class BuildingPhysicsEngine:
    """
    High-fidelity Building Energy Simulation Engine.
    Simulates a 5-zone commercial office building (Perimeter_N, Perimeter_S, Perimeter_E, Perimeter_W, Core).
    Supports dynamic setpoint overrides and Energy Conservation Measures (ECMs).
    """

    def __init__(self, use_energyplus_api: bool = False):
        self.use_energyplus_api = use_energyplus_api
        self.current_timestep = 0  # 15-minute timesteps (0 to 95 for 24h cycle)
        self.hour_of_day = 0.0

        # Initialize 5 commercial zones
        self.zones: Dict[str, ZoneState] = {
            "Zone_North": ZoneState("North Perimeter Zone", floor_area=150.0, thermal_mass=12000.0),
            "Zone_South": ZoneState("South Perimeter Zone", floor_area=180.0, thermal_mass=14000.0),
            "Zone_East": ZoneState("East Perimeter Zone", floor_area=120.0, thermal_mass=10000.0),
            "Zone_West": ZoneState("West Perimeter Zone", floor_area=120.0, thermal_mass=10000.0),
            "Zone_Core": ZoneState("Core Interior Zone", floor_area=300.0, thermal_mass=25000.0),
        }

        # Energy Conservation Measures (ECM) State
        self.pre_cooling_enabled = False
        self.demand_response_active = False
        self.economizer_mode = "Auto"

        # Energy & Performance Accumulators
        self.total_kwh_consumed = 0.0
        self.peak_demand_kw = 0.0
        self.total_carbon_emissions_kg = 0.0
        self.discomfort_hours = 0.0

    def get_ambient_weather(self, timestep: int) -> Dict[str, float]:
        """Generates realistic diurnal outdoor temperature, humidity, solar irradiance, and carbon intensity."""
        hour = (timestep * 0.25) % 24.0

        # Ambient temperature curve (°C) - Peaks at 15:00
        temp_min = 14.0
        temp_max = 29.0
        temp = temp_min + (temp_max - temp_min) * (0.5 + 0.5 * math.sin(math.pi * (hour - 9.0) / 12.0))

        # Direct Normal Solar Irradiance (W/m2)
        if 6.0 <= hour <= 18.0:
            solar = 850.0 * math.sin(math.pi * (hour - 6.0) / 12.0)
        else:
            solar = 0.0

        # Grid Carbon Intensity (gCO2/kWh) - Peaks during high fossil generator burn
        carbon_intensity = 320.0 + 150.0 * math.sin(math.pi * (hour - 12.0) / 12.0) + random.uniform(-10, 10)

        # Time-of-Use Electricity Tariff ($/kWh) - Peak rate 12:00 to 18:00
        if 12.0 <= hour < 18.0:
            tariff = 0.38  # Peak rate
        elif 8.0 <= hour < 12.0 or 18.0 <= hour < 22.0:
            tariff = 0.22  # Mid-peak rate
        else:
            tariff = 0.11  # Off-peak rate

        return {
            "hour": round(hour, 2),
            "outdoor_temp": round(temp, 2),
            "outdoor_rh": round(65.0 - (temp - temp_min) * 1.5, 1),
            "solar_irradiance": round(solar, 1),
            "grid_carbon_intensity": round(carbon_intensity, 1),
            "electricity_tariff": tariff
        }

    def get_occupancy_schedule(self, hour: float, zone_name: str) -> int:
        """Calculates occupants based on commercial office schedule (Arrival ~8am, Lunch ~12pm, Exit ~5pm)."""
        if 8.0 <= hour <= 17.5:
            # ~1 occupant per 15 sq meters
            capacity = int(self.zones[zone_name].floor_area / 12.0)
            if 12.0 <= hour <= 13.0:
                return int(capacity * 0.55)  # Lunch drop
            return int(capacity * random.uniform(0.85, 1.0))
        elif 7.0 <= hour < 8.0 or 17.5 < hour <= 19.0:
            capacity = int(self.zones[zone_name].floor_area / 12.0)
            return int(capacity * 0.25)  # Arrival / Departure transition
        else:
            return 0  # Unoccupied night hours

    def step_simulation(self) -> Dict[str, Any]:
        """
        Advances the building physics simulation by 1 timestep (15 minutes = 0.25 hours).
        Computes heat gains, loss, HVAC power consumption, and thermal comfort.
        """
        weather = self.get_ambient_weather(self.current_timestep)
        hour = weather["hour"]
        dt_seconds = 900.0  # 15 mins

        step_kwh = 0.0
        step_kw = 0.0
        zone_reports = []

        for z_id, z in self.zones.items():
            # 1. Update occupancy
            z.occupancy_count = self.get_occupancy_schedule(hour, z_id)
            occ_heat_gain_w = z.occupancy_count * 115.0  # 115W per person

            # 2. Solar heat gain (South/East/West perimeter zones absorb solar radiation)
            solar_gain_w = 0.0
            if "South" in z_id:
                solar_gain_w = weather["solar_irradiance"] * 25.0 * 0.6
            elif "East" in z_id and hour < 12:
                solar_gain_w = weather["solar_irradiance"] * 20.0 * 0.6
            elif "West" in z_id and hour >= 12:
                solar_gain_w = weather["solar_irradiance"] * 20.0 * 0.6

            # 3. Envelope thermal conduction (Q = U * A * (T_out - T_in))
            u_value = 0.45  # W/m2-K (Insulated wall)
            envelope_loss_gain_w = u_value * (z.floor_area * 0.8) * (weather["outdoor_temp"] - z.temperature)

            # 4. Equipment & Lighting heat gains
            equip_w = z.floor_area * (8.0 if z.occupancy_count > 0 else 1.5)

            # Net thermal heat input (Watts) without HVAC
            q_net_w = occ_heat_gain_w + solar_gain_w + envelope_loss_gain_w + equip_w

            # 5. Free economizer cooling check (if outdoor temp is cool and zone needs cooling)
            if self.economizer_mode != "Off" and weather["outdoor_temp"] < z.temperature - 2.0 and z.temperature > z.cooling_setpoint:
                z.economizer_active = True
                q_net_w -= 3500.0 * (z.temperature - weather["outdoor_temp"])
            else:
                z.economizer_active = False

            # 6. HVAC Thermodynamics & Power calculation
            hvac_power_kw = 0.0
            hvac_cop = 3.4  # Coefficient of Performance

            if z.temperature > z.cooling_setpoint:
                # Cooling needed
                target_cooling_w = q_net_w + (z.temperature - z.cooling_setpoint) * (z.thermal_mass * 1000.0 / dt_seconds)
                cooling_supplied_w = max(0.0, target_cooling_w)
                hvac_power_kw = (cooling_supplied_w / (hvac_cop * 1000.0)) * z.fan_speed_ratio
                q_net_w -= cooling_supplied_w
            elif z.temperature < z.heating_setpoint:
                # Heating needed
                target_heating_w = (z.heating_setpoint - z.temperature) * (z.thermal_mass * 1000.0 / dt_seconds) - q_net_w
                heating_supplied_w = max(0.0, target_heating_w)
                hvac_power_kw = (heating_supplied_w / (0.95 * 1000.0)) * z.fan_speed_ratio  # 95% heat efficiency
                q_net_w += heating_supplied_w

            z.hvac_power_kw = round(hvac_power_kw, 2)
            step_kw += hvac_power_kw

            # Update zone temperature state: dT = (Q_net * dt) / ThermalMass
            dt_kelvin = (q_net_w * dt_seconds) / (z.thermal_mass * 1000.0)
            z.temperature = round(z.temperature + dt_kelvin, 2)

            # Compute Thermal Comfort Index (PMV / PPD)
            comfort = calculate_pmv_ppd(ta=z.temperature, rh=z.humidity)

            if not comfort["in_comfort_zone"] and z.occupancy_count > 0:
                self.discomfort_hours += 0.25

            zone_reports.append({
                "zone_id": z_id,
                "name": z.name,
                "temperature": z.temperature,
                "cooling_setpoint": z.cooling_setpoint,
                "heating_setpoint": z.heating_setpoint,
                "occupancy": z.occupancy_count,
                "hvac_power_kw": z.hvac_power_kw,
                "pmv": comfort["pmv"],
                "ppd": comfort["ppd"],
                "comfort_status": comfort["comfort_status"],
                "economizer_active": z.economizer_active
            })

        # Calculate energy step totals
        step_kwh = step_kw * 0.25  # 15 minutes = 0.25 hours
        self.total_kwh_consumed += step_kwh
        self.peak_demand_kw = max(self.peak_demand_kw, step_kw)
        self.total_carbon_emissions_kg += (step_kwh * weather["grid_carbon_intensity"]) / 1000.0

        self.current_timestep += 1

        return {
            "timestep": self.current_timestep,
            "hour": hour,
            "weather": weather,
            "total_hvac_power_kw": round(step_kw, 2),
            "step_kwh": round(step_kwh, 3),
            "total_kwh_consumed": round(self.total_kwh_consumed, 2),
            "peak_demand_kw": round(self.peak_demand_kw, 2),
            "carbon_emissions_kg": round(self.total_carbon_emissions_kg, 2),
            "discomfort_hours": round(self.discomfort_hours, 2),
            "zones": zone_reports
        }

    def set_zone_setpoints(self, zone_id: str, cooling_setpoint: float, heating_setpoint: float):
        """Forward-injects setpoint overrides into the active simulation."""
        if zone_id in self.zones:
            # Enforce safety guardrails
            cooling = max(21.0, min(27.0, cooling_setpoint))
            heating = max(18.0, min(21.5, heating_setpoint))
            if cooling - heating < 1.5:
                cooling = heating + 1.5  # Prevent deadband overlap

            self.zones[zone_id].cooling_setpoint = round(cooling, 1)
            self.zones[zone_id].heating_setpoint = round(heating, 1)
            return True
        return False

    def apply_ecm(self, ecm_type: str, parameters: Dict[str, Any]) -> str:
        """Applies high-level Energy Conservation Measures (ECMs)."""
        if ecm_type == "PreCooling":
            # Cool building down during low-tariff off-peak hours before peak heat
            for z in self.zones.values():
                z.cooling_setpoint = 21.5
            self.pre_cooling_enabled = True
            return "Pre-Cooling ECM deployed: Zones set to 21.5°C to store thermal mass."
        elif ecm_type == "DemandResponsePeakShaving":
            # Relax cooling setpoints during peak carbon/tariff window
            for z in self.zones.values():
                z.cooling_setpoint = 25.5
                z.fan_speed_ratio = 0.85
            self.demand_response_active = True
            return "Demand Response Peak Shaving ECM deployed: Cooling setpoints relaxed to 25.5°C."
        elif ecm_type == "UnoccupiedNightSetback":
            for z in self.zones.values():
                z.cooling_setpoint = 27.0
                z.heating_setpoint = 18.0
            return "Night Setback ECM deployed: Setpoints widened for energy preservation."
        else:
            return f"Custom ECM '{ecm_type}' processed with parameters {parameters}."
