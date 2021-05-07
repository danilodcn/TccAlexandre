from kivy.app import App

from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file("app.kv")

class HomeScreen(Screen):
    pass

class TccApp(App):
    title = "Soma de Potencias"

    def build(self):
        manager = ScreenManager()
        manager.add_widget(HomeScreen(name="home"))
        return manager
        

if __name__ == "__main__":
    TccApp().run()