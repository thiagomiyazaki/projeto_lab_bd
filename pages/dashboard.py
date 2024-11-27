import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

colunas_disciplinas = [
    'IN_DISC_QUIMICA',
    'IN_DISC_FISICA',
    'IN_DISC_MATEMATICA',
    'IN_DISC_BIOLOGIA',
    'IN_DISC_CIENCIAS',
    'IN_DISC_LINGUA_PORTUGUESA',
    'IN_DISC_LINGUA_INGLES',
    'IN_DISC_LINGUA_ESPANHOL',
    'IN_DISC_LINGUA_FRANCES',
    'IN_DISC_LINGUA_OUTRA',
    'IN_DISC_LINGUA_INDIGENA',
    'IN_DISC_ARTES',
    'IN_DISC_EDUCACAO_FISICA',
    'IN_DISC_HISTORIA',
    'IN_DISC_GEOGRAFIA',
    'IN_DISC_FILOSOFIA',
    'IN_DISC_ENSINO_RELIGIOSO',
    'IN_DISC_ESTUDOS_SOCIAIS',
    'IN_DISC_SOCIOLOGIA',
    'IN_DISC_EST_SOCIAIS_SOCIOLOGIA',
    'IN_DISC_INFORMATICA_COMPUTACAO',
    'IN_DISC_PROFISSIONALIZANTE',
    'IN_DISC_ATENDIMENTO_ESPECIAIS',
    'IN_DISC_DIVER_SOCIO_CULTURAL',
    'IN_DISC_LIBRAS',
    'IN_DISC_PEDAGOGICAS',
    'IN_DISC_OUTRAS'
]

mapa_disciplinas = {
    'IN_DISC_QUIMICA': 'Química',
    'IN_DISC_FISICA': 'Física',
    'IN_DISC_MATEMATICA': 'Matemática',
    'IN_DISC_BIOLOGIA': 'Biologia',
    'IN_DISC_CIENCIAS': 'Ciências',
    'IN_DISC_LINGUA_PORTUGUESA': 'Língua Portuguesa',
    'IN_DISC_LINGUA_INGLES': 'Língua Inglesa',
    'IN_DISC_LINGUA_ESPANHOL': 'Língua Espanhola',
    'IN_DISC_LINGUA_FRANCES': 'Língua Francesa',
    'IN_DISC_LINGUA_OUTRA': 'Outra Língua Estrangeira',
    'IN_DISC_LINGUA_INDIGENA': 'Língua Indígena',
    'IN_DISC_ARTES': 'Artes',
    'IN_DISC_EDUCACAO_FISICA': 'Educação Física',
    'IN_DISC_HISTORIA': 'História',
    'IN_DISC_GEOGRAFIA': 'Geografia',
    'IN_DISC_FILOSOFIA': 'Filosofia',
    'IN_DISC_ENSINO_RELIGIOSO': 'Ensino Religioso',
    'IN_DISC_ESTUDOS_SOCIAIS': 'Estudos Sociais',
    'IN_DISC_SOCIOLOGIA': 'Sociologia',
    'IN_DISC_EST_SOCIAIS_SOCIOLOGIA': 'Estudos Sociais/Sociologia',
    'IN_DISC_INFORMATICA_COMPUTACAO': 'Informática/Computação',
    'IN_DISC_PROFISSIONALIZANTE': 'Profissionalizante',
    'IN_DISC_ATENDIMENTO_ESPECIAIS': 'Atendimento a Necessidades Especiais',
    'IN_DISC_DIVER_SOCIO_CULTURAL': 'Diversidade Sociocultural',
    'IN_DISC_LIBRAS': 'Libras',
    'IN_DISC_PEDAGOGICAS': 'Pedagógicas',
    'IN_DISC_OUTRAS': 'Outra Disciplina'
}


def gerar_disciplinas(row):
    disciplinas = [mapa_disciplinas[col] for col in colunas_disciplinas if row[col] == 1]
    return ', '.join(disciplinas)

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

