# Lista da Visita

Este projeto Streamlit tem como objetivo auxiliar no controle e organização da lista de visitas. Ele permite pesquisar indivíduos por identificação ou nome, adicionar visitantes à lista de presença, especificar quantidades de itens (PETs, homens, mulheres, crianças) e gerenciar a lista, removendo ou limpando conforme necessário.

## Funcionalidades

- **Conexão com o Banco de Dados:**
    - Estabelece conexão com o banco de dados MongoDB para buscar informações dos indivíduos.
    - Prioriza a conexão com o banco de dados local (localhost) e, em caso de falha, tenta conectar-se ao banco de dados remoto (MongoDB Atlas).
    - Exibe mensagens de sucesso ou erro ao conectar-se ao banco de dados.

- **Interface Streamlit:**
    - Título principal "Lista da Visita".
    - Campo de texto para inserir o nome ou identificação do indivíduo a ser pesquisado.
    - Campos numéricos para especificar a quantidade de visitantes (PETs, homens, mulheres, crianças).
    - Botões para "Pesquisar", "Adicionar à Lista", "Limpar Lista" e "Remover Identificações".

- **Pesquisa de Indivíduos:**
    - Permite pesquisar indivíduos por identificação ou nome.
    - Utiliza expressões regulares para realizar a busca de forma flexível e case-insensitive.
    - Exibe os resultados da pesquisa, mostrando o nome e identificação do indivíduo.
    - Emite um aviso caso o indivíduo não seja encontrado.

- **Gerenciamento da Lista de Visitas:**
    - Permite adicionar indivíduos à lista de visitas, especificando a quantidade de visitantes (PETs, homens, mulheres, crianças).
    - Verifica se a identificação já está na lista antes de adicionar, evitando duplicidades.
    - Exibe uma mensagem de sucesso ao adicionar o indivíduo à lista.
    - Exibe a lista de indivíduos em um dataframe Streamlit.
    - Permite remover identificações específicas da lista através de um multiselect.
    - Permite limpar a lista completamente.

## Como Usar

1.  **Conecte-se ao Banco de Dados:**
      - Certifique-se de que o banco de dados MongoDB esteja em execução localmente (mongodb://localhost:27017/).
      - Caso a conexão local falhe, o script tentará se conectar ao banco de dados remoto (MongoDB Atlas).  As credenciais de acesso ao banco remoto estão comentadas no código, sendo necessário descomentar e configurar as variáveis `username` e `password` com as credenciais corretas.

2.  **Execute o Script Streamlit:**
    
      streamlit run main.py
    

3.  **Utilize a Interface:**
      - Insira o nome ou identificação do indivíduo no campo de texto.
      - Especifique a quantidade de visitantes (PETs, homens, mulheres, crianças).
      - Clique no botão "Pesquisar" para buscar o indivíduo.
      - Clique no botão "Adicionar à Lista" para adicionar o indivíduo à lista de visitas.
      - Utilize o multiselect e o botão "Remover Identificações" para remover indivíduos específicos da lista.
      - Clique no botão "Limpar Lista" para remover todos os indivíduos da lista.

## Requisitos

- Python 3.6+
- Streamlit
- pymongo
- pandas
- re
- unicodedata
- urllib.parse

## Instalação


pip install streamlit pymongo pandas

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests com melhorias e correções de bugs.

