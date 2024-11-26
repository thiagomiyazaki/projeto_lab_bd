import streamlit as st
import pandas as pd
import mysql.connector

with st.sidebar:
    st.image('group1.png')
    st.page_link("app.py", label="App")
    st.page_link("pages/lista_de_escolas.py", label="Lista de Escolas")
    st.page_link("pages/alunos_escola.py", label="Métricas por Escolas")
    st.page_link("pages/ordenar_escolas_por_qt_alunos.py", label="Escolas por Quantidade de Alunos")
    st.page_link("pages/crud_usuario.py", label="Cadastrar Usuário")
    st.page_link("pages/turma_por_escola.py", label="Turmas por escola")
    st.page_link("pages/login.py", label="Login")
    st.page_link("pages/mapa.py", label="Mapa")

st.header("Escolas no Mapa de Rio Claro")

conn = mysql.connector.connect(host=st.secrets.DB_HOST
                               , user=st.secrets.DB_USERNAME, password=st.secrets.DB_PASSWORD
                               , port=st.secrets.DB_PORT, db=st.secrets.DB_NAME
                               , auth_plugin='mysql_native_password')
cursor = conn.cursor()
cursor.execute(f'SELECT * FROM rc_geo;')
result = cursor.fetchall()

df_map = pd.DataFrame(result, columns=cursor.column_names)

st.map(data=df_map)