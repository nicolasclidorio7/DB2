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
autor_alvo_2 = "Philip K. Dick"
autor_encontrado_2 = None

for autor in lista_de_autores:
    if autor.nome == autor_alvo_2:
        autor_encontrado_2 = autor
        break

if autor_encontrado_2:
    print(f"Livros de '{autor_encontrado_2.nome}':")
    if autor_encontrado_2.livros:
        # Aqui está a "mágica" da navegação: basta acessar o atributo!
        for livro in autor_encontrado_2.livros:
            print(f"  - Título: {livro.titulo}, Ano: {livro.ano}")
    else:
        print("  - Nenhum livro cadastrado para este autor.")
else:
    print(f"Autor '{autor_alvo_2}' não encontrado.")

# --- 3. Lógica da Busca (Parte 2: Filtrando todos os livros por critério) ---
print("\n--- Iniciando busca para o Exemplo 2 (Parte 2) ---")
print("Buscando todos os livros publicados após 1960:")

livros_encontrados_no_filtro = []
for autor in lista_de_autores: # Itera em todos os autores
    for livro in autor.livros: # Itera nos livros de cada autor
        if livro.ano > 1960:
            livros_encontrados_no_filtro.append((autor.nome, livro.titulo, livro.ano))

if livros_encontrados_no_filtro:
    for autor, titulo, ano in livros_encontrados_no_filtro:
        print(f"  - '{titulo}' ({ano}) por {autor}")
else:
    print("Nenhum livro encontrado para este critério.")


# --- 4. Fechamento da Conexão ---
connection.close()
db.close()