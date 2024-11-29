import streamlit as st
import pandas as pd
import mysql.connector

st.set_page_config(page_title="Censo Escolar Rio Claro", initial_sidebar_state="collapsed", layout='centered')

with st.sidebar:
    st.image('novo_logo.png')
    st.page_link("app.py", label="Home")
    st.page_link("pages/dashboard.py", label="Dashboard")
    st.page_link("pages/crud_usuario.py", label="Cadastrar Usuário")
    if "login" in st.session_state:
        st.page_link("pages/bookmark.py", label="Gerenciar Bookmarks")
    else:
        st.page_link("pages/login.py", label="Login")

if "login" in st.session_state and "display_message" in st.session_state:
    if st.session_state.display_message:
        st.toast('Login bem sucedido!', icon='🎉')
        st.session_state.display_message = False

st.title("Censo Escolar Rio Claro")

st.image('children_studying.jpg')

st.markdown('''
### Bem-vindo ao Dashboard do Censo Escolar de Rio Claro

Este dashboard foi desenvolvido para apresentar, de forma clara e acessível, os principais dados do censo escolar do município de Rio Claro. Com ele, é possível explorar informações detalhadas sobre a educação local, incluindo números de matrículas, infraestrutura escolar, níveis de ensino atendidos e muito mais.

Nosso objetivo é fornecer uma ferramenta interativa e visual que facilite a análise e a tomada de decisões, promovendo um entendimento mais aprofundado do panorama educacional da cidade. Navegue pelos gráficos e tabelas para descobrir consegui insights e acompanhar de perto os indicadores que descrevem a educação em Rio Claro.

''')


if "login" in st.session_state:
    st.write(f"{st.session_state.login} está logado!")

st.markdown("# Mapa das Escolas")

conn = mysql.connector.connect(host=st.secrets.DB_HOST
                               , user=st.secrets.DB_USERNAME, password=st.secrets.DB_PASSWORD
                               , port=st.secrets.DB_PORT, db=st.secrets.DB_NAME
                               , auth_plugin='mysql_native_password')
cursor = conn.cursor()
cursor.execute(f'SELECT * FROM rc_geo;')
result = cursor.fetchall()

df_map = pd.DataFrame(result, columns=cursor.column_names)

st.map(data=df_map, zoom=12)

