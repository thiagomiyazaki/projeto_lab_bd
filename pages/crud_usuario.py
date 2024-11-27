import streamlit as st
import mysql.connector
import datetime

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

def validar(nome, email, senha, dt_nasc):
	if nome=="" or email=="" or senha=="" or dt_nasc=="":
		return False
	return True

def cadastra_usuario(nome, email, senha, dt_nasc):
	# inserir os dados de seu MySQL
    conn = mysql.connector.connect(host=st.secrets.DB_HOST
                                , user=st.secrets.DB_USERNAME, password=st.secrets.DB_PASSWORD
                                , port=st.secrets.DB_PORT, db=st.secrets.DB_NAME
                                , auth_plugin='mysql_native_password')
    cursor = conn.cursor()
	# ajustar conforme os campos da tabela Usuario de seu banco
    inp = f"INSERT INTO usuario (nome, email, data_cadastro, idade, senha, data_nascimento, descricao) VALUES ('{nome}', '{email}', now(), 10, sha('{senha}'), '{dt_nasc}', 'bsvsbv');"
    try:
        cursor.execute(inp)
        st.success("Usuário cadastrado.")
    except Exception as e:
        conn.rollback()
        st.error(f"Erro ao cadastrar o usuário {e}")
    finally:
        cursor.close()
    conn.commit()

with st.form("cadastro", clear_on_submit=True):
    st.title('Cadastro de usuários')
    nome = st.text_input('Nome:')
    email = st.text_input('Email:')
    senha = st.text_input('Senha:', type="password")
    dt_nasc = st.date_input('Data de nascimento:', min_value=datetime.date(1924,1,1), max_value=datetime.date(2024,1,1), format="DD/MM/YYYY")
    submit = st.form_submit_button("Enviar")
    print(dt_nasc)
	
if submit and validar(nome, email, senha, dt_nasc):
	# se o form for submetido e os dados estiverem válidos
	cadastra_usuario(nome, email, senha, dt_nasc)
elif submit:
	# se o form for submetido mas com dados inválidos
	st.warning("Dados inválidos")
	