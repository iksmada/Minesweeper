from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.settings import (SettingsWithSidebar,
                               SettingsWithSpinner,
                               SettingsWithTabbedPanel)
from kivy.properties import OptionProperty, ObjectProperty
from constants import *

class SettingsApp(App):

    display_type = OptionProperty('normal', options=['normal', 'popup'])

    settings_popup = ObjectProperty(None, allownone=True)


    def build(self):

        paneltype = Label(text='Tipo de jogo')

        multi_button = Button(text='Multi Player')
        multi_button.bind(on_press=lambda j: self.set_multiplayer())
        single_button = Button(text='Single Player')
        single_button.bind(on_press=lambda j: self.set_singleplayer())

        mode_buttons = BoxLayout(orientation='horizontal')
        mode_buttons.add_widget(multi_button)
        mode_buttons.add_widget(single_button)

        '''displaytype = Label(text='')
        display_buttons = BoxLayout(orientation='horizontal')
        onwin_button = Button(text='on window')
        onwin_button.bind(on_press=lambda j: self.set_display_type('normal'))
        popup_button = Button(text='in a popup')
        popup_button.bind(on_press=lambda j: self.set_display_type('popup'))'''

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
        '''layout.add_widget(displaytype)
        layout.add_widget(display_buttons)'''
        layout.add_widget(settings_text)
        layout.add_widget(settings_buttons)

        return layout

    def on_settings_cls(self, *args):
        self.destroy_settings()

    def set_multiplayer(self):
        IS_MULTIPLAYER=True

    def set_singleplayer(self):
        IS_MULTIPLAYER = False

    def set_display_type(self, display_type):
        # type: (object) -> object
        self.destroy_settings()
        self.display_type = display_type

    def display_settings(self, settings):
        if self.display_type == 'popup':
            p = self.settings_popup
            if p is None:
                self.settings_popup = p = Popup(content=settings,
                                                title='Settings',
                                                size_hint=(0.8, 0.8))
            if p.content is not settings:
                p.content = settings
            p.open()
        else:
            super(SettingsApp, self).display_settings(settings)

    def close_settings(self, *args):
        if self.display_type == 'popup':
            p = self.settings_popup
            if p is not None:
                p.dismiss()
        else:
            super(SettingsApp, self).close_settings()
