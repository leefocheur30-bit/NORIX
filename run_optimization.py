# run_optimization.py
# Lance l'optimisation automatique des poids

from engines.weight_optimizer import WeightOptimizer
import logging

logging.basicConfig(level=logging.INFO)

def main():
    print("\n" + "="*60)
    print("   🧠  NORYX - OPTIMISATION DES POIDS")
    print("="*60 + "\n")
    
    optimizer = WeightOptimizer()
    weights = optimizer.optimize()
    optimizer.apply_weights()
    
    print("\n📊 NOUVEAUX POIDS :")
    print(f"   Poisson      : {weights['poisson']*100:.1f}%")
    print(f"   ELO          : {weights['elo']*100:.1f}%")
    print(f"   Monte Carlo  : {weights['monte_carlo']*100:.1f}%")
    print("\n✅ Optimisation terminée.")
    print("📁 Les poids ont été sauvegardés dans optimized_weights.json")

if __name__ == "__main__":
    main()