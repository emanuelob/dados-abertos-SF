import sqlite3
"""Adiciona uma resposta da API (XML) ao banco de dados SQLite."""


def adicionar_discursos(data):
    # Conectar ao banco de dados
    conn = sqlite3.connect('data/discursos.db')
    cursor = conn.cursor()

    # Obter informações do senador
    parlamentar = data['DiscursosParlamentar']['Parlamentar'].get('IdentificacaoParlamentar', {})
    senador_dados = (
        int(parlamentar.get('CodigoParlamentar', 0)),
        parlamentar.get('NomeParlamentar', ''),
        parlamentar.get('NomeCompletoParlamentar', ''),
        parlamentar.get('SexoParlamentar', ''),
        parlamentar.get('SiglaPartidoParlamentar', ''),
        parlamentar.get('UfParlamentar', ''),
        parlamentar.get('FormaTratamento', ''),
        parlamentar.get('UrlFotoParlamentar', ''),
        parlamentar.get('UrlPaginaParlamentar', ''),
        parlamentar.get('EmailParlamentar', '')
    )

    # Inserir o senador na tabela Senadores (evitar duplicatas)
    cursor.execute('''
        INSERT OR IGNORE INTO Senadores 
        (codigo_parlamentar, nome_parlamentar, nome_completo, sexo, sigla_partido, uf, forma_tratamento, url_foto, url_pagina, email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', senador_dados)

    # Obter o ID do senador para associar aos discursos
    cursor.execute('SELECT id FROM Senadores WHERE codigo_parlamentar = ?',
                   (int(parlamentar.get('CodigoParlamentar', 0)),))
    senador_id = cursor.fetchone()[0]

    # Processar cada discurso
    for discurso in data['DiscursosParlamentar']['Parlamentar'].get('Pronunciamentos', {}).get('Pronunciamento', []):
        # Inserir a sessão, se ainda não existir
        sessao = discurso.get('SessaoPlenaria', {})
        sessao_dados = (
            int(sessao.get('CodigoSessao', 0)),
            sessao.get('SiglaCasaSessao', ''),
            sessao.get('NomeCasaSessao', ''),
            int(sessao.get('CodigoSessaoLegislativa', 0)),
            sessao.get('SiglaTipoSessao', ''),
            int(sessao.get('NumeroSessao', 0)),
            sessao.get('DataSessao', ''),
            sessao.get('HoraInicioSessao', '')
        )
        cursor.execute('''
            INSERT OR IGNORE INTO Sessoes 
            (codigo_sessao, sigla_casa, nome_casa, codigo_sessao_legislativa, sigla_tipo_sessao, numero_sessao, data_sessao, hora_inicio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sessao_dados)

        # Obter o ID da sessão
        cursor.execute('SELECT id FROM Sessoes WHERE codigo_sessao = ?', (int(sessao.get('CodigoSessao', 0)),))
        sessao_id = cursor.fetchone()[0]

        # Inserir o discurso
        discurso_dados = (
            int(discurso.get('CodigoPronunciamento', 0)),
            senador_id,
            discurso.get('TipoUsoPalavra', {}).get('Descricao', ''),
            discurso.get('DataPronunciamento', ''),
            discurso.get('SiglaPartidoParlamentarNaData', ''),
            discurso.get('UfParlamentarNaData', ''),
            discurso.get('SiglaCasaPronunciamento', ''),
            discurso.get('NomeCasaPronunciamento', ''),
            discurso.get('TextoResumo', ''),
            discurso.get('Indexacao', ''),
            discurso.get('UrlTexto', ''),
            discurso.get('UrlTextoBinario', ''),
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
                       (int(discurso.get('CodigoPronunciamento', 0)),))
        discurso_id = cursor.fetchone()[0]

        # Inserir a publicação relacionada ao discurso
        publicacao = discurso.get('Publicacoes', {}).get('Publicacao', {})
        publicacao_dados = (
            discurso_id,
            publicacao.get('DescricaoVeiculoPublicacao', ''),
            publicacao.get('DataPublicacao', ''),
            int(publicacao.get('NumeroPagInicioPublicacao', 0)),
            int(publicacao.get('NumeroPagFimPublicacao', 0)),
            publicacao.get('IndicadorRepublicacao', ''),
            publicacao.get('UrlDiario', '')
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
