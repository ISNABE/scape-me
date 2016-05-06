from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.logger import Logger

from LevelService import LevelService
from LevelManager import LevelManager

import os


class Menu(FloatLayout):
    FONT_MENU = './resources/menu/SIXTY.TTF'

    def __init__(self, event_dispatcher, **kwargs):
        """
        Initialize menu's button and textures.
        :param kwargs: Args of Layout
        :rtype: void
        """
        super(Menu, self).__init__(**kwargs)
        self.event_dispatcher = event_dispatcher

        # Add fond and title.
        self.canvas.add(
            Rectangle(source='./resources/menu/test_im1.jpeg', size=Window.size)
        )

        self.add_widget(
            Label(text="'Scape me", font_name=self.FONT_MENU, font_size='100sp',
                  size_hint=(0.25, 0.1), pos_hint={'x': 0.37, 'y': 0.75})
        )

        # Add buttons.
        self.add_widget(
            Button(text="Play !", font_name=self.FONT_MENU, font_size='80sp',
                   size_hint=(.45, .15), pos_hint={'x': .3, 'y': .4}, background_color=(0, 0, 0, 0),
                   on_press=self.switch_to_menu_level_screen)
        )

        self.add_widget(
            Button(text="Credits", font_name=self.FONT_MENU, font_size='40sp',
                   size_hint=(.25, .1), pos_hint={'x': 0.4, 'y': 0.2}, background_color=(0, 0, 0, 0))
        )

        self.add_widget(
            Button(text="Options", font_name=self.FONT_MENU, font_size='25sp',
                   size_hint=(0.15, 0.12), pos_hint={'x': 0.85, 'y': 0}, background_color=(0, 0, 0, 0))
        )

    def switch_to_menu_level_screen(self, *args):
        """
        Required method.
        """
        Logger.info("propagate MenuLevel")
        propagate_event('MenuLevel', self)


class MenuLevel(FloatLayout):
    FONT_MENU_LEVEL = './resources/menu/Eraser.ttf'

    def __init__(self, event_dispatcher, **kwargs):
        """
        Initialize button and textures of MenuLevel.
        :param event_dispatcher:
        :param kwargs: args of layout
        :rtype: void
        """
        super(MenuLevel, self).__init__(**kwargs)
        self.event_dispatcher = event_dispatcher
        self.level_service = LevelService()
        self.level_manager = LevelManager()

        # Add fond.
        self.canvas.add(
            Rectangle(source='./resources/menu/test_im7.jpeg', size=Window.size)
        )

        # Add button
        self.add_widget(
            Button(text="Back to Menu", font_name=self.FONT_MENU_LEVEL, background_color=(0.8, 0, 0, 0.85),
                   pos_hint={'x': 0.82, 'y': 0}, size_hint=(0.18, 0.15),
                   on_press=self.switch_to_menu_screen)
        )

        menu_level_grid = GridLayout(size_hint=(0.7, 0.45), pos_hint={'x': 0.15, 'y': 0.3}, row=2)
        self.add_widget(menu_level_grid)

        set_list = os.listdir('./resources/maps/')
        set_number = len(set_list)
        menu_level_grid.cols = set_number / 2

        for index in range(1,set_number+1):
            if index % 2 == 0:
                button_title = "Level " + str(index)
                menu_level_grid.add_widget(
                    Button(text=button_title, font_name=self.FONT_MENU_LEVEL,
                           background_color=(0.1, 0, 0, 0.85), on_press=self.launch_level, cls=[index])
                )

            else:
                button_title = "Level " + str(index)
                menu_level_grid.add_widget(
                    Button(text=button_title, font_name=self.FONT_MENU_LEVEL,
                           background_color=(0.8, 0, 0, 0.85), on_press=self.launch_level, cls=[index])
                )

    def switch_to_menu_screen(self, *args):
        """
        Required method.
        """
        Logger.info("propagate Menu")
        propagate_event('Menu', self)

    def launch_level(self, value):
        """
        Check if player can play this level and in case: load it.
        :param value:
        :rtype: void
        """
        level_id = str(value.cls[0]) + str(1)
        # la on recuperer un string avec set + level

        # maintenant je crois qu'il y a des bugs dans ton truc donc je te laisse enjoy tout ca c'est plus ma partie ^^
        # Sachant qu'il y a ces conditions a check et a retourner des message ducout surement dans le level manager mais en gros : Si le level n'existe pas, Si le set n'est pas unlock

        # il faut test le set pas le level, le mec recommence de zero son set si il deco pendant ce temps je pense
        self.level_manager.load_level(level_id)

        # si jamais l'event est bon il faut le propager
        propagate_event('LevelManager', self)


def propagate_event(value, current_class):
    """
    :param value: screen's name.
    :param current_class: Current active class.
    :rtype: void
    """
    current_class.event_dispatcher.dispatch('on_change_screen', value)
