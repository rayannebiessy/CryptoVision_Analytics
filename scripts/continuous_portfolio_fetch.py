import time
from datetime import datetime
from fetch_portfolio_data import fetch_current_prices

# Liste des cryptos (doit correspondre à ce que tu as initialisé)
CRYPTO_IDS = ['bitcoin', 'ethereum', 'solana']

def run_continuous_portfolio_updates():
    """
    Met à jour les prix du portfolio toutes les 5 minutes
    """
    print("🚀 DÉMARRAGE - Mise à jour continue du portfolio")
    print(f"   Cryptos surveillées : {', '.join(CRYPTO_IDS)}")
    print("   Fréquence : Toutes les 5 minutes")
    print("   Ctrl+C pour arrêter\n")
    
    iteration = 0
    
    while True:
        try:
            iteration += 1
            print(f"\n{'='*70}")
            print(f"🔄 Mise à jour #{iteration} - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"{'='*70}")
            
            result = fetch_current_prices(CRYPTO_IDS)
            
            if result:
                print("✅ Succès ! Prochaine mise à jour dans 5 minutes...")
            else:
                print("⚠️ Échec. Nouvelle tentative dans 5 minutes...")
            
            time.sleep(300)  # 5 minutes
            
        except KeyboardInterrupt:
            print("\n\n⏹️ Arrêt du programme.")
            break
        except Exception as e:
            print(f"❌ Erreur : {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_continuous_portfolio_updates()