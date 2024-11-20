import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

def get_plot_data(cod_escola, df_turma, df_docente, df_matricula):
    print((df_matricula['CO_ENTIDADE'] == cod_escola).sum())
    print((df_turma['CO_ENTIDADE'] == cod_escola).sum())
    print((df_docente['CO_ENTIDADE'] == cod_escola).sum())
    plot_df = pd.DataFrame({
        'Alunos': [(df_matricula['CO_ENTIDADE'] == cod_escola).sum()],
        'Turmas': [(df_turma['CO_ENTIDADE'] == cod_escola).sum()],
        'Docentes': [(df_docente['CO_ENTIDADE'] == cod_escola).sum()]
    })

    return plot_df

with st.sidebar:
    st.page_link("app.py", label="App")
    st.page_link("pages/lista_de_escolas.py", label="Lista de Escolas")
    st.page_link("pages/alunos_escola.py", label="Métricas por Escolas")
    st.page_link("pages/ordenar_escolas_por_qt_alunos.py", label="Escolas por Quantidade de Alunos")
    st.page_link("pages/crud_usuario.py", label="Cadastrar Usuário")

st.title("Total de alunos, professores e turmas por escola")

conn = mysql.connector.connect(host=st.secrets.DB_HOST
                               , user=st.secrets.DB_USERNAME, password=st.secrets.DB_PASSWORD
                               , port=st.secrets.DB_PORT, db=st.secrets.DB_NAME
                               , auth_plugin='mysql_native_password')

cursor = conn.cursor()

cursor.execute("select * from escola;")
res = cursor.fetchall()
df_escola = pd.DataFrame(res, columns=cursor.column_names)

cursor.execute("select * from turma;")
res = cursor.fetchall()
df_turma = pd.DataFrame(res, columns=cursor.column_names)

cursor.execute("select * from docente;")
res = cursor.fetchall()
df_docente = pd.DataFrame(res, columns=cursor.column_names)

cursor.execute("select * from matricula;")
res = cursor.fetchall()
df_matricula = pd.DataFrame(res, columns=cursor.column_names)

nome_escola = st.selectbox("Nome da Escola", df_escola['NO_ENTIDADE'].unique())

cursor.execute(f'SELECT CO_ENTIDADE FROM escola WHERE NO_ENTIDADE = "{nome_escola}";')
cod_entidade = cursor.fetchall()[0][0]

plot_df = get_plot_data(cod_entidade, df_turma, df_docente, df_matricula)

print(plot_df)

st.bar_chart(plot_df, y_label="Quantidade", x_label="", stack=False)

df_query = pd.DataFrame()
