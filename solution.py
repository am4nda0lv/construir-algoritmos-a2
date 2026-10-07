import datetime
import requests


def cotar():
    cotacoes = []
    hoje = datetime.date.today()
    url = (
        "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        "CotacaoDolarDia(dataCotacao=@dataCotacao)"
    )

    for dias_atras in range(365):
        data = (hoje - datetime.timedelta(days=dias_atras)).strftime("%m-%d-%Y")
        resposta = requests.get(
            url,
            params={"@dataCotacao": f"'{data}'", "$format": "json"},
            timeout=30,
        )
        resposta.raise_for_status()
        dados = resposta.json()["value"]
        if dados:
            cotacoes.append(dados[0]["cotacaoCompra"])
        else:
            cotacoes.append(None)

    if all(cotacao is None for cotacao in cotacoes):
        raise ValueError("A API não retornou cotações para o período consultado.")

    for i in range(len(cotacoes) - 2, -1, -1):
        if cotacoes[i] is None:
            cotacoes[i] = cotacoes[i + 1]

    for i in range(1, len(cotacoes)):
        if cotacoes[i] is None:
            cotacoes[i] = cotacoes[i - 1]

    return cotacoes
