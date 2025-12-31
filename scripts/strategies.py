import pandas as pd
import numpy as np

def buy_and_hold_strategy(prices, initial_capital=10000):
    """
    STRATÉGIE 1 : Buy and Hold
    Achète au début et garde jusqu'à la fin
    """
    # Acheter au premier prix
    initial_price = prices.iloc[0]
    shares = initial_capital / initial_price
    
    # Valeur du portfolio à chaque moment
    portfolio_value = shares * prices
    
    return portfolio_value


def moving_average_crossover_strategy(prices, short_window=20, long_window=50, initial_capital=10000):
    """
    STRATÉGIE 2 : Moving Average Crossover (Momentum)
    Achète quand MA courte > MA longue
    Vend quand MA courte < MA longue
    """
    # Calculer les moyennes mobiles
    short_ma = prices.rolling(window=short_window).mean()
    long_ma = prices.rolling(window=long_window).mean()
    
    # Variables de position
    cash = initial_capital
    shares = 0
    position = 0  # 0 = pas de position, 1 = position longue
    
    portfolio_values = []
    
    for i in range(len(prices)):
        current_price = prices.iloc[i]
        current_short_ma = short_ma.iloc[i]
        current_long_ma = long_ma.iloc[i]
        
        # Si pas assez de données pour les MA
        if pd.isna(current_short_ma) or pd.isna(current_long_ma):
            portfolio_values.append(initial_capital)
            continue
        
        # SIGNAL D'ACHAT : MA courte croise au-dessus de MA longue
        if current_short_ma > current_long_ma and position == 0:
            shares = cash / current_price
            cash = 0
            position = 1
            # print(f"📈 ACHAT à ${current_price:.2f}")
        
        # SIGNAL DE VENTE : MA courte croise en-dessous de MA longue
        elif current_short_ma < current_long_ma and position == 1:
            cash = shares * current_price
            shares = 0
            position = 0
            # print(f"📉 VENTE à ${current_price:.2f}")
        
        # Valeur actuelle du portfolio
        portfolio_value = cash + (shares * current_price)
        portfolio_values.append(portfolio_value)
    
    return pd.Series(portfolio_values, index=prices.index)


def simple_momentum_strategy(prices, window=14, initial_capital=10000):
    """
    STRATÉGIE 3 (BONUS) : Simple Momentum
    Achète si prix > moyenne mobile
    Vend si prix < moyenne mobile
    """
    ma = prices.rolling(window=window).mean()
    
    cash = initial_capital
    shares = 0
    position = 0
    
    portfolio_values = []
    
    for i in range(len(prices)):
        current_price = prices.iloc[i]
        current_ma = ma.iloc[i]
        
        if pd.isna(current_ma):
            portfolio_values.append(initial_capital)
            continue
        
        # ACHAT : prix au-dessus de la moyenne
        if current_price > current_ma and position == 0:
            shares = cash / current_price
            cash = 0
            position = 1
        
        # VENTE : prix en-dessous de la moyenne
        elif current_price < current_ma and position == 1:
            cash = shares * current_price
            shares = 0
            position = 0
        
        portfolio_value = cash + (shares * current_price)
        portfolio_values.append(portfolio_value)
    
    return pd.Series(portfolio_values, index=prices.index)


# ======== BACKTESTING ========

def backtest_strategy(prices, strategy_func, **kwargs):
    """
    Exécute le backtesting d'une stratégie
    """
    portfolio_values = strategy_func(prices, **kwargs)
    
    return portfolio_values


# ======== MÉTRIQUES ========

def calculate_metrics(portfolio_values, initial_capital=10000):
    """
    ÉTAPE 5 : Calculer tous les indicateurs & métriques
    """
    # Rendements
    returns = portfolio_values.pct_change().dropna()
    
    # 1. RENDEMENT TOTAL
    final_value = portfolio_values.iloc[-1]
    total_return = ((final_value - initial_capital) / initial_capital) * 100
    
    # 2. RENDEMENT ANNUALISÉ (approximation sur 30 jours)
    days = len(portfolio_values) / 24  # Données horaires -> jours
    annual_return = ((final_value / initial_capital) ** (365 / days) - 1) * 100
    
    # 3. VOLATILITÉ (écart-type des rendements annualisé)
    volatility = returns.std() * np.sqrt(24 * 365) * 100  # Annualisé
    
    # 4. MAX DRAWDOWN (perte maximale depuis le plus haut)
    cumulative = portfolio_values / portfolio_values.iloc[0]
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min() * 100
    
    # 5. SHARPE RATIO (rendement ajusté au risque)
    # On suppose un taux sans risque de 0% pour simplifier
    if returns.std() != 0:
        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(24 * 365)
    else:
        sharpe_ratio = 0
    
    # 6. WIN RATE (pourcentage de trades gagnants)
    winning_trades = (returns > 0).sum()
    total_trades = len(returns)
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
    
    # 7. PROFIT FACTOR
    gains = returns[returns > 0].sum()
    losses = abs(returns[returns < 0].sum())
    profit_factor = gains / losses if losses != 0 else np.inf
    
    return {
        'total_return': total_return,
        'annual_return': annual_return,
        'volatility': volatility,
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe_ratio,
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'final_value': final_value
    }


def print_metrics(metrics, strategy_name):
    """
    Affiche les métriques de manière lisible
    """
    print(f"\n{'='*50}")
    print(f"📊 MÉTRIQUES : {strategy_name}")
    print(f"{'='*50}")
    print(f"💰 Valeur finale       : ${metrics['final_value']:,.2f}")
    print(f"📈 Rendement total     : {metrics['total_return']:.2f}%")
    print(f"📅 Rendement annualisé : {metrics['annual_return']:.2f}%")
    print(f"📉 Max Drawdown        : {metrics['max_drawdown']:.2f}%")
    print(f"📊 Volatilité          : {metrics['volatility']:.2f}%")
    print(f"⚡ Sharpe Ratio        : {metrics['sharpe_ratio']:.2f}")
    print(f"🎯 Win Rate            : {metrics['win_rate']:.2f}%")
    print(f"💵 Profit Factor       : {metrics['profit_factor']:.2f}")
    print(f"{'='*50}\n")


# ======== TEST DES STRATÉGIES ========

if __name__ == "__main__":
    # Charger les données
    df = pd.read_csv('data/bitcoin_prices.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    prices = df['price']
    
    print(f"📊 Données chargées : {len(prices)} points")
    print(f"   Du {df['timestamp'].iloc[0]} au {df['timestamp'].iloc[-1]}")
    
    # STRATÉGIE 1 : Buy and Hold
    print("\n🔄 Test Stratégie 1 : Buy and Hold...")
    portfolio_bh = backtest_strategy(prices, buy_and_hold_strategy)
    metrics_bh = calculate_metrics(portfolio_bh)
    print_metrics(metrics_bh, "Buy and Hold")
    
    # STRATÉGIE 2 : Moving Average Crossover
    print("\n🔄 Test Stratégie 2 : MA Crossover...")
    portfolio_ma = backtest_strategy(prices, moving_average_crossover_strategy, 
                                     short_window=20, long_window=50)
    metrics_ma = calculate_metrics(portfolio_ma)
    print_metrics(metrics_ma, "MA Crossover")
    
    # STRATÉGIE 3 : Simple Momentum (bonus)
    print("\n🔄 Test Stratégie 3 : Simple Momentum...")
    portfolio_mom = backtest_strategy(prices, simple_momentum_strategy, window=14)
    metrics_mom = calculate_metrics(portfolio_mom)
    print_metrics(metrics_mom, "Simple Momentum")