# Pesquisa de Sentenciados - CPPPAC

Este é um aplicativo Streamlit para pesquisar e gerenciar informações sobre sentenciados no Complexo Penitenciário Dr. Paulo César Pacca (CPPPAC). Ele permite pesquisar sentenciados por matrícula ou nome e adicionar matrículas a uma lista para referência.

## Funcionalidades

*   **Pesquisa por Matrícula:** Permite pesquisar sentenciados inserindo sua matrícula. A pesquisa normaliza a matrícula removendo pontos e traços para garantir a correspondência.
*   **Pesquisa por Nome:** Permite pesquisar sentenciados inserindo seu nome. A pesquisa normaliza o nome removendo acentos e convertendo para minúsculas para garantir a correspondência.
*   **Adicionar à Lista:** Permite adicionar matrículas à uma lista de referência. A lista é persistida usando o `session_state` do Streamlit.
*   **Visualização da Lista:** Exibe uma lista de matrículas adicionadas, juntamente com seus nomes e pavilhões correspondentes.
*   **Interface Streamlit:** Interface gráfica interativa construída com Streamlit.

## Como usar

1.  **Configuração do Ambiente:**
    *   Certifique-se de ter o Python instalado (versão 3.7 ou superior).
    *   Instale as dependências usando o pip:

    ```bash
    pip install streamlit pymongo pandas unicodedata
    ```

2.  **Configuração do Banco de Dados MongoDB:**
    *   Certifique-se de ter o MongoDB instalado e rodando na sua máquina.
    *   O aplicativo se conecta ao MongoDB na porta padrão (27017) no localhost. Se você estiver usando uma configuração diferente, ajuste a string de conexão no código.
    *   Crie um banco de dados chamado `cpppac` e uma collection chamada `sentenciados`.
    *   Insira os dados dos sentenciados na collection `sentenciados`. Cada documento deve ter os campos `matricula` e `nome`. O campo `pavilhao` é opcional.

3.  **Execução do Aplicativo:**
    *   Navegue até o diretório onde você salvou o arquivo `main.py`.
    *   Execute o aplicativo Streamlit usando o seguinte comando:

    ```bash
    streamlit run main.py
    ```

    *   O Streamlit abrirá o aplicativo em seu navegador web.

4.  **Usando o Aplicativo:**
    *   Na barra lateral, escolha o tipo de pesquisa (Matrícula ou Nome).
    *   Insira a informação para pesquisa no campo de texto.
    *   Clique no botão "Pesquisar" para exibir os resultados.
    *   Se você pesquisou por matrícula, pode clicar no botão "Adicionar à Lista" para adicionar a matrícula à lista de referência.
    *   A lista de matrículas adicionadas é exibida na parte inferior da página.

## Estrutura do Código

*   `main.py`: Contém o código principal do aplicativo Streamlit.
    *   Conecta-se ao banco de dados MongoDB.
    *   Define as funções para normalizar matrículas e nomes.
    *   Define as funções para pesquisar sentenciados por matrícula ou nome.
    *   Define a função para adicionar matrículas à lista.
    *   Cria a interface do usuário com Streamlit.

## Dependências

*   `streamlit`: Para criar a interface do usuário.
*   `pymongo`: Para conectar ao banco de dados MongoDB.
*   `pandas`: Para exibir a lista de matrículas como uma tabela.
*   `re`: Para usar expressões regulares para normalizar matrículas e nomes.
*   `unicodedata`: Para remover acentos dos nomes.

## Próximos Passos

*   Adicionar funcionalidade para remover matrículas da lista.
*   Implementar paginação para exibir grandes quantidades de resultados de pesquisa.
*   Adicionar mais campos de pesquisa (por exemplo, data de nascimento, crime).
*   Melhorar a interface do usuário.
*   Implementar autenticação e autorização.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests com melhorias e correções de bugs.
