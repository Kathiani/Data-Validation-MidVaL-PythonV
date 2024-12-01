import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Função para aplicar Bias (offset)
def aplicar_bias(dados, bias_valor):
    """
    Aplica um bias (offset) constante aos dados.

    :param dados: Array ou série de dados originais.
    :param bias_valor: Valor constante do bias (offset).
    :return: Série ajustada com bias.
    """
    return dados + bias_valor


# Exemplo de dados (uma função seno)
dados_originais = np.sin(np.linspace(0, 10, 100))  # Série simulada como exemplo

# Valor do bias (offset)
bias_valor = 2  # O valor do bias que será somado a todos os dados

# Aplicar o bias
dados_com_bias = aplicar_bias(dados_originais, bias_valor)

# Criar DataFrame para visualização
df = pd.DataFrame({
    "Original": dados_originais,
    "Com Bias": dados_com_bias
})

# Plotar os dados
plt.figure(figsize=(10, 6))
plt.plot(df['Original'], label='Série Original', color='blue')
plt.plot(df['Com Bias'], label='Série com Bias', color='red')
plt.title('Aplicação de Bias (Offset) em Série Temporal')
plt.xlabel('Índice')
plt.ylabel('Valor')
plt.legend()
plt.grid(True)
plt.show()
