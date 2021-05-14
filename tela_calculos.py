from kivy.app import App
from kivy.core import text

from kivy.lang import Builder
from kivy.metrics import sp
from kivy.uix.gridlayout import GridLayout

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from kivy.graphics import Color, Rectangle

from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class TelaCalulos(Screen):
    def __init__(self, **kw):
        """
        exemplo de dicionario: {
            "Reativa": [
                lista_nomes, lista_keys, lista_valores_padrao
            ]
        }
        """
        super().__init__(**kw)
        ativa = [
            ["A0 (sjksjakjsksj)", "A1 (jsksjksajk)", "A2 (ssss)"],
            "a0 a1 a2".split(),
            "0 0.22 0.78".split()
            ]
        reativa = [
            ["B0 (sjksjakjsksj)", "B1 (jsksjksajk)", "B2 (ssss)"],
            "b0 b1 b2".split(),
            "1 0 0".split()
            ]
        constantes = [
            ["Máximo de interações", "Fator de sensibilidade (kp)"],
            ["max_iter", "kp"],
            ["50", "0.9"]
        ]
        dicionario = {
            "CONSTANTES": constantes,
            "PARTE ATIVA": ativa,
            "PARTE REATIVA": reativa
        }
        self.size = Window.size
        self.dic = dicionario
        self.fonte = sp(18)

        self.inserir_scroll()
        self.inserir_botoes(["Calcular", "Voltar"], ["calcular", "voltar"])

    def inserir_scroll(self):
        padding = [f"{i}sp" for i in [50, 20, 50, 50]]
        spacing = "0sp"
        grid = GridLayout(cols=1, size_hint_y=None, padding=padding)
        grid.bind(minimum_height=grid.setter("height"))

        label = Label(
                    text="Insira os valores das constantes".title(), 
                    size_hint_y=None, 
                    height=self.height*.05, 
                    font_size=self.fonte * 1.5)

        label.text_size = self.width * .9, label.height * 1.5
        label.valign = "middle"
        label.halign = "center"
        grid.add_widget(label)

        for campo, listas in self.dic.items():
            label = Label(text=campo, size_hint_y=None, height=self.height*.05, font_size=self.fonte)
            label.text_size = self.width * .45, label.height * .9
            label.valign = "middle"
            label.halign = "center"
            grid.add_widget(label)

            for texto, key, padrao in zip(*listas):
                label = Label(text=texto, size_hint_y=None, height=self.height*.05, font_size=self.fonte)
                label.text_size = self.width * .45, label.height * .9
                label.valign = label.halign = "center"
                
                inp = TextInput(
                            text=padrao,
                            size_hint_y=None, 
                            height=self.height*.06, 
                            border=[4] * 4, 
                            font_size=self.fonte,
                            input_filter="float")
                padding = [f"{i}sp" for i in [10, 30, 10, 50]]
                box = BoxLayout(orientation="horizontal", size_hint_y=None, padding=padding)
                box.add_widget(label)
                box.add_widget(inp)
                grid.add_widget(box)

                self.ids.update({f"input_{key}": inp})
                

        scroll = ScrollView(size_hint_y=None)
        scroll.width = self.width * .9
        scroll.height = self.height * .95
        scroll.add_widget(grid)
        self.add_widget(scroll)

        self.grid = grid
        
    def inserir_botoes(self, nomes: list, ids: list) -> BoxLayout:
        box = GridLayout(cols=1, padding=[f"{i}sp" for i in (100, 15, 100, 15)], spacing="10sp")
        box.size_hint_y = None
        box.height = Window.height * .2

        for nome, id in zip(nomes, ids):
            bnt = Button(text=nome, font_size=self.fonte)
            box.add_widget(bnt)
            self.ids.update({f"bnt_{id}": bnt})

        self.grid.add_widget(box)
