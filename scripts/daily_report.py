import pathlib
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path

def generate_daily_report():
    """
    Génère un rapport quotidien sur Bitcoin et garde tous les historiques
    """
    print("📄 Génération du rapport quotidien...")
    
    try:
        BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
        DATA_PATH = BASE_DIR / "data" / "bitcoin_prices.csv"

        df = pd.read_csv(DATA_PATH)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Filtrer les données des dernières 24 heures
        now = datetime.now()
        yesterday = now - timedelta(hours=24)
        
        df_today = df[df['timestamp'] >= yesterday].copy()
        
        if len(df_today) == 0:
            print("⚠️ Pas de données pour les dernières 24h")
            return
        
        # Calculer les statistiques
        open_price = df_today['price'].iloc[0]
        close_price = df_today['price'].iloc[-1]
        high_price = df_today['price'].max()
        low_price = df_today['price'].min()
        volatility = df_today['price'].std()
        price_change = ((close_price - open_price) / open_price) * 100
        
        cumulative = df_today['price'] / df_today['price'].iloc[0]
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min() * 100
        
        price_range = high_price - low_price
        range_pct = (price_range / open_price) * 100
        
        # Créer le rapport
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║                    BITCOIN DAILY REPORT                        ║
║                    {now.strftime('%d %B %Y - %H:%M')}                    ║
╚════════════════════════════════════════════════════════════════╝

📊 RÉSUMÉ 24 HEURES
{'─'*66}

💰 PRIX
   Open (24h)         : ${open_price:,.2f}
   Close (actuel)     : ${close_price:,.2f}
   High               : ${high_price:,.2f}
   Low                : ${low_price:,.2f}
   
📈 PERFORMANCE
   Change 24h         : {price_change:+.2f}%
   Range 24h          : ${price_range:,.2f} ({range_pct:.2f}%)
   
📉 RISQUE
   Volatilité         : ${volatility:.2f}
   Max Drawdown 24h   : {max_drawdown:.2f}%

📊 STATISTIQUES
   Nombre de points   : {len(df_today)}
   Prix moyen 24h     : ${df_today['price'].mean():,.2f}
   Prix médian 24h    : ${df_today['price'].median():,.2f}

{'═'*66}

🎯 ANALYSE RAPIDE
"""

        # Analyse simple
        if price_change > 5:
            analysis = "   🚀 FORTE HAUSSE - Bitcoin en forte progression !"
        elif price_change > 2:
            analysis = "   📈 HAUSSE - Tendance haussière modérée"
        elif price_change > -2:
            analysis = "   ➡️ STABLE - Bitcoin en consolidation"
        elif price_change > -5:
            analysis = "   📉 BAISSE - Tendance baissière modérée"
        else:
            analysis = "   ⚠️ FORTE BAISSE - Correction significative"
        
        report += analysis + "\n"
        
        if abs(max_drawdown) > 10:
            report += "   ⚠️ ATTENTION - Drawdown important détecté !\n"
        if volatility > 1000:
            report += "   🌪️ VOLATILITÉ ÉLEVÉE - Marché très agité\n"
        
        report += f"\n{'═'*66}\n"
        report += f"Rapport généré le {now.strftime('%d/%m/%Y à %H:%M:%S')}\n"
        report += f"{'═'*66}\n"

        # --- REPORT FOLDER ---
        REPORTS_DIR = BASE_DIR / "reports"
        REPORTS_DIR.mkdir(exist_ok=True)  # créer le dossier si n'existe pas

        # Nom du fichier avec date + heure + minute + seconde pour éviter l’écrasement
        filename = REPORTS_DIR / f"daily_report_{now.strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Sauvegarder le rapport
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Rapport sauvegardé : {filename}")
        print("\n" + report)
        
        return report
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération : {e}")
        return None

if __name__ == "__main__":
    generate_daily_report()
