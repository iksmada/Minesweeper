from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.settings import (SettingsWithSidebar,
                               SettingsWithSpinner,
                               SettingsWithTabbedPanel)
from kivy.properties import OptionProperty, ObjectProperty
from classes import GameController
from kivy.config import ConfigParser

class TestApp(App):

    def build_config(self, config):
        config.setdefaults('section1', {
            'key1': 'Single'
        })
        config.setdefaults('section2', {
            'key2': '20',
        })

        config.setdefaults('section3', {
            'key3': '10',
            'key4': '20'
        })

    def build(self):
        settings_text = Label(text='Alterar Configuracoes do Tabuleiro?')
        open_settings_button = Button(text='Open settings')
        open_settings_button.bind(on_press=self.open_settings)
        start_button = Button(text='Start')
        start_button.bind(on_press=self.stop)
        settings_buttons = BoxLayout(orientation='horizontal')
        settings_buttons.add_widget(open_settings_button)
        settings_buttons.add_widget(start_button)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(settings_text)
        layout.add_widget(settings_buttons)

        return layout

    def build_settings(self, settings):
        jsondata = """[
    { "type": "title",
      "title": "Modo" },

    { "type": "options",
      "title": "Multi/Single Player",
      "desc": "escolha o modo de jogo",
      "section": "section1",
      "key": "key1",
      "options": ["Single", "Multi"] },

      { "type": "title",
      "title": "Bombas" },
      { "type": "numeric",
      "title": "Numero de bombas",
      "desc": "deixe algo entre 25-10%",
      "section": "section2",
      "key": "key2" },

      { "type": "title",
      "title": "Dimensoes" },
      { "type": "numeric",
      "title": "Numero linhas",
      "desc": "valor bom entre 10 e 20",
      "section": "section3",
      "key": "key3" },
      { "type": "numeric",
      "title": "Numero colunas",
      "desc": "valor bom 2x Linhas",
      "section": "section3",
      "key": "key4" }




]"""
        settings.add_json_panel('Minesweeper',
                                self.config, data=jsondata)

    def on_config_change(self, config, section, key, value):
        if config is self.config:
            token = (section, key)
            if token == ('section1', 'key1'):
                #print('Our key1 have been changed to', value)
                if value=="Single":
                    GameController.is_multiplayer=False
                else:
                    GameController.is_multiplayer = True
                print('GameController.is_multiplayer = ',GameController.is_multiplayer)
            elif token == ('section2', 'key2'):
                #print('Our key2 have been changed to', value)
                GameController.bombs=int(value)
                print('GameController.bombs = ', GameController.bombs)
            elif token == ('section3', 'key3'):
                GameController.rows=int(value)
                print('GameController.rows = ', GameController.rows)
            elif token == ('section3', 'key4'):
                GameController.columns = int(value)
                print('GameController.columns = ', GameController.columns)

    def on_stop(self):
        GameController.totalBlocks=GameController.rows*GameController.columns

    def on_start(self):
        config = ConfigParser()
        #carrega ultimas configuracoes
        config.read('test.ini')
        #atribui ao controlador as ultimas configuracoes
        GameController.bombs    =   config.getint('section2', 'key2')
        GameController.rows     =   config.getint('section3', 'key3')
        GameController.columns  =   config.getint('section3', 'key4')

