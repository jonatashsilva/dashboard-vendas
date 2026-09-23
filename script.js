// ========================================
// CARREGAR VENDAS
// ========================================

async function carregarVendas() {

    try {

        // ========================================
        // DATAS
        // ========================================

        const dataInicial =
            document.getElementById(
                'data-inicial'
            ).value;


        const dataFinal =
            document.getElementById(
                'data-final'
            ).value;


        // ========================================
        // CONSULTAR API
        // ========================================

        const resposta = await fetch(

            `/api/vendas?data_inicial=${dataInicial}&data_final=${dataFinal}`

        );


        if (!resposta.ok) {

            throw new Error(
                'Erro ao consultar a API'
            );

        }


        const dados =
            await resposta.json();


        console.log(
            "Dados recebidos:",
            dados
        );


        if (dados.erro) {

            throw new Error(
                dados.erro
            );

        }


        // ========================================
        // TOTAL DE VENDAS
        // ========================================

        document
            .getElementById(
                'total-vendas'
            )
            .textContent =
            dados.total_vendas;


        // ========================================
        // RANKING
        // ========================================

        const lista =
            document.getElementById(
                'lista-vendedores'
            );


        lista.innerHTML = '';


        if (

            dados.vendedores &&

            dados.vendedores.length > 0

        ) {


            // ========================================
            // MAIOR VENDA
            // ========================================

            const maiorVenda = Math.max(

                ...dados.vendedores.map(

                    vendedor =>
                        vendedor.vendas

                )

            );


            // ========================================
            // CRIAR VENDEDORES
            // ========================================

            dados.vendedores.forEach(

                (vendedor, index) => {


                    const percentual =

                        maiorVenda > 0

                            ? (

                                vendedor.vendas /
                                maiorVenda

                            ) * 100

                            : 0;


                    // LINHA

                    const linha =
                        document.createElement(
                            'div'
                        );


                    linha.className =
                        'vendedor';


                    // POSIÇÃO

                    const posicao =
                        document.createElement(
                            'div'
                        );


                    posicao.className =
                        'posicao';


                    posicao.textContent =
                        index + 1;


                    // DADOS

                    const dadosVendedor =
                        document.createElement(
                            'div'
                        );


                    dadosVendedor.className =
                        'dados-vendedor';


                    // NOME

                    const nome =
                        document.createElement(
                            'div'
                        );


                    nome.className =
                        'nome-vendedor';


                    nome.textContent =
                        vendedor.nome;


                    // FUNDO BARRA

                    const barraContainer =
                        document.createElement(
                            'div'
                        );


                    barraContainer.className =
                        'barra-container';


                    // BARRA

                    const barra =
                        document.createElement(
                            'div'
                        );


                    barra.className =
                        'barra-venda';


                    barra.style.width =
                        percentual + '%';


                    barraContainer.appendChild(
                        barra
                    );


                    dadosVendedor.appendChild(
                        nome
                    );


                    dadosVendedor.appendChild(
                        barraContainer
                    );


                    // QUANTIDADE

                    const quantidade =
                        document.createElement(
                            'div'
                        );


                    quantidade.className =
                        'valor-venda';


                    quantidade.textContent =

                        vendedor.vendas +

                        (

                            vendedor.vendas === 1

                                ? ' venda'

                                : ' vendas'

                        );


                    linha.appendChild(
                        posicao
                    );


                    linha.appendChild(
                        dadosVendedor
                    );


                    linha.appendChild(
                        quantidade
                    );


                    lista.appendChild(
                        linha
                    );

                }

            );

        }


        // ========================================
        // PLANOS VENDIDOS
        // ========================================

        const listaPlanos =
            document.getElementById(
                'lista-planos'
            );


        listaPlanos.innerHTML = '';


        if (

            dados.planos &&

            dados.planos.length > 0

        ) {


            // ========================================
            // MAIOR QUANTIDADE
            // ========================================

            const maiorPlano = Math.max(

                ...dados.planos.map(

                    plano =>
                        plano.quantidade

                )

            );


            // ========================================
            // CRIAR PLANOS
            // ========================================

            dados.planos.forEach(

                plano => {


                    const percentual =

                        maiorPlano > 0

                            ? (

                                plano.quantidade /
                                maiorPlano

                            ) * 100

                            : 0;


                    const item =
                        document.createElement(
                            'div'
                        );


                    item.className =
                        'plano-item';


                    // ========================================
                    // INFORMAÇÕES
                    // ========================================

                    const info =
                        document.createElement(
                            'div'
                        );


                    info.className =
                        'plano-info';


                    // NOME DO PLANO

                    const nome =
                        document.createElement(
                            'span'
                        );


                    nome.className =
                        'plano-nome';


                    nome.textContent =
                        plano.nome;


                    // QUANTIDADE

                    const quantidade =
                        document.createElement(
                            'strong'
                        );


                    quantidade.className =
                        'plano-quantidade';


                    quantidade.textContent =

                        plano.quantidade +

                        (

                            plano.quantidade === 1

                                ? ' venda'

                                : ' vendas'

                        );


                    info.appendChild(
                        nome
                    );


                    info.appendChild(
                        quantidade
                    );


                    // ========================================
                    // BARRA DO PLANO
                    // ========================================

                    const barraFundo =
                        document.createElement(
                            'div'
                        );


                    barraFundo.className =
                        'plano-barra-fundo';


                    const barra =
                        document.createElement(
                            'div'
                        );


                    barra.className =
                        'plano-barra';


                    barra.style.width =
                        percentual + '%';


                    barraFundo.appendChild(
                        barra
                    );


                    // ========================================
                    // MONTAR ITEM
                    // ========================================

                    item.appendChild(
                        info
                    );


                    item.appendChild(
                        barraFundo
                    );


                    listaPlanos.appendChild(
                        item
                    );

                }

            );


        } else {


            listaPlanos.innerHTML = `

                <div class="sem-dados">

                    Nenhum plano encontrado.

                </div>

            `;

        }


    }


    // ========================================
    // ERRO
    // ========================================

    catch (erro) {

        console.error(

            'Erro ao carregar vendas:',

            erro

        );


        document
            .getElementById(
                'lista-vendedores'
            )
            .innerHTML = `

                <div class="erro">

                    Erro ao carregar o ranking.

                </div>

            `;

    }

}


// ========================================
// LIMPAR FILTROS
// ========================================

function limparFiltros() {

    document
        .getElementById(
            'data-inicial'
        )
        .value = '';


    document
        .getElementById(
            'data-final'
        )
        .value = '';


    carregarVendas();

}


// ========================================
// CARREGAMENTO INICIAL
// ========================================

carregarVendas();


// ========================================
// ATUALIZAÇÃO AUTOMÁTICA
// ========================================

setInterval(

    carregarVendas,

    30000

);