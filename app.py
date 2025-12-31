import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
import sys
import os
from pathlib import Path

sys.path.append('scripts')

# ========== CONFIGURATION & THEME ==========
st.set_page_config(
    page_title="CryptoVision Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS pour un design professionnel avec Dark/Light mode
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variables CSS pour les thèmes */
    :root {
        --primary-color: #6366F1;
        --secondary-color: #8B5CF6;
        --accent-color: #10B981;
        --danger-color: #EF4444;
        --warning-color: #F59E0B;
    }
    
    /* Police globale */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        padding: 2rem 1rem;
    }
    
    /* Headers dans la sidebar */
    [data-testid="stSidebar"] h1 {
        color: #FFFFFF !important;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--primary-color);
    }
    
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    [data-testid="stSidebar"] h4 {
        color: #F1F5F9 !important;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
    }
    
    /* Sidebar labels */
    [data-testid="stSidebar"] label {
        color: #F1F5F9 !important;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #E2E8F0 !important;
    }
    
    /* Sidebar markdown text */
    [data-testid="stSidebar"] .stMarkdown {
        color: #F1F5F9 !important;
    }
    
    /* Select box text in sidebar */
    [data-testid="stSidebar"] [data-baseweb="select"] {
        color: #FFFFFF !important;
    }
    
    /* Input fields in sidebar */
    [data-testid="stSidebar"] input {
        color: #1E293B !important;
        background-color: #F8FAFC !important;
    }
    
    /* Slider labels in sidebar */
    [data-testid="stSidebar"] [data-testid="stSlider"] label {
        color: #FFFFFF !important;
    }
    
    /* Radio button labels in sidebar */
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        color: #FFFFFF !important;
    }
    
    /* Multiselect in sidebar */
    [data-testid="stSidebar"] [data-baseweb="tag"] {
        background-color: var(--primary-color) !important;
        color: white !important;
    }
    
    /* Main header gradient */
    .main-header {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        padding: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: rgba(100, 102, 241, 0.1);
        border-radius: 10px;
        color: #64748B;
        font-weight: 600;
        font-size: 1rem;
        padding: 0 2rem;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(100, 102, 241, 0.2);
        border-color: var(--primary-color);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        color: white !important;
        border-color: var(--primary-color);
    }
    
    /* Cards styling */
    .metric-card {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #E2E8F0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem 0;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 2px solid #E2E8F0;
    }
    
    .section-header h2, .section-header h3 {
        color: #1E293B;
        font-weight: 700;
        margin: 0;
        font-size: 1.5rem;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #EBF4FF 0%, #DBEAFE 100%);
        border-left: 4px solid #3B82F6;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border-left: 4px solid #10B981;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border-left: 4px solid #F59E0B;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E293B;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(99, 102, 241, 0.4);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #F8FAFC;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        font-weight: 600;
        color: #1E293B;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0 1rem;
            font-size: 0.9rem;
        }
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #E2E8F0, transparent);
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ========== THEME TOGGLE ==========
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

def toggle_theme():
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

# Header principal avec gradient
st.markdown("""
<div class="main-header">
    <h1>📊 CryptoVision Pro</h1>
    <p>Plateforme professionnelle d'analyse et de trading de cryptomonnaies</p>
</div>
""", unsafe_allow_html=True)

# ========== TABS PRINCIPAUX ==========
tab1, tab2, tab3 = st.tabs(["📈 Analyse Bitcoin", "💼 Portfolio Multi-Actifs", "📋 Rapports & Insights"])

