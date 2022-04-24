from kivy.uix.screenmanager import Screen

class ManagePage(Screen):
    labors = 0
    mines = 0
    
    def update(self):
        self.ids["_mines"].text = str(format(self.mines,  ","))
        self.ids["_labors"].text = str(format(self.labors,  ","))
        
    def print_me(self):
        print(self.parent.parent.parent)
