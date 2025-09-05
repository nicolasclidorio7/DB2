import ZODB, ZODB.FileStorage
import transaction
from model import Autor, Livro

# --- 1. Conexão com o Banco de Dados ---
storage = ZODB.FileStorage.FileStorage('meu_banco.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()
lista_de_autores = root.get('autores', [])

# --- 2. Lógica da Busca (Parte 1: Livros de um autor específico) ---
print("\n--- Iniciando busca para o Exemplo 2 (Parte 1) ---")


for autor in lista_de_autores:
   

 if autor:
    print(f"Livros de '{autor.nome}':")
    if autor.get_livros():
        # Aqui está a "mágica" da navegação: basta acessar o atributo!
        for livro in autor.get_livros():
            print(f"  - Título: {livro.titulo}, Ano: {livro.ano}")
    else:
        print("  - Nenhum livro cadastrado para este autor.")
else:
    print(f"Autor '{autor}' não encontrado.")



# --- 4. Fechamento da Conexão ---
connection.close()
db.close()