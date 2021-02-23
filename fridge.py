import kivy
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.widget import Widget
kivy.require('2.0.0') # replace with your current kivy version !
import sqlite3

from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.properties import ListProperty,BooleanProperty



global connection
connection = sqlite3.connect("database\kartik.db")



#1024x600
class MyScreenManager(ScreenManager):
    pass

class MainScreen(Screen):
    pass

class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''

class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

    def update_changes(self, txt):
        self.text = txt

class RV(BoxLayout):

    cursor = connection.cursor()
    data_items = ListProperty([])
    sqlString = "SELECT DISTINCT box FROM employees"

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.get_submit()

    def get_submit(self):
        self.cursor.execute(self.sqlString)
        rows = self.cursor.fetchall()
        self.create_data_items(rows)

    # create data_items
    def create_data_items(self,rows):

        if not self.data_items:
            for row in rows:
                for col in row:
                    self.data_items.append(col)
        else:
            self.data_items.clear()
            for row in rows:
                for col in row:
                    self.data_items.append(col)

    def selectable_button_function(self):
        
        print('a')

       

presentation = Builder.load_file("frigid.kv")
class MyApp(App):

    def build(self):
        Window.size = (1024,600)
        return presentation

if __name__ == '__main__':
    MyApp().run()