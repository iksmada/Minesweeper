# -*- coding: utf-8

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.config import ConfigParser

from constants import *
from random import randint
from classes import GameController
from game import game


class SettingsApp(App):
    """
        Classe que gera uma instância do menu de congigurações
        Baseada em Kivy
    """
    # Remove as configurações do kivy do menu de configurações do jogo
    use_kivy_settings = False

    # Variaveis estáticas auxiliares
    is_multiplayer = False
    rows = 10
    columns = 20
    bombs = 10
    username = ''
    match = '' # username do usuário que criou uma partida
    color = '' # cor da bandeira escolhido

    def on_start(self):
        """
            Método chamado para inicializar o menu inicial
        :return: nada
        """
        Window.size = (300, 100)
        config = ConfigParser()
        # Carrega últimas configurações utilizadas (ou padrões se arquivo não é encontrado)
        config.read('settings.ini')
        self.username = config.get('section0', 'key00')
        self.color = SettingsApp.get_color(config.get('section0', 'key01'))
        if config.get('section1', 'key10') == "Single":
            self.is_multiplayer = False
        else:
            self.is_multiplayer = True
        self.match = config.get('section1', 'key11')
        self.rows = config.getint('section2', 'key20')
        self.columns = config.getint('section2', 'key21')
        self.bombs = config.getint('section3', 'key30')

    def build(self):
        """
            Método que cria o menu inicial
        :return: arquivo layout do menu inicial
        """
        settings_text = Label(text='Alterar Configurações do Tabuleiro ?')
        open_settings_button = Button(text='Abrir configurações')
        open_settings_button.bind(on_press=self.open_settings)
        start_button = Button(text='Iniciar')
        start_button.bind(on_press=self.on_game)
        settings_buttons = BoxLayout(orientation='horizontal')
        settings_buttons.add_widget(open_settings_button)
        settings_buttons.add_widget(start_button)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(settings_text)
        layout.add_widget(settings_buttons)

        return layout

    def build_config(self, config):
        """
            Gera, caso não encontrado, um novo arquivo com configurações padrões
        :param config: objeto de configuração a ser alterado
        :return: nada
        """
        random_id = randint(1000,9999)
        config.setdefaults('section0', {
            'key00':'player' + str(random_id), # Gera um username aleatório 'playerXXXX'
            'key01':'Branco'
        })
        config.setdefaults('section1', {
            'key10': 'Single',
            'key11': ''
        })
        config.setdefaults('section2', {
            'key20': '10',
            'key21': '20'
        })
        config.setdefaults('section3', {
            'key30': '10',
        })

    def open_settings(self, *largs):
        """
            Método é chamado toda vez que o menu de configurações é exibido
            Redimensiona a janela de configurações e a exibe
        :param largs: lista de argumentos (não é utilizado)
        :return: nada
        """
        Window.size = (500, 605)
        super(SettingsApp, self).open_settings()

    def close_settings(self, *largs):
        """
            Método é chamado toda vez que o menu de configurações é fechado e retorna ao menu inicial.
            Redimensiona a janela para o tamanho antigo
        :param largs: lista de argumentos (não é utilizado)
        :return: nada
        """
        Window.size = (300, 100)
        super(SettingsApp, self).close_settings()

    def build_settings(self, settings):
        """
            Carrega as possíveis configurações do arquivo JSON
        :param settings: objeto que contem a informacao das configuracoes a ser alterado
        :return: nada
        """
        jsondata = open('settings.json').read()
        settings.add_json_panel('Minesweeper',
                                self.config, data=jsondata)

    def on_config_change(self, config, section, key, value):
        """
            Método que é chamado para registrar as mudanças de configurações
        :param config: objeto de configuração a ser alterado
        :param section: sessão da configuração alterada
        :param key: chave da configuração alterada
        :param value: valor da configuração alterada
        :return: nada
        """
        # Se é uma instância de configuração
        if config is self.config:
            token = (section, key)
            if token == ('section0','key00'):
                self.username = str(value)                  # atualiza username
            elif token == ('section0','key01'):
                self.color = SettingsApp.get_color(value)   # atualiza cor escolhida
            elif token == ('section1', 'key10'):
                if value == "Single":                       # atualiza modo do jogo
                    self.is_multiplayer = False
                else:
                    self.is_multiplayer = True
            elif token == ('section1','key11'):             # atualiza username de quem criou a partida
                self.match = str(value)
            elif token == ('section2', 'key20'):            # atualiza numero de linhas do tabuleiro
                self.rows = max(int(value), 5)
                config.set(section, key, self.rows)
                config.write()
                self.build_settings(self._app_settings)
            elif token == ('section2', 'key21'):            # atualiza numero de colunas
                self.columns = max(int(value), 10)
                config.set(section, key, self.columns)
                config.write()
            elif token == ('section3', 'key30'):            # atualiza porcentagem de bombas
                if 100 >= int(value) > 0:
                    self.bombs = max(5,int(value))
                else:
                    self.bombs = 5
                config.set(section, key, self.bombs)
                config.write()

    def on_game(self, *largs):
        """
            Método chamado quando o jogo precisa ser iniciado (pygame)
        :param largs: lista de argumentos (não utilizado, mas necessário para assinatura do método)
        :return: nada
        """
        # Transfere os valores do menu para o controlador do jogo
        GameController.is_multiplayer = self.is_multiplayer
        GameController.username = self.username
        GameController.player_color = self.color
        if len(self.match) > 0:
            GameController.match_ID = self.match
        else:
            GameController.match_ID = self.username
        GameController.bombs = max(5,self.columns*self.rows*self.bombs/100)
        GameController.rows = max(5,self.rows)
        GameController.columns = max(10,self.columns)
        # Inicializa valores default
        GameController.totalBlocks = GameController.rows * GameController.columns
        GameController.screen_width = GameController.columns * BLOCK_SIZE + PADDING + 2*BLOCK_SIZE
        GameController.screen_height = GameController.rows * BLOCK_SIZE + PADDING + TITLE_AND_SCORE_SIZE + 2*BLOCK_SIZE
        GameController.score = 0
        # Inicia o jogo
        game()

    @staticmethod
    def get_color(color):
        """
            Traduz a cor escolhida para o seu ID interno (usado no arquivo).
        :param color: string com o nome da cor
        :return: string com o ID da cor
        """
        if color == "Amarelo":
            return 'yellow'
        elif color == "Azul":
            return 'blue'
        elif color == "Branco":
            return 'white'
        elif color == "Ciano":
            return 'cyan'
        elif color == "Rosa":
            return 'pink'
        elif color == "Roxo":
            return 'violet'
        elif color == "Verde":
            return 'green'
        elif color == "Vermelho":
            return 'red'
