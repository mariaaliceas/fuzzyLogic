import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

df = pd.read_csv("hospitalidade.csv")

# Definindo as variáveis fuzzy
avaliacao_hotel = ctrl.Antecedent(np.arange(1, 5, 1), "avaliacao_hotel")
proximidade_atracoes = ctrl.Antecedent(np.arange(1, 5, 1), "proximidade_atracoes")
precoNoite = ctrl.Antecedent(
    np.arange(
        df["precoNoite"].min(),
        df["precoNoite"].max() + 1,
        1,
    ),
    "precoNoite",
)
facilidades_hotel = ctrl.Antecedent(np.arange(1, 5, 1), "facilidades_hotel")
satisfacao_hospede = ctrl.Consequent(np.arange(0, 5, 1), "satisfacao_hospede")

# Funções de pertinência definidas manualmente
avaliacao_hotel["baixo"] = fuzz.trimf(avaliacao_hotel.universe, [1, 1, 3])
avaliacao_hotel["medio"] = fuzz.trimf(avaliacao_hotel.universe, [1, 3, 5])
avaliacao_hotel["alto"] = fuzz.trimf(avaliacao_hotel.universe, [3, 5, 5])

proximidade_atracoes["perto"] = fuzz.trimf(proximidade_atracoes.universe, [1, 1, 3])
proximidade_atracoes["medio"] = fuzz.trimf(proximidade_atracoes.universe, [1, 3, 5])
proximidade_atracoes["longe"] = fuzz.trimf(proximidade_atracoes.universe, [3, 5, 5])

precoNoite["baixo"] = fuzz.trimf(
    precoNoite.universe,
    [
        df["precoNoite"].min(),
        df["precoNoite"].min(),
        df["precoNoite"].mean(),
    ],
)
precoNoite["medio"] = fuzz.trimf(
    precoNoite.universe,
    [
        df["precoNoite"].min(),
        df["precoNoite"].mean(),
        df["precoNoite"].max(),
    ],
)
precoNoite["alto"] = fuzz.trimf(
    precoNoite.universe,
    [
        df["precoNoite"].mean(),
        df["precoNoite"].max(),
        df["precoNoite"].max(),
    ],
)

facilidades_hotel["poucas"] = fuzz.trimf(facilidades_hotel.universe, [1, 1, 3])
facilidades_hotel["medio"] = fuzz.trimf(facilidades_hotel.universe, [1, 3, 5])
facilidades_hotel["muitas"] = fuzz.trimf(facilidades_hotel.universe, [3, 5, 5])

satisfacao_hospede["baixo"] = fuzz.trimf(satisfacao_hospede.universe, [1, 1, 5])
satisfacao_hospede["medio"] = fuzz.trimf(satisfacao_hospede.universe, [1, 3, 5])
satisfacao_hospede["alto"] = fuzz.trimf(satisfacao_hospede.universe, [3, 5, 5])

# Regras do sistema de controle
regras = [
    ctrl.Rule(
        avaliacao_hotel["alto"]
        & proximidade_atracoes["perto"]
        & precoNoite["baixo"]
        & facilidades_hotel["muitas"],
        satisfacao_hospede["alto"],
    ),
    ctrl.Rule(
        avaliacao_hotel["alto"]
        & proximidade_atracoes["medio"]
        & precoNoite["baixo"]
        & facilidades_hotel["medio"],
        satisfacao_hospede["medio"],
    ),
    ctrl.Rule(
        avaliacao_hotel["alto"]
        & proximidade_atracoes["longe"]
        & precoNoite["alto"]
        & facilidades_hotel["poucas"],
        satisfacao_hospede["baixo"],
    ),
    ctrl.Rule(
        avaliacao_hotel["medio"]
        & proximidade_atracoes["perto"]
        & precoNoite["medio"]
        & facilidades_hotel["medio"],
        satisfacao_hospede["medio"],
    ),
    ctrl.Rule(
        avaliacao_hotel["medio"]
        & proximidade_atracoes["medio"]
        & precoNoite["alto"]
        & facilidades_hotel["poucas"],
        satisfacao_hospede["baixo"],
    ),
    ctrl.Rule(
        avaliacao_hotel["baixo"]
        & proximidade_atracoes["longe"]
        & precoNoite["alto"]
        & facilidades_hotel["poucas"],
        satisfacao_hospede["baixo"],
    ),
    ctrl.Rule(
        avaliacao_hotel["baixo"]
        & proximidade_atracoes["perto"]
        & precoNoite["baixo"]
        & facilidades_hotel["muitas"],
        satisfacao_hospede["medio"],
    ),
    ctrl.Rule(
        avaliacao_hotel["medio"]
        & proximidade_atracoes["medio"]
        & precoNoite["medio"]
        & facilidades_hotel["medio"],
        satisfacao_hospede["medio"],
    ),
    ctrl.Rule(
        avaliacao_hotel["alto"]
        & proximidade_atracoes["longe"]
        & precoNoite["alto"]
        & facilidades_hotel["muitas"],
        satisfacao_hospede["medio"],
    ),
    # Regras adicionais para garantir que todas as combinações são cobertas
    ctrl.Rule(
        avaliacao_hotel["baixo"]
        & proximidade_atracoes["medio"]
        & precoNoite["baixo"]
        & facilidades_hotel["medio"],
        satisfacao_hospede["medio"],
    ),
    ctrl.Rule(
        avaliacao_hotel["baixo"]
        & proximidade_atracoes["medio"]
        & precoNoite["medio"]
        & facilidades_hotel["poucas"],
        satisfacao_hospede["baixo"],
    ),
    ctrl.Rule(
        avaliacao_hotel["medio"]
        & proximidade_atracoes["longe"]
        & precoNoite["medio"]
        & facilidades_hotel["muitas"],
        satisfacao_hospede["medio"],
    ),
    ctrl.Rule(
        avaliacao_hotel["alto"]
        & proximidade_atracoes["medio"]
        & precoNoite["alto"]
        & facilidades_hotel["medio"],
        satisfacao_hospede["medio"],
    ),
]

# Sistema de controle e a simulação
sistema_controle = ctrl.ControlSystem(regras)
simulacao = ctrl.ControlSystemSimulation(sistema_controle)

# Entradas e cálculo da saída para cada linha do DataFrame
teste = df.iloc[:5, :].copy()

for index, row in teste.iterrows():
    simulacao.input["avaliacao_hotel"] = row["Avaliacao_Hotel"]
    simulacao.input["proximidade_atracoes"] = row["Proximidade_Atracoes"]
    simulacao.input["precoNoite"] = row["precoNoite"]
    simulacao.input["facilidades_hotel"] = row["Facilidades_Hotel"]
    simulacao.compute()
    print(
        f"Satisfação do hóspede (linha {index}): {simulacao.output['satisfacao_hospede']}"
    )
    satisfacao_hospede.view(sim=simulacao)
    plt.show()
