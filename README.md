# Projeto de Laboratório de Banco de Dados

## Instanciando o Banco de Dados
- `dumpfile.sql` é o arquivo gerado pelo comando `mysqldump -u local_user -p local_database_name > dumpfile.sql`
- Através dele podemos criar uma instância do Banco de Dados que utilizamos para o nosso projeto.
- Com o MySQL instalado na sua máquina, para importar o Banco de Dados de `dumpfile.sql`:

```bash
# Entrar no terminal do MySQL:
mysql -u your_user -p

# Na CLI do MySQL, digite:
CREATE DATABASE labbd;

# Saia do MySQL e no bash digite:
mysql -u local_used -p labbd < dumpfile.sql
```

## Criando secrets.toml

- Defina os seguintes parâmetros no arquivo `.streamlit/secrets.toml`.

```
[database]
DB_HOST = mysql server address
DB_USERNAME = seu usuario
DB_PASSWORD = password do usuario
DB_PORT = 3306
DB_NAME = labbd
```

## Executando

- Com o virtual environment criado, as dependências instaladas (`pip install -r requirements.txt`), ao executar `streamlit run app.py` o aplicativo já deve funcionar localmente!

## Arquivos
- `CREATE_VIEW_LISTAR_ESCOLA.sql`: query para a criar a view de listar criando uma contagem de estudantes.
- `dumpfile.sql`: arquivo gerado pelo dump do servidor MySQL utilizado durante o projeto.
- `QueryCriacaoBD.sql`: arquivo utilizado para criar o Banco de Dados (arquivo gerado em aula). Para rodar esta query é necessário que os arquivos .csv estejam nos diretórios corretos (Ubuntu).
