import streamlit as st
import mysql.connector
import hashlib

st.set_page_config(page_title="Login", initial_sidebar_state="collapsed", layout="wide")

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

class Login:
    conn = mysql.connector.connect(host=st.secrets.DB_HOST
                               , user=st.secrets.DB_USERNAME, password=st.secrets.DB_PASSWORD
                               , port=st.secrets.DB_PORT, db=st.secrets.DB_NAME
                               , auth_plugin='mysql_native_password')
    cursor = conn.cursor()

    @staticmethod
    def email_exists(email):
        Login.cursor.execute(f'SELECT * FROM usuario WHERE email = "{email}";')
        result = Login.cursor.fetchall()
        return result

    @staticmethod
    def password_correct(email, senha):
        Login.cursor.execute(f'SELECT senha FROM usuario WHERE email = "{email}";')
        result = Login.cursor.fetchall()
        hashed = hashlib.sha1(senha.encode())
        print(f'{result=}')
        print(f'{hashed.hexdigest()=}')
        return hashed.hexdigest() == result[0][0]


with st.form("Login", clear_on_submit=True):
    st.title('Login')
    email = st.text_input('Email:')
    senha = st.text_input('Senha:', type="password")
    submit = st.form_submit_button("Login")

if submit:
    if Login.email_exists(email):
        # print(Login.email_exists(email))
        if Login.password_correct(email, senha):
            st.session_state.display_message = True
            # st.write("**Login bem sucedido!**")
            # st.toast('Login bem sucedido!', icon='🎉')
            # st.success('This is a success message!', icon="✅")
            st.session_state.login = email
            st.switch_page('app.py')
        else:
            st.write("**Senha errada!**")
        
    else:
        st.write("Este e-mail não existe.")


# if submit:
#     if Login.email_exists():
#         if Login.password_correct():
#             # incorrect password
#             pass
#     else:
#         # raise e-mail does not exist
#         pass
