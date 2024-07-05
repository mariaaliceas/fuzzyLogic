import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definindo as variáveis do universo
Volume_Trafego = ctrl.Antecedent(np.arange(0, 11, 1), "Volume_Trafego")
Condicao_Estrada = ctrl.Antecedent(np.arange(0, 11, 1), "Condicao_Estrada")
Hora_Dia = ctrl.Antecedent(np.arange(0, 24, 1), "Hora_Dia")
Dia_Semana = ctrl.Antecedent(np.arange(0, 7, 1), "Dia_Semana")
Duracao_Semaforo = ctrl.Consequent(np.arange(0, 101, 1), "Duracao_Semaforo")

# Definindo as funções de pertinência
Volume_Trafego["baixo"] = fuzz.trimf(Volume_Trafego.universe, [0, 0, 5])
Volume_Trafego["medio"] = fuzz.trimf(Volume_Trafego.universe, [0, 5, 10])
Volume_Trafego["alto"] = fuzz.trimf(Volume_Trafego.universe, [5, 10, 10])

Condicao_Estrada["boa"] = fuzz.trimf(Condicao_Estrada.universe, [0, 0, 5])
Condicao_Estrada["media"] = fuzz.trimf(Condicao_Estrada.universe, [0, 5, 10])
Condicao_Estrada["ruim"] = fuzz.trimf(Condicao_Estrada.universe, [5, 10, 10])

Hora_Dia["madrugada"] = fuzz.trimf(Hora_Dia.universe, [0, 0, 6])
Hora_Dia["manha"] = fuzz.trimf(Hora_Dia.universe, [6, 12, 12])
Hora_Dia["tarde"] = fuzz.trimf(Hora_Dia.universe, [12, 18, 18])
Hora_Dia["noite"] = fuzz.trimf(Hora_Dia.universe, [18, 24, 24])

Dia_Semana["semana"] = fuzz.trimf(Dia_Semana.universe, [0, 3, 4])
Dia_Semana["fim_semana"] = fuzz.trimf(Dia_Semana.universe, [4, 6, 6])

Duracao_Semaforo["curta"] = fuzz.trimf(Duracao_Semaforo.universe, [0, 0, 50])
Duracao_Semaforo["media"] = fuzz.trimf(Duracao_Semaforo.universe, [0, 50, 100])
Duracao_Semaforo["longa"] = fuzz.trimf(Duracao_Semaforo.universe, [50, 100, 100])

# Definindo as regras
regra1 = ctrl.Rule(
    Volume_Trafego["alto"]
    & Condicao_Estrada["ruim"]
    & Hora_Dia["manha"]
    & Dia_Semana["semana"],
    Duracao_Semaforo["curta"],
)
regra2 = ctrl.Rule(
    Volume_Trafego["baixo"]
    & Condicao_Estrada["boa"]
    & Hora_Dia["madrugada"]
    & Dia_Semana["fim_semana"],
    Duracao_Semaforo["longa"],
)
regra3 = ctrl.Rule(
    Volume_Trafego["medio"]
    & Condicao_Estrada["media"]
    & Hora_Dia["tarde"]
    & Dia_Semana["semana"],
    Duracao_Semaforo["media"],
)
#
# regra4 = ctrl.Rule(
# Volume_Trafego["alto"]
# & Condicao_Estrada["media"]
# & Hora_Dia["noite"]
# & Dia_Semana["fim_semana"],
# Duracao_Semaforo["media"],
# )

# Criando e simulando um controlador fuzzy
sistema_controle = ctrl.ControlSystem([regra1, regra2, regra3])  # , regra4])
simulacao = ctrl.ControlSystemSimulation(sistema_controle)

# Definindo um conjunto de casos de teste
casos_teste = [
    {"Volume_Trafego": 8, "Condicao_Estrada": 9, "Hora_Dia": 8, "Dia_Semana": 2},
    {"Volume_Trafego": 3, "Condicao_Estrada": 1, "Hora_Dia": 2, "Dia_Semana": 5},
    {"Volume_Trafego": 5, "Condicao_Estrada": 5, "Hora_Dia": 15, "Dia_Semana": 3},
    {"Volume_Trafego": 10, "Condicao_Estrada": 1, "Hora_Dia": 15, "Dia_Semana": 4},
    {"Volume_Trafego": 1, "Condicao_Estrada": 10, "Hora_Dia": 5, "Dia_Semana": 2},
]

# Executando os casos de teste
for i, caso_teste in enumerate(casos_teste):
    simulacao.input["Volume_Trafego"] = caso_teste["Volume_Trafego"]
    simulacao.input["Condicao_Estrada"] = caso_teste["Condicao_Estrada"]
    simulacao.input["Hora_Dia"] = caso_teste["Hora_Dia"]
    simulacao.input["Dia_Semana"] = caso_teste["Dia_Semana"]

    # Computando a duração do semáforo
    simulacao.compute()

    # Imprimindo o resultado
    print(f"Caso de teste {i+1}: {simulacao.output['Duracao_Semaforo']}")

    # Plotando a saída do sistema fuzzy
    Duracao_Semaforo.view(simulacao)

    # Exibindo o gráfico
    plt.show()
