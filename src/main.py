from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.pickers.datepicker import DatePickerInputField
from db.db_manager import DBManager
import sqlite3
from src.util import utilities
from src.db.run_migrations import run_migrations


db_path = utilities.read_ini('DB', 'DB_PATH')


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DBManager(db_path)

        # init widgets
        self.layout = FloatLayout()
        self.add_button_widget = Button(text='+',
                                        size_hint=(.5, None),
                                        height=25,
                                        background_color="#55DD55",
                                        pos_hint={'x': .25, 'y': .9})

        self.task_box = GridLayout(padding=0,
                                   cols=1,
                                   size_hint=(0.5, 0.9),
                                   pos_hint={'x': 0.25, 'y': -0.03})
        self.build_task_list()

        self.add_button_widget.on_press = self.change_to_add_task_screen

        self.layout.add_widget(self.add_button_widget)
        self.layout.add_widget(self.task_box)

        self.add_widget(self.layout)

    def build_task_list(self):
        self.task_box.clear_widgets()
        task_list = self.db.select_tasks()

        for task in task_list:
            new_label = Label(text=task[1] + '(' + str(task[2]) + ')',
                              size_hint=(.5, None),
                              height=30,
                              color='#000000')

            self.task_box.add_widget(new_label)

    # Actions:
    def change_to_add_task_screen(self):
        self.manager.current = 'add'


class AddScreen(Screen):
    def __init__(self, custom_refresh_callback, **kw):
        super().__init__(**kw)
        self.db = DBManager(db_path)

        self.refresh_callback = custom_refresh_callback

        form_layout = GridLayout(cols=1)

        self.text_input = TextInput()
        form_layout.add_widget(self.text_input)
        self.due_date_input = TextInput()  # DatePickerInputField()
        form_layout.add_widget(self.due_date_input)
        form_layout.add_widget(Button(text='Add', on_press=self.add_task_and_go_back_to_main))

        self.add_widget(form_layout)

    def add_task_and_go_back_to_main(self, event):
        self.db.insert_task((self.text_input.text, self.due_date_input.text))
        self.refresh_callback()
        self.manager.current = 'main'


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sm = ScreenManager()
        self.main_screen = MainScreen(name='main')
        self.add_screen = AddScreen(name='add', custom_refresh_callback=self.main_screen.build_task_list)

    def build(self):
        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(self.add_screen)

        return self.sm


if __name__ == '__main__':
    run_migrations()

    app = MainApp()
    app.run()
