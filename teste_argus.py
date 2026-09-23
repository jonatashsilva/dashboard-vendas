from playwright.sync_api import sync_playwright
from datetime import date
import os


URL_ARGUS = "https://argos.dtel.com.br:8444/#home"

USUARIO = "jonatas.carmo"
SENHA = "#Satanoj12"

# Pasta onde o arquivo será salvo
PASTA_DESTINO = r"C:\Automacaorelatorios\VendasMes"


def calcular_periodo():
    hoje = date.today()

    # Se hoje for dia 01:
    # período = dia 02 do mês anterior até dia 01 deste mês
    if hoje.day == 1:

        # Mês anterior
        if hoje.month == 1:
            ano_inicio = hoje.year - 1
            mes_inicio = 12
        else:
            ano_inicio = hoje.year
            mes_inicio = hoje.month - 1

        data_inicial = date(
            ano_inicio,
            mes_inicio,
            2
        )

        data_final = date(
            hoje.year,
            hoje.month,
            1
        )

    # Se hoje for do dia 02 em diante:
    # período = dia 02 deste mês até dia 01 do próximo mês
    else:

        data_inicial = date(
            hoje.year,
            hoje.month,
            2
        )

        # Próximo mês
        if hoje.month == 12:
            ano_final = hoje.year + 1
            mes_final = 1
        else:
            ano_final = hoje.year
            mes_final = hoje.month + 1

        data_final = date(
            ano_final,
            mes_final,
            1
        )

    return data_inicial, data_final


with sync_playwright() as p:

    # =========================
    # ABRIR NAVEGADOR
    # =========================

    navegador = p.chromium.launch(
        headless=True
    )

    pagina = navegador.new_page()

    pagina.goto(
        URL_ARGUS,
        wait_until="domcontentloaded"
    )

    pagina.wait_for_timeout(3000)

    print("Página de login carregada.")

    # =========================
    # LOGIN
    # =========================

    pagina.locator(
        'input[type="text"]'
    ).first.fill(USUARIO)

    pagina.locator(
        'input[type="password"]'
    ).fill(SENHA)

    print("Usuário e senha preenchidos.")

    pagina.get_by_role(
        "button",
        name="Entrar"
    ).click()

    print("Botão Entrar clicado.")

    pagina.wait_for_timeout(5000)

    print("URL após login:", pagina.url)

    # =========================
    # MENU / RELATÓRIO
    # =========================

    pagina.get_by_role(
        "button",
        name=" Versão clássica"
    ).click()

    pagina.wait_for_timeout(2000)

    pagina.get_by_role(
        "button"
    ).first.click()

    pagina.locator(
        "span"
    ).filter(
        has_text="Atendimento"
    ).click()

    pagina.get_by_text(
        "Relatórios Analíticos"
    ).click()

    pagina.get_by_role(
        "link",
        name="Atendimento"
    ).click()

    print("Relatório de Atendimento aberto.")

    # =========================
    # FILTROS
    # =========================

    frame = pagina.locator(
        "iframe"
    ).nth(1).content_frame

    print("Abrindo filtros...")

    frame.get_by_role(
        "button",
        name=" Filtros"
    ).click()

    pagina.wait_for_timeout(1500)

    # =========================
    # CATEGORIA
    # =========================

    print("Selecionando categoria INSTALACAO...")

    campo_categoria = frame.get_by_placeholder(
        "Categoria",
        exact=True
    )

    campo_categoria.click()

    pagina.wait_for_timeout(500)

    campo_categoria.fill("")

    pagina.wait_for_timeout(300)

    campo_categoria.fill(
        "INSTALACAO"
    )

    pagina.wait_for_timeout(1500)

    campo_categoria.press(
        "Enter"
    )

    print(
        "Categoria INSTALACAO selecionada."
    )

    pagina.wait_for_timeout(1500)

    # =========================
    # DATAS
    # =========================

    data_inicial, data_final = calcular_periodo()

    data_inicial_str = data_inicial.strftime(
        "%Y-%m-%d"
    )

    data_final_str = data_final.strftime(
        "%Y-%m-%d"
    )

    print(
        f"Período selecionado: "
        f"{data_inicial.strftime('%d/%m/%Y')} "
        f"até "
        f"{data_final.strftime('%d/%m/%Y')}"
    )

    # =========================
    # DATA INICIAL
    # =========================

    print(
        "Preenchendo data inicial..."
    )

    campo_data_inicial = frame.get_by_role(
        "group",
        name="Finalização"
    ).get_by_placeholder(
        "Data inicial"
    )

    campo_data_inicial.fill(
        data_inicial_str
    )

    pagina.wait_for_timeout(1000)

    # =========================
    # DATA FINAL
    # =========================

    print(
        "Preenchendo data final..."
    )

    campo_data_final = frame.get_by_role(
        "group",
        name="Finalização"
    ).get_by_placeholder(
        "Data final"
    )

    campo_data_final.fill(
        data_final_str
    )

    pagina.wait_for_timeout(1500)

    # =========================
    # APLICAR FILTROS
    # =========================

    print(
        "Aplicando filtros..."
    )

    pagina.wait_for_timeout(1000)

    frame.get_by_role(
        "button",
        name="Aplicar Filtros"
    ).click()

    print(
        "Filtros aplicados!"
    )

    # =========================
    # AGUARDAR RELATÓRIO
    # =========================

    print(
        "Aguardando 60 segundos para "
        "o relatório carregar..."
    )

    pagina.wait_for_timeout(60000)

    print(
        "Relatório carregado."
    )

    # =========================
    # DOWNLOAD DO EXCEL
    # =========================

    print(
        "Preparando download do Excel..."
    )

    # Cria a pasta de destino
    os.makedirs(
        PASTA_DESTINO,
        exist_ok=True
    )

    arquivo_destino = os.path.join(
        PASTA_DESTINO,
        "vendas.xlsx"
    )

    # Se já existir um arquivo anterior,
    # remove para evitar conflito
    if os.path.exists(
        arquivo_destino
    ):
        os.remove(
            arquivo_destino
        )

        print(
            "Arquivo vendas.xlsx anterior "
            "removido."
        )

    print(
        "Clicando no botão Excel..."
    )

    # Aguarda o download começar
    with pagina.expect_download(
        timeout=30000
    ) as download_info:

        frame.get_by_role(
            "button",
            name=" Excel"
        ).click()

    download = download_info.value

    print(
        "Download iniciado."
    )

    # Salva diretamente na pasta definitiva
    download.save_as(
        arquivo_destino
    )

    print(
        "================================="
    )

    print(
        "DOWNLOAD CONCLUÍDO!"
    )

    print(
        f"Arquivo salvo em:"
    )

    print(
        arquivo_destino
    )

    print(
        "================================="
    )

    # =========================
    # MANTER NAVEGADOR ABERTO
    # =========================

    navegador.close()