import requests
import xmltodict
from datetime import datetime

BASE_URL = "https://legis.senado.leg.br/dadosabertos"

#código do Senador Rodrigo Pacheco
#SENADOR_CODIGO = 5732

#DATA_INICIO = "20210202"  #02/02/2021
#DATA_FIM = datetime.now().strftime("%Y%m%d")  #data atual

def obter_discursos(SENADOR_CODIGO, DATA_INICIO, DATA_FIM):
    #endpoint da API
    url = f"{BASE_URL}/senador/{SENADOR_CODIGO}/discursos?casa=SF&dataInicio={DATA_INICIO}&dataFim={DATA_FIM}"
    
    try:
        #requisição GET
        response = requests.get(url)
        
        #requisição foi bem-sucedida?
        print(response.raise_for_status())
        
        #processa a resposta como XML e converte para dicionário
        data = xmltodict.parse(response.text)
        return data
    
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP: {http_err}")
    except Exception as err:
        print(f"Erro: {err}")

#callback
if __name__ == "__main__":
    discursos = obter_discursos()
    if discursos:
        print(discursos)
