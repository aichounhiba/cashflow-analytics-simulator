import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from core.simulator import CashFlowSimulator

# Configuration visuelle - Thème Épuré Blanc, Orange et Jaune
st.set_page_config(page_title="Cash-Flow & Liquidity AI Simulator", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size:38px; font-weight:bold; color:#FF9F1C; text-align:center; margin-bottom:20px; }
    .metric-box { background-color: #FFF9E6; padding: 15px; border-radius: 10px; border-left: 5px solid #FF9F1C; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 Simulateur Prédictif de Trésorerie & Risque de Liquidité</div>', unsafe_allow_html=True)
st.write("Cet outil corporatif permet d'anticiper le risque de faillite technique en simulant les flux financiers futurs via la méthode stochastique de Monte Carlo.")

# --- BARRE LATÉRALE CONTROLE DES RISQUES ---
st.sidebar.header("⚙️ Paramètres Financiers")
cash_init = st.sidebar.number_input("Trésorerie Actuelle (€)", value=100000, step=5000)
costs_fixed = st.sidebar.number_input("Charges Fixes Mensuelles (€)", value=18000, step=1000)
rev_avg = st.sidebar.number_input("Revenus Mensuels Moyens (€)", value=20000, step=1000)
volatility = st.sidebar.slider("Volatilité des Revenus (Incertitude %)", min_value=0.0, max_value=1.0, value=0.25, step=0.05)
months_to_sim = st.sidebar.slider("Horizon de prévision (Mois)", min_value=3, max_value=24, value=12)

# --- CALCULS ---
sim = CashFlowSimulator(cash_init, costs_fixed, rev_avg, volatility)
paths = sim.run_simulation(months=months_to_sim, simulations=200)
metrics = sim.calculate_metrics(paths)

# --- AFFICHAGE DES CLÉS DE PERFORMANCE (KPI) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-box"><b>Burn Rate Mensuel Fixe</b><br><span style="font-size:24px; color:#D62246;">{costs_fixed:,} €</span></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-box"><b>Trésorerie Finale Estimée (Moyenne)</b><br><span style="font-size:24px; color:#2EC4B6;">{metrics["median"][-1]:,.0f} €</span></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-box"><b>Autonomie Financière (Runway)</b><br><span style="font-size:24px; color:#FF9F1C;">{metrics["runway"]}</span></div>', unsafe_allow_html=True)

st.write("---")

# --- GRAPHIQUE DES TRAJECTOIRE DE LIQUIDITÉ ---
st.subheader("📈 Projections de Trésorerie à l'horizon choisi")

fig = go.Figure()
x_months = [f"Mois {i}" for i in range(months_to_sim + 1)]

# Ajout des courbes de scénarios
fig.add_trace(go.Scatter(x=x_months, y=metrics["optimistic"], name="Scénario Optimiste (Top 5%)", line=dict(color='#2EC4B6', dash='dash')))
fig.add_trace(go.Scatter(x=x_months, y=metrics["median"], name="Trajectoire Médiane (Réaliste)", line=dict(color='#FF9F1C', width=4)))
fig.add_trace(go.Scatter(x=x_months, y=metrics["pessimistic"], name="Scénario à Risque (VaR 5%)", line=dict(color='#D62246', width=2)))

# Ligne critique de faillite (0 €)
fig.add_trace(go.Scatter(x=x_months, y=[0]*(months_to_sim+1), name="Seuil de Rupture (0 €)", line=dict(color='black', width=1, dash='dot')))

fig.update_layout(template="plotly_white", xaxis_title="Horizon Temporel", yaxis_title="Solde Bancaire (€)", legend=dict(x=0, y=1))
st.plotly_chart(fig, use_container_width=True)