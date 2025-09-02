# app.py

import ZODB, ZODB.FileStorage
import transaction
import random
from flask import Flask, render_template, request, redirect, url_for, g

# Importa nossas classes do ZODB
from model import JogoDaForca, RegistroHistorico

# --- Configuração Inicial ---
app = Flask(__name__)
app.secret_key = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
DB_FILE = 'forca.fs'
PALAVRAS_INICIAIS = {
    'Frutas': ['morango', 'abacaxi', 'melancia', 'laranja', 'banana'],
    'Animais': ['cachorro', 'elefante', 'girafa', 'macaco', 'rinoceronte'],
    'Países': ['brasil', 'argentina', 'japao', 'canada', 'egito']
}

storage = ZODB.FileStorage.FileStorage(DB_FILE)
db = ZODB.DB(storage)

@app.before_request
def before_request():
    """Executado ANTES de cada requisição. Abre uma conexão e a armazena em 'g'."""
    g.connection = db.open()
    g.root = g.connection.root()

@app.teardown_request
def teardown_request(exception=None):
    """Executado DEPOIS de cada requisição. Fecha a conexão."""
    connection = getattr(g, 'connection', None)
    if connection is not None:
        connection.close()

def inicializar_banco():
    """Verifica se o banco precisa ser inicializado com dados padrão."""
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
        print("Banco de dados inicializado.")
    connection.close()

def adicionar_log(root, tipo, detalhes=""):
    novo_registro = RegistroHistorico(tipo, detalhes)
    root['historico'].append(novo_registro)

# app.py
from flask import Flask, render_template, request, redirect, url_for, g, flash # ADICIONE 'flash' AOS IMPORTS

# ...

@app.route('/', methods=['GET', 'POST'])
def index():
    jogo_atual = g.root.get('jogo_em_andamento')
    placar = {
        'vitorias': g.root.get('vitorias', 0),
        'derrotas': g.root.get('derrotas', 0)
    }
    mensagem_erro = None
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if request.method == 'POST':
        # Se não houver jogo, redireciona para a página de novo jogo
        if not jogo_atual or jogo_atual.fim_de_jogo:
            return redirect(url_for('novo_jogo'))

        letra = request.form.get('letra', '').strip().lower()
        if len(letra) == 1 and letra.isalpha():
            mensagem_erro = jogo_atual.tentar_letra(letra)
            if not mensagem_erro:
                detalhes_log = jogo_atual.obter_estado_para_log(letra)
                adicionar_log(g.root, "Jogada", detalhes_log)
            
            # --- LÓGICA DE FIM DE JOGO CORRIGIDA ---
            if jogo_atual.fim_de_jogo:
                palavra_final = jogo_atual.palavra_secreta
                if jogo_atual.vitoria:
                    g.root['vitorias'] += 1
                    adicionar_log(g.root, "Vitória", f"Palavra: {palavra_final}")
                    # Envia a mensagem de sucesso para a próxima tela
                    flash(f"🎉 Parabéns! Você venceu! A palavra era '{palavra_final}'. 🎉", "success")
                else:
                    g.root['derrotas'] += 1
                    adicionar_log(g.root, "Derrota", f"Palavra: {palavra_final}")
                    # Envia a mensagem de falha para a próxima tela
                    flash(f"☠️ Que pena! Você perdeu. A palavra era '{palavra_final}'. ☠️", "danger")
                
                # Anula o jogo no banco de dados, como você sugeriu
                g.root['jogo_em_andamento'] = None
            
            transaction.commit()
            return redirect(url_for('index'))
        else:
            mensagem_erro = "Por favor, digite uma única letra."
    
    return render_template('index.html', jogo=jogo_atual, placar=placar, erro=mensagem_erro, alfabeto=alfabeto)

@app.route('/novo_jogo', methods=['GET', 'POST'])
def novo_jogo():
    if request.method == 'POST':
        categoria = request.form.get('categoria')
        if categoria and categoria in g.root['palavras']:
            palavra = random.choice(g.root['palavras'][categoria])
            novo_jogo_obj = JogoDaForca(palavra, categoria)
            g.root['jogo_em_andamento'] = novo_jogo_obj
            adicionar_log(g.root, "Novo Jogo Iniciado", f"Categoria: {categoria}")
            transaction.commit()
            return redirect(url_for('index'))
    
    categorias = list(g.root['palavras'].keys())
    return render_template('novo_jogo.html', categorias=categorias)

@app.route('/historico')
def historico():
    historico_ordenado = sorted(g.root.get('historico', []), key=lambda r: r.timestamp, reverse=True)
    return render_template('historico.html', historico=historico_ordenado)

@app.route('/jogar')
def jogar_redirect():
    """
    Verifica se há um jogo em andamento e redireciona o usuário
    para a página correta (continuar ou criar um novo).
    """
    if g.root.get('jogo_em_andamento'):
        return redirect(url_for('index'))
    else:
        return redirect(url_for('novo_jogo'))

if __name__ == '__main__':
    inicializar_banco()
    app.run(debug=False)