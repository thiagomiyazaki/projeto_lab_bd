import streamlit as st
import pandas as pd
import mysql.connector


class Bookmark:
    tabela_escola = None
    bookmarks = None
    conn = mysql.connector.connect(host=st.secrets.DB_HOST
                                   , user=st.secrets.DB_USERNAME, password=st.secrets.DB_PASSWORD
                                   , port=st.secrets.DB_PORT, db=st.secrets.DB_NAME
                                   , auth_plugin='mysql_native_password')
    cursor = conn.cursor()

    @classmethod
    def get_tabela_escola(cls):
        cls.cursor.execute(f'SELECT CO_ENTIDADE, NO_ENTIDADE FROM escola;')
        cls.tabela_escola = cls.cursor.fetchall()

    @classmethod
    def get_bookmarks(cls, user_mail):
        cls.cursor.execute(f'SELECT * FROM usuario WHERE email = "{user_mail}";')
        resultado = cls.cursor.fetchall()
        cls.cursor.execute(f'SELECT * FROM bookmark WHERE id_usuario = "{resultado[0][0]}"')
        cls.bookmarks = cls.cursor.fetchall()

    @classmethod
    def write_bookmark(cls, co_entidade, id_usuario):
        cls.cursor.execute(f"SELECT id FROM usuario WHERE email = '{id_usuario}'")
        resultado = cls.cursor.fetchall()[0][0]
        cls.cursor.execute(
            "INSERT INTO bookmark (id_usuario, id_escola) VALUES (%s, %s);",
            (result, co_entidade)
        )
        cls.conn.commit()

    @classmethod
    def delete_bookmark(cls, co_entidade, id_usuario):
        cls.cursor.execute(f"SELECT id FROM usuario WHERE email = '{id_usuario}'")
        resultado = cls.cursor.fetchall()[0][0]
        cls.cursor.execute(f'DELETE FROM bookmark WHERE id_usuario = {result} AND id_escola = {co_entidade};')
        cls.conn.commit()


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
    st.page_link("pages/crud_usuario.py", label="Cadastrar Usuário")
    if "login" in st.session_state:
        st.page_link("pages/bookmark.py", label="Gerenciar Bookmarks")
    else:
        st.page_link("pages/login.py", label="Login")

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

if "login" in st.session_state:
    Bookmark.get_bookmarks(st.session_state.login)
    bookmarks_df = pd.DataFrame(Bookmark.bookmarks, columns=["id", "User mail", "CO_ENTIDADE"])
    print(f'{Bookmark.bookmarks=}')
    lista_entidade_priorizar = bookmarks_df['CO_ENTIDADE'].to_list()
    print(f'{lista_entidade_priorizar=}')

    # Create a priority column: 1 for codes in the list, 2 for others
    result['Prioridade'] = result['CO_ENTIDADE'].apply(lambda x: 1 if x in lista_entidade_priorizar else 2)
    result = result.sort_values(by='Prioridade').reset_index()

