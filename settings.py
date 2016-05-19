# -*- coding: utf-8

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from constants import *
from kivy.config import ConfigParser

from random import randint
from classes import GameController
from game import game


class SettingsApp(App):
    use_kivy_settings = False
    # variaveis locais auxiliares
    is_multiplayer = False
    rows = 10
    columns = 20
    bombs = 10
    username = ''
    match = ''

    def build_config(self, config):
        random_id = randint(1000,9999)
        config.setdefaults('section0', {
            'key0':'player' + str(random_id)
        })
        config.setdefaults('section1', {
            'key1': 'Single',
            'key10': ''
        })
        config.setdefaults('section2', {
            'key3': '10',
            'key4': '20'
        })
        config.setdefaults('section3', {
            'key2': '10',
        })

    def open_settings(self, *largs):
        Window.size = (500, 605)
        super(SettingsApp, self).open_settings()

    def close_settings(self, *largs):
        Window.size = (300, 100)
        super(SettingsApp, self).close_settings()

    def build(self):
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

    def build_settings(self, settings):
        # carrega arquivo JSON com layout
        jsondata = open('settings.json').read()
        settings.add_json_panel('Minesweeper',
                                self.config, data=jsondata)

    def on_config_change(self, config, section, key, value):
        if config is self.config:
            token = (section, key)
            if token == ('section0','key0'):
                self.username = str(value)
            elif token == ('section1', 'key1'):
                if value == "Single":
                    self.is_multiplayer = False
                else:
                    self.is_multiplayer = True
            elif token == ('section1','key10'):
                self.match = str(value)
            elif token == ('section2', 'key3'):
                self.rows = int(value)
            elif token == ('section2', 'key4'):
                self.columns = int(value)
            elif token == ('section3', 'key2'):
                self.bombs = int(value)

    def on_game(self, *largs):
        # salva valores
        GameController.is_multiplayer = self.is_multiplayer
        GameController.username = self.username
        if len(self.match) > 0:
            GameController.match_ID = self.match
        else:
            GameController.match_ID = self.username
        GameController.bombs = self.columns*self.rows*self.bombs/100
        GameController.rows = self.rows
        GameController.columns = self.columns
        GameController.totalBlocks = self.rows * self.columns
        GameController.screen_width = self.columns * BLOCK_SIZE + PADDING
        GameController.screen_height = self.rows * BLOCK_SIZE + PADDING + TITLE_AND_SCORE_SIZE
        GameController.score = 0
        # TODO criar trhread quando cria game
        game()

    def on_start(self):
        Window.size = (300, 100)
        config = ConfigParser()
        # carrega ultimas configuracoes
        config.read('settings.ini')

        # atribui ao controlador as ultimas configuracoes
        if config.get('section1', 'key1') == "Single":
            self.is_multiplayer = False
        else:
            self.is_multiplayer = True
        self.rows = config.getint('section2', 'key3')
        self.columns = config.getint('section2', 'key4')
        self.bombs = config.getint('section3', 'key2')
        self.username = config.get('section0','key0')
        self.match = config.get('section1','key10')
