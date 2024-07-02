import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

df = pd.read_csv("carro.csv")

# variáveis fuzzy
preco = ctrl.Antecedent(np.arange(df["preco"].min(), df["preco"].max(), 1), "preco")
taxa = ctrl.Antecedent(np.arange(df["taxa"].min(), df["taxa"].max(), 1), "taxa")
km_por_litro = ctrl.Antecedent(
    np.arange(df["km/l"].min(), df["km/l"].max(), 1), "km_por_litro"
)
km_rodado = ctrl.Antecedent(np.arange(df["km"].min(), df["km"].max(), 1), "km_rodado")
beneficio = ctrl.Consequent(np.arange(0, 11, 1), "beneficio")

# funções de pertinência
preco.automf(number=3, names=["baixo", "medio", "alto"])
taxa.automf(number=3, names=["baixo", "medio", "alto"])
km_por_litro.automf(number=3, names=["alto", "medio", "baixo"])
km_rodado.automf(number=3, names=["baixo", "medio", "alto"])
beneficio.automf(number=3, names=["baixo", "medio", "alto"])

# regras do sistema de controle
regras = [
    ctrl.Rule(
        preco["baixo"] & taxa["baixo"] & km_por_litro["medio"] & km_rodado["alto"],
        beneficio["medio"],
    ),
    ctrl.Rule(
        preco["baixo"] & taxa["baixo"] & km_por_litro["alto"] & km_rodado["baixo"],
        beneficio["alto"],
    ),
    ctrl.Rule(
        preco["baixo"] & taxa["medio"] & km_por_litro["baixo"] & km_rodado["alto"],
        beneficio["medio"],
    ),
    ctrl.Rule(
        preco["baixo"] & taxa["medio"] & km_por_litro["medio"] & km_rodado["alto"],
        beneficio["medio"],
    ),
    ctrl.Rule(
        preco["baixo"] & taxa["alto"] & km_por_litro["medio"] & km_rodado["alto"],
        beneficio["baixo"],
    ),
    ctrl.Rule(
        preco["baixo"] & taxa["alto"] & km_por_litro["baixo"] & km_rodado["alto"],
        beneficio["baixo"],
    ),
    ctrl.Rule(
        preco["baixo"] & taxa["baixo"] & km_por_litro["baixo"] & km_rodado["medio"],
        beneficio["alto"],
    ),
    ctrl.Rule(
        preco["alto"] & taxa["baixo"] & km_por_litro["baixo"] & km_rodado["medio"],
        beneficio["alto"],
    ),
    ctrl.Rule(
        preco["alto"] & taxa["baixo"] & km_por_litro["alto"] & km_rodado["alto"],
        beneficio["baixo"],
    ),
    ctrl.Rule(
        preco["alto"] & taxa["medio"] & km_por_litro["baixo"] & km_rodado["baixo"],
        beneficio["medio"],
    ),
    ctrl.Rule(
        preco["alto"] & taxa["medio"] & km_por_litro["medio"] & km_rodado["medio"],
        beneficio["medio"],
    ),
    ctrl.Rule(
        preco["alto"] & taxa["medio"] & km_por_litro["alto"] & km_rodado["alto"],
        beneficio["baixo"],
    ),
    ctrl.Rule(
        preco["alto"] & taxa["alto"] & km_por_litro["baixo"] & km_rodado["baixo"],
        beneficio["baixo"],
    ),
    ctrl.Rule(
        preco["alto"] & taxa["alto"] & km_por_litro["medio"] & km_rodado["medio"],
        beneficio["baixo"],
    ),
    ctrl.Rule(
        preco["alto"] & taxa["alto"] & km_por_litro["alto"] & km_rodado["alto"],
        beneficio["baixo"],
    ),
    ctrl.Rule(
        preco["medio"] & taxa["baixo"] & km_por_litro["baixo"] & km_rodado["baixo"],
        beneficio["alto"],
    ),
    ctrl.Rule(
        preco["medio"] & taxa["baixo"] & km_por_litro["medio"] & km_rodado["baixo"],
        beneficio["alto"],
    ),
    ctrl.Rule(
        preco["medio"] & taxa["baixo"] & km_por_litro["alto"] & km_rodado["medio"],
        beneficio["alto"],
    ),
    ctrl.Rule(
        preco["medio"] & taxa["medio"] & km_por_litro["medio"] & km_rodado["medio"],
        beneficio["medio"],
    ),
    ctrl.Rule(
        preco["medio"] & taxa["medio"] & km_por_litro["alto"] & km_rodado["alto"],
        beneficio["baixo"],
    ),
    ctrl.Rule(
        preco["medio"] & taxa["alto"] & km_por_litro["baixo"] & km_rodado["medio"],
        beneficio["medio"],
    ),
    ctrl.Rule(
        preco["medio"] & taxa["alto"] & km_por_litro["alto"] & km_rodado["alto"],
        beneficio["baixo"],
    ),
]

# sistema de controle e a simulação
recomendacao_compra = ctrl.ControlSystem(regras)
recomendacao = ctrl.ControlSystemSimulation(recomendacao_compra)

# entradas e calculo da saída para cada linha do DataFrame

teste = df.iloc[:20, :].copy()

for index, row in teste.iterrows():
    recomendacao.input["preco"] = row["preco"]
    recomendacao.input["taxa"] = row["taxa"]
    recomendacao.input["km_por_litro"] = row["km/l"]
    recomendacao.input["km_rodado"] = row["km"]
    recomendacao.compute()
    print(recomendacao.output["beneficio"])
    beneficio.view(sim=recomendacao)
    plt.show()
