from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.settings import (SettingsWithSidebar,
                               SettingsWithSpinner,
                               SettingsWithTabbedPanel)
from kivy.properties import OptionProperty, ObjectProperty
class TestApp(App):

    def build_config(self, config):
        config.setdefaults('section1', {
            'key1': 'value1',
            'key2': '42'
        })

    def build(self):
        paneltype = Label(text='Tipo de jogo')

        multi_button = Button(text='Multi Player')
        multi_button.bind(on_press=lambda j: self.set_multiplayer())
        single_button = Button(text='Single Player')
        single_button.bind(on_press=lambda j: self.set_singleplayer())

        mode_buttons = BoxLayout(orientation='horizontal')
        mode_buttons.add_widget(multi_button)
        mode_buttons.add_widget(single_button)

        settings_text = Label(text='Alterar Configuracoes do Tabuleiro?')
        open_settings_button = Button(text='Open settings')
        open_settings_button.bind(on_press=self.open_settings)
        start_button = Button(text='Start')
        start_button.bind(on_press=self.close_settings)
        settings_buttons = BoxLayout(orientation='horizontal')
        settings_buttons.add_widget(open_settings_button)
        settings_buttons.add_widget(start_button)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(paneltype)
        layout.add_widget(mode_buttons)
        layout.add_widget(settings_text)
        layout.add_widget(settings_buttons)

        return layout

    def build_settings(self, settings):
        jsondata = """[
    { "type": "title",
      "title": "Test application" },

    { "type": "options",
      "title": "My first key",
      "desc": "Description of my first key",
      "section": "section1",
      "key": "key1",
      "options": ["value1", "value2", "another value"] },

    { "type": "numeric",
      "title": "My second key",
      "desc": "Description of my second key",
      "section": "section1",
      "key": "key2" }
]"""
        settings.add_json_panel('Test application',
                                self.config, data=jsondata)

    def on_config_change(self, config, section, key, value):
        if config is self.config:
            token = (section, key)
            if token == ('section1', 'key1'):
                print('Our key1 have been changed to', value)
            elif token == ('section1', 'key2'):
                print('Our key2 have been changed to', value)