selected_row = st.dataframe(result,
                            use_container_width=True,
                            on_select='rerun',
                            selection_mode='single-row',
                            column_config={
                                "_index": None,
                                "index": None,
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

# ------- NIVEIS ENSINO GERAL MUNICIPIO ----------

st.markdown(f"## Quantidade de alunos por nível escolar")
st.text("")

cursor.execute(f"""
    SELECT 
        COUNT(CASE WHEN TP_ETAPA_ENSINO <= 3 THEN 1 END) AS EI,
        COUNT(CASE WHEN (TP_ETAPA_ENSINO BETWEEN 4 AND 8) OR (TP_ETAPA_ENSINO BETWEEN 14 AND 18) THEN 1 END) AS EF_1,
        COUNT(CASE WHEN (TP_ETAPA_ENSINO BETWEEN 9 AND 13) OR (TP_ETAPA_ENSINO BETWEEN 19 AND 21) OR (TP_ETAPA_ENSINO = 41) THEN 1 END) AS EF_2, 
        COUNT(CASE WHEN (TP_ETAPA_ENSINO BETWEEN 25 AND 29) OR (TP_ETAPA_ENSINO BETWEEN 35 AND 38) THEN 1 END) AS EM, 
        COUNT(CASE WHEN (TP_ETAPA_ENSINO BETWEEN 65 AND 67) OR (TP_ETAPA_ENSINO BETWEEN 69 AND 74) THEN 1 END) AS EJA,
        COUNT(CASE WHEN (TP_ETAPA_ENSINO BETWEEN 30 AND 34) OR (TP_ETAPA_ENSINO BETWEEN 39 AND 40) OR (TP_ETAPA_ENSINO = 56) OR (TP_ETAPA_ENSINO = 64) THEN 1 END) AS EP
    FROM matricula""")

res = cursor.fetchall()
df_niveis_ensino = pd.DataFrame(res, columns=cursor.column_names)

# transpoe e reseta index
df_niveis_ensino_transposed = df_niveis_ensino.T.reset_index()

# Renomeia as colunas para melhor legibilidade
df_niveis_ensino_transposed.columns = ['Nível de Ensino', 'Quantidade']

st.bar_chart(df_niveis_ensino_transposed, y_label="Quantidade", x="Nível de Ensino", x_label=None, stack=False, width=600,
             use_container_width=False, color="Nível de Ensino")

if selected_row['selection']['rows']:
    st.text("")
    st.text("")
    st.markdown(f"# Dados Específicos da Escola")
    st.markdown(f"####  *:grey[{result.loc[selected_row['selection']['rows'][0], 'NO_ENTIDADE']}]*")
    st.text("")
    st.text("")
    st.markdown(f"## Quantidade de Alunos, Docentes e Turmas")

    print(f'{selected_row}')

    print(f"{selected_row['selection']['rows'][0]=}")
    value = result.loc[selected_row['selection']['rows'][0], 'CO_ENTIDADE']
    print(f'{value=}')

    plot_df = get_plot_data(value, df_turma, df_docente, df_matricula)

    # transpoe e reseta index
    df_transposed = plot_df.T.reset_index()

    # renomear colunas
    df_transposed.columns = ['Categoria', 'Quantidade']

    print(plot_df)
    print(df_transposed)

    st.bar_chart(df_transposed, y_label="Quantidade", x="Categoria", x_label=None, stack=False, width=600,
                 use_container_width=False, color="Categoria")

    # ------- TURMAS POR ESCOLA ----------

    st.markdown(f"## Lista de Turmas")
    st.markdown(f"####  *:grey[{result.loc[selected_row['selection']['rows'][0], 'NO_ENTIDADE']}]*")
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

    st.markdown(f"## Quantidade de alunos por nível escolar")
    st.markdown(f"####  *:grey[{result.loc[selected_row['selection']['rows'][0], 'NO_ENTIDADE']}]*")
    st.text("")

    cursor.execute(f"""
        SELECT 
            COUNT(CASE WHEN TP_ETAPA_ENSINO <= 3 THEN 1 END) AS EI,
            COUNT(CASE WHEN (TP_ETAPA_ENSINO BETWEEN 4 AND 8) OR (TP_ETAPA_ENSINO BETWEEN 14 AND 18) THEN 1 END) AS EF_1,
            COUNT(CASE WHEN (TP_ETAPA_ENSINO BETWEEN 9 AND 13) OR (TP_ETAPA_ENSINO BETWEEN 19 AND 21) OR (TP_ETAPA_ENSINO = 41) THEN 1 END) AS EF_2, 
            COUNT(CASE WHEN (TP_ETAPA_ENSINO BETWEEN 25 AND 29) OR (TP_ETAPA_ENSINO BETWEEN 35 AND 38) THEN 1 END) AS EM, 
            COUNT(CASE WHEN (TP_ETAPA_ENSINO BETWEEN 65 AND 67) OR (TP_ETAPA_ENSINO BETWEEN 69 AND 74) THEN 1 END) AS EJA,
            COUNT(CASE WHEN (TP_ETAPA_ENSINO BETWEEN 30 AND 34) OR (TP_ETAPA_ENSINO BETWEEN 39 AND 40) OR (TP_ETAPA_ENSINO = 56) OR (TP_ETAPA_ENSINO = 64) THEN 1 END) AS EP
        FROM matricula WHERE CO_ENTIDADE = {value}""")

    res = cursor.fetchall()
    df_niveis_ensino = pd.DataFrame(res, columns=cursor.column_names)

    # Transpoe e reseta index
    df_niveis_ensino_transposed = df_niveis_ensino.T.reset_index()

    # Renomeia as colunas para melhor legibilidade
    df_niveis_ensino_transposed.columns = ['Nível de Ensino', 'Quantidade']

    st.bar_chart(df_niveis_ensino_transposed, y_label="Quantidade", x="Nível de Ensino", x_label=None, stack=False,
                 width=600,
                 use_container_width=False, color="Nível de Ensino")
