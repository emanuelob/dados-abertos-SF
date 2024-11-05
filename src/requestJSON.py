import requests
from datetime import datetime

BASE_URL = "https://legis.senado.leg.br/dadosabertos"

#código do Senador Rodrigo Pacheco
SENADOR_CODIGO = 5732

DATA_INICIO = "20210202"  #02/02/2021
DATA_FIM = datetime.now().strftime("%Y%m%d")  #data atual

def obter_discursos():
    #endpoint completo com parâmetros na URL
    url = f"{BASE_URL}/senador/{SENADOR_CODIGO}/discursos?casa=SF&dataInicio={DATA_INICIO}&dataFim={DATA_FIM}"
    
    try:
        #requisição GET
        response = requests.get(url)
        
        #requisição foi bem-sucedida?
        response.raise_for_status()
        
        #o conteúdo retornado é JSON?
        if response.headers.get("Content-Type") == "application/json":
            return response.json()
        else:
            print("Resposta não é JSON:", response.text)
    
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP: {http_err}")
    except ValueError as json_err:
        print("Erro ao decodificar JSON:", json_err)
        print("Conteúdo da resposta:", response.text)
    except Exception as err:
        print(f"Erro: {err}")

if __name__ == "__main__":
    discursos = obter_discursos()
    if discursos:
        print(discursos)
