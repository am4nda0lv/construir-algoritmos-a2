import datetime
import requests

def cotar():
cotacoes = []
hoje = datetime.date.today()

```
for i in range(365):
    data = (hoje - datetime.timedelta(days=i)).strftime("%m-%d-%Y")

    url = (
        "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
        "CotacaoDolarDia(dataCotacao=@dataCotacao)"
    )

    resposta = requests.get(
        url,
        params={
            "@dataCotacao": f"'{data}'",
            "$format": "json"
        }
    )

    dados = resposta.json()["value"]

    if dados:
        cotacoes.append(dados[0]["cotacaoCompra"])
    else:
        cotacoes.append(None)

return cotacoes
```
