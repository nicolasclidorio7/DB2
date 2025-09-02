# main.py
import ZODB, ZODB.FileStorage
import transaction
import random
import os
from model import JogoDaForca, RegistroHistorico # Importa ambas as classes

DB_FILE = 'forca.fs'
# Agora as palavras estão em um dicionário de categorias
PALAVRAS_INICIAIS = {
    'Frutas': ['morango', 'abacaxi', 'melancia', 'laranja', 'banana'],
    'Animais': ['cachorro', 'elefante', 'girafa', 'macaco', 'rinoceronte'],
    'Países': ['brasil', 'argentina', 'japao', 'canada', 'egito']
}

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def configurar_banco():
    storage = ZODB.FileStorage.FileStorage(DB_FILE)
    db = ZODB.DB(storage)
    connection = db.open()
    root = connection.root()

    if 'palavras' not in root:
        print("Primeira execução: Inicializando banco de dados...")
        root['palavras'] = PALAVRAS_INICIAIS
        root['jogo_em_andamento'] = None
        root['historico'] = []
        root['vitorias'] = 0
        root['derrotas'] = 0
        transaction.commit()
        print("Banco de dados inicializado com sucesso.")
    return connection, root

def adicionar_log(root, tipo, detalhes=""):
    """Cria e adiciona um novo registro ao histórico."""
    novo_registro = RegistroHistorico(tipo, detalhes)
    root['historico'].append(novo_registro)

def exibir_historico(root):
    limpar_tela()
    print("--- HISTÓRICO DE JOGADAS ---")
    if not root['historico']:
        print("\nNenhuma atividade registrada ainda.")
    else:
        # Exibe do mais recente para o mais antigo
        for registro in sorted(root['historico'], key=lambda r: r.timestamp, reverse=True):
            print(registro)
    input("\nPressione Enter para voltar ao menu...")

def jogar(root, jogo_atual):
    while not jogo_atual.fim_de_jogo:
        limpar_tela()
        print(jogo_atual.obter_visualizacao())
        letra = input("Digite uma letra (ou 'sair' para salvar e sair): ").strip().lower()

        if letra == 'sair':
            print("\nJogo salvo! Até a próxima.")
            return

        if len(letra) == 1 and letra.isalpha():
            mensagem = jogo_atual.tentar_letra(letra)
            if mensagem:
                print(mensagem)
                input("Pressione Enter para continuar...")
            else:
                # Log da jogada bem-sucedida
                detalhes_log = jogo_atual.obter_estado_para_log(letra)
                adicionar_log(root, "Jogada", detalhes_log)
        else:
            print("Entrada inválida. Por favor, digite uma única letra.")
            input("Pressione Enter para continuar...")
        
        transaction.commit()

    limpar_tela()
    print(jogo_atual.obter_visualizacao())
    if jogo_atual.vitoria:
        print(f"*** Parabéns! Você acertou a palavra '{jogo_atual.palavra_secreta}'! ***")
        root['vitorias'] += 1
        adicionar_log(root, "Vitória", f"Palavra: {jogo_atual.palavra_secreta}")
    else:
        print(f"--- Que pena! Você foi enforcado. A palavra era '{jogo_atual.palavra_secreta}'. ---")
        root['derrotas'] += 1
        adicionar_log(root, "Derrota", f"Palavra: {jogo_atual.palavra_secreta}")
    
    root['jogo_em_andamento'] = None
    transaction.commit()
    input("\nPressione Enter para voltar ao menu...")

if __name__ == "__main__":
    connection, root = configurar_banco()

    while True:
        limpar_tela()
        placar = f"(Vitórias: {root.get('vitorias', 0)} | Derrotas: {root.get('derrotas', 0)})"
        print(f"--- JOGO DA FORCA COM ZODB --- \n{placar}\n")
        print("[J] Jogar")
        print("[H] Histórico")
        print("[S] Sair")
        
        escolha = input("\nEscolha uma opção: ").strip().lower()

        if escolha == 'j':
            jogo_atual = root.get('jogo_em_andamento')
            if jogo_atual and not jogo_atual.fim_de_jogo:
                adicionar_log(root, "Jogo Carregado", f"Categoria: {jogo_atual.categoria}")
                transaction.commit()
                jogar(root, jogo_atual)
            else:
                # Lógica para iniciar um novo jogo
                limpar_tela()
                print("Escolha uma categoria:")
                categorias = list(root['palavras'].keys())
                for i, cat in enumerate(categorias):
                    print(f"[{i+1}] {cat}")
                
                try:
                    escolha_cat_idx = int(input("\nDigite o número da categoria: ")) - 1
                    if 0 <= escolha_cat_idx < len(categorias):
                        categoria_escolhida = categorias[escolha_cat_idx]
                        palavra_escolhida = random.choice(root['palavras'][categoria_escolhida])
                        
                        novo_jogo = JogoDaForca(palavra_escolhida, categoria_escolhida)
                        root['jogo_em_andamento'] = novo_jogo
                        adicionar_log(root, "Novo Jogo Iniciado", f"Categoria: {categoria_escolhida}")
                        transaction.commit()
                        jogar(root, novo_jogo)
                    else:
                        print("Número de categoria inválido.")
                        input("Pressione Enter para continuar...")
                except ValueError:
                    print("Entrada inválida. Por favor, digite um número.")
                    input("Pressione Enter para continuar...")

        elif escolha == 'h':
            exibir_historico(root)
        
        elif escolha == 's':
            print("Obrigado por jogar!")
            break
        
        else:
            print("Opção inválida!")
            input("Pressione Enter para tentar novamente...")

    connection.close()