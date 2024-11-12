import requests
import xmltodict
from datetime import datetime
from typing import Dict, Any
import pandas as pd
import calendar
import json
import os

# Carregar senadores e legislaturas do arquivo CSV
senadores_df = pd.read_csv('data/senadores_legislaturas_56_57.csv')
BASE_URL = "https://legis.senado.leg.br/dadosabertos"
PROGRESS_FILE = 'progress.json'

# Lista para armazenar resultados inesperados
resultados_inesperados = []

# Lista para armazenar todos os discursos
todos_discursos = []

# Função para salvar o progresso em um arquivo JSON
def salvar_progresso(progresso: Dict[str, Any]) -> None:
    """Salva o progresso em um arquivo JSON.

    Args:
        progresso (Dict[str, Any]): Dicionário contendo o progresso atual.
    """
    with open(PROGRESS_FILE, 'w') as file:
        json.dump(progresso, file)
    print(f"Progresso salvo em {PROGRESS_FILE}.")

# Função para carregar o progresso de um arquivo JSON
def carregar_progresso() -> Dict[str, Any]:
    """Carrega o progresso de um arquivo JSON, se disponível.

    Returns:
        Dict[str, Any]: Dicionário contendo o progresso carregado.
    """
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as file:
            progresso = json.load(file)
        print(f"Progresso carregado de {PROGRESS_FILE}.")
        return progresso
    else:
        print("Nenhum progresso salvo encontrado.")
        return {'verificados': []}

# Função para atualizar o progresso
def atualizar_progresso(progresso: Dict[str, Any], senador_codigo: int, ano: int, trimestre: int, mes: int) -> None:
    """Atualiza o progresso atual.

    Args:
        progresso (Dict[str, Any]): Dicionário contendo o progresso atual.
        senador_codigo (int): Código do senador.
        ano (int): Ano atual.
        trimestre (int): Trimestre atual.
        mes (int): Mês atual.
    """
    verificado = {
        'senador_codigo': senador_codigo,
        'ano': ano,
        'trimestre': trimestre,
        'mes': mes
    }
    progresso['verificados'].append(verificado)
    salvar_progresso(progresso)

# Função para verificar se o progresso já contém o item
def progresso_contem(progresso: Dict[str, Any], senador_codigo: int, ano: int, trimestre: int, mes: int) -> bool:
    """Verifica se um item já foi verificado.

    Args:
        progresso (Dict[str, Any]): Dicionário contendo o progresso atual.
        senador_codigo (int): Código do senador.
        ano (int): Ano a ser verificado.
        trimestre (int): Trimestre a ser verificado.
        mes (int): Mês a ser verificado.

    Returns:
        bool: True se o item já foi verificado, False caso contrário.
    """
    for item in progresso['verificados']:
        if (item['senador_codigo'] == senador_codigo and item['ano'] == ano and
                item['trimestre'] == trimestre and item['mes'] == mes):
            return True
    return False

# Função para obter discursos de um ano
def obter_discursos_ano(senador_codigo: int, ano: int) -> bool:
    """Verifica se o senador fez algum discurso no ano especificado.

    Args:
        senador_codigo (int): Código do senador.
        ano (int): Ano a ser verificado.

    Returns:
        bool: True se houver discursos no ano, False caso contrário.
    """
    print(f"Verificando discursos do senador {senador_codigo} no ano {ano}...")
    url = f"{BASE_URL}/senador/{senador_codigo}/discursos?casa=SF&dataInicio={ano}0101&dataFim={ano}1231"
    try:
        response = requests.get(url)
        response.raise_for_status()
        discursos = xmltodict.parse(response.text)
        if discursos.get('DiscursosParlamentar') and discursos['DiscursosParlamentar'].get('Parlamentar') and discursos['DiscursosParlamentar']['Parlamentar'].get('Pronunciamentos') and discursos['DiscursosParlamentar']['Parlamentar']['Pronunciamentos'].get('Pronunciamento'):
            print(f"Discursos encontrados para o senador {senador_codigo} no ano {ano}.")
            return True
        else:
            print(f"Nenhum discurso encontrado para o senador {senador_codigo} no ano {ano}.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Erro ao verificar discursos do ano {ano} para senador {senador_codigo}: {e}")
        resultados_inesperados.append({'senador_codigo': senador_codigo, 'ano': ano, 'erro': str(e)})
        return False

# Função para obter discursos de um trimestre
def obter_discursos_trimestre(senador_codigo: int, ano: int, trimestre: int) -> bool:
    """Verifica se o senador fez algum discurso no trimestre especificado.

    Args:
        senador_codigo (int): Código do senador.
        ano (int): Ano a ser verificado.
        trimestre (int): Trimestre (1 a 4) a ser verificado.

    Returns:
        bool: True se houver discursos no trimestre, False caso contrário.
    """
    print(f"Verificando discursos do senador {senador_codigo} no ano {ano}, trimestre {trimestre}...")
    meses = {
        1: ('01', '03'),
        2: ('04', '06'),
        3: ('07', '09'),
        4: ('10', '12')
    }
    mes_inicio, mes_fim = meses[trimestre]
    url = f"{BASE_URL}/senador/{senador_codigo}/discursos?casa=SF&dataInicio={ano}{mes_inicio}01&dataFim={ano}{mes_fim}{calendar.monthrange(ano, int(mes_fim))[1]}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        discursos = xmltodict.parse(response.text)
        if discursos.get('DiscursosParlamentar') and discursos['DiscursosParlamentar'].get('Parlamentar') and discursos['DiscursosParlamentar']['Parlamentar'].get('Pronunciamentos') and discursos['DiscursosParlamentar']['Parlamentar']['Pronunciamentos'].get('Pronunciamento'):
            print(f"Discursos encontrados para o senador {senador_codigo} no trimestre {trimestre} do ano {ano}.")
            return True
        else:
            print(f"Nenhum discurso encontrado para o senador {senador_codigo} no trimestre {trimestre} do ano {ano}.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Erro ao verificar discursos do trimestre {trimestre} do ano {ano} para senador {senador_codigo}: {e}")
        resultados_inesperados.append({'senador_codigo': senador_codigo, 'ano': ano, 'trimestre': trimestre, 'erro': str(e)})
        return False

