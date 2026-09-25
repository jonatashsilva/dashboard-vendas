from flask import Flask, jsonify, send_from_directory, request

import pandas as pd
import os
import re


app = Flask(__name__)


# ========================================
# CONFIGURAÇÕES
# ========================================

ARQUIVO_EXCEL = r"C:\Automacaorelatorios\VendasMes\vendas.xlsx"


VENDEDORES = [

    "JONATAS HENRIQUE SILVA DO CARMO",

    "KEILA THAIS LIMA SANTOS",

    "LEILANY LAVINIA LOPES DA SILVA",

    "DENILSON SOARES DA SILVA"

]


# ========================================
# CACHE DO EXCEL
# ========================================

cache_dataframe = None
cache_modificacao = None


# ========================================
# NORMALIZAR TEXTO
# ========================================

def normalizar_texto(texto):

    if pd.isna(texto):
        return ""

    texto = str(texto)

    texto = texto.strip()

    texto = texto.upper()

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto


# ========================================
# VENDEDORES NORMALIZADOS
# ========================================

VENDEDORES_NORMALIZADOS = [

    normalizar_texto(nome)

    for nome in VENDEDORES

]


# ========================================
# CARREGAR EXCEL
# ========================================

def carregar_excel():

    global cache_dataframe
    global cache_modificacao


    # ========================================
    # VERIFICAR ARQUIVO
    # ========================================

    if not os.path.exists(ARQUIVO_EXCEL):

        raise FileNotFoundError(

            f"Arquivo não encontrado: {ARQUIVO_EXCEL}"

        )


    # ========================================
    # VERIFICAR ALTERAÇÃO DO ARQUIVO
    # ========================================

    modificacao_atual = os.path.getmtime(
        ARQUIVO_EXCEL
    )


    # ========================================
    # CARREGAR SOMENTE SE NECESSÁRIO
    # ========================================

    if (

        cache_dataframe is None

        or

        cache_modificacao != modificacao_atual

    ):

        print("\n========================================")
        print("CARREGANDO EXCEL")
        print("========================================")


        # ========================================
        # LER EXCEL
        # ========================================

        df = pd.read_excel(
            ARQUIVO_EXCEL
        )


        # ========================================
        # LIMPAR NOMES DAS COLUNAS
        # ========================================

        df.columns = (

            df.columns

            .astype(str)

            .str.strip()

        )


        print("COLUNAS ENCONTRADAS:")

        print(
            list(df.columns)
        )


        # ========================================
        # COLUNAS OBRIGATÓRIAS
        # ========================================

        colunas_obrigatorias = [

            "Vendedor",

            "Técnico",

            "Finalização Data",

            "Plano"

        ]


        for coluna in colunas_obrigatorias:

            if coluna not in df.columns:

                raise Exception(

                    f"A coluna '{coluna}' "
                    f"não foi encontrada no Excel."

                )


        # ========================================
        # NORMALIZAR VENDEDORES
        # ========================================

        df["Vendedor"] = (

            df["Vendedor"]

            .fillna("")

            .apply(
                normalizar_texto
            )

        )


        # ========================================
        # NORMALIZAR TÉCNICOS
        # ========================================

        df["Técnico"] = (

            df["Técnico"]

            .fillna("")

            .apply(
                normalizar_texto
            )

        )


        # ========================================
        # NORMALIZAR PLANOS
        # ========================================

        df["Plano"] = (

            df["Plano"]

            .fillna("")

            .apply(
                normalizar_texto
            )

        )


        # ========================================
        # CONVERTER DATA
        # ========================================

        df["Finalização Data"] = pd.to_datetime(

            df["Finalização Data"],

            errors="coerce",

            dayfirst=True

        )


        # ========================================
        # RETIRAR TÉCNICO COE
        # ========================================

        df = df[

            df["Técnico"] != "COE"

        ]


        # ========================================
        # SOMENTE VENDEDORES DESEJADOS
        # ========================================

        df = df[

            df["Vendedor"].isin(

                VENDEDORES_NORMALIZADOS

            )

        ]


        # ========================================
        # SALVAR NA MEMÓRIA
        # ========================================

        cache_dataframe = df

        cache_modificacao = modificacao_atual


        print()

        print(
            f"Excel carregado com sucesso."
        )

        print(
            f"Registros válidos: {len(df)}"
        )

        print(
            "Dados armazenados na memória."
        )

        print("========================================\n")


    else:

        print(
            "Usando dados do Excel armazenados na memória."
        )


    return cache_dataframe.copy()


# ========================================
# LER VENDAS
# ========================================

