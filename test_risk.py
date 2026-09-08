from engines.risk import calculate_risk


consensus = {
    "home": 0.55,
    "draw": 0.23,
    "away": 0.22,
}


agreement_score = 1.0


result = calculate_risk(
    consensus,
    agreement_score,
)


print()
print("==============================================")
print("           NORYX - RISK ENGINE")
print("==============================================")
print()

print(
    f"Probabilité principale : "
    f"{max(consensus.values()) * 100:.2f}%"
)

print(
    f"Accord des moteurs : "
    f"{agreement_score * 100:.0f}%"
)

print()

print(
    f"Confiance : "
    f"{result['confidence'] * 100:.2f}%"
)

print(
    f"Niveau de risque : "
    f"{result['risk_level']}"
)

print()
print("==============================================")