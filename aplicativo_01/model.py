# model.py
import persistent
from datetime import datetime

HANGMAN_PICS = [
    '''
       +---+
           |
           |
           |
          ===
    ''',
    '''
       +---+
       O   |
           |
           |
          ===
    ''',
    '''
       +---+
       O   |
       |   |
           |
          ===
    ''',
    '''
       +---+
       O   |
      /|   |
           |
          ===
    ''',
    '''
       +---+
       O   |
      /|\\  |
           |
          ===
    ''',
    '''
       +---+
       O   |
      /|\\  |
      /    |
          ===
    ''',
    '''
       +---+
       O   |
      /|\\  |
      / \\  |
          ===
    '''
]


class JogoDaForca(persistent.Persistent):
    """
    Classe que armazena e gerencia o estado de um jogo da forca.
    """
    def __init__(self, palavra, categoria):
        self.palavra_secreta = palavra.upper()
        self.categoria = categoria
        self.letras_corretas = set()
        self.letras_erradas = set()
        self.tentativas_restantes = 6
        self.fim_de_jogo = False
        self.vitoria = False

    def tentar_letra(self, letra):
        letra = letra.upper()
        if letra in self.letras_corretas or letra in self.letras_erradas:
            return "Você já tentou esta letra."
        if letra in self.palavra_secreta:
            self.letras_corretas.add(letra)
        else:
            self.letras_erradas.add(letra)
            self.tentativas_restantes -= 1
        self._p_changed = True
        self._verificar_fim_de_jogo()
        return None

    def _verificar_fim_de_jogo(self):
        if all(letra in self.letras_corretas for letra in self.palavra_secreta):
            self.fim_de_jogo = True
            self.vitoria = True
        if self.tentativas_restantes <= 0:
            self.fim_de_jogo = True
            self.vitoria = False

    def _get_palavra_mostrada(self):
        return ''.join([f"{letra} " if letra in self.letras_corretas else '_ ' for letra in self.palavra_secreta])

    def obter_visualizacao(self):
        palavra_mostrada = self._get_palavra_mostrada()
        desenho_forca = HANGMAN_PICS[6 - self.tentativas_restantes]
        letras_erradas_str = 'Letras erradas: ' + ', '.join(sorted(list(self.letras_erradas)))
        return f"Categoria: {self.categoria}\n{desenho_forca}\n\nPalavra: {palavra_mostrada}\n\n{letras_erradas_str}\n"

    def obter_estado_para_log(self, letra_tentada):
        """Retorna uma string formatada do estado atual para o histórico."""
        palavra_mostrada = self._get_palavra_mostrada().strip()
        letras_erradas_str = ', '.join(sorted(list(self.letras_erradas)))
        return (f"Letra: '{letra_tentada.upper()}'. "
                f"Estado: {palavra_mostrada}. "
                f"Erradas: {letras_erradas_str}")

class RegistroHistorico(persistent.Persistent):
    """Classe para armazenar um único evento no histórico do jogo."""
    def __init__(self, tipo_evento, detalhes=""):
        self.timestamp = datetime.now()
        self.tipo_evento = tipo_evento
        self.detalhes = detalhes

    def __str__(self):
        # Formata o timestamp para exibição amigável
        ts_formatado = self.timestamp.strftime('%d/%m/%Y %H:%M:%S')
        return f"{ts_formatado} - {self.tipo_evento}: {self.detalhes}"