def ler_vendas(

    data_inicial=None,

    data_final=None

):


    # ========================================
    # PEGAR DADOS
    # ========================================

    df = carregar_excel()


    # ========================================
    # FILTRO DATA INICIAL
    # ========================================

    if data_inicial:

        try:

            inicio = pd.to_datetime(
                data_inicial
            )


            df = df[

                df["Finalização Data"]
                >= inicio

            ]


        except Exception:

            raise Exception(

                f"Data inicial inválida: "
                f"{data_inicial}"

            )


    # ========================================
    # FILTRO DATA FINAL
    # ========================================

    if data_final:

        try:

            fim = (

                pd.to_datetime(
                    data_final
                )

                +

                pd.Timedelta(
                    days=1
                )

            )


            df = df[

                df["Finalização Data"]
                < fim

            ]


        except Exception:

            raise Exception(

                f"Data final inválida: "
                f"{data_final}"

            )


    # ========================================
    # CONTAGEM POR VENDEDOR
    # ========================================

    contagem_vendedores = (

        df["Vendedor"]

        .value_counts()

        .to_dict()

    )


    # ========================================
    # MONTAR RANKING
    # ========================================

    vendedores = []


    for nome_original, nome_normalizado in zip(

        VENDEDORES,

        VENDEDORES_NORMALIZADOS

    ):

        quantidade = contagem_vendedores.get(

            nome_normalizado,

            0

        )


        vendedores.append({

            "nome":
                nome_original,

            "vendas":
                int(quantidade)

        })


    # ========================================
    # ORDENAR RANKING
    # ========================================

    vendedores.sort(

        key=lambda x: x["vendas"],

        reverse=True

    )


    # ========================================
    # TOTAL DE VENDAS
    # ========================================

    total_vendas = sum(

        vendedor["vendas"]

        for vendedor in vendedores

    )


    # ========================================
    # CONTAGEM DOS PLANOS
    # ========================================

    df_planos = df[

        df["Plano"] != ""

    ]


    contagem_planos = (

        df_planos["Plano"]

        .value_counts()

        .to_dict()

    )


    # ========================================
    # MONTAR LISTA DE PLANOS
    # ========================================

    planos = []


    for nome_plano, quantidade in contagem_planos.items():

        planos.append({

            "nome":
                nome_plano,

            "quantidade":
                int(quantidade)

        })


    # ========================================
    # ORDENAR PLANOS
    # ========================================

    planos.sort(

        key=lambda x: x["quantidade"],

        reverse=True

    )


    # ========================================
    # TERMINAL - RANKING
    # ========================================

    print("\n========================================")
    print("RESULTADO DO RANKING")
    print("========================================")


    for vendedor in vendedores:

        print(

            vendedor["nome"],

            "->",

            vendedor["vendas"],

            "vendas"

        )


    print(
        "TOTAL:",
        total_vendas
    )


    # ========================================
    # TERMINAL - PLANOS
    # ========================================

    print("\n========================================")
    print("PLANOS VENDIDOS")
    print("========================================")


    for plano in planos:

        print(

            plano["nome"],

            "->",

            plano["quantidade"]

        )


    print("========================================\n")


    # ========================================
    # RETORNO DA API
    # ========================================

    return {

        "vendedores":
            vendedores,

        "total_vendas":
            total_vendas,

        "quantidade_vendedores":
            len(vendedores),

        "planos":
            planos

    }


# ========================================
# PÁGINA PRINCIPAL
# ========================================

@app.route("/")
def pagina():

    return send_from_directory(

        ".",

        "index.html"

    )


# ========================================
# CSS
# ========================================

@app.route("/style.css")
def estilo():

    return send_from_directory(

        ".",

        "style.css"

    )


# ========================================
# JAVASCRIPT
# ========================================

@app.route("/script.js")
def javascript():

    return send_from_directory(

        ".",

        "script.js"

    )


# ========================================
# STATIC
# ========================================

@app.route("/static/<path:filename>")
def static_files(filename):

    return send_from_directory(

        "static",

        filename

    )


# ========================================
# API
# ========================================

@app.route("/api/vendas")
def vendas():

    data_inicial = request.args.get(

        "data_inicial",

        ""

    )


    data_final = request.args.get(

        "data_final",

        ""

    )


    try:

        dados = ler_vendas(

            data_inicial,

            data_final

        )


        return jsonify(
            dados
        )


    except Exception as erro:

        print(
            "ERRO:",
            erro
        )


        return jsonify({

            "erro":
                str(erro)

        }), 500


# ========================================
# SERVIDOR
# ========================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )