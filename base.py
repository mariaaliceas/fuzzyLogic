import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

df = pd.read_csv("hospitalidade.csv")

# variáveis fuzzy
avaliacaoHotel = ctrl.Antecedent(
    np.arange(df["Avaliacao_Hotel"].min(), df["Avaliacao_Hotel"].max(), 1),
    "Avaliacao_Hotel",
)
proximidadeAtracoes = ctrl.Antecedent(
    np.arange(df["Proximidade_Atracoes"].min(), df["Proximidade_Atracoes"].max(), 1),
    "Proximidade_Atracoes",
)
precoNoite = ctrl.Antecedent(
    np.arange(df["precoNoite"].min(), df["precoNoite"].max(), 1),
    "precoNoite",
)
facilidadesHotel = ctrl.Antecedent(
    np.arange(df["Facilidades_Hotel"].min(), df["Facilidades_Hotel"].max(), 1),
    "Facilidades_Hotel",
)
satisfacao_hospede = ctrl.Consequent(np.arange(0, 11, 1), "satisfacao_hospede")

# funções de pertinência
avaliacaoHotel.automf(number=3, names=["baixo", "medio", "alto"])
proximidadeAtracoes.automf(number=3, names=["baixo", "medio", "alto"])
precoNoite.automf(number=3, names=["baixo", "medio", "alto"])
facilidadesHotel.automf(number=3, names=["baixo", "medio", "alto"])
satisfacao_hospede.automf(number=3, names=["baixo", "medio", "alto"])

# regras do sistema de controle
regras = [
    ctrl.Rule(
        avaliacaoHotel["baixo"]
        & proximidadeAtracoes["baixo"]
        & precoNoite["medio"]
        & facilidadesHotel["alto"],
        satisfacao_hospede["medio"],
    ),
    ctrl.Rule(
        avaliacaoHotel["baixo"]
        & proximidadeAtracoes["baixo"]
        & precoNoite["alto"]
        & facilidadesHotel["baixo"],
        satisfacao_hospede["alto"],
    ),
    ctrl.Rule(
        avaliacaoHotel["baixo"]
        & proximidadeAtracoes["medio"]
        & precoNoite["baixo"]
        & facilidadesHotel["alto"],
        satisfacao_hospede["medio"],
    ),
    ctrl.Rule(
        avaliacaoHotel["baixo"]
        & proximidadeAtracoes["medio"]
        & precoNoite["medio"]
        & facilidadesHotel["alto"],
        satisfacao_hospede["medio"],
    ),
    ctrl.Rule(
        avaliacaoHotel["baixo"]
        & proximidadeAtracoes["alto"]
        & precoNoite["medio"]
        & facilidadesHotel["alto"],
        satisfacao_hospede["baixo"],
    ),
    ctrl.Rule(
        avaliacaoHotel["baixo"]
        & proximidadeAtracoes["alto"]
        & precoNoite["baixo"]
        & facilidadesHotel["alto"],
        satisfacao_hospede["baixo"],
    ),
    ctrl.Rule(
        avaliacaoHotel["baixo"]
        & proximidadeAtracoes["baixo"]
        & precoNoite["baixo"]
        & facilidadesHotel["medio"],
        satisfacao_hospede["alto"],
    ),
    ctrl.Rule(
        avaliacaoHotel["alto"]
        & proximidadeAtracoes["baixo"]
        & precoNoite["baixo"]
        & facilidadesHotel["medio"],
        satisfacao_hospede["alto"],
    ),
    ctrl.Rule(
        avaliacaoHotel["alto"]
        & proximidadeAtracoes["baixo"]
        & precoNoite["alto"]
        & facilidadesHotel["alto"],
        satisfacao_hospede["baixo"],
    ),
    ctrl.Rule(
        avaliacaoHotel["alto"]
        & proximidadeAtracoes["medio"]
        & precoNoite["baixo"]
        & facilidadesHotel["baixo"],
        satisfacao_hospede["medio"],
    ),
    ctrl.Rule(
        avaliacaoHotel["alto"]
        & proximidadeAtracoes["medio"]
        & precoNoite["medio"]
        & facilidadesHotel["medio"],
        satisfacao_hospede["medio"],
    ),
    ctrl.Rule(
        avaliacaoHotel["alto"]
        & proximidadeAtracoes["medio"]
        & precoNoite["alto"]
        & facilidadesHotel["alto"],
        satisfacao_hospede["baixo"],
    ),
    ctrl.Rule(
        avaliacaoHotel["alto"]
        & proximidadeAtracoes["alto"]
        & precoNoite["baixo"]
        & facilidadesHotel["baixo"],
        satisfacao_hospede["baixo"],
    ),
    ctrl.Rule(
        avaliacaoHotel["alto"]
        & proximidadeAtracoes["alto"]
        & precoNoite["medio"]
        & facilidadesHotel["medio"],
        satisfacao_hospede["baixo"],
    ),
    ctrl.Rule(
        avaliacaoHotel["alto"]
        & proximidadeAtracoes["alto"]
        & precoNoite["alto"]
        & facilidadesHotel["alto"],
        satisfacao_hospede["baixo"],
    ),
    ctrl.Rule(
        avaliacaoHotel["medio"]
        & proximidadeAtracoes["baixo"]
        & precoNoite["baixo"]
        & facilidadesHotel["baixo"],
        satisfacao_hospede["alto"],
    ),
    ctrl.Rule(
        avaliacaoHotel["medio"]
        & proximidadeAtracoes["baixo"]
        & precoNoite["medio"]
        & facilidadesHotel["baixo"],
        satisfacao_hospede["alto"],
    ),
    ctrl.Rule(
        avaliacaoHotel["medio"]
        & proximidadeAtracoes["baixo"]
        & precoNoite["alto"]
        & facilidadesHotel["medio"],
        satisfacao_hospede["alto"],
    ),
    ctrl.Rule(
        avaliacaoHotel["medio"]
        & proximidadeAtracoes["medio"]
        & precoNoite["medio"]
        & facilidadesHotel["medio"],
        satisfacao_hospede["medio"],
    ),
    ctrl.Rule(
        avaliacaoHotel["medio"]
        & proximidadeAtracoes["medio"]
        & precoNoite["alto"]
        & facilidadesHotel["alto"],
        satisfacao_hospede["baixo"],
    ),
    ctrl.Rule(
        avaliacaoHotel["medio"]
        & proximidadeAtracoes["alto"]
        & precoNoite["baixo"]
        & facilidadesHotel["medio"],
        satisfacao_hospede["medio"],
    ),
    ctrl.Rule(
        avaliacaoHotel["medio"]
        & proximidadeAtracoes["alto"]
        & precoNoite["alto"]
        & facilidadesHotel["alto"],
        satisfacao_hospede["baixo"],
    ),
]

# sistema de controle e a simulação
recomendacao_compra = ctrl.ControlSystem(regras)
recomendacao = ctrl.ControlSystemSimulation(recomendacao_compra)

# entradas e calculo da saída para cada linha do DataFrame

teste = df.iloc[:5, :].copy()

for index, row in teste.iterrows():
    recomendacao.input["Avaliacao_Hotel"] = row["Avaliacao_Hotel"]
    recomendacao.input["Proximidade_Atracoes"] = row["Proximidade_Atracoes"]
    recomendacao.input["precoNoite"] = row["precoNoite"]
    recomendacao.input["Facilidades_Hotel"] = row["Facilidades_Hotel"]
    recomendacao.compute()
    print(recomendacao.output["satisfacao_hospede"])
    satisfacao_hospede.view(sim=recomendacao)
    plt.show()
