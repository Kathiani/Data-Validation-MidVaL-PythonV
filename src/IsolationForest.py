import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# Simular dados de temperatura
np.random.seed(42)
temperatures = np.random.normal(loc=42, scale=5, size=10)  # Dados normais
temperatures = np.append(temperatures, [50, 55, 60])  # Adicionar valores anômalos

# Reshape dos dados para ajuste dos modelos
temperatures = temperatures.reshape(-1, 1)

# Modelo Isolation Forest
iso_forest = IsolationForest(contamination=0.1, random_state=42)
iso_forest.fit(temperatures)
iso_preds = iso_forest.predict(temperatures)

# Visualizar os resultados
plt.figure(figsize=(12, 6))
plt.title("Isolation Forest para Validação de Dados de Temperatura")
scatter = plt.scatter(np.arange(len(temperatures)), temperatures, c=iso_preds, cmap='coolwarm', s=100, edgecolor='k')

# Adicionar números aos pontos
for i, txt in enumerate(temperatures):
    plt.annotate(f'{txt[0]:.1f}', (i, temperatures[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Adicionar barra de cores
plt.colorbar(scatter, label="Anomaly Score")

plt.xlabel("Index")
plt.ylabel("Temperature")
plt.tight_layout()
plt.show()

# Exibir os resultados
print("Isolation Forest Predictions:", iso_preds)
