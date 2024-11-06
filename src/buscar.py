# TO DO: funcao que tem como argumentos o codigo do senador, a materia desejada na indexacao e as datas
# Importante: a pesquisa deve ser feita de mês a mês, porque a resposta da API tem um limite de discursos por requisição

from requestXML import obter_discursos
from add_to_database import adicionar_discursos

discursos = obter_discursos(SENADOR_CODIGO=5732, DATA_INICIO="20210202", DATA_FIM="20210228")
adicionar_discursos(discursos)
