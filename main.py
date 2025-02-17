import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import re
import pandas as pd
import unicodedata
import urllib.parse
# Conexão com o banco de dados remoto
import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import re
import pandas as pd
import unicodedata
import urllib.parse

def conectar_banco_de_dados():
    """
    Tenta conectar ao banco de dados remoto e, se falhar, tenta o banco de dados local.
    Retorna o banco de dados e um booleano indicando se a conexão foi bem-sucedida.
    """
    conexao_remota = False
    db = None
    try:
        username = urllib.parse.quote_plus('fernandopereira3')
        password = urllib.parse.quote_plus('@Leon02023091')
        url = f"mongodb+srv://{username}:{password}@pesquisavisita.2h6au.mongodb.net/?retryWrites=true&w=majority&appName=pesquisaVisita"
        client = MongoClient(url, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
        client.server_info()  # Force connection attempt
        db = client.cpppac
        sentenciados = db.sentenciados
        st.toast('Conexão com o banco de dados remoto estabelecida!', icon='👍')
        conexao_remota = True
        return db, conexao_remota
    except Exception as e:
        st.toast('Timeout na conexão com o banco de dados remoto. Tentando conexão local...', icon='👎')
        conexao_remota = False

    # Tenta a conexão local se a remota falhar
    if not conexao_remota:
        try:
            client = MongoClient('mongodb://localhost:27017/')
            db = client.cpppac
            sentenciados = db.sentenciados
            st.toast('Conexão com o banco de dados local estabelecida!', icon='👍')
            return db, True  # Retorna True para indicar sucesso na conexão local
        except Exception as e:
            st.error(f"Erro ao conectar ao banco de dados local: {e}", icon='👎')
            return None, False  # Retorna False para indicar falha na conexão

try:
    db, conexao_status = conectar_banco_de_dados()
    if db:
        sentenciados = db.sentenciados
    else:
        st.error("Não foi possível conectar ao banco de dados.", icon='👎')
except Exception as e:
    st.error(f"Erro ao conectar ao banco de dados: {e}", icon='👎')

st.title('Lista da Visita')

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
def adicionar_a_lista(matricula, pet, homem, mulher, crianca):
    matricula_normalizada = re.compile(f".*{matricula}.*", re.IGNORECASE)
    sentenciado = sentenciados.find_one({'matricula': {'$regex': matricula_normalizada}})
    
    if not sentenciado:
        st.warning('Sentenciado não encontrado!')
        return
 
    # Verifica se a matrícula já está na lista antes de adicionar
    if any(s['matricula'] == sentenciado['matricula'] for s in st.session_state['sentenciados_lista']):
        st.info('Esta matrícula já está na lista!')
        return
    
    st.session_state['sentenciados_lista'].append({
        'matricula': sentenciado['matricula'],
        'nome': sentenciado['nome'],
        'PET': pet,
        'HOMEM': homem,
        'MULHER': mulher,
        'CRIANCA': crianca,
    })
    
    if st.session_state['sentenciados_lista']:
        st.toast(f'Matrícula {sentenciado["matricula"]} adicionada à lista com sucesso!')
        df = pd.DataFrame(st.session_state['sentenciados_lista'])
        st.dataframe(df)


coluna = st.columns(1)
txt_d_pesquisa = coluna[0].text_input('Digite a quem esta procurando')

col1, col2 = st.columns(2)

pet = col1.number_input('Quantidade de GARRAFAS PETS', min_value=0, max_value=10, value=0)
homem = col1.number_input('Quantidade de HOMENS', min_value=0, max_value=10, value=0)
mulher = col2.number_input('Quantidade de MULHERES', min_value=0, max_value=10, value=0)
crianca = col2.number_input('Quantidade de CRIANCAS', min_value=0, max_value=10, value=0)

# Criando colunas para botões
col1, col2, col3, col4 = st.columns(4)

# Botão de Pesquisa
if col1.button('Pesquisar'):
    if txt_d_pesquisa:
        resultados = buscar_por_matricula(txt_d_pesquisa)
        if not resultados:
            resultados = buscar_por_nome(txt_d_pesquisa)
        if resultados:
            for sentenciado in resultados:
                st.write(f"**Nome:** {sentenciado['nome']} --- **Matr:** {sentenciado['matricula']} --- {sentenciado.get('pavilhao', 'N/A')}")
                st.markdown('---')
        else:
            st.json(buscar_por_matricula(resultados))
            st.write(buscar_por_matricula(resultados))
            st.warning(f'O sentenciado com {txt_d_pesquisa} não foi encontrado.')
    else:
        st.warning('Digite nome ou matricula para pesquisar.')

# Botão Adicionar à Lista (apenas para matrícula)
if col2.button('ADICIONAR'):
    if normalizar_matricula(txt_d_pesquisa):
        adicionar_a_lista(txt_d_pesquisa, pet, homem, mulher, crianca)
    else:
        st.warning('Somente matrículas podem ser adicionadas na lista !.')

# Botão Limpar Lista
if col4.button('Limpar Lista'):
    st.session_state['sentenciados_lista'] = []
    st.success('Lista de sentenciados foi limpa!')
    
# Botão para remover as matrículas
if col3.button('Remover Matrículas'):
 # Multiselect para selecionar matrículas para remover
    matriculas_para_remover = st.multiselect(
        'Selecione as matrículas para remover:',
        [s['matricula'] for s in st.session_state['sentenciados_lista']]
    )
    if matriculas_para_remover:
        st.session_state['sentenciados_lista'] = [
            s for s in st.session_state['sentenciados_lista']
                if s['matricula'] not in matriculas_para_remover
                ]
        st.success('Matrículas removidas com sucesso!')
    else:
        st.info('Nenhuma matrícula selecionada para remover.')
    
  