st.set_page_config(page_title="Censo Escolar Rio Claro", initial_sidebar_state="collapsed", layout='wide')

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
    st.image('novo_logo.png')
    st.page_link("app.py", label="Home")
    st.page_link("pages/dashboard.py", label="Dashboard")
    # st.page_link("pages/lista_de_escolas.py", label="Lista de Escolas")
    # st.page_link("pages/alunos_escola.py", label="Métricas por Escolas")
    # st.page_link("pages/ordenar_escolas_por_qt_alunos.py", label="Escolas por Quantidade de Alunos")
    st.page_link("pages/crud_usuario.py", label="Cadastrar Usuário")
    # st.page_link("pages/turma_por_escola.py", label="Turmas por escola")
    st.page_link("pages/login.py", label="Login")
    # st.page_link("pages/mapa.py", label="Mapa")

st.image("criancas_dashboard.png")

st.title("Dashboard de Escolas de Rio Claro")

st.markdown('## Lista de Escolas')

st.markdown('Escolha uma escola para receber mais informações.\n')

conn = mysql.connector.connect(host=st.secrets.DB_HOST
                               , user=st.secrets.DB_USERNAME, password=st.secrets.DB_PASSWORD
                               , port=st.secrets.DB_PORT, db=st.secrets.DB_NAME
                               , auth_plugin='mysql_native_password')

cursor = conn.cursor()
cursor.execute("SELECT CO_ENTIDADE, NO_ENTIDADE, TP_SITUACAO_FUNCIONAMENTO, CO_MUNICIPIO, TP_LOCALIZACAO, TP_DEPENDENCIA FROM escola;")
res = cursor.fetchall()
df = pd.DataFrame(res, columns=cursor.column_names)

print(df)

cursor.execute("select * from listar_escolas_por_qt_alunos;")
res = cursor.fetchall()
df_lista_escolas = pd.DataFrame(res, columns=cursor.column_names)

result = df.merge(df_lista_escolas[['CO_ENTIDADE', 'contagem_estudantes']], on='CO_ENTIDADE', how='left')

map_funcionamento = {
    1: "Em Atividade",
    2: "Paralisada",
    3: "Extinta (Ano Censo)",
    4: "Extinta (Ano Anterior)"
}

map_municipio = {
    3543907: "Rio Claro"
}

result['funcionamento'] = result['TP_SITUACAO_FUNCIONAMENTO'].map(map_funcionamento)
result['municipio'] = result['CO_MUNICIPIO'].map(map_municipio)

print(result)

result = result[['CO_ENTIDADE', 'NO_ENTIDADE', 'funcionamento', 'TP_SITUACAO_FUNCIONAMENTO', 'CO_MUNICIPIO', 'municipio', 'TP_LOCALIZACAO', 'TP_DEPENDENCIA', 'contagem_estudantes']]

selected_row = st.dataframe(result,
                            use_container_width=True,
                            on_select='rerun',
                            selection_mode='single-row',
                            column_config={
                                "_index": None,
                                "CO_ENTIDADE": None,
                                "NO_ENTIDADE": "Nome",
                                "TP_SITUACAO_FUNCIONAMENTO": None,
                                "funcionamento": "Funcionamento",
                                "municipio": "Município",
                                "CO_MUNICIPIO": None,
                                "TP_LOCALIZACAO": "Localização",
                                "TP_DEPENDENCIA": "Dependência",
                                "contagem_estudantes": "Contagem Estudantes",
                                }
                            )

