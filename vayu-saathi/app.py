import os
from datetime import datetime
from typing import List, Optional
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from fastapi.responses import FileResponse, Response



app = FastAPI(title="VayuSaathi - Winter Smog & Air Pollution Assistant")

# Mount static directory for the frontend
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the official Google GenAI client (reads GEMINI_API_KEY from env)
client = genai.Client()
MODEL_ID = "gemini-3.8-flash"


# ---------------------------------------------------------
# 1. Request & Response Schemas (Structured GenAI Outputs)
# ---------------------------------------------------------
class HouseholdProfile(BaseModel):
    city: str = Field(..., examples=["Delhi", "Lahore", "Bengaluru", "London"])
    household_members: str = Field(..., examples=["2 adults, 1 toddler (4 yrs), 1 senior with asthma"])
    housing_type: str = Field(..., examples=["Ground-floor apartment near main road, leaky windows"])
    commute_habit: str = Field(..., examples=["15 km daily solo petrol car commute + school drop-off"])
    cooking_and_energy: str = Field(..., examples=["LPG gas stove without chimney, occasional incense"])
    budget_tier: str = Field(..., examples=["Low-cost / DIY preferred", "Moderate", "Flexible"])
    community_role: str = Field(default="Family", examples=["Family", "RWA / Apartment Lead", "School Coordinator"])


class RoutineStep(BaseModel):
    time_window: str
    activity: str
    smog_adaptation: str
    direct_impact_explanation: str


class IndoorAirHack(BaseModel):
    title: str
    cost_tier: str = Field(..., description="Zero-cost, Low-cost DIY, or Equipment")
    how_to_do_it: str
    target_pollutant: str
    direct_health_impact: str
    estimated_indoor_pm25_reduction_pct: int = Field(..., ge=0, le=95)


class SustainableAlternative(BaseModel):
    current_habit: str
    sustainable_swap: str
    scale: str = Field(..., description="Individual/Family or Neighborhood/Community")
    why_it_matters_for_smog: str
    monthly_pm25_avoided_grams: float
    monthly_co2e_avoided_kg: float


class SmogAssistantPlan(BaseModel):
    severity_summary: str
    health_risk_alert: str
    low_emission_daily_routine: List[RoutineStep]
    indoor_air_quality_hacks: List[IndoorAirHack]
    sustainable_alternatives: List[SustainableAlternative]
    community_action_nudge: str


class ChatRequest(BaseModel):
    city: str
    profile_summary: str
    aqi_summary: str
    question: str


# ---------------------------------------------------------
# 2. Live Air Quality & Thermal Inversion Window Service
# ---------------------------------------------------------
async def fetch_air_quality(city: str) -> dict:
    async with httpx.AsyncClient(timeout=12.0) as http:
        # Step A: Geocode city name
        geo_resp = await http.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en", "format": "json"},
        )
        geo_data = geo_resp.json()
        if not geo_data.get("results"):
            raise HTTPException(status_code=404, detail=f"Could not find location: {city}")

        loc = geo_data["results"][0]
        lat, lon = loc["latitude"], loc["longitude"]
        resolved_name = f"{loc['name']}, {loc.get('admin1', '')} {loc.get('country', '')}".strip()

        # Step B: Fetch current & 24h hourly forecast from Open-Meteo Air Quality API
        aq_resp = await http.get(
            "https://air-quality-api.open-meteo.com/v1/air-quality",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "us_aqi,pm2_5,pm10,nitrogen_dioxide,ozone,carbon_monoxide",
                "hourly": "pm2_5,pm10,us_aqi",
                "forecast_days": 2,
                "timezone": "auto",
            },
        )
        aq_data = aq_resp.json()

    current = aq_data.get("current", {})
    hourly = aq_data.get("hourly", {})
    times = hourly.get("time", [])[:24]
    pm25_series = hourly.get("pm2_5", [])[:24]
    aqi_series = hourly.get("us_aqi", [])[:24]

    # Find cleanest 2-hour daytime window (07:00 - 20:00) & worst peak hour
    daytime_slots = []
    for idx in range(len(times) - 1):
        hour_int = datetime.fromisoformat(times[idx]).hour
        if 7 <= hour_int <= 19 and pm25_series[idx] is not None and pm25_series[idx + 1] is not None:
            avg_pm25 = round((pm25_series[idx] + pm25_series[idx + 1]) / 2, 1)
            daytime_slots.append((avg_pm25, times[idx], times[idx + 1]))

    if daytime_slots:
        best_window = min(daytime_slots, key=lambda x: x[0])
        best_str = f"{best_window[1][-5:]}–{best_window[2][-5:]} (avg PM2.5: {best_window[0]} µg/m³)"
    else:
        best_str = "Mid-afternoon (13:00–15:00 typically has highest mixing height)"

    valid_hours = [(p, t[-5:]) for p, t in zip(pm25_series, times) if p is not None]
    peak_hour = max(valid_hours, key=lambda x: x[0]) if valid_hours else (current.get("pm2_5", 0), "08:00")

    return {
        "location": resolved_name,
        "latitude": lat,
        "longitude": lon,
        "us_aqi": current.get("us_aqi"),
        "pm2_5": current.get("pm2_5"),
        "pm10": current.get("pm10"),
        "no2": current.get("nitrogen_dioxide"),
        "ozone": current.get("ozone"),
        "cleanest_window_24h": best_str,
        "peak_smog_hour_24h": f"{peak_hour[1]} (~{round(peak_hour[0], 1)} µg/m³ PM2.5)",
        "aqi_category": classify_us_aqi(current.get("us_aqi") or 0),
    }


