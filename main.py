import streamlit as st
from rich import print
import pymongo
from pymongo import MongoClient
import re
import pandas as pd

client = MongoClient('mongodb://localhost:27017/')
db = client.cpppac
sentenciados = db.sentenciados

st.title(' ')

barra = st.sidebar

# Remove 'Lista de Matrículas' da selectbox
escolha = barra.selectbox('O que voce quer pesquisar',['Preso'])

# Inicializa a lista de matrículas no session_state se não existir
if 'lista_matriculas' not in st.session_state:
    st.session_state.lista_matriculas = []

if escolha in ['Preso', 'Visita']:
    # Campo de pesquisa dinâmico baseado na escolha
    campo_pesquisa = ''
    if escolha == 'Preso':
        tipo_busca = st.radio('Pesquisar por:', ['Matrícula', 'Nome'])
        if tipo_busca == 'Matrícula':
            campo_pesquisa = st.text_input('Qual a matrícula a ser pesquisada')
        else:
            campo_pesquisa = st.text_input('Qual o nome a ser pesquisado')

    # Cria duas colunas para os botões
    col1, col2 = st.columns(2)

    # Botão Pesquisa na primeira coluna
    if col1.button('Pesquisa'):
        if campo_pesquisa:
            padrao = re.compile(f".*{campo_pesquisa}.*", re.IGNORECASE)
            campo_busca = 'matricula' if tipo_busca == 'Matrícula' else 'nome'
            resultados = sentenciados.find({campo_busca: {'$regex': padrao}})
            encontrou = False
            for sentenciado in resultados:
                st.write(f"Nome: {sentenciado['nome']}, Matrícula: {sentenciado['matricula']}, Pavilhão: {sentenciado['pavilhao']}")
                encontrou = True
            if not encontrou:
                st.warning(f'Nenhum sentenciado encontrado com este {tipo_busca.lower()}.')
        else:
            st.warning('Digite um valor para pesquisar')

    # Botão Adicionar à Lista
    if col2.button('Adicionar à Lista'):
        if campo_pesquisa and tipo_busca == 'Matrícula':
            if campo_pesquisa not in st.session_state.lista_matriculas:
                st.session_state.lista_matriculas.append(campo_pesquisa)
                st.success(f'Matrícula {campo_pesquisa} adicionada à lista!')
            else:
                st.info('Esta matrícula já está na lista!')
        elif tipo_busca != 'Matrícula':
            st.info('A função de lista só está disponível para pesquisa por matrícula')
        else:
            st.warning('Digite uma matrícula para adicionar à lista')

# Move a exibição da lista para fora do if/else
if st.session_state.lista_matriculas:
    st.markdown('---')  # Linha divisória
    st.subheader('Matrículas na Lista:')
    
    # Lista os dados
    for idx, matricula in enumerate(st.session_state.lista_matriculas, 1):
        sentenciado = sentenciados.find_one({'matricula': matricula})
        if sentenciado:
            # Cria um container para cada item da lista
            with st.container():
                st.markdown(f"""
                    **{idx}.** Matrícula: {matricula}  
                    Nome: {sentenciado['nome']}  
                    Pavilhão: {sentenciado['pavilhao']}
                """)
                st.markdown('---')  # Linha divisória entre itens
    