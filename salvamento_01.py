import ZODB, ZODB.FileStorage
import transaction
# Importando as classes do slide anterior
from model import Autor

# 1. Configura o armazenamento e abre a conexão
storage = ZODB.FileStorage.FileStorage('meu_banco.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root()

# 2. Cria uma lista para autores na raiz (se não existir)
if 'autores' not in root:
    root['autores'] = []

# 3. Cria uma instância de um objeto persistente
autor_asimov = Autor("Isaac Asimov")

# 4. Adiciona o objeto à lista que está na raiz
root['autores'].append(autor_asimov)

# 5. Salva permanentemente as alterações
transaction.commit()

# 6. Fecha a conexão
connection.close()
db.close()