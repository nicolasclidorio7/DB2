# Jogo da Forca com Persistência em ZODB

Este é um projeto de um clássico Jogo da Forca desenvolvido em Python para ser executado no terminal. O principal diferencial deste projeto é o uso do **ZODB (Zope Object Database)**, um banco de dados orientado a objetos, para gerenciar de forma transparente e persistente todo o estado da aplicação.

O objetivo é demonstrar como um BDOO pode simplificar o armazenamento de dados complexos (objetos de jogo, histórico, placares) sem a necessidade de um Mapeador Objeto-Relacional (ORM) ou da tradução de dados para tabelas.

## ✨ Funcionalidades

  * **Jogabilidade Clássica:** Adivinhe as letras para descobrir a palavra secreta antes que o boneco seja enforcado.
  * **Categorias de Palavras:** Ao iniciar um novo jogo, o jogador pode escolher entre diferentes categorias (ex: Frutas, Animais, Países).
  * **Persistência de Sessão:** O estado do jogo é salvo atomicamente após cada jogada. O jogador pode fechar o terminal a qualquer momento e continuar o jogo exatamente de onde parou.
  * **Placar Persistente:** O número de vitórias e derrotas é armazenado e exibido no menu principal.
  * **Histórico Detalhado:** Todas as ações importantes (início de jogo, cada jogada, vitórias, derrotas) são registradas com data e hora e podem ser consultadas a qualquer momento.
  * **Interface de Terminal:** Simples, intuitiva e multiplataforma.

## 🛠️ Tecnologias Utilizadas

  * **Python 3:** Linguagem de programação principal.
  * **ZODB (Zope Object Database):** Banco de dados orientado a objetos para persistência de dados.

## 🚀 Como Executar

### Pré-requisitos

  * Python 3 instalado em seu sistema.
  * `pip` (gerenciador de pacotes do Python).

### Instalação

1.  **Clone este repositório ou baixe os arquivos** `main.py` e `model.py` para um diretório local.

2.  **Navegue até o diretório do projeto** pelo seu terminal:

    ```bash
    cd /caminho/para/o/projeto
    ```

3.  **Instale a única dependência necessária**, o ZODB:

    ```bash
    pip install ZODB
    ```

### Executando a Aplicação

Para iniciar o jogo, basta executar o arquivo `main.py`:

```bash
python main.py
```

Na primeira execução, o programa criará automaticamente o arquivo de banco de dados `forca.fs`.

## 📂 Estrutura do Projeto

O projeto é organizado em dois arquivos principais para separar as responsabilidades:

  * 📄 `model.py`

      * Define as classes de dados que serão salvas no banco de dados (os "modelos").
      * `JogoDaForca(persistent.Persistent)`: Modela o estado de um jogo em andamento (palavra secreta, letras tentadas, etc.).
      * `RegistroHistorico(persistent.Persistent)`: Modela uma entrada no log de histórico.

  * 📄 `main.py`

      * Contém a lógica principal da aplicação.
      * Gerencia a conexão com o banco de dados ZODB.
      * Exibe o menu, controla o fluxo do jogo e interage com o usuário.
      * Orquestra a criação e modificação dos objetos definidos em `model.py`.

  * 🗃️ `forca.fs` (gerado automaticamente)

      * Este é o arquivo do banco de dados. É um arquivo binário que contém todos os objetos Python serializados (salvos).

## 💡 Como a Persistência com ZODB Funciona

O ZODB permite tratar o banco de dados quase como um dicionário Python gigante, acessado através do objeto `root`.

1.  **Classes Persistentes:** Qualquer classe que precise ser salva no banco deve herdar de `persistent.Persistent`, como visto em `model.py`. Isso "ensina" os objetos a rastrearem suas próprias alterações.

2.  **O Objeto Raiz (`root`):** Acessamos o banco através de uma "raiz". Armazenamos tudo a partir dela:

      * `root['palavras']`: Um dicionário com as categorias e listas de palavras.
      * `root['jogo_em_andamento']`: Armazena o objeto `JogoDaForca` da partida atual. Se for `None`, não há jogo em andamento.
      * `root['historico']`: Uma lista de objetos `RegistroHistorico`.
      * `root['vitorias']` e `root['derrotas']`: Contadores inteiros para o placar.

3.  **Transações (`transaction.commit()`):** Nenhuma alteração é salva permanentemente no disco até que `transaction.commit()` seja chamado. Neste projeto, essa função é chamada após cada jogada, garantindo que mesmo que o programa seja interrompido, a última ação do jogador estará salva. Isso garante a **atomicidade** e a **consistência** dos dados.