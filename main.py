import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import re
import pandas as pd
import unicodedata
import urllib.parse

# Conexão com o banco de dados
username = urllib.parse.quote_plus('fernandopereira3')
password = urllib.parse.quote_plus('@Leon02023091')
url = f"mongodb+srv://{username}:{password}@pesquisavisita.2h6au.mongodb.net/?retryWrites=true&w=majority&appName=pesquisaVisita"


client = MongoClient(url, server_api=ServerApi('1'))
db = client.cpppac
sentenciados = db.sentenciados


st.title('Lista para o dia de Visita')

# Inicializa a lista no session_state, se ainda não existir
if 'sentenciados_lista' not in st.session_state:
    st.session_state['sentenciados_lista'] = []

# Função para normalizar matrícula (remover pontos e traços)
def normalizar_matricula(matricula):
    return re.sub(r'[\.\-]', '', matricula).strip()  # Remove pontos, traços e espaços extras

# Função para normalizar textos (remover acentos e caracteres especiais)
def normalizar_texto(texto):
    if not texto:
        return ""
    texto = texto.lower().strip()  # Converte para minúsculas e remove espaços extras
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')  # Remove acentos
    return texto

# Função para buscar sentenciado por matrícula
def buscar_por_matricula(matricula):
    matricula_normalizada = re.compile(f".*{campo_pesquisa}.*", re.IGNORECASE)
    consulta_exata = {'matricula': matricula_normalizada}

    resultado = list(sentenciados.find(consulta_exata))
    if not resultado:
        resultado = list(sentenciados.find({'matricula': {'$regex': matricula_normalizada}}))
    return resultado

# Função para buscar sentenciado por nome
def buscar_por_nome(nome):
    nome_normalizado = normalizar_texto(nome)
    padrao_nome = re.compile(f".*{nome_normalizado}.*", re.IGNORECASE)
    return list(sentenciados.find({'nome': {'$regex': padrao_nome}}))

# Função para adicionar sentenciado à lista
def adicionar_a_lista(matricula):
    matricula_normalizada = re.compile(f".*{matricula}.*", re.IGNORECASE)
    # Busca exata no banco para melhor performance
    sentenciado = sentenciados.find_one({'matricula': {'$regex': matricula_normalizada}})

    if sentenciado:
        if sentenciado['matricula'] not in [s['matricula'] for s in st.session_state['sentenciados_lista']]:
            st.session_state['sentenciados_lista'].append({
                'matricula': sentenciado['matricula'],
                'nome': sentenciado['nome'],
                'pavilhao': sentenciado.get('pavilhao', 'N/A')
            })
            st.success(f'Matrícula {sentenciado["matricula"]} adicionada à lista com sucesso!')
        else:
            st.info('Esta matrícula já está na lista!')
    else:
        st.write(sentenciado)
        st.warning('Sentenciado não encontrado! ')
        
# Escolha do tipo de busca
tipo_busca = st.radio('Pesquisar por:', ['Matrícula', 'Nome'])

# Campo de entrada dinâmico baseado na escolha
campo_pesquisa = st.text_input('Digite a informação para pesquisa')

# Criando colunas para botões
col1, col2 = st.columns(2)

# Botão de Pesquisa
if col1.button('Pesquisar'):
    if campo_pesquisa:
        if tipo_busca == 'Matrícula':
            resultados = buscar_por_matricula(campo_pesquisa)
        else:
            resultados = buscar_por_nome(campo_pesquisa)

        if resultados:
            for sentenciado in resultados:
                st.write(f"**Nome:** {sentenciado['nome']}")
                st.write(f"**Matrícula:** {sentenciado['matricula']}")
                st.write(f"**Pavilhão:** {sentenciado.get('pavilhao', 'N/A')}")
                st.markdown("---")  # Linha divisória
        else:
            st.warning('Nenhum sentenciado encontrado.')
    else:
        st.warning('Digite um valor para pesquisar.')

# Botão Adicionar à Lista (apenas para matrícula)
if col2.button('Adicionar matriculas'):
    if campo_pesquisa != False:
        adicionar_a_lista(campo_pesquisa)
    else:
        st.write(campo_pesquisa)
        st.warning('Somente matrículas podem ser adicionadas na lista !.')

# Exibição da lista de sentenciados
if st.session_state['sentenciados_lista']:
    st.markdown('---')  # Linha divisória
    st.subheader('Matrículas na Lista:')
    
    # Exibe os dados como tabela
    df = pd.DataFrame(st.session_state['sentenciados_lista'])
    st.dataframe(df)
