import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

#st.write(st.session_state.teste)
#st.write(st.session_state.counter)

allow_download = 'None' if "login" not in st.session_state else 'true'

st.markdown(
    f"""
    <style>
    [data-testid="stElementToolbar"] {{
        display: {allow_download};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.page_link("app.py", label="App")
    st.page_link("pages/lista_de_escolas.py", label="Lista de Escolas")
    st.page_link("pages/alunos_escola.py", label="Métricas por Escolas")
    st.page_link("pages/ordenar_escolas_por_qt_alunos.py", label="Escolas por Quantidade de Alunos")
    st.page_link("pages/crud_usuario.py", label="Cadastrar Usuário")


st.title("Lista de Escolas")

conn = mysql.connector.connect(host=st.secrets.DB_HOST
                               , user=st.secrets.DB_USERNAME, password=st.secrets.DB_PASSWORD
                               , port=st.secrets.DB_PORT, db=st.secrets.DB_NAME
                               , auth_plugin='mysql_native_password')

cursor = conn.cursor()


# (nome, status de funcionamento, município, localização,
# dependência, níveis atendidos: EI, EF1, EF2, EM, EJA, EP, EE)
#cursor.execute("SELECT NO_ENTIDADE, TP_SITUACAO_FUNCIONAMENTO, CO_MUNICIPIO, TP_LOCALIZACAO, TP_DEPENDENCIA,  FROM escola;")
cursor.execute("SELECT NO_ENTIDADE, TP_SITUACAO_FUNCIONAMENTO, CO_MUNICIPIO, TP_LOCALIZACAO, TP_DEPENDENCIA FROM escola;")
res = cursor.fetchall()
df = pd.DataFrame(res, columns=["Nome da Escola", "Situação Funcionamento", "Codigo do Municipio", "Localização", "Dependência"])

selected_row = st.dataframe(df, use_container_width=True, on_select='rerun', selection_mode='single-row')

if selected_row:
    print(selected_row)