import requests
import pandas as pd
from datetime import datetime
import time
import os
from pathlib import Path

def fetch_historical_bitcoin(days=30):
    """
    Récupère l'historique Bitcoin sur X jours
    VERSION GRATUITE - Sans interval=hourly
    """
    print(f"📥 Récupération de {days} jours d'historique Bitcoin...")
    
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    
    # IMPORTANT : Ne pas mettre interval pour la version gratuite
    # CoinGecko donne automatiquement :
    # - 1-2 jours : données toutes les 5 minutes
    # - 3-30 jours : données toutes les heures
    # - 31-90 jours : données quotidiennes
    params = {
        'vs_currency': 'usd',
        'days': days
        # PAS de 'interval' pour la version gratuite !
    }
    
    try:
        print("   Connexion à CoinGecko API...")
        response = requests.get(url, params=params, timeout=15)
        
        print(f"   Status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Erreur API: Status {response.status_code}")
            print(f"   Réponse: {response.text[:300]}")
            return None
        
        data = response.json()
        
        # Vérifier que 'prices' existe
        if 'prices' not in data:
            print(f"❌ Erreur: 'prices' non trouvé")
            return None
        
        prices = data['prices']
        
        if len(prices) == 0:
            print("❌ Aucune donnée reçue")
            return None
        
        print(f"   ✅ {len(prices)} points reçus")
        
        # Convertir en DataFrame
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['change_24h'] = 0.0
        
        # Créer dossier data (chemin projet)
        BASE_DIR = Path(__file__).resolve().parents[1]
        DATA_DIR = BASE_DIR / 'data'
        BITCOIN_CSV = DATA_DIR / 'bitcoin_prices.csv'
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        # Sauvegarder
        df.to_csv(BITCOIN_CSV, index=False)
        
        print(f"✅ {len(df)} lignes sauvegardées dans {BITCOIN_CSV}")
        print(f"   Du {df['timestamp'].iloc[0]} au {df['timestamp'].iloc[-1]}")
        print(f"   Premier prix : ${df['price'].iloc[0]:,.2f}")
        print(f"   Dernier prix : ${df['price'].iloc[-1]:,.2f}")
        
        return df
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return None


def fetch_current_bitcoin():
    """
    Récupère le prix actuel du Bitcoin
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    
    params = {
        'ids': 'bitcoin',
        'vs_currencies': 'usd',
        'include_24hr_change': 'true'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Erreur API: Status {response.status_code}")
            return None, None
        
        data = response.json()
        
        if 'bitcoin' not in data:
            print(f"❌ 'bitcoin' non trouvé")
            return None, None
        
        price = data['bitcoin']['usd']
        change = data['bitcoin'].get('usd_24h_change', 0.0)
        
        timestamp = datetime.now()
        
        new_row = pd.DataFrame([{
            'timestamp': timestamp,
            'price': price,
            'change_24h': change
        }])
        
        # Ajouter à l'historique (chemin basé sur le dossier du projet)
        BASE_DIR = Path(__file__).resolve().parents[1]
        DATA_DIR = BASE_DIR / 'data'
        BITCOIN_CSV = DATA_DIR / 'bitcoin_prices.csv'

        if BITCOIN_CSV.exists():
            df = pd.read_csv(BITCOIN_CSV)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = pd.concat([df, new_row], ignore_index=True)
            df = df.drop_duplicates(subset=['timestamp'], keep='last')
            df = df.sort_values('timestamp').reset_index(drop=True)
            df.to_csv(BITCOIN_CSV, index=False)

            print(f"✅ Prix mis à jour: ${price:,.2f} (Change: {change:.2f}%)")
        else:
            # Si le fichier historique est absent, créer le dossier et écrire la dernière valeur
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            new_row.to_csv(BITCOIN_CSV, index=False)
            print(f"ℹ️ Fichier historique introuvable — créé {BITCOIN_CSV} avec la dernière valeur.")
        
        return price, change
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None, None


if __name__ == "__main__":
    print("="*70)
    print("   BITCOIN DATA FETCHER - VERSION GRATUITE")
    print("="*70)
    
    print("\n=== RÉCUPÉRATION HISTORIQUE ===")
    df = fetch_historical_bitcoin(days=30)
    
    if df is not None:
        print("\n✅ Initialisation réussie !")
        
        print("\n=== TEST MISE À JOUR ===")
        time.sleep(2)
        fetch_current_bitcoin()
        
        print("\n" + "="*70)
        print("🎉 TOUT FONCTIONNE !")
        print("="*70)
    else:
        print("\n❌ Échec")