import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definindo as variáveis do universo
Avaliacao_Hotel = ctrl.Antecedent(np.arange(1, 5, 1), "Avaliacao_Hotel")  # estrelas
Proximidade_Atracoes = ctrl.Antecedent(
    np.arange(10, 2000, 1), "Proximidade_Atracoes"
)  # metros
Preco_Noite = ctrl.Antecedent(np.arange(100, 5000, 10), "Preco_Noite")  # reais
Facilidades_Hotel = ctrl.Antecedent(
    np.arange(1, 10, 1), "Facilidades_Hotel"
)  # quantidade
Satisfacao_hospede = ctrl.Consequent(np.arange(1, 10, 1), "Satisfacao_hospede")

# Definindo as funções de pertinência
Avaliacao_Hotel["baixo"] = fuzz.trimf(Avaliacao_Hotel.universe, [1, 1, 3])
Avaliacao_Hotel["medio"] = fuzz.trimf(Avaliacao_Hotel.universe, [2, 3, 5])
Avaliacao_Hotel["alto"] = fuzz.trimf(Avaliacao_Hotel.universe, [3, 5, 5])

Proximidade_Atracoes["baixo"] = fuzz.trimf(Proximidade_Atracoes.universe, [10, 10, 500])
Proximidade_Atracoes["medio"] = fuzz.trimf(Proximidade_Atracoes.universe, [1, 5, 5])
Proximidade_Atracoes["alto"] = fuzz.trimf(Proximidade_Atracoes.universe, [3, 5, 5])
