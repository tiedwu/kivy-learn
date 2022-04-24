from kivy.uix.screenmanager import ScreenManager
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from kivy.lang import Builder
#from kivy.utils import utils

Builder.load_file("layout.kv")
Builder.load_file("manage_page.kv")
Builder.load_file("building_page.kv")
Builder.load_file("military_page.kv")


class MainInfo(BoxLayout):
    pass

class MultiPage(ScreenManager):
    pass

class FuncMenu(BoxLayout):
    def switch_screen(self,  name):
        self.parent.ids["_multipage"].current = name

class RootWidget(BoxLayout):
    pass

    
class MyApp(App):
    def build(self):
        return RootWidget()
    
app = MyApp()
app.run()
