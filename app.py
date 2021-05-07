from kivy.app import App

from kivy.lang import Builder
from kivy.metrics import sp

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


Builder.load_file("app.kv")

class HomeScreen(Screen):
    pass

class CalculoScreen(Screen):
    def __init__(self, *args, **kw):
        super(CalculoScreen, self).__init__(*args, **kw)
        self._font_size = sp(20)
        self.add_widget(self.criar_parte_ativa())

    def criar_parte_ativa(self):
        box = BoxLayout()
        box.orientation = "vertical"
        label = Label(text="Parte Ativa")
        label.font_size = "20sp"
        box.add_widget(label)

        nomes_labels = [
                "A0 (sjksjakjsksj)",
                "A1 (jsksjksajk)",
                "A2 (ssss)"]
        nomes_campos = "a0 a1 a2".split()

        for nome, campo in zip(nomes_labels, nomes_campos):
            b = BoxLayout(orientation="horizontal", spacing="10sp")
            label = Label(text=nome, font_size=self._font_size)
            input = TextInput(text=campo, font_size=self._font_size)
            
            b.add_widget(label)
            b.add_widget(input)
            box.add_widget(b)

        return box
    

class TccApp(App):
    title = "Soma de Potencias"

    def build(self):
        manager = ScreenManager()
        manager.add_widget(HomeScreen(name="home"))
        manager.add_widget(CalculoScreen(name="calculo"))
        return manager

    def _clica_botao_home(self, *args):
        self.root.current = "calculo"



if __name__ == "__main__":
    TccApp().run()