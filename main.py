import streamlit as st
from rich import print
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://10.14.180.204:27017/')
db = client.cpppac
sentenciados = db.sentenciados

st.title('Pesquisa')

barra = st.sidebar

escolha = barra.selectbox('O que voce quer pesquisar',['Preso','Visita'])
matr = st.text_input('Qual a matricula a ser pesquisada')


if st.button('Pesquisa'):
    for matr in sentenciados.find({'matricula': matr}):
      st.write('Nome: ', matr['nome'],',', matr['pavilhao'])