# Função para obter discursos de um mês
def obter_discursos_mes(senador_codigo: int, ano: int, mes: int) -> Dict[str, Any]:
    """Obtém os discursos de um senador em um determinado mês.

    Args:
        senador_codigo (int): Código do senador.
        ano (int): Ano a ser verificado.
        mes (int): Mês a ser verificado.

    Returns:
        Dict[str, Any]: Dados dos discursos no mês.
    """
    print(f"Verificando discursos do senador {senador_codigo} no ano {ano}, mês {mes}...")
    data_inicio = f"{ano}{mes:02d}01"
    data_fim = f"{ano}{mes:02d}{calendar.monthrange(ano, mes)[1]}"
    url = f"{BASE_URL}/senador/{senador_codigo}/discursos?casa=SF&dataInicio={data_inicio}&dataFim={data_fim}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        discursos = xmltodict.parse(response.text)
        if discursos.get('DiscursosParlamentar') and discursos['DiscursosParlamentar'].get('Parlamentar') and discursos['DiscursosParlamentar']['Parlamentar'].get('Pronunciamentos') and discursos['DiscursosParlamentar']['Parlamentar']['Pronunciamentos'].get('Pronunciamento'):
            print(f"Discursos encontrados para o senador {senador_codigo} no mês {mes} do ano {ano}.")
            return discursos
        else:
            print(f"Nenhum discurso encontrado para o senador {senador_codigo} no mês {mes} do ano {ano}.")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Erro ao obter discursos do mês {mes} do ano {ano} para senador {senador_codigo}: {e}")
        resultados_inesperados.append({'senador_codigo': senador_codigo, 'ano': ano, 'mes': mes, 'erro': str(e)})
        return {}

# Função para adicionar discursos à lista em memória
def adicionar_discursos_em_memoria(senador_codigo: int, data: Dict[str, Any]) -> None:
    """Adiciona os discursos de um senador à lista de todos os discursos.

    Args:
        senador_codigo (int): Código do senador.
        data (Dict[str, Any]): Dados dos discursos de um senador.
    """
    if data:
        pronunciamentos = data.get('DiscursosParlamentar', {}).get('Parlamentar', {}).get('Pronunciamentos', {}).get('Pronunciamento', [])
        if isinstance(pronunciamentos, list):
            for discurso in pronunciamentos:
                discurso['codigo_parlamentar'] = senador_codigo
                todos_discursos.append(discurso)
                print(f"Discurso adicionado: Código do Pronunciamento {discurso.get('CodigoPronunciamento', 'desconhecido')}.")
        else:
            pronunciamentos['codigo_parlamentar'] = senador_codigo
            todos_discursos.append(pronunciamentos)
            print(f"Discurso adicionado: Código do Pronunciamento {pronunciamentos.get('CodigoPronunciamento', 'desconhecido')}.")
    else:
        print("Nenhum discurso para adicionar à lista em memória.")

if __name__ == "__main__":
    progresso = carregar_progresso()

    for _, row in senadores_df.iterrows():
        senador_codigo = row['codigo_parlamentar']
        print(f"Iniciando verificação para o senador {senador_codigo}...")
        for ano in range(2019, 2025):  # Ajuste conforme as legislaturas
            print(f"Verificando ano {ano} para o senador {senador_codigo}...")
            if obter_discursos_ano(senador_codigo, ano):
                for trimestre in range(1, 5):
                    print(f"Verificando trimestre {trimestre} do ano {ano} para o senador {senador_codigo}...")
                    if obter_discursos_trimestre(senador_codigo, ano, trimestre):
                        for mes in range((trimestre - 1) * 3 + 1, trimestre * 3 + 1):
                            print(f"Verificando mês {mes} do ano {ano} para o senador {senador_codigo}...")
                            if progresso_contem(progresso, senador_codigo, ano, trimestre, mes):
                                print(f"Pulando mês {mes}, já processado anteriormente.")
                                continue
                            discursos = obter_discursos_mes(senador_codigo, ano, mes)
                            if discursos:
                                adicionar_discursos_em_memoria(senador_codigo, discursos)
                            atualizar_progresso(progresso, senador_codigo, ano, trimestre, mes)

    # Exibindo resultados inesperados
    if resultados_inesperados:
        print("\nResultados inesperados:")
        for resultado in resultados_inesperados:
            print(resultado)

    # Exibindo todos os discursos
    print("\nTodos os discursos:")
    for discurso in todos_discursos:
        print(discurso)

    print("Processamento concluído.")