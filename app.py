import streamlit as st
import joblib
import psutil

# Function to get battery information
def get_battery_info():
    battery = psutil.sensors_battery()
    if battery:
        return {
            "percent": battery.percent,
            "plugged": battery.power_plugged,
            "secsleft": battery.secsleft,
            "voltage": 3.7  # Placeholder since psutil doesn't provide voltage directly
        }
    return None

# Load ML model
@st.cache_resource
def load_model():
    return joblib.load("battery_model.pkl")

model = load_model()

# Streamlit App UI
st.set_page_config(page_title="Phoenix Cells", page_icon="🔋")
st.title("🔋 Phoenix Cells – Smart Battery Scanner")
st.markdown("Predict your battery’s health using real-time scanned data + AI")

battery_info = get_battery_info()

if battery_info:
    st.subheader("📡 Scanned Battery Information:")
    st.write(f"🔋 Percentage: {battery_info['percent']}%")
    st.write(f"⚡ Plugged in: {'Yes' if battery_info['plugged'] else 'No'}")
    st.write(f"⏳ Time Remaining: {battery_info['secsleft']} seconds")
    st.write(f"🔌 Estimated Voltage: {battery_info['voltage']}V (Assumed)")

    # You can improve this part with real sensor data if available
    voltage = battery_info["voltage"]                     # Estimated voltage
    temperature = st.slider("Estimated Temperature (°C)", 25, 50, 30)  # Approx or from IoT sensors
    capacity = battery_info["percent"] * 10               # Example: percent x 10 mAh

    if st.button("🔍 Analyze Battery Health"):
        prediction = model.predict([[voltage, temperature, capacity]])
        st.success(f"🧠 Predicted Battery Health: **{prediction[0]}**")
else:
    st.error("⚠️ Battery information could not be retrieved. This app only works on devices with battery sensors (like laptops).")
