import sqlite3
"""Adiciona uma resposta da API (XML) ao banco de dados SQLite."""

def adicionar_discursos(data):
    """Adiciona ao banco de dados os discursos de um senador, modificando data/discursos.db.
    Args: data (dict): dados dos discursos de um senador obtidos por meio da API de dados abertos do Senado.
    Returns: None
    
    """
    # Conectar ao banco de dados
    conn = sqlite3.connect('../data/discursos.db')
    cursor = conn.cursor()

    # Obter informações do senador
    parlamentar = data['DiscursosParlamentar']['Parlamentar']['IdentificacaoParlamentar']
    senador_dados = (
        int(parlamentar['CodigoParlamentar']),
        parlamentar['NomeParlamentar'],
        parlamentar['NomeCompletoParlamentar'],
        parlamentar['SexoParlamentar'],
        parlamentar['SiglaPartidoParlamentar'],
        parlamentar['UfParlamentar'],
        parlamentar['FormaTratamento'],
        parlamentar['UrlFotoParlamentar'],
        parlamentar['UrlPaginaParlamentar'],
        parlamentar['EmailParlamentar']
    )

    # Inserir o senador na tabela Senadores (evitar duplicatas)
    cursor.execute('''
        INSERT OR IGNORE INTO Senadores 
        (codigo_parlamentar, nome_parlamentar, nome_completo, sexo, sigla_partido, uf, forma_tratamento, url_foto, url_pagina, email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', senador_dados)

    # Obter o ID do senador para associar aos discursos
    cursor.execute('SELECT id FROM Senadores WHERE codigo_parlamentar = ?', (int(parlamentar['CodigoParlamentar']),))
    senador_id = cursor.fetchone()[0]

    # Processar cada discurso
    for discurso in data['DiscursosParlamentar']['Parlamentar']['Pronunciamentos']['Pronunciamento']:
        # Inserir a sessão, se ainda não existir
        sessao = discurso['SessaoPlenaria']
        sessao_dados = (
            int(sessao['CodigoSessao']),
            sessao['SiglaCasaSessao'],
            sessao['NomeCasaSessao'],
            int(sessao['CodigoSessaoLegislativa']),
            sessao['SiglaTipoSessao'],
            int(sessao['NumeroSessao']),
            sessao['DataSessao'],
            sessao['HoraInicioSessao']
        )
        cursor.execute('''
            INSERT OR IGNORE INTO Sessoes 
            (codigo_sessao, sigla_casa, nome_casa, codigo_sessao_legislativa, sigla_tipo_sessao, numero_sessao, data_sessao, hora_inicio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sessao_dados)

        # Obter o ID da sessão
        cursor.execute('SELECT id FROM Sessoes WHERE codigo_sessao = ?', (int(sessao['CodigoSessao']),))
        sessao_id = cursor.fetchone()[0]

        # Inserir o discurso
        discurso_dados = (
            int(discurso['CodigoPronunciamento']),
            senador_id,
            discurso['TipoUsoPalavra']['Descricao'],
            discurso['DataPronunciamento'],
            discurso['SiglaPartidoParlamentarNaData'],
            discurso['UfParlamentarNaData'],
            discurso['SiglaCasaPronunciamento'],
            discurso['NomeCasaPronunciamento'],
            discurso['TextoResumo'],
            discurso['Indexacao'],
            discurso['UrlTexto'],
            discurso['UrlTextoBinario'],
            sessao_id
        )
        cursor.execute('''
            INSERT OR IGNORE INTO Discursos 
            (codigo_pronunciamento, senador_id, tipo_uso_palavra, data_pronunciamento, sigla_partido_na_data, uf_na_data, sigla_casa_pronunciamento,
             nome_casa_pronunciamento, texto_resumo, indexacao, url_texto, url_texto_binario, sessao_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', discurso_dados)

        # Obter o ID do discurso para associar às publicações
        cursor.execute('SELECT id FROM Discursos WHERE codigo_pronunciamento = ?',
                       (int(discurso['CodigoPronunciamento']),))
        discurso_id = cursor.fetchone()[0]

        # Inserir a publicação relacionada ao discurso
        publicacao = discurso['Publicacoes']['Publicacao']
        publicacao_dados = (
            discurso_id,
            publicacao['DescricaoVeiculoPublicacao'],
            publicacao['DataPublicacao'],
            int(publicacao['NumeroPagInicioPublicacao']),
            int(publicacao['NumeroPagFimPublicacao']),
            publicacao['IndicadorRepublicacao'],
            publicacao['UrlDiario']
        )
        cursor.execute('''
            INSERT OR IGNORE INTO Publicacoes 
            (discurso_id, descricao_veiculo, data_publicacao, numero_pag_inicio, numero_pag_fim, indicador_republicacao, url_diario)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', publicacao_dados)

    # Salvar as alterações e fechar a conexão
    conn.commit()
    conn.close()

    print("Dados inseridos com sucesso!")
