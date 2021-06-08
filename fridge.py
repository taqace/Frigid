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
from kivy.properties import ObjectProperty,ListProperty,BooleanProperty,StringProperty

#test commit

global connection
connection = sqlite3.connect("database\kartik.db")


#1024x600
class MyScreenManager(ScreenManager):
    pass


class MainScreen(Screen):
    
    def test(self):
        print(self.ids.rv.ids.gg.text)

class BoxScreen(Screen):
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
            App.get_running_app().root.ids.mainScreen.ids.rv.selectable_button_function(self.text)
            print(self.text)
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)


    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

class RV(BoxLayout):

    cursor = connection.cursor()
    data_items = ListProperty([])
    search = StringProperty('testing')
    filterBy = "default"
    searchString = ""

    ggg = StringProperty("A")

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.get_submit()
    
    def get_submit(self,text = "SELECT DISTINCT box FROM employees",boxName=None):

        if boxName != None:
            self.data_items.clear()           
            search = self.cursor.execute("SELECT position FROM employees WHERE box=?",(boxName,))
            for i in search:
                self.data_items.append(boxName+"-"+i[0])

        else:
            self.cursor.execute(text)
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

    def selectable_button_function(self,box = "None"):
        
        if self.filterBy == 'default':
            self.filterBy = 'box'
            query = "SELECT position FROM employees WHERE box=?"
            self.get_submit(query,box)
        elif self.filterBy == 'box':
            App.get_running_app().root.current = 'boxScreen'
        elif self.filterBy == 'contents':
            self.get_submit("SELECT DISTINCT contents FROM employees")
        elif self.filterBy == 'contact':
            self.get_submit("SELECT DISTINCT contact FROM employees")
        
       

    def search_function(self,text):
        split = text.split()
        column_list = ["contents","contact","note1","note2"]
        param_dict = { "param_" + str(i) : "%" + split[i] + "%" for (i,v) in enumerate(split) }
        cross_list = [col + " LIKE :param_" + str(i) for i in range(len(split)) for col in column_list]
        sql = "SELECT box,position" + " FROM employees WHERE " + " OR ".join(cross_list)
        sqlSearch = self.cursor.execute(sql,param_dict)

        self.data_items.clear()

        for box in sqlSearch:
            self.data_items.append(box[0]+"-"+box[1])
        

        

presentation = Builder.load_file("frigid.kv")
class MyApp(App):

    def build(self):
        Window.size = (1024,600)
        return presentation

if __name__ == '__main__':
    MyApp().run()