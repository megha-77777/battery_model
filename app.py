import streamlit as st
import joblib
import psutil

# Function to safely get battery info
def get_battery_info():
    try:
        battery = psutil.sensors_battery()
        if battery:
            return {
                "percent": battery.percent,
                "plugged": battery.power_plugged,
                "secsleft": battery.secsleft,
                "voltage": 3.7  # Assumed voltage
            }
        return None
    except Exception as e:
        return None

# Load ML model
@st.cache_resource
def load_model():
    return joblib.load("battery_model.pkl")

model = load_model()

# App UI
st.set_page_config(page_title="Phoenix Cells", page_icon="🔋")
st.title("🔋 Phoenix Cells – Smart Battery Scanner")
st.markdown("Predict your battery’s health using real-time scanned data or manual input.")

battery_info = get_battery_info()

if battery_info:
    st.subheader("📡 Scanned Battery Info:")
    st.write(f"🔋 Percentage: {battery_info['percent']}%")
    st.write(f"⚡ Plugged in: {'Yes' if battery_info['plugged'] else 'No'}")
    st.write(f"⏳ Time Left: {battery_info['secsleft']} seconds")
    st.write(f"🔌 Voltage: {battery_info['voltage']}V")

    # Use scanned or override values
    voltage = battery_info["voltage"]
    temperature = st.slider("Estimated Temperature (°C)", 25, 50, 30)
    capacity = battery_info["percent"] * 10  # Example estimation

else:
    st.warning("⚠ Battery info not available (you're probably on a cloud server). Please enter manually.")
    voltage = st.number_input("Enter Voltage (V)", min_value=0.0, step=0.1, value=3.7)
    temperature = st.number_input("Enter Temperature (°C)", min_value=0.0, step=0.5, value=30.0)
    capacity = st.number_input("Enter Capacity (mAh)", min_value=0.0, step=50.0, value=800.0)

if st.button("🔍 Analyze Battery Health"):
    prediction = model.predict([[voltage, temperature, capacity]])
    st.success(f"🧠 Predicted Battery Health: **{prediction[0]}**")
