import sqlite3
import json

# Load data from the JSON file
with open('data/discursos_em_memoria.json', 'r') as file:
    discursos_data = json.load(file)

# Connect to the SQLite3 database
conn = sqlite3.connect('data/discursos.db')
cursor = conn.cursor()

# Insert data into the Discursos table
for discurso in discursos_data:
    cursor.execute('''
    INSERT OR IGNORE INTO Discursos (
        CodigoPronunciamento, DataPronunciamento, Indexacao, NomeCasaPronunciamento, SessaoPlenaria_CodigoSessao,
        SessaoPlenaria_CodigoSessaoLegislativa, SessaoPlenaria_DataSessao, SessaoPlenaria_HoraInicioSessao,
        SessaoPlenaria_NomeCasaSessao, SessaoPlenaria_NumeroSessao, SessaoPlenaria_SiglaCasaSessao,
        SessaoPlenaria_SiglaTipoSessao, SiglaCasaPronunciamento, SiglaPartidoParlamentarNaData, TextoResumo,
        TipoUsoPalavra_Codigo, TipoUsoPalavra_Descricao, TipoUsoPalavra_IndicadorAtivo, TipoUsoPalavra_Sigla,
        UfParlamentarNaData, UrlTexto, UrlTextoBinario, codigo_parlamentar
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        discurso.get('CodigoPronunciamento'), discurso.get('DataPronunciamento'), discurso.get('Indexacao'),
        discurso.get('NomeCasaPronunciamento'), discurso.get('SessaoPlenaria_CodigoSessao'),
        discurso.get('SessaoPlenaria_CodigoSessaoLegislativa'), discurso.get('SessaoPlenaria_DataSessao'),
        discurso.get('SessaoPlenaria_HoraInicioSessao'), discurso.get('SessaoPlenaria_NomeCasaSessao'),
        discurso.get('SessaoPlenaria_NumeroSessao'), discurso.get('SessaoPlenaria_SiglaCasaSessao'),
        discurso.get('SessaoPlenaria_SiglaTipoSessao'), discurso.get('SiglaCasaPronunciamento'),
        discurso.get('SiglaPartidoParlamentarNaData'), discurso.get('TextoResumo'), discurso.get('TipoUsoPalavra_Codigo'),
        discurso.get('TipoUsoPalavra_Descricao'), discurso.get('TipoUsoPalavra_IndicadorAtivo'),
        discurso.get('TipoUsoPalavra_Sigla'), discurso.get('UfParlamentarNaData'), discurso.get('UrlTexto'),
        discurso.get('UrlTextoBinario'), discurso.get('codigo_parlamentar')
    ))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database populated successfully.")