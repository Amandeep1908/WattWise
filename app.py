from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json or {}
    household_size = int(data.get('household', 4))
    appliance_hours = float(data.get('hours', 8))
    temp = float(data.get('temp', 32))
    tariff = float(data.get('tariff', 7.5))

    base_kwh = (household_size * 2.5) + (appliance_hours * 1.2) + (temp * 0.15)
    daily_kwh = round(base_kwh * random.uniform(0.95, 1.05), 2)
    monthly_kwh = round(daily_kwh * 30, 2)
    estimated_bill = round(monthly_kwh * tariff, 2)
    co2_footprint = round(monthly_kwh * 0.82, 2)

    return jsonify({
        'daily_kwh': daily_kwh,
        'monthly_kwh': monthly_kwh,
        'estimated_bill': estimated_bill,
        'co2_footprint': co2_footprint
    })

if __name__ == '__main__':
    app.run(debug=True)