import pandas as pd
import streamlit as st
import mysql.connector

st.set_page_config(page_title="Bookmarks", initial_sidebar_state="collapsed", layout="wide")

with st.sidebar:
    st.image('novo_logo.png')
    st.page_link("app.py", label="Home")
    st.page_link("pages/dashboard.py", label="Dashboard")
    st.page_link("pages/crud_usuario.py", label="Cadastrar Usuário")
    if "login" in st.session_state:
        st.page_link("pages/bookmark.py", label="Gerenciar Bookmarks")
    else:
        st.page_link("pages/login.py", label="Login")


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
        result = cls.cursor.fetchall()
        cls.cursor.execute(f'SELECT * FROM bookmark WHERE id_usuario = "{result[0][0]}"')
        cls.bookmarks = cls.cursor.fetchall()

    @classmethod
    def write_bookmark(cls, co_entidade, id_usuario):
        cls.cursor.execute(f"SELECT id FROM usuario WHERE email = '{id_usuario}'")
        result = cls.cursor.fetchall()[0][0]
        cls.cursor.execute(
            "INSERT INTO bookmark (id_usuario, id_escola) VALUES (%s, %s);",
            (result, co_entidade)
        )
        cls.conn.commit()

    @classmethod
    def delete_bookmark(cls, co_entidade, id_usuario):
        cls.cursor.execute(f"SELECT id FROM usuario WHERE email = '{id_usuario}'")
        result = cls.cursor.fetchall()[0][0]
        cls.cursor.execute(f'DELETE FROM bookmark WHERE id_usuario = {result} AND id_escola = {co_entidade};')
        cls.conn.commit()


Bookmark.get_tabela_escola()
escolas_df = pd.DataFrame(Bookmark.tabela_escola, columns=["Codigo Entidade", "Nome da Escola"])
st.markdown("# Lista de Escolas")
selected_row = st.dataframe(escolas_df, on_select='rerun',
             selection_mode='single-row', column_config={"_index": None})

bookmark_btn = st.button("Bookmark!")

if bookmark_btn and selected_row['selection']['rows']:
    Bookmark.write_bookmark(int(escolas_df.loc[selected_row['selection']['rows'][0], "Codigo Entidade"]),
                            st.session_state.login)


st.markdown("# Lista de Bookmarks")
Bookmark.get_bookmarks(st.session_state.login)
bookmarks_df = pd.DataFrame(Bookmark.bookmarks, columns=["id", "User mail", "CO_ENTIDADE"])
escolas2_df = pd.DataFrame(Bookmark.tabela_escola, columns=["CO_ENTIDADE", "Nome da Escola"])
merged_df = pd.merge(bookmarks_df, escolas2_df, on='CO_ENTIDADE', how='left')

selected_row_del = st.dataframe(
    merged_df,
    column_config={
        "_index": None,
        "id": None,
        "User mail": None,
        "CO_ENTIDADE": "Codigo Entidade",
        },
    on_select='rerun',
    selection_mode='single-row'
    )

remove_btn = st.button("Remover Bookmark!")

if selected_row_del['selection']['rows'] and remove_btn:
    Bookmark.delete_bookmark(merged_df.loc[selected_row_del['selection']['rows'][0], "CO_ENTIDADE"],
                            st.session_state.login)
    st.markdown(f"pressed! {selected_row_del}")
    st.rerun()
