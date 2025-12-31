import time
import schedule
from datetime import datetime
from daily_report import generate_daily_report

def job():
    """
    Fonction qui sera exécutée toutes les 10 minutes
    """
    print(f"\n{'='*70}")
    print(f"⏰ Exécution du rapport - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"{'='*70}")
    
    try:
        generate_daily_report()
        print("✅ Rapport généré avec succès")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def run_scheduler():
    """
    Lance le scheduler qui tourne en continu
    """
    print("🚀 DÉMARRAGE DU SCHEDULER DE RAPPORTS")
    print("="*70)
    print("📋 Configuration :")
    print("   - Fréquence : Toutes les 10 minutes")
    print("   - Premier rapport : Immédiatement")
    print("   - Appuie sur Ctrl+C pour arrêter")
    print("="*70)
    
    # Programmer la tâche toutes les 10 minutes
    schedule.every(10).minutes.do(job)
    
    # Exécuter immédiatement un premier rapport
    print("\n📝 Génération du premier rapport...")
    job()
    
    # Boucle infinie
    print("\n⏳ En attente... Prochain rapport dans 10 minutes")
    
    while True:
        schedule.run_pending()
        time.sleep(30)  # Vérifier toutes les 30 secondes

if __name__ == "__main__":
    run_scheduler()

