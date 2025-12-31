import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import os
from pathlib import Path
from portfolio_engine import Portfolio, calculate_portfolio_metrics

def generate_portfolio_daily_report():
    """
    Génère un rapport quotidien du portfolio
    """
    now = datetime.now()
    print(f"📄 Génération rapport portfolio : {now.strftime('%d/%m/%Y %H:%M')}")
    
    try:
        # Charger les données
        data_file = Path(__file__).resolve().parent.parent / 'data' / 'portfolio_prices.csv'
        df = pd.read_csv(data_file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Détecter les cryptos
        price_cols = [col for col in df.columns if col.endswith('_price')]
        cryptos = [col.replace('_price', '') for col in price_cols]
        
        # Dernières 24h
        yesterday = now - timedelta(hours=24)
        df_24h = df[df['timestamp'] >= yesterday].copy()
        
        if len(df_24h) == 0:
            print("⚠️ Pas assez de données")
            return None
        
        # Calculer performance de chaque crypto
        crypto_performance = {}
        
        for crypto in cryptos:
            price_col = f"{crypto}_price"
            open_price = df_24h[price_col].iloc[0]
            close_price = df_24h[price_col].iloc[-1]
            high_price = df_24h[price_col].max()
            low_price = df_24h[price_col].min()
            change = ((close_price - open_price) / open_price) * 100
            
            crypto_performance[crypto] = {
                'open': open_price,
                'close': close_price,
                'high': high_price,
                'low': low_price,
                'change': change
            }
        
        # Identifier top/bottom
        sorted_cryptos = sorted(crypto_performance.items(), key=lambda x: x[1]['change'], reverse=True)
        top_winner = sorted_cryptos[0]
        top_loser = sorted_cryptos[-1]
        
        # Calculer portfolio (equal weight pour le rapport)
        weights = {crypto: 1.0/len(cryptos) for crypto in cryptos}
        
        portfolio = Portfolio(df_24h, weights, initial_capital=10000, rebalance='none')
        result_df = portfolio.run_backtest()
        portfolio_metrics = calculate_portfolio_metrics(result_df, 10000)
        
        # Créer le rapport
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║          PORTFOLIO DAILY REPORT - {now.strftime('%d/%m/%Y %H:%M')}          ║
╚════════════════════════════════════════════════════════════════╝

📊 PÉRIODE : Dernières 24 heures
{'─'*66}

💼 PORTFOLIO PERFORMANCE (Equal Weight)
   Rendement 24h      : {portfolio_metrics['total_return']:+.2f}%
   Valeur finale      : ${portfolio_metrics['final_value']:,.2f}
   Sharpe Ratio       : {portfolio_metrics['sharpe_ratio']:.2f}
   Max Drawdown       : {portfolio_metrics['max_drawdown']:.2f}%
   Volatilité         : {portfolio_metrics['annual_volatility']:.2f}%

{'─'*66}

💰 PERFORMANCE PAR ACTIF
"""
        
        for crypto, perf in crypto_performance.items():
            report += f"""
   {crypto}:
      Open   : ${perf['open']:,.2f}
      Close  : ${perf['close']:,.2f}
      High   : ${perf['high']:,.2f}
      Low    : ${perf['low']:,.2f}
      Change : {perf['change']:+.2f}%
"""
        
        report += f"""
{'─'*66}

🏆 TOP PERFORMER : {top_winner[0]} ({top_winner[1]['change']:+.2f}%)
📉 WORST PERFORMER : {top_loser[0]} ({top_loser[1]['change']:+.2f}%)

{'═'*66}

🎯 ANALYSE
"""
        
        # Analyse automatique
        if portfolio_metrics['total_return'] > 5:
            report += "\n   🚀 EXCELLENTE JOURNÉE - Portfolio en forte hausse"
        elif portfolio_metrics['total_return'] > 2:
            report += "\n   📈 BONNE JOURNÉE - Portfolio en hausse"
        elif portfolio_metrics['total_return'] > -2:
            report += "\n   ➡️ JOURNÉE STABLE - Portfolio peu volatil"
        elif portfolio_metrics['total_return'] > -5:
            report += "\n   📉 JOURNÉE DIFFICILE - Portfolio en baisse"
        else:
            report += "\n   ⚠️ JOURNÉE TRÈS DIFFICILE - Forte correction"
        
        # Alertes risque
        if abs(portfolio_metrics['max_drawdown']) > 10:
            report += "\n   🔴 ALERTE RISQUE : Drawdown important (>10%)"
        
        if portfolio_metrics['annual_volatility'] > 100:
            report += "\n   🌪️ ALERTE VOLATILITÉ : Marché très agité"
        
        # Diversification
        changes = [perf['change'] for perf in crypto_performance.values()]
        if max(changes) > 0 and min(changes) < 0:
            report += "\n   ⚖️ DIVERSIFICATION EFFECTIVE : Actifs découplés"
        
        report += f"\n\n{'═'*66}\n"
        report += f"Rapport généré : {now.strftime('%d/%m/%Y à %H:%M:%S')}\n"
        report += f"Nombre d'actifs : {len(cryptos)}\n"
        report += f"Points de données : {len(df_24h)}\n"
        report += f"{'═'*66}\n"
        
        # Sauvegarder (reports in project root)
        reports_dir = Path(__file__).resolve().parent.parent / 'reports'
        reports_dir.mkdir(parents=True, exist_ok=True)
        filename = reports_dir / f"portfolio_report_{now.strftime('%Y%m%d_%H%M%S')}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"✅ Rapport sauvegardé : {filename}")
        print("\n" + report)
        
        return filename, report
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    generate_portfolio_daily_report()