import streamlit as st
import joblib

# Load the trained ML model
model = joblib.load("battery_model.pkl")

# App Title
st.title("🔋 Phoenix Cells – Battery Life Analyzer")

# User inputs
voltage = st.number_input("Enter Battery Voltage (V)", min_value=0.0, step=0.1)
temperature = st.number_input("Enter Battery Temperature (°C)", min_value=0.0, step=0.5)
capacity = st.number_input("Enter Battery Capacity (mAh)", min_value=0.0, step=50.0)

# Prediction
if st.button("🔍 Analyze Battery"):
    prediction = model.predict([[voltage, temperature, capacity]])
    st.success(f"Predicted Battery Health: **{prediction[0]}**")
