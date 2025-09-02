import ZODB, ZODB.FileStorage
import transaction
from model import Autor

# --- 1. Conexão com o Banco de Dados ---
storage = ZODB.FileStorage.FileStorage('meu_banco.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

# --- 2. Lógica da Busca ---
print("--- Iniciando busca para o Exemplo 1 ---")
autor_alvo = "Isaac Asimov"
autor_encontrado = None

# Acessa a lista de autores na raiz de forma segura
lista_de_autores = root.get('autores', [])

for autor in lista_de_autores:
    if autor.nome == autor_alvo:
        autor_encontrado = autor
        break # Para a busca assim que encontrar

# --- 3. Exibição do Resultado ---
if autor_encontrado:
    print(f"SUCESSO: Autor '{autor_encontrado.nome}' encontrado no banco.")
else:
    print(f"FALHA: Autor '{autor_alvo}' não foi encontrado.")

# --- 4. Fechamento da Conexão ---
connection.close()
db.close()