import persistent

class Autor(persistent.Persistent):
    def __init__(self, nome):
        self.nome = nome
        self.livros = [] # Atributo para o relacionamento

class Livro(persistent.Persistent):
    def __init__(self, titulo, ano):
        self.titulo = titulo
        self.ano = ano