def classify_us_aqi(aqi: float) -> str:
    if aqi <= 50:
        return "Good"
    if aqi <= 100:
        return "Moderate"
    if aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    if aqi <= 200:
        return "Unhealthy"
    if aqi <= 300:
        return "Very Unhealthy"
    return "Hazardous"


# ---------------------------------------------------------
# 3. Deterministic Baseline Impact Reference for Grounding
# ---------------------------------------------------------
def build_impact_reference(pm25: float) -> str:
    who_ratio = round((pm25 or 15) / 15.0, 1)  # WHO 24-hr PM2.5 guideline = 15 µg/m³
    return f"""
GROUNDED ENVIRONMENTAL & EXPOSURE FACTS (use these to keep impact numbers realistic):
- Current outdoor PM2.5 is {pm25} µg/m³ ({who_ratio}x the WHO 24-hour guideline of 15 µg/m³).
- Winter thermal inversions trap ground-level exhaust & biomass smoke between ~19:00 and 09:30; midday solar heating lifts the boundary layer.
- A properly fitted N95/FFP2 mask filters ~94–95% of PM2.5 particles during outdoor commutes.
- Avoiding 10 km/day of solo petrol car travel (shifting to metro/bus/carpool) cuts ~1.8 kg CO2e/day (~54 kg/month) and reduces local tailpipe NOx + brake/tire/exhaust PM2.5 (~12–18 g PM2.5/month).
- Stopping indoor incense/dhoop/mosquito coils eliminates acute indoor PM2.5 spikes that can exceed 200–400 µg/m³ inside closed winter rooms.
- A DIY Corsi-Rosenthal box (4 MERV-13 filters + box fan) or HEPA purifier sized to the room reduces indoor PM2.5 by ~60–85% within 45 minutes.
- Wet mopping + sealing window gaps cuts indoor dust resuspension and infiltration by ~20–35% at near-zero cost.
- Preventing 1 neighborhood dry-leaf/trash bonfire (~15 kg biomass) avoids ~120–180 g of direct PM2.5 and carcinogenic PAHs in the immediate street radius.
"""


# ---------------------------------------------------------
# 4. API Endpoints
# ---------------------------------------------------------
@app.get("/")
async def serve_home():
    return FileResponse("static/index.html")


@app.post("/api/plan")
async def generate_smog_plan(profile: HouseholdProfile):
    aq = await fetch_air_quality(profile.city)
    impact_facts = build_impact_reference(aq["pm2_5"] or 0)

    system_instruction = (
        "You are VayuSaathi, an empathetic, practical environmental health and urban sustainability assistant "
        "helping families and communities navigate winter smog and severe urban air pollution. "
        "Always tailor advice to the user's exact live air quality metrics, housing constraints, budget tier, "
        "and vulnerable household members. Never give generic fluff—give actionable, localized steps and clearly "
        "explain the direct causal impact of every choice on both family inhalation exposure and neighborhood emissions."
    )

    prompt = f"""
LIVE AIR QUALITY TELEMETRY FOR {aq['location']}:
- US AQI: {aq['us_aqi']} ({aq['aqi_category']})
- PM2.5: {aq['pm2_5']} µg/m³ | PM10: {aq['pm10']} µg/m³ | NO2: {aq['no2']} µg/m³ | O3: {aq['ozone']} µg/m³
- Cleanest 2-Hour Daytime Window (next 24h): {aq['cleanest_window_24h']}
- Peak Smog Risk Hour (next 24h): {aq['peak_smog_hour_24h']}

HOUSEHOLD & COMMUNITY PROFILE:
- Members & Vulnerabilities: {profile.household_members}
- Housing & Ventilation: {profile.housing_type}
- Commute & Mobility: {profile.commute_habit}
- Cooking & Energy Use: {profile.cooking_and_energy}
- Budget Tier: {profile.budget_tier}
- Role: {profile.community_role}

{impact_facts}

Generate a personalized, structured winter-smog action plan:
1. Summarize today's severity and specific health risks for the household members.
2. Build a time-blocked low-emission daily routine (4–6 blocks) anchored around today's cleanest window and peak smog hour.
3. Provide 4 practical indoor air quality hacks matching their housing and budget (include at least one zero-cost hack and one DIY/tech option), explaining exact indoor PM2.5 reduction impacts.
4. Suggest 4 high-impact sustainable alternatives (covering mobility, cooking/energy, and community/neighborhood actions) with realistic monthly PM2.5 (grams) and CO2e (kg) avoided, plus a clear explanation of why each swap reduces local winter smog.
5. End with one actionable community nudge appropriate to their role.
"""

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=SmogAssistantPlan,
                temperature=0.35,
            ),
        )
        plan: SmogAssistantPlan = response.parsed
        return {"air_quality": aq, "plan": plan.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GenAI generation error: {str(e)}")

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

@app.post("/api/chat")
async def community_chat(req: ChatRequest):
    system_instruction = (
        "You are VayuSaathi, a concise, science-grounded air quality and winter smog advisor. "
        "Answer the family or community question using the provided live AQI context and household profile. "
        "Always include: (1) Direct recommendation, (2) Why it works, and (3) Direct health or emission impact. "
        "Keep answers practical, empathetic, and under 180 words."
    )
    prompt = f"""
Location: {req.city}
Live AQI Context: {req.aqi_summary}
Household Profile: {req.profile_summary}
User Question: {req.question}
"""
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.4,
            ),
        )
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")