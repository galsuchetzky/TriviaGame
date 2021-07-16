from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.base import runTouchApp

from os import listdir
from Strings import *

class SayHello(App):
    def build(self):
        self.window = GridLayout()
        #add widgets to window

        questionnaire_dropdown = DropDown()
        # Create choose question file label
        choose_questions_label = Label(text="choose subject")

        question_files = [file_name.replace('.json', '') for file_name in listdir(QUESTIONS_LOCATION) if
                          file_name.endswith('.json')]
        question_files = question_files if question_files else [[]]
        print(question_files)

        for file_name in question_files:
            btn = Button(text=file_name, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: questionnaire_dropdown.select(btn.text))
            questionnaire_dropdown.add_widget(btn)

        mainbutton = Button(text ="Select Questions File", pos =(350, 300))
        mainbutton.bind(on_release=questionnaire_dropdown.open)
        questionnaire_dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        self.window.add_widget(mainbutton)
        return self.window

if __name__ == "__main__":
    SayHello().run()