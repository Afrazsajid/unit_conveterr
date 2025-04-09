import streamlit as st
from pydantic import BaseModel, ValidationError
from typing import Dict, Callable
import math

class UnitConverter:
    def __init__(self):
        self.categories: Dict[str, Dict[str, float | Callable]] = {
            'Length': {
                'meters': 1.0,
                'kilometers': 1000.0,
                'miles': 1609.34,
                'feet': 0.3048,
                'inches': 0.0254,
            },
            'Weight': {
                'grams': 1.0,
                'kilograms': 1000.0,
                'pounds': 453.592,
                'ounces': 28.3495,
            },
            'Temperature': {
                'celsius': lambda x: x,
                'fahrenheit': lambda x: (x - 32) * 5/9,
                'kelvin': lambda x: x - 273.15,
            },
            'Time': {
                'seconds': 1.0,
                'minutes': 60.0,
                'hours': 3600.0,
                'days': 86400.0,
            },
            'Volume': {
                'liters': 1.0,
                'milliliters': 0.001,
                'gallons': 3.78541,
                'cups': 0.24,
            },
            'Area': {
                'square meters': 1.0,
                'square kilometers': 1e6,
                'acres': 4046.86,
                'square miles': 2.59e6,
            },
            'Speed': {
                'm/s': 1.0,
                'km/h': 0.277778,
                'mph': 0.44704,
            },
            'Energy': {
                'joules': 1.0,
                'calories': 4.184,
                'kilojoules': 1000.0,
                'kilocalories': 4184.0,
            },
            'Pressure': {
                'pascals': 1.0,
                'bar': 100000.0,
                'psi': 6894.76,
                'atmospheres': 101325.0,
            },
            'Digital Storage': {
                'bytes': 1.0,
                'kilobytes': 1024.0,
                'megabytes': 1024.0**2,
                'gigabytes': 1024.0**3,
            }
        }

    def convert(self, category: str, value: float, from_unit: str, to_unit: str) -> float:
        if category == 'Temperature':
            from_func = self.categories[category][from_unit]
            to_func = self.categories[category][to_unit]
            celsius = from_func(value)
            if to_unit == 'fahrenheit':
                return celsius * 9/5 + 32
            elif to_unit == 'kelvin':
                return celsius + 273.15
            return celsius
        else:
            base_value = value * self.categories[category][from_unit]
            return base_value / self.categories[category][to_unit]



st.set_page_config(page_title="Advanced Unit Converter", layout="centered")
st.title("🔄 Advanced Unit Converter")

converter = UnitConverter()




category = st.selectbox("Select Category", list(converter.categories.keys()))
units = list(converter.categories[category].keys())

col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox("From", units, key="from")
with col2:
    to_unit = st.selectbox("To", units, key="to")

col3, col4 = st.columns([2, 1])
with col3:
    value = st.number_input("Enter value", value=0.0, step=0.1)
with col4:
    if st.button("🔁 Swap"):
        from_unit, to_unit = to_unit, from_unit

try:
    result = converter.convert(category, value, from_unit, to_unit)
    st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")
except Exception as e:
    st.error(f"Conversion failed: {str(e)}")

# Optional: show formula or explanation (simplified)
if st.checkbox("Show conversion explanation"):
    if category == 'Temperature':
        st.info("Temperature conversions are non-linear. Conversions use formulas depending on the selected units.")
    else:
        factor_from = converter.categories[category][from_unit]
        factor_to = converter.categories[category][to_unit]
        st.code(f"value * {factor_from} / {factor_to}")