# ==================== TAB 1 : MODULE BITCOIN ====================
with tab1:
    from strategies import (
        buy_and_hold_strategy,
        moving_average_crossover_strategy,
        simple_momentum_strategy,
        calculate_metrics
    )
    
    @st.cache_data(ttl=300)
    def load_bitcoin_data():
        try:
            df = pd.read_csv('data/bitcoin_prices.csv')
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            return None
    
    df_btc = load_bitcoin_data()
    
    if df_btc is None:
        st.error("⚠️ **Données indisponibles** - Veuillez exécuter : `python scripts/fetch_data.py`")
    else:
        prices = df_btc['price']
        
        # ========== SIDEBAR MODULE A ==========
        with st.sidebar:
            st.markdown("### ⚙️ Configuration Bitcoin")
            
            # Prix actuel avec card
            current_price = prices.iloc[-1]
            try:
                change_24h = df_btc['change_24h'].iloc[-1]
            except:
                change_24h = 0
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #F7931A 0%, #FF6B00 100%); 
                        padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;
                        box-shadow: 0 8px 16px rgba(247, 147, 26, 0.3);">
                <div style="color: white; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem;">
                    💰 BITCOIN (BTC)
                </div>
                <div style="color: white; font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;">
                    ${current_price:,.2f}
                </div>
                <div style="color: {'#10B981' if change_24h >= 0 else '#EF4444'}; 
                           font-size: 1rem; font-weight: 600;">
                    {'▲' if change_24h >= 0 else '▼'} {abs(change_24h):.2f}% (24h)
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Informations sur les données
            last_update = df_btc['timestamp'].iloc[-1]
            st.markdown("#### 📅 Période des données")
            st.info(f"""
            **Début** : {df_btc['timestamp'].iloc[0].strftime('%d/%m/%Y')}  
            **Fin** : {df_btc['timestamp'].iloc[-1].strftime('%d/%m/%Y')}  
            **Points** : {len(df_btc):,}  
            **Dernière MAJ** : {last_update.strftime('%H:%M:%S')}
            """)
            
            st.markdown("---")
            
            # Sélection de stratégie
            st.markdown("#### 📊 Stratégie de Trading")
            
            strategy_choice = st.selectbox(
                "Sélectionner une stratégie",
                ["Buy and Hold", "MA Crossover", "Simple Momentum"],
                help="Choisissez votre stratégie d'investissement"
            )
            
            initial_capital_a = st.number_input(
                "💵 Capital Initial ($)",
                min_value=1000,
                max_value=1000000,
                value=10000,
                step=1000,
                key="capital_a"
            )
            
            # Paramètres selon la stratégie
            if strategy_choice == "MA Crossover":
                st.markdown("#### ⚙️ Paramètres MA Crossover")
                short_window = st.slider("📉 Moyenne Mobile Courte", 5, 50, 20)
                long_window = st.slider("📈 Moyenne Mobile Longue", 20, 200, 50)
                
                if short_window >= long_window:
                    st.warning("⚠️ La MM courte doit être inférieure à la MM longue")
            
            elif strategy_choice == "Simple Momentum":
                st.markdown("#### ⚙️ Paramètres Momentum")
                momentum_window = st.slider("📊 Fenêtre de Momentum", 5, 50, 14)
        
        # ========== CALCUL DE LA STRATÉGIE ==========
        with st.spinner("⏳ Calcul de la stratégie en cours..."):
            if strategy_choice == "Buy and Hold":
                portfolio_values = buy_and_hold_strategy(prices, initial_capital_a)
                strategy_name = "Buy and Hold"
            elif strategy_choice == "MA Crossover":
                portfolio_values = moving_average_crossover_strategy(
                    prices, short_window, long_window, initial_capital_a
                )
                strategy_name = f"MA Crossover ({short_window}/{long_window})"
            else:
                portfolio_values = simple_momentum_strategy(
                    prices, momentum_window, initial_capital_a
                )
                strategy_name = f"Simple Momentum ({momentum_window})"
            
            metrics = calculate_metrics(portfolio_values, initial_capital_a)
        
        # ========== MÉTRIQUES PRINCIPALES ==========
        st.markdown(f"""
        <div class="section-header">
            <h2>📊 Performance : {strategy_name}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💰 Valeur Finale",
                f"${metrics['final_value']:,.0f}",
                f"{metrics['total_return']:.2f}%",
                delta_color="normal"
            )
        
        with col2:
            st.metric(
                "📊 Ratio de Sharpe",
                f"{metrics['sharpe_ratio']:.2f}",
                help="Rendement ajusté au risque (> 1 = Bon)"
            )
        
        with col3:
            st.metric(
                "📉 Drawdown Max",
                f"{metrics['max_drawdown']:.2f}%",
                help="Perte maximale depuis le plus haut"
            )
        
        with col4:
            st.metric(
                "📈 Volatilité",
                f"{metrics['volatility']:.2f}%",
                help="Volatilité annualisée"
            )
        
        # ========== GRAPHIQUE PRINCIPAL ==========
        st.markdown("""
        <div class="section-header">
            <h3>📈 Évolution du Prix et du Portfolio</h3>
        </div>
        """, unsafe_allow_html=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_btc['timestamp'],
            y=prices,
            name="Prix Bitcoin",
            line=dict(color='#F7931A', width=3),
            yaxis='y1',
            fill='tozeroy',
            fillcolor='rgba(247, 147, 26, 0.1)'
        ))
        
        fig.add_trace(go.Scatter(
            x=df_btc['timestamp'],
            y=portfolio_values,
            name=f"Valeur Portfolio",
            line=dict(color='#10B981', width=3),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title=dict(
                text=f"Comparaison Prix BTC vs Portfolio ({strategy_name})",
                font=dict(size=20, color='#1E293B', family='Inter')
            ),
            xaxis=dict(
                title="Date",
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)'
            ),
            yaxis=dict(
                title="Prix Bitcoin ($)",
                titlefont=dict(color="#F7931A"),
                tickfont=dict(color="#F7931A"),
                side='left',
                showgrid=False
            ),
            yaxis2=dict(
                title="Valeur Portfolio ($)",
                titlefont=dict(color="#10B981"),
                tickfont=dict(color="#10B981"),
                overlaying='y',
                side='right',
                showgrid=False
            ),
            hovermode='x unified',
            height=600,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # ========== MÉTRIQUES DÉTAILLÉES ==========
        st.markdown("""
        <div class="section-header">
            <h3>📋 Analyse Détaillée des Performances</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 💰 Rendements")
            profit = metrics['final_value'] - initial_capital_a
            
            st.markdown(f"""
            <div class="metric-card">
                <p><strong>Rendement Total :</strong> {metrics['total_return']:.2f}%</p>
                <p><strong>Rendement Annualisé :</strong> {metrics['annual_return']:.2f}%</p>
                <p><strong>Capital Initial :</strong> ${initial_capital_a:,.0f}</p>
                <p><strong>Capital Final :</strong> ${metrics['final_value']:,.0f}</p>
                <p><strong>Profit/Perte :</strong> <span style="color: {'#10B981' if profit >= 0 else '#EF4444'};">
                    ${profit:,.0f}</span></p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 📊 Ratios de Performance")
            
            st.markdown(f"""
            <div class="metric-card">
                <p><strong>Sharpe Ratio :</strong> {metrics['sharpe_ratio']:.2f}</p>
                <p><strong>Win Rate :</strong> {metrics['win_rate']:.2f}%</p>
                <p><strong>Profit Factor :</strong> {metrics['profit_factor']:.2f}</p>
                <p><strong>Volatilité :</strong> {metrics['volatility']:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("#### 📉 Analyse du Risque")
            
            st.markdown(f"""
            <div class="metric-card">
                <p><strong>Max Drawdown :</strong> <span style="color: #EF4444;">
                    {metrics['max_drawdown']:.2f}%</span></p>
                <p><strong>Volatilité Annuelle :</strong> {metrics['volatility']:.2f}%</p>
                <p><strong>Ratio Rendement/Risque :</strong> 
                    {(metrics['annual_return'] / metrics['volatility'] if metrics['volatility'] > 0 else 0):.2f}</p>
            </div>
            """, unsafe_allow_html=True)
"""
Intégration du module de prédiction dans Streamlit
À ajouter dans votre fichier principal app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from predictor import BitcoinPredictor
import numpy as np


st.markdown("""
<div class="section-header">
    <h3>🔮 Prédictions Machine Learning </h3>
</div>
""", unsafe_allow_html=True)

# Sidebar pour les paramètres de prédiction
with st.sidebar:
    st.markdown("---")
    st.markdown("#### 🔮 Prédictions ML")
    
    enable_predictions = st.checkbox(
        "Activer les prédictions",
        value=False,
        help="Active le module de prédiction ML"
    )
    
    if enable_predictions:
        prediction_days = st.slider(
            "Jours à prédire",
            min_value=3,
            max_value=30,
            value=7,
            help="Nombre de jours futurs à prédire"
        )
        
        model_choice = st.multiselect(
            "Modèles à utiliser",
            ["Linear Regression", "Random Forest", "ARIMA"],
            default=["Random Forest"],
            help="Sélectionner les modèles ML"
        )

# Si les prédictions sont activées
if enable_predictions and len(model_choice) > 0:
    
    with st.spinner("🔮 Calcul des prédictions ML..."):
        try:
            # Créer le prédicteur
            predictor = BitcoinPredictor(df_btc, prediction_days=prediction_days)
            
            # Calculer les prédictions
            results = {}
            
            if "Linear Regression" in model_choice:
                lr_result = predictor.predict_linear_regression()
                results['Linear Regression'] = lr_result
            
            if "Random Forest" in model_choice:
                rf_result = predictor.predict_random_forest()
                results['Random Forest'] = rf_result
            
            if "ARIMA" in model_choice:
                from predictor import ARIMA_AVAILABLE
                if ARIMA_AVAILABLE:
                    arima_result = predictor.predict_arima()
                    if arima_result:
                        results['ARIMA'] = arima_result
                else:
                    st.warning("⚠️ ARIMA non disponible. Installer: `pip install statsmodels`")
            
            if len(results) > 0:
                # ========== MÉTRIQUES DE PERFORMANCE ==========
                st.markdown("#### 📊 Performance des Modèles sur les Données de Test")
                
                cols = st.columns(len(results))
                
                for idx, (model_name, result) in enumerate(results.items()):
                    with cols[idx]:
                        st.markdown(f"**{model_name}**")
                        st.metric("MAE", f"${result['mae']:,.0f}")
                        st.metric("RMSE", f"${result['rmse']:,.0f}")
                        if result['r2']:
                            st.metric("R² Score", f"{result['r2']:.3f}")
                
                # ========== GRAPHIQUE PRÉDICTIONS FUTURES ==========
                st.markdown("#### 📈 Prédictions Futures du Prix Bitcoin")
                
                fig_pred = go.Figure()
                
                # Prix historique
                # convert timestamps to plain python datetimes to avoid pandas Timestamp arithmetic issues
                hist_x = df_btc['timestamp'].dt.to_pydatetime() if hasattr(df_btc['timestamp'], 'dt') else df_btc['timestamp']
                fig_pred.add_trace(go.Scatter(
                    x=hist_x,
                    y=df_btc['price'],
                    name="Prix Historique",
                    line=dict(color='#F7931A', width=3),
                    mode='lines'
                ))
                
                # Couleurs pour chaque modèle
                colors = {
                    'Linear Regression': '#3B82F6',
                    'Random Forest': '#10B981',
                    'ARIMA': '#8B5CF6'
                }
                
                # Prédictions de chaque modèle
                for model_name, result in results.items():
                    future_df = result['future_predictions']
                    color = colors.get(model_name, '#6366F1')
                    
                    # Ligne de prédiction
                    fut_x = future_df['timestamp'].dt.to_pydatetime() if hasattr(future_df['timestamp'], 'dt') else future_df['timestamp']
                    fig_pred.add_trace(go.Scatter(
                        x=fut_x,
                        y=future_df['predicted_price'],
                        name=f"Prédiction {model_name}",
                        line=dict(color=color, width=2, dash='dash'),
                        mode='lines+markers'
                    ))
                    
                    # Intervalle de confiance (si disponible)
                    if 'lower_bound' in future_df.columns:
                        # build x list with python datetimes
                        fut_ts = future_df['timestamp'].dt.to_pydatetime() if hasattr(future_df['timestamp'], 'dt') else future_df['timestamp']
                        x_fill = list(fut_ts) + list(fut_ts)[::-1]
                        fig_pred.add_trace(go.Scatter(
                            x=x_fill,
                            y=future_df['upper_bound'].tolist() + future_df['lower_bound'].tolist()[::-1],
                            fill='toself',
                            fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.2)',
                            line=dict(color='rgba(255,255,255,0)'),
                            name=f"IC 95% {model_name}",
                            showlegend=True,
                            hoverinfo='skip'
                        ))
                
                # Ligne verticale séparant historique/prédiction
                last_date = df_btc['timestamp'].iloc[-1]
                # ensure x is passed as python datetime (or str) to avoid pandas Timestamp arithmetic issues inside plotly
                if hasattr(last_date, 'to_pydatetime'):
                    vline_x = last_date.to_pydatetime()
                else:
                    vline_x = str(last_date)

                # Add a vertical line as a shape (avoids internal add_vline timestamp/mean issues)
                fig_pred.add_shape(
                    type='line',
                    x0=vline_x,
                    x1=vline_x,
                    y0=0,
                    y1=1,
                    xref='x',
                    yref='paper',
                    line=dict(dash='dot', color='gray')
                )

                # Add annotation for the vertical line
                fig_pred.add_annotation(
                    x=vline_x,
                    y=1.0,
                    xref='x',
                    yref='paper',
                    text="Aujourd'hui",
                    showarrow=False,
                    yanchor='bottom'
                )
                
                fig_pred.update_layout(
                    title=dict(
                        text=f"Bitcoin: Prix Historique vs Prédictions ML ({prediction_days} jours)",
                        font=dict(size=18, color='#1E293B', family='Inter')
                    ),
                    xaxis=dict(
                        title="Date",
                        showgrid=True,
                        gridcolor='rgba(0,0,0,0.05)'
                    ),
                    yaxis=dict(
                        title="Prix ($)",
                        showgrid=True,
                        gridcolor='rgba(0,0,0,0.05)'
                    ),
                    hovermode='x unified',
                    height=600,
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family='Inter'),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                st.plotly_chart(fig_pred, use_container_width=True)
                
                # ========== TABLEAU DES PRÉDICTIONS ==========
                st.markdown("#### 📋 Tableau des Prédictions Détaillées")
                
                # Créer un tableau combiné
                combined_predictions = None
                
                for model_name, result in results.items():
                    future_df = result['future_predictions'][['timestamp', 'predicted_price']].copy()
                    future_df = future_df.rename(columns={'predicted_price': model_name})
                    
                    if combined_predictions is None:
                        combined_predictions = future_df
                    else:
                        combined_predictions = combined_predictions.merge(
                            future_df, on='timestamp', how='outer'
                        )
                
                # Formater le tableau
                combined_predictions['Date'] = combined_predictions['timestamp'].dt.strftime('%d/%m/%Y')
                
                # Calculer la moyenne et écart-type
                pred_cols = [col for col in combined_predictions.columns if col not in ['timestamp', 'Date']]
                combined_predictions['Moyenne'] = combined_predictions[pred_cols].mean(axis=1)
                combined_predictions['Écart-type'] = combined_predictions[pred_cols].std(axis=1)
                
                # Réorganiser les colonnes
                display_cols = ['Date'] + pred_cols + ['Moyenne', 'Écart-type']
                display_df = combined_predictions[display_cols]
                
                # Styler le dataframe
                styled_pred = display_df.style.format({
                    col: '${:,.2f}' for col in display_cols if col != 'Date'
                }).background_gradient(
                    subset=['Moyenne'],
                    cmap='RdYlGn'
                )
                
                st.dataframe(styled_pred, use_container_width=True)
                
                # ========== STATISTIQUES DES PRÉDICTIONS ==========
                with st.expander("📊 Statistiques et Insights des Prédictions"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("##### 📈 Tendance Prédite")
                        
                        current_price = df_btc['price'].iloc[-1]
                        final_prices = {
                            model_name: result['future_predictions']['predicted_price'].iloc[-1]
                            for model_name, result in results.items()
                        }
                        
                        avg_final_price = np.mean(list(final_prices.values()))
                        change_pct = ((avg_final_price - current_price) / current_price) * 100
                        
                        st.markdown(f"""
                        <div class="metric-card">
                            <p><strong>Prix Actuel:</strong> ${current_price:,.2f}</p>
                            <p><strong>Prix Prédit (moyenne {prediction_days}j):</strong> ${avg_final_price:,.2f}</p>
                            <p><strong>Changement Prédit:</strong> 
                                <span style="color: {'#10B981' if change_pct >= 0 else '#EF4444'};">
                                    {'+' if change_pct >= 0 else ''}{change_pct:.2f}%
                                </span>
                            </p>
                            <p><strong>Volatilité Prédite:</strong> ${np.std(list(final_prices.values())):,.2f}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("##### 🎯 Consensus des Modèles")
                        
                        # Analyser le consensus
                        predictions_list = list(final_prices.values())
                        min_pred = min(predictions_list)
                        max_pred = max(predictions_list)
                        spread = max_pred - min_pred
                        
                        if spread / avg_final_price < 0.02:
                            consensus = "🟢 Fort consensus"
                            confidence = "Haute"
                        elif spread / avg_final_price < 0.05:
                            consensus = "🟡 Consensus modéré"
                            confidence = "Moyenne"
                        else:
                            consensus = "🔴 Divergence importante"
                            confidence = "Faible"
                        
                        st.markdown(f"""
                        <div class="metric-card">
                            <p><strong>Consensus:</strong> {consensus}</p>
                            <p><strong>Confiance:</strong> {confidence}</p>
                            <p><strong>Prix Min Prédit:</strong> ${min_pred:,.2f}</p>
                            <p><strong>Prix Max Prédit:</strong> ${max_pred:,.2f}</p>
                            <p><strong>Écart:</strong> ${spread:,.2f} ({(spread/avg_final_price)*100:.2f}%)</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Feature Importance (si Random Forest)
                    if "Random Forest" in results:
                        st.markdown("##### 🔍 Importance des Features (Random Forest)")
                        
                        importance_df = results['Random Forest']['feature_importance'].head(10)
                        
                        fig_importance = go.Figure(go.Bar(
                            x=importance_df['importance'],
                            y=importance_df['feature'],
                            orientation='h',
                            marker=dict(
                                color=importance_df['importance'],
                                colorscale='Viridis'
                            )
                        ))
                        
                        fig_importance.update_layout(
                            title="Top 10 Features les plus importantes",
                            xaxis_title="Importance",
                            yaxis_title="Feature",
                            height=400,
                            plot_bgcolor='white'
                        )
                        
                        st.plotly_chart(fig_importance, use_container_width=True)
                
                st.success("✅ Prédictions générées avec succès !")
                
        except Exception as e:
            st.error(f"❌ Erreur lors des prédictions: {e}")
            import traceback
            with st.expander("Voir les détails de l'erreur"):
                st.code(traceback.format_exc())

else:
    if enable_predictions:
        st.info("ℹ️ Veuillez sélectionner au moins un modèle de prédiction")
    else:
        st.info("ℹ️ Activez les prédictions dans la sidebar pour voir les projections futures du prix Bitcoin")

# ==================== TAB 2 : PORTFOLIO ====================
with tab2:
    from portfolio_engine import (
        Portfolio,
        calculate_portfolio_metrics,
        calculate_asset_metrics,
        calculate_correlation_matrix
    )
    
    @st.cache_data(ttl=300)
    def load_portfolio_data():
        try:
            df = pd.read_csv('data/portfolio_prices.csv')
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        except Exception as e:
            return None
    
    df_portfolio = load_portfolio_data()
    
    if df_portfolio is None:
        st.error("⚠️ **Données portfolio indisponibles** - Exécutez : `python scripts/fetch_portfolio_data.py`")
    else:
        price_cols = [col for col in df_portfolio.columns if col.endswith('_price')]
        available_cryptos = [col.replace('_price', '') for col in price_cols]
        
        st.success(f"✅ **{len(df_portfolio)} points de données** chargés pour {len(available_cryptos)} cryptomonnaies")
        
        # ========== PRIX EN TEMPS RÉEL ==========
        st.markdown("""
        <div class="section-header">
            <h2>💰 Prix Actuels des Cryptomonnaies</h2>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(len(available_cryptos))
        
        crypto_colors = {
            'BTC': '#F7931A',
            'ETH': '#627EEA',
            'BNB': '#F3BA2F',
            'SOL': '#14F195',
            'ADA': '#0033AD'
        }
        
        for i, crypto in enumerate(available_cryptos):
            with cols[i]:
                current_price = df_portfolio[f"{crypto}_price"].iloc[-1]
                
                if len(df_portfolio) >= 24:
                    price_24h_ago = df_portfolio[f"{crypto}_price"].iloc[-24]
                    change_24h = ((current_price - price_24h_ago) / price_24h_ago) * 100
                else:
                    change_24h = 0
                
                color = crypto_colors.get(crypto, '#6366F1')
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {color}15 0%, {color}25 100%); 
                            padding: 1.25rem; border-radius: 10px; border: 2px solid {color}40;
                            text-align: center;">
                    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">
                        {crypto}
                    </div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: {color}; margin-bottom: 0.5rem;">
                        ${current_price:,.2f}
                    </div>
                    <div style="font-size: 0.95rem; font-weight: 600; 
                               color: {'#10B981' if change_24h >= 0 else '#EF4444'};">
                        {'▲' if change_24h >= 0 else '▼'} {abs(change_24h):.2f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        last_update = df_portfolio['timestamp'].iloc[-1]
        st.info(f"🕒 **Dernière mise à jour** : {last_update.strftime('%d/%m/%Y à %H:%M:%S')}")
        
        # ========== SIDEBAR PORTFOLIO ==========
        with st.sidebar:
            st.markdown("### ⚙️ Configuration Portfolio")
            
            st.markdown("#### 📊 Sélection des Actifs")
            
            if len(available_cryptos) < 3:
                st.error("⚠️ Minimum 3 cryptomonnaies requises")
                st.stop()
            
            default_selection = available_cryptos[:min(3, len(available_cryptos))]
            
            selected_cryptos = st.multiselect(
                "Choisissez vos actifs (minimum 3)",
                available_cryptos,
                default=default_selection
            )
            
            if len(selected_cryptos) < 3:
                st.warning("⚠️ Veuillez sélectionner au moins 3 cryptomonnaies")
                st.stop()
            
            st.markdown("#### ⚖️ Allocation du Capital")
            
            weight_mode = st.radio(
                "Mode d'allocation",
                ["Équipondéré", "Personnalisé"],
                help="Équipondéré = poids égaux pour tous les actifs"
            )
            
            weights = {}
            
            if weight_mode == "Équipondéré":
                equal_weight = 1.0 / len(selected_cryptos)
                for crypto in selected_cryptos:
                    weights[crypto] = equal_weight
                st.success(f"✅ Chaque actif : **{equal_weight*100:.2f}%**")
            else:
                st.markdown("**Ajustez les pourcentages** (total = 100%)")
                total = 0
                for crypto in selected_cryptos:
                    weight = st.slider(
                        f"{crypto}",
                        0, 100,
                        int(100 / len(selected_cryptos)),
                        1,
                        key=f"weight_{crypto}"
                    )
                    weights[crypto] = weight / 100
                    total += weight
                
                if abs(total - 100) > 0.1:
                    st.error(f"⚠️ Total actuel : **{total}%** (doit être 100%)")
                    st.stop()
                else:
                    st.success(f"✅ Total : **{total}%**")
            
            initial_capital_b = st.number_input(
                "💵 Capital Initial ($)",
                min_value=1000,
                max_value=1000000,
                value=10000,
                step=1000,
                key="capital_b"
            )
            
            st.markdown("#### 🔄 Rééquilibrage")
            
            rebalance_mode = st.selectbox(
                "Fréquence de rééquilibrage",
                ["Aucun", "Hebdomadaire (7 jours)", "Mensuel (30 jours)"],
                help="Le rééquilibrage ajuste automatiquement les poids"
            )
            
            rebalance_map = {
                "Aucun": "none",
                "Hebdomadaire (7 jours)": "weekly",
                "Mensuel (30 jours)": "monthly"
            }
            
            rebalance = rebalance_map[rebalance_mode]
        
        # ========== CALCUL DU PORTFOLIO ==========
        with st.spinner("⏳ Calcul du portfolio en cours..."):
            try:
                portfolio = Portfolio(
                    df_portfolio,
                    weights,
                    initial_capital_b,
                    rebalance
                )
                
                result_df = portfolio.run_backtest()
                portfolio_metrics = calculate_portfolio_metrics(result_df, initial_capital_b)
                
                assets_metrics = []
                for crypto in selected_cryptos:
                    prices = result_df[f"{crypto}_price"]
                    metrics = calculate_asset_metrics(prices, crypto)
                    assets_metrics.append(metrics)
                
                assets_metrics_df = pd.DataFrame(assets_metrics)
                corr_matrix = calculate_correlation_matrix(result_df, selected_cryptos)
                
            except Exception as e:
                st.error(f"❌ Erreur lors du calcul : {e}")
                import traceback
                st.code(traceback.format_exc())
                st.stop()
        
        # ========== MÉTRIQUES PORTFOLIO ==========
        st.markdown("""
        <div class="section-header">
            <h2>📊 Performance Globale du Portfolio</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "💰 Valeur Finale",
                f"${portfolio_metrics['final_value']:,.0f}",
                f"{portfolio_metrics['total_return']:.2f}%"
            )
        
        with col2:
            st.metric(
                "📈 Sharpe Ratio",
                f"{portfolio_metrics['sharpe_ratio']:.2f}"
            )
        
        with col3:
            st.metric(
                "📉 Max Drawdown",
                f"{portfolio_metrics['max_drawdown']:.2f}%"
            )
        
        with col4:
            st.metric(
                "🎯 Sortino Ratio",
                f"{portfolio_metrics['sortino_ratio']:.2f}"
            )
        
        with col5:
            st.metric(
                "📊 Volatilité",
                f"{portfolio_metrics['annual_volatility']:.2f}%"
            )
        
        # ========== GRAPHIQUE PORTFOLIO ==========
        st.markdown("""
        <div class="section-header">
            <h3>📈 Évolution du Portfolio vs Actifs Individuels</h3>
        </div>
        """, unsafe_allow_html=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=result_df['timestamp'],
            y=result_df['portfolio_value'],
            name="Portfolio Global",
            line=dict(color='#8B5CF6', width=4),
            fill='tozeroy',
            fillcolor='rgba(139, 92, 246, 0.1)'
        ))
        
        colors_map = {
            'BTC': '#F7931A',
            'ETH': '#627EEA',
            'BNB': '#F3BA2F',
            'SOL': '#14F195',
            'ADA': '#0033AD'
        }
        
        for crypto in selected_cryptos:
            prices = result_df[f"{crypto}_price"]
            normalized = (prices / prices.iloc[0]) * initial_capital_b
            
            fig.add_trace(go.Scatter(
                x=result_df['timestamp'],
                y=normalized,
                name=crypto,
                line=dict(
                    color=colors_map.get(crypto, '#6366F1'),
                    width=2,
                    dash='dot'
                ),
                visible='legendonly'
            ))
        
        fig.update_layout(
            title=dict(
                text="Comparaison Portfolio Global vs Actifs (normalisés au capital initial)",
                font=dict(size=18, color='#1E293B', family='Inter')
            ),
            xaxis=dict(
                title="Date",
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)'
            ),
            yaxis=dict(
                title="Valeur ($)",
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)'
            ),
            hovermode='x unified',
            height=600,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter'),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # ========== ALLOCATION & CORRÉLATION ==========
        st.markdown("""
        <div class="section-header">
            <h3>📊 Analyse de Diversification</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🥧 Répartition du Portfolio")
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=list(weights.keys()),
                values=list(weights.values()),
                hole=0.4,
                marker=dict(
                    colors=[colors_map.get(c, '#6366F1') for c in weights.keys()],
                    line=dict(color='white', width=2)
                ),
                textinfo='label+percent',
                textfont=dict(size=14, family='Inter', color='white'),
                hovertemplate='<b>%{label}</b><br>Allocation: %{percent}<br>Valeur: $%{value:.2f}<extra></extra>'
            )])
            
            fig_pie.update_layout(
                height=450,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05
                ),
                font=dict(family='Inter')
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("#### 🔥 Matrice de Corrélation")
            
            fig_corr = px.imshow(
                corr_matrix,
                text_auto='.2f',
                color_continuous_scale='RdYlGn',
                aspect="auto",
                labels=dict(color="Corrélation")
            )
            
            fig_corr.update_layout(
                height=450,
                font=dict(family='Inter'),
                xaxis=dict(side='bottom')
            )
            
            st.plotly_chart(fig_corr, use_container_width=True)
            
            st.info("💡 **Interprétation** : Une corrélation proche de 1 indique que les actifs évoluent ensemble, tandis qu'une corrélation proche de -1 indique qu'ils évoluent en sens inverse.")
        
        # ========== TABLEAU COMPARATIF ==========
        st.markdown("""
        <div class="section-header">
            <h3>📋 Tableau Comparatif des Performances</h3>
        </div>
        """, unsafe_allow_html=True)
        
        portfolio_row = {
            'asset': '🏆 PORTFOLIO',
            'total_return': portfolio_metrics['total_return'],
            'annual_return': portfolio_metrics['annual_return'],
            'annual_volatility': portfolio_metrics['annual_volatility'],
            'sharpe_ratio': portfolio_metrics['sharpe_ratio'],
            'max_drawdown': portfolio_metrics['max_drawdown']
        }
        
        comparison_df = pd.concat([
            pd.DataFrame([portfolio_row]),
            assets_metrics_df
        ], ignore_index=True)
        
        comparison_df['asset'] = comparison_df['asset'].apply(
            lambda x: x if x == '🏆 PORTFOLIO' else f"💎 {x}"
        )
        
        styled_df = comparison_df.style.format({
            'total_return': '{:.2f}%',
            'annual_return': '{:.2f}%',
            'annual_volatility': '{:.2f}%',
            'sharpe_ratio': '{:.2f}',
            'max_drawdown': '{:.2f}%'
        }).background_gradient(
            subset=['total_return', 'sharpe_ratio'],
            cmap='RdYlGn',
            vmin=-50,
            vmax=50
        ).background_gradient(
            subset=['max_drawdown'],
            cmap='RdYlGn_r',
            vmin=-100,
            vmax=0
        )
        
        st.dataframe(styled_df, use_container_width=True, height=400)
        
        # ========== MÉTRIQUES DÉTAILLÉES ==========
        with st.expander("📊 **Métriques Complètes et Analyse Approfondie**", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 💰 Analyse des Rendements")
                st.markdown(f"""
                <div class="metric-card">
                    <p><strong>Rendement Total :</strong> {portfolio_metrics['total_return']:.2f}%</p>
                    <p><strong>Rendement Annualisé :</strong> {portfolio_metrics['annual_return']:.2f}%</p>
                    <p><strong>Win Rate :</strong> {portfolio_metrics['win_rate']:.2f}%</p>
                    <p><strong>Capital Initial :</strong> ${initial_capital_b:,.0f}</p>
                    <p><strong>Capital Final :</strong> ${portfolio_metrics['final_value']:,.0f}</p>
                    <p><strong>Profit/Perte :</strong> ${portfolio_metrics['final_value'] - initial_capital_b:,.0f}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### 📊 Ratios de Performance")
                st.markdown(f"""
                <div class="metric-card">
                    <p><strong>Sharpe Ratio :</strong> {portfolio_metrics['sharpe_ratio']:.2f}</p>
                    <p><strong>Sortino Ratio :</strong> {portfolio_metrics['sortino_ratio']:.2f}</p>
                    <p><strong>Calmar Ratio :</strong> {portfolio_metrics['calmar_ratio']:.2f}</p>
                    <p><strong>Volatilité Annuelle :</strong> {portfolio_metrics['annual_volatility']:.2f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("#### 📉 Analyse du Risque")
                st.markdown(f"""
                <div class="metric-card">
                    <p><strong>Max Drawdown :</strong> <span style="color: #EF4444;">
                        {portfolio_metrics['max_drawdown']:.2f}%</span></p>
                    <p><strong>Volatilité :</strong> {portfolio_metrics['annual_volatility']:.2f}%</p>
                    <p><strong>Ratio Rendement/Risque :</strong> 
                        {(portfolio_metrics['annual_return'] / portfolio_metrics['annual_volatility'] if portfolio_metrics['annual_volatility'] > 0 else 0):.2f}</p>
                </div>
                """, unsafe_allow_html=True)

# ==================== TAB 3 : RAPPORTS ====================
with tab3:
    st.markdown("""
    <div class="section-header">
        <h2>📋 Centre de Rapports et Analyses</h2>
    </div>
    """, unsafe_allow_html=True)
    
    REPORTS_DIR = Path("reports")
    
    # Boutons de génération en haut
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🔄 Générer Rapport Bitcoin", type="primary", use_container_width=True):
            with st.spinner("⏳ Génération du rapport Bitcoin..."):
                try:
                    from scripts.daily_report import generate_daily_report
                    result = generate_daily_report()
                    if result:
                        st.success("✅ Rapport Bitcoin généré avec succès !")
                        st.rerun()
                    else:
                        st.error("❌ Échec de la génération")
                except Exception as e:
                    st.error(f"❌ Erreur : {e}")
    
    with col2:
        if st.button("🔄 Générer Rapport Portfolio", type="primary", use_container_width=True):
            with st.spinner("⏳ Génération du rapport Portfolio..."):
                try:
                    from scripts.portfolio_daily_report import generate_portfolio_daily_report
                    result = generate_portfolio_daily_report()
                    if result:
                        st.success("✅ Rapport Portfolio généré avec succès !")
                        st.rerun()
                    else:
                        st.error("❌ Échec de la génération")
                except Exception as e:
                    st.error(f"❌ Erreur : {e}")
    
    st.markdown("---")
    
    if not REPORTS_DIR.exists() or len(list(REPORTS_DIR.glob("*.txt"))) == 0:
        st.markdown("""
        <div class="info-box">
            <h3>📭 Aucun Rapport Disponible</h3>
            <p>Générez votre premier rapport en utilisant les boutons ci-dessus.</p>
            <p>Les rapports fournissent une analyse détaillée des performances et des métriques clés.</p>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        report_files = sorted(
            REPORTS_DIR.glob("*.txt"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        st.markdown(f"""
        <div class="success-box">
            <h4>✅ {len(report_files)} Rapport(s) Disponible(s)</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Affichage des rapports
        for idx, file in enumerate(report_files):
            try:
                text = file.read_text(encoding="utf-8")
                preview_lines = text.splitlines()[:12]
                preview = "\n".join(preview_lines)
                
                date_modif = datetime.fromtimestamp(file.stat().st_mtime)
                file_size = file.stat().st_size / 1024
                
                # Déterminer le type de rapport
                report_type = "📈 Bitcoin" if "bitcoin" in file.name.lower() else "💼 Portfolio"
                
                with st.expander(
                    f"{report_type} | {file.name} | {date_modif.strftime('%d/%m/%Y %H:%M')} | {file_size:.1f} KB",
                    expanded=(idx == 0)
                ):
                    st.markdown(f"""
                    <div style="background-color: #F8FAFC; padding: 1rem; border-radius: 8px; 
                                border-left: 4px solid #6366F1; margin-bottom: 1rem;">
                        <strong>📅 Date :</strong> {date_modif.strftime('%d/%m/%Y à %H:%M:%S')}<br>
                        <strong>📁 Fichier :</strong> {file.name}<br>
                        <strong>💾 Taille :</strong> {file_size:.1f} KB
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("**Aperçu du rapport :**")
                    st.code(preview, language="text")
                    
                    if len(preview_lines) < len(text.splitlines()):
                        st.info(f"ℹ️ Aperçu limité aux 12 premières lignes. Le rapport complet contient {len(text.splitlines())} lignes.")
                    
                    col1, col2, col3 = st.columns([1, 1, 2])
                    
                    with col1:
                        st.download_button(
                            label="⬇️ Télécharger",
                            data=text,
                            file_name=file.name,
                            mime="text/plain",
                            key=f"download_{file.name}_{idx}",
                            use_container_width=True
                        )
                    
                    with col2:
                        if st.button("👁️ Afficher Complet", key=f"view_{file.name}_{idx}", use_container_width=True):
                            st.markdown("---")
                            st.markdown("**📄 Contenu Complet du Rapport :**")
                            st.text_area(
                                "Rapport complet",
                                text,
                                height=500,
                                key=f"full_text_{file.name}_{idx}",
                                label_visibility="collapsed"
                            )
            
            except Exception as e:
                st.error(f"❌ Erreur lors de la lecture de {file.name} : {e}")

# ========== FOOTER PROFESSIONNEL ==========
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0 1rem 0; color: #64748B;">
    <p style="margin: 0; font-size: 0.9rem; font-weight: 500;">
        <strong>CryptoVision Pro</strong> | Plateforme d'Analyse de Trading
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem;">
        Module A: Analyse Bitcoin | Module B: Portfolio Multi-Actifs | Rapports & Insights
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; color: #94A3B8;">
        Développé avec Streamlit & Plotly | © 2024
    </p>
</div>
""", unsafe_allow_html=True)