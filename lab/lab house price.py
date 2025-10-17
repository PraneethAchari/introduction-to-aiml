"""
🏡 Lab Exercise: Predicting House Prices
----------------------------------------
We have a small dataset of houses with:
- Area (sqft)
- Number of rooms
- Distance from city (km)
- Age of the house (years)
and the target variable — Price (in ₹ Lacs)

Goal:
👉 Build a simple Linear Regression model to predict the house price.
"""

# --- Import libraries ---
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# -----------------------------
# Step 1: Create the dataset
# -----------------------------
print("📥 Step 1: Creating the dataset...")

data = {
    'Area (sqft)': [1200, 1400, 1600, 1700, 1850],
    'Rooms': [3, 4, 3, 5, 4],
    'Distance (km)': [5, 3, 8, 2, 4],
    'Age (years)': [10, 3, 20, 15, 7],
    'Price (₹ Lacs)': [120, 150, 130, 180, 170]
}

df = pd.DataFrame(data)
print("\nHere’s our dataset:")
print(df)

# -----------------------------
# Step 2: Define features (X) and target (y)
# -----------------------------
print("\n⚙️ Step 2: Defining features and target...")

X = df[['Area (sqft)', 'Rooms', 'Distance (km)', 'Age (years)']]
y = df['Price (₹ Lacs)']

print("✅ Features selected:", list(X.columns))
print("✅ Target variable: Price (₹ Lacs)")

# -----------------------------
# Step 3: Train Linear Regression Model
# -----------------------------
print("\n🚀 Step 3: Training the Linear Regression model...")

model = LinearRegression()
model.fit(X, y)

print("\n✅ Model training complete!")
print("📈 Coefficients (impact of each feature):")
for feature, coef in zip(X.columns, model.coef_):
    print(f"   - {feature}: {coef:.2f}")

print(f"📉 Intercept: {model.intercept_:.2f}")

# -----------------------------
# Step 4: Predict using the trained model
# -----------------------------
print("\n🔮 Step 4: Making predictions on training data...")

y_pred = model.predict(X)
df['Predicted Price (₹ Lacs)'] = y_pred.round(2)

print("\n📊 Actual vs Predicted Prices:")
print(df[['Price (₹ Lacs)', 'Predicted Price (₹ Lacs)']])

# -----------------------------
# Step 5: Evaluate model performance
# -----------------------------
print("\n📏 Step 5: Evaluating model performance...")

mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)

print(f"📊 Mean Squared Error (MSE): {mse:.2f}")
print(f"⭐ R² Score: {r2:.2f}")

# -----------------------------
# Step 6: Predict a new house
# -----------------------------
print("\n🏠 Step 6: Predicting price for a new house...")

# Example: Area=1500 sqft, Rooms=4, Distance=4 km, Age=8 years
new_house = [[1500, 4, 4, 8]]
predicted_price = model.predict(new_house)[0]

print(f"💰 Predicted Price for 1500 sqft, 4-room, 4km, 8-year-old house: ₹{predicted_price:.2f} Lacs")

print("\n✅ Task Complete! You've built a simple yet powerful house price predictor.")
