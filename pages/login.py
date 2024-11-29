import streamlit as st
import mysql.connector
import hashlib

st.set_page_config(page_title="Login")

with st.sidebar:
    st.image('novo_logo.png')
    st.page_link("app.py", label="Home")
    st.page_link("pages/dashboard.py", label="Dashboard")
    st.page_link("pages/crud_usuario.py", label="Cadastrar Usuário")
    if "login" in st.session_state:
        st.page_link("pages/bookmark.py", label="Gerenciar Bookmarks")
    else:
        st.page_link("pages/login.py", label="Login")


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

        if Login.password_correct(email, senha):
            st.session_state.display_message = True
 
            st.session_state.login = email
            st.switch_page('app.py')
        else:
            st.write("**Senha errada!**")
        
    else:
        st.write("Este e-mail não existe.")

