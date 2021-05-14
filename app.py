from kivy.app import App

from kivy.lang import Builder
from kivy.metrics import sp

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from kivy.core.window import Window
from kivy.utils import get_color_from_hex




Builder.load_file("app.kv")

class HomeScreen(Screen):
    pass

class CalculoScreen(Screen):
    def __init__(self, *args, **kw):
        super(CalculoScreen, self).__init__(*args, **kw)
        self._font_size = sp(20)
        self.layout = BoxLayout(spacing=10, size_hint_y=None, orientation="vertical")
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.layout.add_widget(self.criar_parte_ativa())
        self.layout.add_widget(self.criar_parte_reativa())

        scroll = ScrollView(size_hint_y=None, height=Window.height)
        scroll.add_widget(self.layout)
        box = BoxLayout(spacing=10, size_hint_y=None, orientation="vertical")
        box.bind(minimum_height=self.layout.setter('height'))
        box.add_widget(scroll)
        self.add_widget(box)



    def criar_parte_ativa(self):
        box = BoxLayout(
                orientation="vertical", 
                padding=[f"{i}sp" for i in (20, 10, 20, 10)], 
                spacing="10sp")

        box.orientation = "vertical"
        label = Label(
                text="Parte Ativa",
                size_hint_y=None,
                height=Window.size[1] * .1)
        label.text_size = (Window.width, Window.height * .1)
        label.halign = "center"
        label.valign = "middle"

        label.font_size = "20sp"
        box.add_widget(label)

        nomes_labels = [
                "A0 (sjksjakjsksj)",
                "A1 (jsksjksajk)",
                "A2 (ssss)"]
        nomes_campos = "a0 a1 a2".split()
        valores_campos = "0 0.22 0.78".split()

        for nome, campo, valores in zip(nomes_labels, nomes_campos, valores_campos):
            b = BoxLayout(orientation="horizontal", spacing="10sp")
            label = Label(
                        text=nome, 
                        font_size=self._font_size,)

            input = TextInput(
                        text=valores,
                        font_size=self._font_size,
                        multiline=False,
                        input_filter="float")
            #input.input_filter = "float"
            #input.bind(text=self._processa_input)

            b.add_widget(label)
            b.add_widget(input)
            box.add_widget(b)
            self.ids.update({f"input_{campo}": input})

        return box

    def criar_parte_reativa(self):
        box = BoxLayout()
        box.orientation = "vertical"
        label = Label(text="Parte Reativa")
        label.font_size = "20sp"
        box.add_widget(label)

        nomes_labels = [
                "B0 (sjksjakjsksj)",
                "B1 (jsksjksajk)",
                "B2 (ssss)"]
        nomes_campos = "b0 b1 b2".split()

        for nome, campo in zip(nomes_labels, nomes_campos):
            b = BoxLayout(orientation="horizontal", spacing="10sp")
            label = Label(
                        text=nome, 
                        font_size=self._font_size, 
                        height=self._font_size * 1.5, 
                        size_hint_y=None)

            input = TextInput(text=campo, font_size=self._font_size)
            
            b.add_widget(label)
            b.add_widget(input)
            box.add_widget(b)

        return box
    
    @staticmethod
    def _processa_input(instance, value):
        print("instancia: ", instance, "value", value)

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
    from kivy.config import Config
    from kivy.core.text import LabelBase

    # print("meio", get_color_from_hex("6b7c85"))
    # print("laranja", get_color_from_hex("fCB001"))

    LabelBase.register(name="Roboto",
                       fn_regular="./fontes/Roboto-Thin.ttf",
                       fn_bold="./fontes/Roboto-Medium.ttf")

    altura = 650
    largura = 800

    Config.set("graphics", "width", largura)
    Config.set("graphics", "height", altura)
    Config.set("input", "mouse", "mouse,disable_multitouch")
    Config.set("graphics", "resizable", False)

    from kivy.core.window import Window

    Window.size = (largura, altura)

    Window.clearcolor = get_color_from_hex("4C6B8A")
    Window.clearcolor = get_color_from_hex("1ABC9C")
    #Window.clearcolor = get_color_from_hex("#22A178")
    #Window.clearcolor = get_color_from_hex("#040348")

    print(altura, largura)
    TccApp().run()