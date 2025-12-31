import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class Portfolio:
    """
    Classe pour gérer un portfolio multi-actifs avec rebalancing
    """
    
    def __init__(self, prices_df, weights, initial_capital=10000, rebalance='none'):
        """
        prices_df: DataFrame avec colonnes [timestamp, BTC_price, ETH_price, ...]
        weights: dict comme {'BTC': 0.5, 'ETH': 0.3, 'SOL': 0.2}
        rebalance: 'none', 'weekly', 'monthly'
        """
        self.prices_df = prices_df.copy()
        self.weights = weights
        self.initial_capital = initial_capital
        self.rebalance = rebalance
        
        # Vérifier que les poids somment à 1
        total_weight = sum(weights.values())
        if abs(total_weight - 1.0) > 0.01:
            raise ValueError(f"Les poids doivent sommer à 1.0 (actuel: {total_weight})")
        
        # Assets
        self.assets = list(weights.keys())
        
        # Résultats
        self.portfolio_values = []
        self.holdings = {}  # Nombre de parts de chaque crypto
        
    def run_backtest(self):
        """
        Exécute le backtest du portfolio
        """
        cash = self.initial_capital
        
        # Allocation initiale
        for asset in self.assets:
            price_col = f"{asset}_price"
            initial_price = self.prices_df[price_col].iloc[0]
            allocation = self.initial_capital * self.weights[asset]
            self.holdings[asset] = allocation / initial_price
        
        cash = 0  # Tout investi
        
        # Calculer les dates de rebalancing
        rebalance_dates = self._get_rebalance_dates()
        
        # Parcourir chaque point de temps
        for i, row in self.prices_df.iterrows():
            timestamp = row['timestamp']
            
            # Rebalancing si nécessaire
            if timestamp in rebalance_dates and i > 0:
                total_value = self._calculate_portfolio_value(row)
                self._rebalance_portfolio(row, total_value)
            
            # Calculer la valeur totale
            portfolio_value = self._calculate_portfolio_value(row)
            self.portfolio_values.append(portfolio_value)
        
        # Ajouter au DataFrame
        self.prices_df['portfolio_value'] = self.portfolio_values
        
        return self.prices_df
    
    def _calculate_portfolio_value(self, row):
        """Calcule la valeur actuelle du portfolio"""
        total_value = 0
        
        for asset in self.assets:
            price_col = f"{asset}_price"
            current_price = row[price_col]
            total_value += self.holdings[asset] * current_price
        
        return total_value
    
    def _rebalance_portfolio(self, row, total_value):
        """Rebalance le portfolio aux poids initiaux"""
        for asset in self.assets:
            price_col = f"{asset}_price"
            current_price = row[price_col]
            target_allocation = total_value * self.weights[asset]
            self.holdings[asset] = target_allocation / current_price
    
    def _get_rebalance_dates(self):
        """Retourne les dates de rebalancing"""
        if self.rebalance == 'none':
            return []
        
        dates = []
        start_date = self.prices_df['timestamp'].iloc[0]
        end_date = self.prices_df['timestamp'].iloc[-1]
        
        if self.rebalance == 'weekly':
            # Tous les 7 jours
            current = start_date + timedelta(days=7)
            while current <= end_date:
                # Trouver la date la plus proche dans les données
                closest = self.prices_df.iloc[(self.prices_df['timestamp'] - current).abs().argsort()[:1]]['timestamp'].values[0]
                dates.append(closest)
                current += timedelta(days=7)
        
        elif self.rebalance == 'monthly':
            # Tous les 30 jours
            current = start_date + timedelta(days=30)
            while current <= end_date:
                closest = self.prices_df.iloc[(self.prices_df['timestamp'] - current).abs().argsort()[:1]]['timestamp'].values[0]
                dates.append(closest)
                current += timedelta(days=30)
        
        return dates


def calculate_portfolio_metrics(portfolio_df, initial_capital=10000):
    """
    Calcule toutes les métriques du portfolio
    """
    portfolio_values = portfolio_df['portfolio_value']
    returns = portfolio_values.pct_change().dropna()
    
    # 1. Performance totale
    final_value = portfolio_values.iloc[-1]
    total_return = ((final_value - initial_capital) / initial_capital) * 100
    
    # 2. Rendement annualisé
    days = len(portfolio_df) / 24  # Données horaires
    annual_return = ((final_value / initial_capital) ** (365 / days) - 1) * 100
    
    # 3. Volatilité annualisée
    annual_volatility = returns.std() * np.sqrt(24 * 365) * 100
    
    # 4. Sharpe Ratio (taux sans risque = 0%)
    sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(24 * 365) if returns.std() != 0 else 0
    
    # 5. Sortino Ratio (pénalise seulement la volatilité négative)
    downside_returns = returns[returns < 0]
    downside_std = downside_returns.std() * np.sqrt(24 * 365)
    sortino_ratio = (returns.mean() * 24 * 365) / downside_std if downside_std != 0 else 0
    
    # 6. Max Drawdown
    cumulative = portfolio_values / portfolio_values.iloc[0]
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min() * 100
    
    # 7. Calmar Ratio (rendement annualisé / max drawdown)
    calmar_ratio = abs(annual_return / max_drawdown) if max_drawdown != 0 else 0
    
    # 8. Win Rate
    winning_periods = (returns > 0).sum()
    win_rate = (winning_periods / len(returns)) * 100 if len(returns) > 0 else 0
    
    return {
        'final_value': final_value,
        'total_return': total_return,
        'annual_return': annual_return,
        'annual_volatility': annual_volatility,
        'sharpe_ratio': sharpe_ratio,
        'sortino_ratio': sortino_ratio,
        'max_drawdown': max_drawdown,
        'calmar_ratio': calmar_ratio,
        'win_rate': win_rate
    }


def calculate_asset_metrics(prices, asset_name):
    """
    Calcule les métriques pour un seul actif
    """
    returns = prices.pct_change().dropna()
    
    initial = prices.iloc[0]
    final = prices.iloc[-1]
    total_return = ((final - initial) / initial) * 100
    
    days = len(prices) / 24
    annual_return = ((final / initial) ** (365 / days) - 1) * 100
    
    annual_volatility = returns.std() * np.sqrt(24 * 365) * 100
    sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(24 * 365) if returns.std() != 0 else 0
    
    cumulative = prices / prices.iloc[0]
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min() * 100
    
    return {
        'asset': asset_name,
        'total_return': total_return,
        'annual_return': annual_return,
        'annual_volatility': annual_volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown
    }


def calculate_correlation_matrix(prices_df, assets):
    """
    Calcule la matrice de corrélation
    """
    price_cols = [f"{asset}_price" for asset in assets]
    
    # Extraire les prix
    prices_only = prices_df[price_cols].copy()
    prices_only.columns = assets  # Renommer pour clarté
    
    # Calculer la corrélation
    corr_matrix = prices_only.corr()
    
    return corr_matrix


if __name__ == "__main__":
    # Test
    print("🧪 Test du Portfolio Engine")
    
    from pathlib import Path
    data_file = Path(__file__).resolve().parent.parent / 'data' / 'portfolio_prices.csv'
    df = pd.read_csv(data_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    weights = {'BTC': 0.5, 'ETH': 0.3, 'SOL': 0.2}
    
    portfolio = Portfolio(df, weights, initial_capital=10000, rebalance='weekly')
    result_df = portfolio.run_backtest()
    
    metrics = calculate_portfolio_metrics(result_df)
    
    print("\n📊 Métriques du Portfolio:")
    for key, value in metrics.items():
        print(f"   {key}: {value:.2f}")