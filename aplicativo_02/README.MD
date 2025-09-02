# Jogo da Forca com Flask e ZODB

Este projeto apresenta uma versão web completa do clássico Jogo da Forca, construído com Python e o microframework Flask. Seu principal diferencial é a utilização do **ZODB (Zope Object Database)** para uma persistência de dados transparente e orientada a objetos, eliminando a necessidade de um banco de dados relacional tradicional ou de um ORM.

A aplicação evoluiu de uma versão inicial de terminal para uma interface web interativa e amigável, demonstrando a flexibilidade de um modelo de dados bem desacoplado da camada de apresentação.

## ✨ Funcionalidades

  * **Interface Web Completa:** Uma aplicação web responsiva e intuitiva construída com Flask e HTML/CSS puros.
  * **Jogabilidade Interativa:** Em vez de campos de texto, a interface utiliza botões para cada letra do alfabeto, que são desabilitados após o uso para um feedback visual claro.
  * **Seleção de Categoria com Um Clique:** Para iniciar um novo jogo, basta clicar no botão da categoria desejada.
  * **Persistência de Sessão Robusta:** O estado do jogo é salvo no ZODB após cada jogada. O jogador pode fechar o navegador e, ao retornar, continuar o jogo exatamente de onde parou.
  * **Placar Persistente:** O placar de vitórias e derrotas é armazenado de forma duradoura.
  * **Timeline de Histórico:** Todas as ações (início de jogo, jogadas, resultados) são registradas em um histórico visualmente agradável, formatado como uma timeline de "cards" com ícones e cores.

## 🛠️ Tecnologias Utilizadas

  * **Backend:** Python 3, Flask
  * **Banco de Dados:** ZODB (Zope Object Database)
  * **Frontend:** HTML5, CSS3 (sem frameworks, apenas estilos customizados)

## 📂 Estrutura do Projeto

O código é modularizado para separar responsabilidades, seguindo as melhores práticas de desenvolvimento web.

  * `app.py`

      * O coração da aplicação Flask. Define todas as rotas (URLs), gerencia as requisições HTTP e orquestra a interação entre a interface do usuário e o banco de dados. Implementa o padrão de gerenciamento de conexão com o ZODB (uma conexão por requisição).

  * `model.py`

      * Define o modelo de dados da aplicação. Contém as classes `JogoDaForca` e `RegistroHistorico`, que herdam de `persistent.Persistent` para poderem ser salvas diretamente no ZODB. Esta camada é completamente independente da interface (seja ela terminal ou web).

  * `static/`
    * Pasta que contém todos os arquivos estáticos, que não são processados pelo back-end.
    * `css/estilo.css`: A folha de estilos (CSS) que define toda a aparência da aplicação.

  * `templates/`

      * Diretório que contém todos os arquivos HTML renderizados pelo Jinja2.
      * `layout.html`: O template base que define a estrutura comum (menu de navegação, estilos CSS) para todas as páginas.
      * `index.html`: A página principal onde o jogo acontece.
      * `novo_jogo.html`: A página de seleção de categorias.
      * `historico.html`: A página que exibe a timeline de histórico.

  * `forca.fs` (gerado automaticamente)

      * O arquivo do banco de dados ZODB. Contém todos os objetos Python persistidos.

## 🚀 Setup e Execução

### Pré-requisitos

  * Python 3.x
  * pip (gerenciador de pacotes do Python)

### Instalação

1.  Clone este repositório ou baixe os arquivos para um diretório local em uma pasta com permissão de escrita (ex: `Documentos`, `Desktop`).

2.  Navegue até o diretório do projeto pelo seu terminal.

3.  (Recomendado) Crie e ative um ambiente virtual:

    ```bash
    # No Windows
    python -m venv venv
    .\venv\Scripts\activate

    # No macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  Instale as dependências:

    ```bash
    pip install Flask ZODB
    ```

### Executando a Aplicação

1.  No terminal, a partir do diretório raiz do projeto, execute o script principal:
    ```bash
    python app.py
    ```
2.  Abra seu navegador de internet e acesse o seguinte endereço:
    `http://127.0.0.1:5000`

## 💡 Conceitos-Chave da Implementação

  * **Gerenciamento de Conexão no Flask:** Para evitar erros de `LockError` com o reiniciador automático do Flask, a aplicação usa os decoradores `@app.before_request` e `@app.teardown_request`. Isso garante que uma nova conexão com o ZODB seja aberta no início de cada requisição e fechada ao final, um padrão robusto para aplicações web.

  * **Persistência Transparente:** A lógica do jogo em `model.py` não se preocupa em "como" salvar os dados. Ela simplesmente modifica os atributos dos objetos (ex: `self.letras_erradas.add(letra)`). O ZODB, junto com `transaction.commit()`, cuida de detectar essas mudanças e persistir o estado do objeto no banco de dados.

  * **Estado entre Requisições:** Como o protocolo HTTP é sem estado (stateless), o objeto do jogo em andamento (`g.root['jogo_em_andamento']`) é recuperado do banco de dados no início de cada requisição e salvo de volta ao final, permitindo a continuidade do jogo entre os cliques do usuário.