from skfuzzy import control
from matplotlib import pyplot # type: ignore
import numpy

# variaveis antecedentes
avaliacao_hotel = control.Antecedent(numpy.arange(1, 5, 1), "avaliacao_hotel")
proximidade_atracoes = control.Antecedent(numpy.arange(10, 2000, 100), "proximidade_atracoes")
preco_noite = control.Antecedent(numpy.arange(100, 5000, 10), "preco_noite")
facilidades_hotel = control.Antecedent(numpy.arange(1, 10, 1), "facilidades_hotel")

# variavel consequente
satisfacao_hospede = control.Consequent(numpy.arange(1, 10, 1), "satisfacao_hospede")

# funcoes de pertinencia (membership)
avaliacao_hotel.automf(number=3, names=["baixa", "media", "alta"])
proximidade_atracoes.automf(number=3, names=["perto", "medio", "longe"])
preco_noite.automf(number=3, names=["baixo", "medio", "alto"])
facilidades_hotel.automf(number=3, names=["poucas", "moderadas", "muitas"])
satisfacao_hospede.automf(number=3, names=["baixa", "media", "alta"])

regras = [
    control.Rule(
        avaliacao_hotel["baixa"] & proximidade_atracoes["longe"] & preco_noite["medio"] & facilidades_hotel["muitas"],
        satisfacao_hospede["baixa"],
    ),
    control.Rule(
        avaliacao_hotel["alta"] & proximidade_atracoes["medio"] & preco_noite["alto"] & facilidades_hotel["poucas"],
        satisfacao_hospede["media"],
    ),
    control.Rule(
        avaliacao_hotel["baixa"] & proximidade_atracoes["medio"] & preco_noite["baixo"] & facilidades_hotel["muitas"],
        satisfacao_hospede["media"],
    ),
    control.Rule(
        avaliacao_hotel["baixa"] & proximidade_atracoes["medio"] & preco_noite["medio"] & facilidades_hotel["muitas"],
        satisfacao_hospede["media"],
    ),
    control.Rule(
        avaliacao_hotel["media"] & proximidade_atracoes["perto"] & preco_noite["medio"] & facilidades_hotel["muitas"],
        satisfacao_hospede["alta"],
    ),
    control.Rule(
        avaliacao_hotel["media"] & proximidade_atracoes["medio"] & preco_noite["baixo"] & facilidades_hotel["poucas"],
        satisfacao_hospede["media"],
    ),
    control.Rule(
        avaliacao_hotel["baixa"] & proximidade_atracoes["longe"] & preco_noite["baixo"] & facilidades_hotel["moderadas"],
        satisfacao_hospede["baixa"],
    ),
    control.Rule(
        avaliacao_hotel["alta"] & proximidade_atracoes["longe"] & preco_noite["baixo"] & facilidades_hotel["moderadas"],
        satisfacao_hospede["media"],
    ),
    control.Rule(
        avaliacao_hotel["alta"] & proximidade_atracoes["longe"] & preco_noite["alto"] & facilidades_hotel["muitas"],
        satisfacao_hospede["media"],
    ),
    control.Rule(
        avaliacao_hotel["alta"] & proximidade_atracoes["medio"] & preco_noite["baixo"] & facilidades_hotel["poucas"],
        satisfacao_hospede["alta"],
    ),
    control.Rule(
        avaliacao_hotel["alta"] & proximidade_atracoes["medio"] & preco_noite["medio"] & facilidades_hotel["moderadas"],
        satisfacao_hospede["alta"],
    ),
    control.Rule(
        avaliacao_hotel["alta"] & proximidade_atracoes["medio"] & preco_noite["alto"] & facilidades_hotel["muitas"],
        satisfacao_hospede["media"],
    ),
    control.Rule(
        avaliacao_hotel["alta"] & proximidade_atracoes["perto"] & preco_noite["baixo"] & facilidades_hotel["poucas"],
        satisfacao_hospede["alta"],
    ),
    control.Rule(
        avaliacao_hotel["alta"] & proximidade_atracoes["perto"] & preco_noite["medio"] & facilidades_hotel["moderadas"],
        satisfacao_hospede["alta"],
    ),
    control.Rule(
        avaliacao_hotel["alta"] & proximidade_atracoes["perto"] & preco_noite["alto"] & facilidades_hotel["muitas"],
        satisfacao_hospede["media"],
    ),
    control.Rule(
        avaliacao_hotel["media"] & proximidade_atracoes["longe"] & preco_noite["baixo"] & facilidades_hotel["poucas"],
        satisfacao_hospede["baixa"],
    ),
    control.Rule(
        avaliacao_hotel["media"] & proximidade_atracoes["longe"] & preco_noite["medio"] & facilidades_hotel["poucas"],
        satisfacao_hospede["baixa"],
    ),
    control.Rule(
        avaliacao_hotel["media"] & proximidade_atracoes["longe"] & preco_noite["alto"] & facilidades_hotel["moderadas"],
        satisfacao_hospede["baixa"],
    ),
    control.Rule(
        avaliacao_hotel["media"] & proximidade_atracoes["medio"] & preco_noite["medio"] & facilidades_hotel["moderadas"],
        satisfacao_hospede["media"],
    ),
    control.Rule(
        avaliacao_hotel["media"] & proximidade_atracoes["medio"] & preco_noite["alto"] & facilidades_hotel["muitas"],
        satisfacao_hospede["baixa"],
    ),
    control.Rule(
        avaliacao_hotel["media"] & proximidade_atracoes["perto"] & preco_noite["baixo"] & facilidades_hotel["moderadas"],
        satisfacao_hospede["alta"],
    ),
    control.Rule(
        avaliacao_hotel["media"] & proximidade_atracoes["perto"] & preco_noite["alto"] & facilidades_hotel["muitas"],
        satisfacao_hospede["media"],
    ),
    control.Rule(
        avaliacao_hotel["alta"] & proximidade_atracoes["perto"] & preco_noite["baixo"] & facilidades_hotel["muitas"],
        satisfacao_hospede["alta"],
    )
]

testes = [
    {'avaliacao_hotel': 3, 'proximidade_atracoes': 500, 'preco_noite': 1800, 'facilidades_hotel': 9},
    {'avaliacao_hotel': 5, 'proximidade_atracoes': 910, 'preco_noite': 4500, 'facilidades_hotel': 2},
    {'avaliacao_hotel': 5, 'proximidade_atracoes': 10, 'preco_noite': 100, 'facilidades_hotel': 10},
    {'avaliacao_hotel': 1, 'proximidade_atracoes': 1500, 'preco_noite': 200, 'facilidades_hotel': 7},
]

simulacao = control.ControlSystemSimulation(control.ControlSystem(regras))

for teste in testes:
    simulacao.input['avaliacao_hotel'] = teste['avaliacao_hotel']
    simulacao.input['proximidade_atracoes'] = teste['proximidade_atracoes']
    simulacao.input['preco_noite'] = teste['preco_noite']
    simulacao.input['facilidades_hotel'] = teste['facilidades_hotel']

    simulacao.compute()

    satisfacao_hospede.view(simulacao)

    print(f"{teste}: {simulacao.output['satisfacao_hospede']}")

    pyplot.show()
