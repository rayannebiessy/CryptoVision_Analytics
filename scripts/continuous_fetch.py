import time
from datetime import datetime
from fetch_data import fetch_current_bitcoin

def run_continuous_updates():
    """
    Met à jour les données toutes les 5 minutes
    """
    print("🚀 Démarrage de la mise à jour continue...")
    print("   Mise à jour toutes les 5 minutes")
    print("   Appuie sur Ctrl+C pour arrêter\n")
    
    iteration = 0
    
    while True:
        try:
            iteration += 1
            print(f"\n{'='*60}")
            print(f"🔄 Mise à jour #{iteration} - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"{'='*60}")
            
            price, change = fetch_current_bitcoin()
            
            if price:
                print(f"✅ Succès ! Prochaine mise à jour dans 5 minutes...")
            else:
                print(f"⚠️ Échec. Nouvelle tentative dans 5 minutes...")
            
            # Attendre 5 minutes (300 secondes)
            time.sleep(300)
            
        except KeyboardInterrupt:
            print("\n\n⏹️ Arrêt du programme.")
            break
            
        except Exception as e:
            print(f"❌ Erreur inattendue : {e}")
            print("   Nouvelle tentative dans 1 minute...")
            time.sleep(60)

if __name__ == "__main__":
    run_continuous_updates()