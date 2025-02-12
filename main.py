import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import re
import pandas as pd
import unicodedata
import urllib.parse

# Conexão com o banco de dados
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client.cpppac
    sentenciados = db.sentenciados
    st.toast('Conexão com o banco de dados local estabelecida!', icon ='👍')
except Exception as e:
    st.error(f"Erro ao conectar ao banco de dados: {e}", icon = '👎')
#finally:
#    username = urllib.parse.quote_plus('fernandopereira3')
#    password = urllib.parse.quote_plus('@Leon02023091')
#    url = f"mongodb+srv://{username}:{password}@pesquisavisita.2h6au.mongodb.net/?retryWrites=true&w=majority&appName=pesquisaVisita"    
#    try:
#        client = MongoClient(url, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
#        client.server_info()  # Force connection attempt
#        db = client.cpppac
#        sentenciados = db.sentenciados
#        st.toast('Conexão com o banco de dados remoto estabelecida!', icon ='👍')
#    except Exception as e:
#        st.error('Timeout na conexão com o banco de dados remoto. Tente novamente.', icon='👎')

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
    matricula_normalizada = re.compile(f".*{txt_d_pesquisa}.*", re.IGNORECASE)
    consulta_exata = {'matricula': matricula_normalizada}
#{ "<field>": { "$regex": "pattern", "$options": "<options>" } } REGEX DO MONGODB
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
    sentenciado = sentenciados.find_one({'matricula': {'$regex': matricula_normalizada}})
    pet = st.number_input('Quantidade de garrafas PET', min_value=0, max_value=10, value=0)
    homem = st.number_input('Quantidade de HOMENS', min_value=0, max_value=10, value=0)
    mulher = st.number_input('Quantidade de MULHERES', min_value=0, max_value=10, value=0)
    crianca = st.number_input('Quantidade de CRIANCAS', min_value=0, max_value=10, value=0)

    if sentenciado:
        if (homem > 0 or mulher > 0):
            if sentenciado['matricula'] not in [s['matricula'] for s in st.session_state['sentenciados_lista']]:
                st.session_state['sentenciados_lista'].append({
                    'matricula': sentenciado['matricula'],
                    'nome': sentenciado['nome'],
                    'PET': pet,
                    'HOMEM': homem,
                    'MULHER': mulher,
                    'CRIANCA': crianca,
                })
                st.success(f'Matrícula {sentenciado["matricula"]} adicionada à lista com sucesso!')
            else:
                st.info('Esta matrícula já está na lista!')
        else:
            st.warning('É necessário ter pelo menos um visitante (homem ou mulher) para adicionar à lista!')
    else:
        st.write(sentenciado)
        st.warning('Sentenciado não encontrado! ')
# Escolha do tipo de busca

tipo_busca = st.radio('Pesquisar por:', ['Matrícula', 'Nome'])

# Campo de entrada dinâmico baseado na escolha
txt_d_pesquisa = st.text_input('Digite a informação para pesquisa')

# Criando colunas para botões
col1, col2, col3, col4 = st.columns(4)

# Botão de Pesquisa
if col1.button('Pesquisar'):
    if txt_d_pesquisa:
        if tipo_busca == 'Matrícula':
            resultados = buscar_por_matricula(txt_d_pesquisa)
        else:
            resultados = buscar_por_nome(txt_d_pesquisa)

        if resultados:
            for sentenciados in resultados:
                st.write(f"**Nome:** {sentenciados['nome']} --- **Matr:** {sentenciados['matricula']} --- {sentenciados.get('pavilhao', 'N/A')}")
                st.markdown('---')
        else:
            st.warning('Debug')
            st.write(buscar_por_matricula(txt_d_pesquisa))
            st.write(f'MATRICULA NORMALIZADA {normalizar_matricula(txt_d_pesquisa)}')
            st.write(list(sentenciados.find({'matricula': {'$regex': txt_d_pesquisa}})))
            st.warning(f'O sentenciado com {txt_d_pesquisa} não foi encontrado.')
    else:
        st.warning('Digite nome ou matricula para pesquisar.')

# Botão Adicionar à Lista (apenas para matrícula)
if col2.button('Add matriculas'):
    if txt_d_pesquisa != False:
        adicionar_a_lista(txt_d_pesquisa)
    else:
        st.write(txt_d_pesquisa)
        st.warning('Somente matrículas podem ser adicionadas na lista !.')

if col4.button('Limpar Lista'):
    st.session_state['sentenciados_lista'] = []
    st.success('Lista de sentenciados foi limpa!')

# Exibição da lista de sentenciados
if st.session_state['sentenciados_lista']:
    #st.markdown('---')  # Linha divisória
    st.subheader('Matrículas na Lista:')
    
    # Exibe os dados como tabela
    df = pd.DataFrame(st.session_state['sentenciados_lista'])
    st.dataframe(df)

    # Multiselect para selecionar matrículas para remover
    matriculas_para_remover = st.multiselect(
        'Selecione as matrículas para remover:',
        [s['matricula'] for s in st.session_state['sentenciados_lista']]
    )

# Botão para remover as matrículas selecionadas
if col3.button('Remover Matrículas'):
    if matriculas_para_remover:
        st.session_state['sentenciados_lista'] = [
            s for s in st.session_state['sentenciados_lista']
                if s['matricula'] not in matriculas_para_remover
                ]
        st.success('Matrículas removidas com sucesso!')
    else:
        st.info('Nenhuma matrícula selecionada para remover.')
    
  