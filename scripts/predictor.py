"""
Bitcoin Price Prediction Module
Implements multiple ML models: Linear Regression, ARIMA, Random Forest, LSTM
"""
from pathlib import Path
import pathlib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ML Libraries
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Time Series
try:
    from statsmodels.tsa.arima.model import ARIMA
    ARIMA_AVAILABLE = True
except ImportError:
    ARIMA_AVAILABLE = False
    print("⚠️ ARIMA non disponible - installer: pip install statsmodels")


class BitcoinPredictor:
    """
    Classe pour prédire le prix du Bitcoin avec plusieurs modèles
    """
    
    def __init__(self, df, prediction_days=7):
        """
        Args:
            df: DataFrame avec colonnes 'timestamp' et 'price'
            prediction_days: Nombre de jours à prédire
        """
        self.df = df.copy()
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.df = self.df.sort_values('timestamp').reset_index(drop=True)
        self.prediction_days = prediction_days
        
        # Préparer les features
        self._prepare_features()
        
    def _prepare_features(self):
        """Créer des features pour le ML"""
        df = self.df.copy()
        
        # Features temporelles
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_month'] = df['timestamp'].dt.day
        
        # Features techniques
        df['returns'] = df['price'].pct_change()
        df['log_returns'] = np.log(df['price'] / df['price'].shift(1))
        
        # Moving averages
        df['ma_7'] = df['price'].rolling(window=7, min_periods=1).mean()
        df['ma_14'] = df['price'].rolling(window=14, min_periods=1).mean()
        df['ma_30'] = df['price'].rolling(window=30, min_periods=1).mean()
        
        # Volatilité
        df['volatility_7'] = df['returns'].rolling(window=7, min_periods=1).std()
        df['volatility_14'] = df['returns'].rolling(window=14, min_periods=1).std()
        
        # RSI (Relative Strength Index)
        delta = df['price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14, min_periods=1).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14, min_periods=1).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # Lags
        for i in [1, 2, 3, 7, 14]:
            df[f'price_lag_{i}'] = df['price'].shift(i)
        
        # Remplir les NaN
        df = df.fillna(method='bfill').fillna(method='ffill')
        
        self.df_features = df
    
    def train_test_split(self, test_size=0.2):
        """Séparer en train/test"""
        split_idx = int(len(self.df_features) * (1 - test_size))
        
        train_df = self.df_features.iloc[:split_idx].copy()
        test_df = self.df_features.iloc[split_idx:].copy()
        
        # Features à utiliser
        feature_cols = [
            'day_of_week', 'hour', 'day_of_month',
            'ma_7', 'ma_14', 'ma_30',
            'volatility_7', 'volatility_14',
            'rsi',
            'price_lag_1', 'price_lag_2', 'price_lag_3',
            'price_lag_7', 'price_lag_14'
        ]
        
        X_train = train_df[feature_cols].values
        y_train = train_df['price'].values
        
        X_test = test_df[feature_cols].values
        y_test = test_df['price'].values
        
        return X_train, X_test, y_train, y_test, feature_cols
    
    def predict_linear_regression(self):
        """Prédiction avec régression linéaire"""
        print("📊 Entraînement Régression Linéaire...")
        
        X_train, X_test, y_train, y_test, feature_cols = self.train_test_split()
        
        # Normalisation
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Entraînement
        model = LinearRegression()
        model.fit(X_train_scaled, y_train)
        
        # Prédictions sur test
        y_pred = model.predict(X_test_scaled)
        
        # Métriques
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        # Prédiction future
        future_predictions = self._predict_future(model, scaler, feature_cols)
        
        return {
            'model_name': 'Linear Regression',
            'predictions': y_pred,
            'actual': y_test,
            'mae': mae,
            'rmse': rmse,
            'r2': r2,
            'future_predictions': future_predictions,
            'model': model,
            'scaler': scaler
        }
    
    def predict_random_forest(self):
        """Prédiction avec Random Forest"""
        print("🌲 Entraînement Random Forest...")
        
        X_train, X_test, y_train, y_test, feature_cols = self.train_test_split()
        
        # Entraînement
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        
        # Prédictions
        y_pred = model.predict(X_test)
        
        # Métriques
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': feature_cols,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Prédiction future
        future_predictions = self._predict_future_rf(model, feature_cols)
        
        return {
            'model_name': 'Random Forest',
            'predictions': y_pred,
            'actual': y_test,
            'mae': mae,
            'rmse': rmse,
            'r2': r2,
            'future_predictions': future_predictions,
            'feature_importance': feature_importance,
            'model': model
        }
    
    def predict_arima(self, order=(5, 1, 0)):
        """Prédiction avec ARIMA"""
        if not ARIMA_AVAILABLE:
            return None
        
        print("📈 Entraînement ARIMA...")
        
        try:
            # Utiliser seulement les prix
            prices = self.df['price'].values
            
            # Split
            split_idx = int(len(prices) * 0.8)
            train = prices[:split_idx]
            test = prices[split_idx:]
            
            # Entraînement
            model = ARIMA(train, order=order)
            model_fit = model.fit()
            
            # Prédictions sur test
            y_pred = model_fit.forecast(steps=len(test))
            
            # Métriques
            mae = mean_absolute_error(test, y_pred)
            rmse = np.sqrt(mean_squared_error(test, y_pred))
            
            # Prédiction future
            future_pred = model_fit.forecast(steps=self.prediction_days)
            
            # Confidence intervals
            forecast_result = model_fit.get_forecast(steps=self.prediction_days)
            conf_int = forecast_result.conf_int()
            # statsmodels may return a numpy array for conf_int in some versions; ensure DataFrame
            if not hasattr(conf_int, 'iloc'):
                try:
                    conf_int = pd.DataFrame(conf_int)
                except Exception:
                    # fallback: convert to numpy then DataFrame
                    conf_int = pd.DataFrame(np.asarray(conf_int))
            
            future_dates = pd.date_range(
                start=self.df['timestamp'].iloc[-1] + timedelta(hours=1),
                periods=self.prediction_days,
                freq='D'
            )
            
            future_predictions = pd.DataFrame({
                'timestamp': future_dates,
                'predicted_price': future_pred,
                'lower_bound': conf_int.iloc[:, 0],
                'upper_bound': conf_int.iloc[:, 1]
            })
            
            return {
                'model_name': 'ARIMA',
                'predictions': y_pred,
                'actual': test,
                'mae': mae,
                'rmse': rmse,
                'r2': None,
                'future_predictions': future_predictions,
                'model': model_fit
            }
            
        except Exception as e:
            print(f"❌ Erreur ARIMA: {e}")
            return None
    
    def _predict_future(self, model, scaler, feature_cols):
        """Prédire les prochains jours (Linear Regression)"""
        last_data = self.df_features.iloc[-1:].copy()
        predictions = []
        dates = []
        
        current_date = self.df['timestamp'].iloc[-1]
        
        for i in range(self.prediction_days):
            # Préparer features
            X_future = last_data[feature_cols].values
            X_future_scaled = scaler.transform(X_future)
            
            # Prédire
            pred_price = model.predict(X_future_scaled)[0]
            predictions.append(pred_price)
            
            # Date future
            future_date = current_date + timedelta(days=i+1)
            dates.append(future_date)
            
            # Mettre à jour pour prochaine prédiction
            last_data = last_data.copy()
            last_data['price'] = pred_price
            last_data['price_lag_1'] = last_data['price'].values[0]
            last_data['ma_7'] = (last_data['ma_7'].values[0] * 0.9 + pred_price * 0.1)
        
        return pd.DataFrame({
            'timestamp': dates,
            'predicted_price': predictions
        })
    
    def _predict_future_rf(self, model, feature_cols):
        """Prédire les prochains jours (Random Forest)"""
        last_data = self.df_features.iloc[-1:].copy()
        predictions = []
        lower_bounds = []
        upper_bounds = []
        dates = []
        
        current_date = self.df['timestamp'].iloc[-1]
        
        for i in range(self.prediction_days):
            X_future = last_data[feature_cols].values
            
            # Prédiction moyenne
            pred_price = model.predict(X_future)[0]
            
            # Intervalle de confiance (approximatif via trees)
            tree_predictions = np.array([tree.predict(X_future)[0] 
                                        for tree in model.estimators_])
            std = np.std(tree_predictions)
            
            predictions.append(pred_price)
            lower_bounds.append(pred_price - 1.96 * std)
            upper_bounds.append(pred_price + 1.96 * std)
            
            future_date = current_date + timedelta(days=i+1)
            dates.append(future_date)
            
            # Update features
            last_data = last_data.copy()
            last_data['price'] = pred_price
            last_data['price_lag_1'] = pred_price
        
        return pd.DataFrame({
            'timestamp': dates,
            'predicted_price': predictions,
            'lower_bound': lower_bounds,
            'upper_bound': upper_bounds
        })
    
    def compare_models(self):
        """Comparer tous les modèles"""
        results = {}
        
        # Linear Regression
        lr_result = self.predict_linear_regression()
        results['Linear Regression'] = lr_result
        
        # Random Forest
        rf_result = self.predict_random_forest()
        results['Random Forest'] = rf_result
        
        # ARIMA
        if ARIMA_AVAILABLE:
            arima_result = self.predict_arima()
            if arima_result:
                results['ARIMA'] = arima_result
        
        return results


def calculate_confidence_interval(predictions, confidence=0.95):
    """Calculer l'intervalle de confiance"""
    std = np.std(predictions)
    z_score = 1.96 if confidence == 0.95 else 2.576  # 95% ou 99%
    
    margin = z_score * std
    
    return predictions - margin, predictions + margin


# ========== EXEMPLE D'UTILISATION ==========
if __name__ == "__main__":
    print("="*70)
    print("   BITCOIN PRICE PREDICTION - ML MODELS")
    print("="*70)
    
    BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
    DATA_PATH = BASE_DIR / "data" / "bitcoin_prices.csv"

    df = pd.read_csv(DATA_PATH)
    print(f"\n📊 Données chargées: {len(df)} points")
    print(f"   Du {df['timestamp'].iloc[0]} au {df['timestamp'].iloc[-1]}")
    
    # Créer le prédicteur
    predictor = BitcoinPredictor(df, prediction_days=7)
    
    # Comparer les modèles
    print("\n" + "="*70)
    print("   COMPARAISON DES MODÈLES")
    print("="*70)
    
    results = predictor.compare_models()
    
    # Afficher les performances
    print("\n📊 PERFORMANCES SUR LES DONNÉES DE TEST:")
    print("-" * 70)
    
    for model_name, result in results.items():
        print(f"\n{result['model_name']}:")
        print(f"  MAE:  ${result['mae']:,.2f}")
        print(f"  RMSE: ${result['rmse']:,.2f}")
        if result['r2']:
            print(f"  R²:   {result['r2']:.4f}")
        
        # Afficher prédictions futures
        print(f"\n  Prédictions futures ({predictor.prediction_days} jours):")
        future_df = result['future_predictions']
        for idx, row in future_df.head(3).iterrows():
            date_str = row['timestamp'].strftime('%Y-%m-%d')
            price = row['predicted_price']
            print(f"    {date_str}: ${price:,.2f}")
        
        if len(future_df) > 3:
            print(f"    ... et {len(future_df)-3} jours de plus")
    
    print("\n" + "="*70)
    print("✅ PRÉDICTIONS TERMINÉES !")
    print("="*70)