import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

st.title("Lista de escola por quantidade de alunos")

st.markdown("- A lista é implementada por uma VIEW.")

with st.sidebar:
    st.page_link("app.py", label="App")
    st.page_link("pages/lista_de_escolas.py", label="Lista de Escolas")
    st.page_link("pages/alunos_escola.py", label="Métricas por Escolas")
    st.page_link("pages/ordenar_escolas_por_qt_alunos.py", label="Escolas por Quantidade de Alunos")
    st.page_link("pages/crud_usuario.py", label="Cadastrar Usuário")

conn = mysql.connector.connect(host=st.secrets.DB_HOST
                               , user=st.secrets.DB_USERNAME, password=st.secrets.DB_PASSWORD
                               , port=st.secrets.DB_PORT, db=st.secrets.DB_NAME
                               , auth_plugin='mysql_native_password')

cursor = conn.cursor()

cursor.execute("select * from listar_escolas_por_qt_alunos;")
res = cursor.fetchall()
df_lista_escolas = pd.DataFrame(res, columns=cursor.column_names)

st.write(df_lista_escolas)