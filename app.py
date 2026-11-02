from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

FULL_DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WattWise - ML Electricity Usage Prediction & Cost Optimization</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-slate-950 text-slate-100 font-sans min-h-screen p-4 md:p-8">
    <div class="max-w-7xl mx-auto space-y-6">
        
        <!-- Header -->
        <header class="bg-slate-900 border border-slate-800 p-6 rounded-2xl flex flex-col md:flex-row justify-between items-center shadow-xl gap-4">
            <div>
                <div class="flex items-center gap-3">
                    <span class="text-3xl">⚡</span>
                    <h1 class="text-2xl md:text-3xl font-extrabold text-cyan-400">WattWise</h1>
                    <span class="bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-xs px-3 py-1 rounded-full font-semibold">ML v2.4 ACTIVE</span>
                </div>
                <p class="text-slate-400 text-sm mt-1">Electricity Usage Prediction & Cost Optimization Platform</p>
            </div>
            <div class="flex items-center gap-4 text-sm bg-slate-950 px-4 py-2 rounded-xl border border-slate-800">
                <div>
                    <p class="text-xs text-slate-400">PSIT Kanpur • Mini Project</p>
                    <p class="font-bold text-slate-200">Amandeep Singh (2501640100102)</p>
                </div>
                <span class="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs px-2.5 py-1 rounded-lg">Hardware-Free ML</span>
            </div>
        </header>

        <!-- Navigation Tabs -->
        <div class="flex flex-wrap gap-2 bg-slate-900 p-2 rounded-xl border border-slate-800">
            <button onclick="switchTab('dashboard')" id="btn-dashboard" class="tab-btn px-4 py-2 rounded-lg font-medium text-sm transition bg-cyan-500 text-slate-950 font-bold">📊 Dashboard Overview</button>
            <button onclick="switchTab('predictor')" id="btn-predictor" class="tab-btn px-4 py-2 rounded-lg font-medium text-sm transition text-slate-400 hover:text-white">⚡ ML Appliance Predictor</button>
            <button onclick="switchTab('tariff')" id="btn-tariff" class="tab-btn px-4 py-2 rounded-lg font-medium text-sm transition text-slate-400 hover:text-white">💰 Tariff & Cost Calculator</button>
            <button onclick="switchTab('optimization')" id="btn-optimization" class="tab-btn px-4 py-2 rounded-lg font-medium text-sm transition text-slate-400 hover:text-white">💡 Energy Optimization</button>
            <button onclick="switchTab('synopsis')" id="btn-synopsis" class="tab-btn px-4 py-2 rounded-lg font-medium text-sm transition text-slate-400 hover:text-white">📄 Project Synopsis & IEEE</button>
        </div>

        <!-- TAB 1: DASHBOARD OVERVIEW -->
        <div id="tab-dashboard" class="tab-content space-y-6">
            <!-- Metric Cards -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
                    <p class="text-xs font-bold text-slate-400 uppercase">Projected Daily Usage</p>
                    <p class="text-3xl font-black text-white mt-2">56.88 <span class="text-sm font-normal text-slate-400">kWh/day</span></p>
                    <p class="text-xs text-cyan-400 mt-2">✨ Based on 8 active loads</p>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
                    <p class="text-xs font-bold text-slate-400 uppercase">Monthly Consumption</p>
                    <p class="text-3xl font-black text-cyan-400 mt-2">1,706 <span class="text-sm font-normal text-slate-400">Units</span></p>
                    <p class="text-xs text-slate-400 mt-2">🤖 ML Model: RANDOM FOREST</p>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
                    <p class="text-xs font-bold text-slate-400 uppercase">Estimated Monthly Bill</p>
                    <p class="text-3xl font-black text-emerald-400 mt-2">₹ 16,260</p>
                    <p class="text-xs text-emerald-400 mt-2">Potential Savings: ₹ 3,883</p>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-5 rounded-2xl">
                    <p class="text-xs font-bold text-slate-400 uppercase">Carbon Footprint</p>
                    <p class="text-3xl font-black text-amber-400 mt-2">1,399 <span class="text-sm font-normal text-slate-400">kg CO₂</span></p>
                    <p class="text-xs text-amber-400 mt-2">🌱 ~70 trees equivalent load</p>
                </div>
            </div>

            <!-- Charts Section -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="lg:col-span-2 bg-slate-900 border border-slate-800 p-6 rounded-2xl">
                    <h3 class="text-lg font-bold text-white mb-1">📈 30-Day Power Consumption Predictive Forecast</h3>
                    <p class="text-xs text-slate-400 mb-4">Simulated daily trajectory based on weighted appliance usage & weather factors</p>
                    <div class="h-72"><canvas id="forecastChart"></canvas></div>
                </div>
                <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
                    <h3 class="text-lg font-bold text-white mb-1">🥧 Load Distribution</h3>
                    <p class="text-xs text-slate-400 mb-4">Proportion of energy consumed by household functions</p>
                    <div class="h-64 flex justify-center"><canvas id="pieChart"></canvas></div>
                </div>
            </div>
        </div>
