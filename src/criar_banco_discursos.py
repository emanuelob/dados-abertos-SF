import sqlite3

# Connect to the SQLite3 database (or create it if it doesn't exist)
conn = sqlite3.connect('data/discursos.db')
cursor = conn.cursor()

# Create the Senadores table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Senadores (
    codigo_parlamentar TEXT PRIMARY KEY,
    nome_parlamentar TEXT,
    nome_completo TEXT,
    sexo TEXT,
    sigla_partido TEXT,
    uf TEXT,
    forma_tratamento TEXT,
    url_foto TEXT,
    url_pagina TEXT,
    email TEXT
)
''')

# Create the Discursos table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Discursos (
    CodigoPronunciamento TEXT PRIMARY KEY,
    DataPronunciamento TEXT,
    Indexacao TEXT,
    NomeCasaPronunciamento TEXT,
    SessaoPlenaria_CodigoSessao TEXT,
    SessaoPlenaria_CodigoSessaoLegislativa TEXT,
    SessaoPlenaria_DataSessao TEXT,
    SessaoPlenaria_HoraInicioSessao TEXT,
    SessaoPlenaria_NomeCasaSessao TEXT,
    SessaoPlenaria_NumeroSessao TEXT,
    SessaoPlenaria_SiglaCasaSessao TEXT,
    SessaoPlenaria_SiglaTipoSessao TEXT,
    SiglaCasaPronunciamento TEXT,
    SiglaPartidoParlamentarNaData TEXT,
    TextoResumo TEXT,
    TipoUsoPalavra_Codigo TEXT,
    TipoUsoPalavra_Descricao TEXT,
    TipoUsoPalavra_IndicadorAtivo TEXT,
    TipoUsoPalavra_Sigla TEXT,
    UfParlamentarNaData TEXT,
    UrlTexto TEXT,
    UrlTextoBinario TEXT,
    codigo_parlamentar TEXT,
    FOREIGN KEY (codigo_parlamentar) REFERENCES Senadores (codigo_parlamentar)
)
''')

# Create the Aparteantes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Aparteantes (
    CodigoPronunciamento TEXT,
    CodigoParlamentar TEXT,
    NomeAparteante TEXT,
    FOREIGN KEY (CodigoPronunciamento) REFERENCES Discursos (CodigoPronunciamento),
    FOREIGN KEY (CodigoParlamentar) REFERENCES Senadores (codigo_parlamentar)
)
''')

# Create the Publicacoes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Publicacoes (
    CodigoPronunciamento TEXT,
    DataPublicacao TEXT,
    DescricaoVeiculoPublicacao TEXT,
    IndicadorRepublicacao TEXT,
    NumeroPagFimPublicacao TEXT,
    NumeroPagInicioPublicacao TEXT,
    UrlDiario TEXT,
    FOREIGN KEY (CodigoPronunciamento) REFERENCES Discursos (CodigoPronunciamento)
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")