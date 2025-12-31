import requests
import pandas as pd
from datetime import datetime
import time
import os
from pathlib import Path

# Liste des cryptos supportées
AVAILABLE_CRYPTOS = {
    'bitcoin': 'BTC',
    'ethereum': 'ETH',
    'solana': 'SOL',
    'cardano': 'ADA',
    'binancecoin': 'BNB',
    'ripple': 'XRP',
    'polkadot': 'DOT',
    'avalanche-2': 'AVAX'
}

def fetch_multiple_cryptos_historical(crypto_ids, days=30):
    """
    Récupère l'historique de plusieurs cryptos
    crypto_ids: list comme ['bitcoin', 'ethereum', 'solana']
    """
    print(f"📥 Récupération de {days} jours pour {len(crypto_ids)} cryptos...")
    
    all_data = {}
    
    for crypto_id in crypto_ids:
        print(f"\n   → {crypto_id.upper()}...")
        
        url = "https://api.coingecko.com/api/v3/coins/{}/market_chart".format(crypto_id)
        
        params = {
            'vs_currency': 'usd',
            'days': days
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code != 200:
                print(f"      ❌ Erreur {response.status_code}")
                continue
            
            data = response.json()
            
            if 'prices' not in data:
                print(f"      ❌ Pas de données")
                continue
            
            prices = data['prices']
            df = pd.DataFrame(prices, columns=['timestamp', 'price'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['crypto'] = AVAILABLE_CRYPTOS[crypto_id]
            
            all_data[crypto_id] = df
            
            print(f"      ✅ {len(df)} points récupérés")
            
            # Pause pour éviter rate limit
            time.sleep(1)
            
        except Exception as e:
            print(f"      ❌ Erreur: {e}")
            continue
    
    if len(all_data) == 0:
        print("\n❌ Aucune donnée récupérée")
        return None
    
    # Fusionner toutes les données sur le timestamp
    print(f"\n🔄 Fusion des données...")
    
    # Prendre le premier crypto comme base
    first_crypto = list(all_data.keys())[0]
    merged_df = all_data[first_crypto][['timestamp']].copy()
    
    # Ajouter les prix de chaque crypto
    for crypto_id, df in all_data.items():
        symbol = AVAILABLE_CRYPTOS[crypto_id]
        merged_df = merged_df.merge(
            df[['timestamp', 'price']].rename(columns={'price': f'{symbol}_price'}),
            on='timestamp',
            how='outer'
        )
    
    # Trier par timestamp
    merged_df = merged_df.sort_values('timestamp').reset_index(drop=True)
    
    # Remplir les valeurs manquantes (forward fill)
    merged_df = merged_df.fillna(method='ffill')
    merged_df = merged_df.dropna()
    
    # Créer dossier data (proj root)
    data_dir = Path(__file__).resolve().parent.parent / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)

    # Sauvegarder
    target_file = data_dir / 'portfolio_prices.csv'
    merged_df.to_csv(target_file, index=False)

    print(f"\n✅ Données fusionnées : {len(merged_df)} points")
    print(f"   Cryptos: {', '.join([AVAILABLE_CRYPTOS[c] for c in all_data.keys()])}")
    print(f"   Du {merged_df['timestamp'].iloc[0]} au {merged_df['timestamp'].iloc[-1]}")
    print(f"   Fichier: {target_file}")
    
    return merged_df


def fetch_current_prices(crypto_ids):
    """
    Récupère les prix actuels de plusieurs cryptos
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    
    params = {
        'ids': ','.join(crypto_ids),
        'vs_currencies': 'usd',
        'include_24hr_change': 'true'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Erreur {response.status_code}")
            return None
        
        data = response.json()
        
        # Créer une nouvelle ligne pour chaque crypto
        timestamp = datetime.now()
        
        new_data = {'timestamp': timestamp}
        
        for crypto_id in crypto_ids:
            if crypto_id in data:
                symbol = AVAILABLE_CRYPTOS[crypto_id]
                new_data[f'{symbol}_price'] = data[crypto_id]['usd']
        
        # Ajouter à l'historique
        data_dir = Path(__file__).resolve().parent.parent / 'data'
        target_file = data_dir / 'portfolio_prices.csv'
        if target_file.exists():
            df = pd.read_csv(target_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            new_row = pd.DataFrame([new_data])
            df = pd.concat([df, new_row], ignore_index=True)
            df = df.drop_duplicates(subset=['timestamp'], keep='last')
            df = df.sort_values('timestamp').reset_index(drop=True)
            
            data_dir.mkdir(parents=True, exist_ok=True)
            df.to_csv(target_file, index=False)
            
            print(f"✅ Prix mis à jour pour {len(crypto_ids)} cryptos")
            for crypto_id in crypto_ids:
                symbol = AVAILABLE_CRYPTOS[crypto_id]
                if f'{symbol}_price' in new_data:
                    print(f"   {symbol}: ${new_data[f'{symbol}_price']:,.2f}")
        
        return new_data
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None


if __name__ == "__main__":
    print("="*70)
    print("   PORTFOLIO DATA FETCHER")
    print("="*70)
    
    # Choisir les cryptos (modifiable)
    selected_cryptos = ['bitcoin', 'ethereum', 'solana']
    
    print(f"\n📋 Cryptos sélectionnées: {', '.join([AVAILABLE_CRYPTOS[c] for c in selected_cryptos])}")
    
    print("\n=== RÉCUPÉRATION HISTORIQUE ===")
    df = fetch_multiple_cryptos_historical(selected_cryptos, days=30)
    
    if df is not None:
        print("\n✅ Succès !")
        
        print("\n=== TEST MISE À JOUR ===")
        time.sleep(2)
        fetch_current_prices(selected_cryptos)
        
        print("\n" + "="*70)
        print("🎉 DONNÉES PORTFOLIO PRÊTES !")
        print("="*70)