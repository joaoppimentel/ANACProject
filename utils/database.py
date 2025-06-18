import sqlite3
from unidecode import unidecode
import pandas as pd
import streamlit as st

def rename_columns(col, parentheses=True):
    nome = col.lower()
    if parentheses:
        nome = nome.split('(')[-1].strip(')').strip()
    nome = nome.replace('(', '').replace(')', '')
    nome = unidecode(nome)
    return nome.replace(' ', '_')

def execute_query(query, params=None, fetch=False, return_columns=False, df=False, db_path='anac.db'):
    """
    Executa uma query no banco SQLite.

    Args:
        query (str): Comando SQL a ser executado.
        params (tuple, optional): Parâmetros para query parametrizada. Default é None.
        fetch (bool, optional): Se True, retorna os resultados da query (ex: SELECT). Default é False.
        return_columns (bool, optional): Se True, retorna os resultados com o nome das colunas. Default é False.
        df (bool, optional): Se True, retorna os resultados como dataframe. Default é False.
        db_path (str, optional): Caminho para o arquivo do banco SQLite. Default é 'anac.csv'

    Returns:
        list: Resultados da query, se fetch=True. Caso contrário, None.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if fetch or return_columns or df:
                data = cursor.fetchall()
                if return_columns or df:
                    columns = [desc[0] for desc in cursor.description]
                    result = [dict(zip(columns, row)) for row in data]
                    if df:
                        result = pd.DataFrame(result)
                    return result
                else:
                    return data
            else:
                conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao executar a query: {e}")
        return None
    
def get_all(table, fields=["*"], filters=[], df=True):
    fields = ", ".join(fields)
    query = f"SELECT {fields} FROM {table}"
    if filters:
        query += " WHERE "+ format_filters(filters)
    df = execute_query(query, df=df)
    return df

def get_count(table, filters=[], group_by=""):
    query = f"SELECT "
    if group_by:
        query += f"{group_by}, "
    query += f"COUNT(*) FROM {table}"
    if filters:
        query += " WHERE "+ format_filters(filters)
    if group_by:
        query += f" GROUP BY {group_by}"
        return execute_query(query, df=True)
    return execute_query(query, fetch=True)[0][0]

def get_sum(table, fields, filters=[]):
    query_fields = " + ".join(fields)
    query = f"SELECT SUM({query_fields}) FROM {table}"
    if filters:
        query += " WHERE "+ format_filters(filters)
    return execute_query(query, fetch=True)[0][0]
    
def get_mean(table, field, filters=[]):
    query = f"SELECT AVG({field}) FROM {table}"
    if filters:
        query += " WHERE "+ format_filters(filters)
    return execute_query(query, fetch=True)[0][0]

def get_unique(table, field, filters=[]):
    query = f"SELECT DISTINCT {field} FROM {table}"
    if filters:
        query += " WHERE "+ format_filters(filters)
    query += f" ORDER BY {field} ASC"
    result = execute_query(query, fetch=True)
    result = [item[0] for item in result]
    return result

def create_tables():
    execute_query('''
    CREATE TABLE IF NOT EXISTS empresas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sigla TEXT,
        nome TEXT,
        nacionalidade TEXT
    )''')

    execute_query('''
    CREATE TABLE IF NOT EXISTS aeroportos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sigla TEXT,
        nome TEXT,
        uf TEXT,
        regiao TEXT,
        pais TEXT,
        continente TEXT
    )''')

    execute_query('''
        CREATE TABLE IF NOT EXISTS voos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empresa_id INTEGER,
        ano INTEGER,
        mes INTEGER,
        aeroporto_origem_id INTEGER,
        aeroporto_destino_id INTEGER,
        natureza TEXT,
        grupo_voo TEXT,
        passageiros_pagos INTEGER,
        passageiros_gratis INTEGER,
        carga_paga_kg INTEGER,
        carga_gratis_kg INTEGER,
        correio_kg INTEGER,
        ask INTEGER,
        rpk INTEGER,
        atk INTEGER,
        rtk INTEGER,
        combustivel_litros INTEGER,
        distancia_voada_km INTEGER,
        decolagens INTEGER,
        carga_paga_km INTEGER,
        carga_gratis_km INTEGER,
        correio_km INTEGER,
        assentos INTEGER,
        payload INTEGER,
        horas_voadas INTEGER,
        bagagem_kg INTEGER,
        FOREIGN KEY (empresa_id) REFERENCES empresas(id),
        FOREIGN KEY (aeroporto_origem_id) REFERENCES aeroportos(id),
        FOREIGN KEY (aeroporto_destino_id) REFERENCES aeroportos(id)
    )''')

def escape_value(val):
    if pd.isna(val):
        return 'NULL'
    val_str = str(val).replace("'", "''")
    return f"'{val_str}'"

def fill_empresas(df):
    empresas = df[['EMPRESA (SIGLA)', 'EMPRESA (NOME)', 'EMPRESA (NACIONALIDADE)']].drop_duplicates()
    empresas.columns = [rename_columns(col) for col in empresas.columns]
    
    empresas_dict = empresas.to_dict('index')
    values = []
    for item in empresas_dict.values():
        values.append(f"""(
            {escape_value(item['sigla'])},
            {escape_value(item['nome'])},
            {escape_value(item['nacionalidade'])}
        )""")
    
    query = (f"""
    INSERT INTO empresas (
        sigla, 
        nome, 
        nacionalidade
    ) VALUES
    {" ,".join(values)};
    """)

    execute_query(query)

def fill_aeroportos(df):
    aeroportos_origem = df[['AEROPORTO DE ORIGEM (SIGLA)', 'AEROPORTO DE ORIGEM (NOME)', 'AEROPORTO DE ORIGEM (UF)',
                        'AEROPORTO DE ORIGEM (REGIÃO)', 'AEROPORTO DE ORIGEM (PAÍS)', 'AEROPORTO DE ORIGEM (CONTINENTE)']
                        ]
    aeroportos_destino = df[['AEROPORTO DE DESTINO (SIGLA)', 'AEROPORTO DE DESTINO (NOME)', 'AEROPORTO DE DESTINO (UF)',
                            'AEROPORTO DE DESTINO (REGIÃO)', 'AEROPORTO DE DESTINO (PAÍS)', 'AEROPORTO DE DESTINO (CONTINENTE)']
                            ]
    
    aeroportos_origem.columns = [rename_columns(col) for col in aeroportos_origem.columns]
    aeroportos_destino.columns = [rename_columns(col) for col in aeroportos_destino.columns]

    aeroportos = pd.concat([aeroportos_origem, aeroportos_destino]).drop_duplicates(ignore_index=True)
    
    aeroportos_dict = aeroportos.to_dict('index')
    values = []
    for item in aeroportos_dict.values():
        values.append(f"""(
            {escape_value(item['sigla'])},
            {escape_value(item['nome'])},
            {escape_value(item['uf'])},
            {escape_value(item['regiao'])},
            {escape_value(item['pais'])},
            {escape_value(item['continente'])}
            )"""
        )

    query = f"""
    INSERT INTO aeroportos (
        sigla,
        nome,
        uf,
        regiao,
        pais,
        continente
    ) VALUES 
    {" ,".join(values)};
    """
    execute_query(query)

def fill_voos(df):
    empresas = execute_query("SELECT id, sigla FROM empresas", return_columns=True)
    empresas = {row['sigla']:row['id'] for row in empresas}
    aeroportos = execute_query("SELECT id, sigla FROM aeroportos", return_columns=True)
    aeroportos = {row['sigla']:row['id'] for row in aeroportos}

    voos = df[["EMPRESA (SIGLA)","ANO", "MÊS", "AEROPORTO DE ORIGEM (SIGLA)", "AEROPORTO DE DESTINO (SIGLA)", "NATUREZA", "GRUPO DE VOO", "PASSAGEIROS PAGOS", "PASSAGEIROS GRÁTIS",
       "CARGA PAGA (KG)", "CARGA GRÁTIS (KG)", "CORREIO (KG)", "ASK", "RPK",
       "ATK", "RTK", "COMBUSTÍVEL (LITROS)", "DISTÂNCIA VOADA (KM)",
       "DECOLAGENS", "CARGA PAGA KM", "CARGA GRATIS KM", "CORREIO KM",
       "ASSENTOS", "PAYLOAD", "HORAS VOADAS", "BAGAGEM (KG)"]] 

    voos.columns = [rename_columns(col, parentheses=False) for col in voos.columns]
    voos['horas_voadas'] = voos['horas_voadas'].str.replace(',','.').astype(float)
    voos_dict = voos.to_dict('index')
    
    values = []
    for item in voos_dict.values():
        empresa_id = empresas[item['empresa_sigla']]
        aeroporto_origem_id = aeroportos[item['aeroporto_de_origem_sigla']]
        aeroporto_destino_id = aeroportos[item['aeroporto_de_destino_sigla']]

        values.append(f"""(
            {escape_value(empresa_id)},
            {escape_value(item['ano'])},
            {escape_value(item['mes'])},
            {escape_value(aeroporto_origem_id)},
            {escape_value(aeroporto_destino_id)},
            {escape_value(item['natureza'])},
            {escape_value(item['grupo_de_voo'])},
            {escape_value(item['passageiros_pagos'])},
            {escape_value(item['passageiros_gratis'])},
            {escape_value(item['carga_paga_kg'])},
            {escape_value(item['carga_gratis_kg'])},
            {escape_value(item['correio_kg'])},
            {escape_value(item['ask'])},
            {escape_value(item['rpk'])},
            {escape_value(item['atk'])},
            {escape_value(item['rtk'])},
            {escape_value(item['combustivel_litros'])},
            {escape_value(item['distancia_voada_km'])},
            {escape_value(item['decolagens'])},
            {escape_value(item['carga_paga_km'])},
            {escape_value(item['carga_gratis_km'])},
            {escape_value(item['correio_km'])},
            {escape_value(item['assentos'])},
            {escape_value(item['payload'])},
            {escape_value(item['horas_voadas'])},
            {escape_value(item['bagagem_kg'])}
        )""")

    query = f"""
    INSERT INTO voos (
        empresa_id,
        ano,
        mes,
        aeroporto_origem_id,
        aeroporto_destino_id,
        natureza,
        grupo_voo,
        passageiros_pagos,
        passageiros_gratis,
        carga_paga_kg,
        carga_gratis_kg,
        correio_kg,
        ask,
        rpk,
        atk,
        rtk,
        combustivel_litros,
        distancia_voada_km,
        decolagens,
        carga_paga_km,
        carga_gratis_km,
        correio_km,
        assentos,
        payload,
        horas_voadas,
        bagagem_kg
        ) VALUES 
        {" ,".join(values)};
    """
    execute_query(query)

def fill_tables(df):
    if get_count("empresas") == 0:
        fill_empresas(df)
    if get_count("aeroportos") == 0:
        fill_aeroportos(df)
    if get_count("voos") == 0:
        fill_voos(df)

def check_view(view):
    return execute_query(f"SELECT name FROM sqlite_master WHERE type='view' AND name='{view}';", fetch=True)

def create_views():
    if not check_view("RelatorioVoosDetalhado"):
        execute_query('''CREATE VIEW RelatorioVoosDetalhado AS
                         SELECT
                            v.id,
                            e.sigla AS sigla_empresa,
                            e.nome AS nome_empresa,
                            e.nacionalidade AS nacionalidade_empresa,
                            v.ano,
                            v.mes,
                            ao.sigla AS sigla_aeroporto_origem,
                            ao.nome AS nome_aeroporto_origem,
                            ao.uf AS uf_aeroporto_origem,
                            ao.regiao AS regiao_aeroporto_origem,
                            ao.pais AS pais_aeroporto_origem,
                            ao.continente AS continente_aeroporto_origem,
                            ad.sigla AS sigla_aeroporto_destino,
                            ad.nome AS nome_aeroporto_destino,
                            ad.uf AS uf_aeroporto_destino,
                            ad.regiao AS regiao_aeroporto_destino,
                            ad.pais AS pais_aeroporto_destino,
                            ad.continente AS continente_aeroporto_destino,
                            v.natureza,
                            v.grupo_voo,
                            v.passageiros_pagos,
                            v.passageiros_gratis,
                            v.carga_paga_kg,
                            v.carga_gratis_kg,
                            v.correio_kg,
                            v.ask,
                            v.rpk,
                            v.atk,
                            v.rtk,
                            v.combustivel_litros,
                            v.distancia_voada_km,
                            v.decolagens,
                            v.carga_paga_km,
                            v.carga_gratis_km,
                            v.correio_km,
                            v.assentos,
                            v.payload,
                            v.horas_voadas,
                            v.bagagem_kg
                        FROM
                            voos AS v
                        INNER JOIN
                            empresas AS e ON v.empresa_id = e.id
                        INNER JOIN
                            aeroportos AS ao ON v.aeroporto_origem_id = ao.id
                        INNER JOIN
                            aeroportos AS ad ON v.aeroporto_destino_id = ad.id;''')

    if not check_view('RotasVoo'):
        execute_query('''CREATE VIEW RotasVoo AS
                         SELECT
                            mes,
                            sigla_aeroporto_origem AS sigla_origem,
                            nome_aeroporto_origem AS nome_origem,
                            continente_aeroporto_origem AS continente_origem,
                            pais_aeroporto_origem AS pais_origem,
                            sigla_aeroporto_destino AS sigla_destino,
                            nome_aeroporto_destino AS nome_destino,
                            continente_aeroporto_destino AS continente_destino,
                            pais_aeroporto_destino AS pais_destino
                        FROM
                            RelatorioVoosDetalhado;''')
        
    if not check_view('VariacaoMensal'):
        execute_query('''CREATE VIEW VariacaoMensal AS
                         SELECT
                            mes,
                            SUM(passageiros_pagos + passageiros_gratis) AS Passageiros,
                            SUM(decolagens) AS Decolagens,
                            SUM(combustivel_litros) AS Combustivel,
                            SUM(carga_paga_kg + carga_gratis_kg) AS 'Carga'
                        FROM
                            voos
                        GROUP BY
                            mes;''')

def format_filters(filters, suffix=""):
    formated = []
    if isinstance(filters, dict):
        for c, v in filters.items():
            formated.append((f"{c+suffix} = '{v}'"))
    else:
        formated = filters
    return " AND ".join(formated)