if selected_row['selection']['rows']:
    st.text("")
    st.text("")
    st.markdown(f"## Quantidade de Alunos, Docentes e Turmas por Escola")
    st.markdown(f"####  *:grey[{result.loc[selected_row['selection']['rows'][0], 'NO_ENTIDADE']}]*")

    print(f'{selected_row}')

    print(f"{selected_row['selection']['rows'][0]=}")
    value = result.loc[selected_row['selection']['rows'][0], 'CO_ENTIDADE']
    print(f'{value=}')

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

    plot_df = get_plot_data(value, df_turma, df_docente, df_matricula)

    # Transpose and reset index
    df_transposed = plot_df.T.reset_index()

    # Rename columns for better readability
    df_transposed.columns = ['Categoria', 'Quantidade']

    print(plot_df)
    print(df_transposed)

    st.bar_chart(df_transposed, y_label="Quantidade", x="Categoria", x_label=None, stack=False, width=600,
                 use_container_width=False, color="Categoria")

    # --------------- CODIGO RYAN ---------------- #

    # ------- NIVEIS ENSINO ----------

    st.markdown(f"## Quantidade de alunos por nível escolar")
    st.text("")

    cursor.execute("""
        SELECT 
            COUNT(CASE WHEN TP_ETAPA_ENSINO <= 3 THEN 1 END) AS EI,
            COUNT(CASE WHEN (TP_ETAPA_ENSINO BETWEEN 4 AND 8) OR (TP_ETAPA_ENSINO BETWEEN 14 AND 18) THEN 1 END) AS EF_1,
            COUNT(CASE WHEN (TP_ETAPA_ENSINO BETWEEN 9 AND 13) OR (TP_ETAPA_ENSINO BETWEEN 19 AND 21) OR (TP_ETAPA_ENSINO = 41) THEN 1 END) AS EF_2, 
            COUNT(CASE WHEN (TP_ETAPA_ENSINO BETWEEN 25 AND 29) OR (TP_ETAPA_ENSINO BETWEEN 35 AND 38) THEN 1 END) AS EM, 
            COUNT(CASE WHEN (TP_ETAPA_ENSINO BETWEEN 65 AND 67) OR (TP_ETAPA_ENSINO BETWEEN 69 AND 74) THEN 1 END) AS EJA,
            COUNT(CASE WHEN (TP_ETAPA_ENSINO BETWEEN 30 AND 34) OR (TP_ETAPA_ENSINO BETWEEN 39 AND 40) OR (TP_ETAPA_ENSINO = 56) OR (TP_ETAPA_ENSINO = 64) THEN 1 END) AS EP
        FROM matricula;
                    """)

    res = cursor.fetchall()
    df_niveis_ensino = pd.DataFrame(res, columns=cursor.column_names)

    # Transpose and reset index
    df_niveis_ensino_transposed = df_niveis_ensino.T.reset_index()

    # Rename columns for better readability
    df_niveis_ensino_transposed.columns = ['Nível de Ensino', 'Quantidade']

    st.bar_chart(df_niveis_ensino_transposed, y_label="Quantidade", x="Nível de Ensino", x_label=None, stack=False, width=600,
                 use_container_width=False, color="Nível de Ensino")

    # ------- TURMAS POR ESCOLA ----------

    st.markdown(f"## Turmas por Escola")
    st.text("")

    df_turma['Disciplinas'] = df_turma.apply(gerar_disciplinas, axis=1)

    colunas = ['NO_TURMA', 'Disciplinas']

    df_filtrado = df_turma[df_turma['CO_ENTIDADE'] == value][colunas]

    st.dataframe(df_filtrado,
                 width=1100,
                 column_config={
                    "_index": None,
                    "NO_TURMA": st.column_config.Column("Codigo Turma", width="small")
                    }
                 )

    # --------------- PROFESSORES E ALUNOS DA ESCOLA ---------------------

    df_alunos = df_matricula[df_matricula['CO_ENTIDADE'] == value]

    df_docente = df_docente[df_docente['CO_ENTIDADE'] == value]

    # Exibir alunos e professores na página
    st.markdown("## Alunos da Escola")
    st.markdown(f"####  *:grey[{result.loc[selected_row['selection']['rows'][0], 'NO_ENTIDADE']}]*")
    st.text("")
    st.dataframe(df_alunos[['CO_PESSOA_FISICA', 'ID_MATRICULA']],
                 column_config={
                     "_index": None,
                     "CO_PESSOA_FISICA": "Codigo P.Física",
                     "ID_MATRICULA": "ID da Matrícula"
                    }
                 )

    st.markdown(f"## Professores da Escola ")
    st.markdown(f"####  *:grey[{result.loc[selected_row['selection']['rows'][0], 'NO_ENTIDADE']}]*")
    st.text("")
    st.dataframe(df_docente[['CO_PESSOA_FISICA']],
                 column_config={
                     "_index": None,
                     "CO_PESSOA_FISICA": "Codigo P.Física"
                 }
                 )
