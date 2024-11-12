import requests
import xmltodict
from datetime import datetime

BASE_URL = "https://legis.senado.leg.br/dadosabertos"

#código do Senador Rodrigo Pacheco
senador_codigo = 5732

data_inicio = "20210202"  #02/02/2021
data_fim = datetime.now().strftime("%Y%m%d")  #data atual

def obter_discursos(senador_codigo=senador_codigo, data_inicio=data_inicio, data_fim=data_fim):
    # endpoint da API
    url = f"{BASE_URL}/senador/{senador_codigo}/discursos?casa=SF&dataInicio={data_inicio}&dataFim={data_fim}"

    try:
        # requisição GET
        response = requests.get(url)

        # requisição foi bem-sucedida?
        response.raise_for_status()

        # processa a resposta como XML e converte para dicionário
        discursos = xmltodict.parse(response.text)

        # verifica se há discursos na resposta
        if len(discursos.get('DiscursosParlamentar', {}).get('Parlamentar', {}).get('Pronunciamentos', {}).get(
                'Pronunciamento', [])) > 0:
            return discursos
        else:
            return False

    except requests.exceptions.HTTPError as http_err:
        print(f"Erro na obtenção de discursos na API. Erro HTTP: {http_err}")
    except Exception as err:
        print(f"Erro na obtenção de discursos na API. Erro geral: {err}")

    return False

