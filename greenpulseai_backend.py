# greenpulseai_backend.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Разрешаем запросы с любых источников (для девелопмента)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    electricity: float     # kWh/month
    meat: float            # grams/day
    plastic: float         # items/week
    transport_km: float    # km/week
    fuel_type: str         # petrol | diesel | electric
    language: str          # ru | en | it

# Коэффициенты для топлива
FUEL_COEFFICIENTS = {
    "petrol": 0.25,
    "diesel": 0.3,
    "electric": 0.05
}

# Локализация единицы измерения
UNIT_MAP = {
    "ru": "кг CO₂ в месяц",
    "en": "kg CO₂ per month",
    "it": "kg CO₂ al mese"
}

@app.post("/calculate")
async def calculate_index(data: InputData):
    # Расчёт эмиссий
    transport_emission   = data.transport_km * FUEL_COEFFICIENTS.get(data.fuel_type, 0.25)
    meat_emission        = data.meat * 0.02 * 30       # 0.02 kg CO₂ per gram * 30 days
    electricity_emission = data.electricity * 0.4      # 0.4 kg CO₂ per kWh
    plastic_emission     = data.plastic * 0.1 * 4      # 0.1 kg CO₂ per item * 4 weeks

    index = round(
        transport_emission +
        meat_emission +
        electricity_emission +
        plastic_emission,
        2
    )

    unit = UNIT_MAP.get(data.language, UNIT_MAP["ru"])

    return {
        "index": index,
        "unit": unit
    }
