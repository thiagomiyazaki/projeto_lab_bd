import streamlit as st

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

st.header("**Home**")

if "login" in st.session_state:
    st.write(f"{st.session_state.login} está logado!")

st.session_state.teste = "batatinha"

if "counter" not in st.session_state:
    st.session_state.counter = 0

st.write(st.session_state.teste)

button = st.button("Counter")
if button:
    st.session_state.counter += 1

st.write(st.session_state.counter)