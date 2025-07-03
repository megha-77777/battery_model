import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load the battery data
df = pd.read_csv("battery_data.csv")

# Features and target
X = df[['Voltage', 'Temperature', 'Capacity']]
y = df['BatteryHealth']

# Train a simple decision tree model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save the trained model
joblib.dump(model, "battery_model.pkl")

print("✅ Model trained and saved as battery_model.pkl")
