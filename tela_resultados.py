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

class TelaResultados(Screen):
    def __init__(self, **kw):
        """
        exemplo de dicionario: {
            "Reativa": [
                lista_nomes, lista_keys, lista_valores_padrao
            ]
        }
        """
        super().__init__(**kw)
        self.size = Window.size
        self.fonte = sp(18)
        print(self.ids)

    def carrega_imagens(self):
        frequencia = self.ids.frequencia
        frequencia.source = "./.salvos/saida/f.png"

        v = self.ids.v
        v.source = "./.salvos/saida/Vbus_t.png"

        p = self.ids.p
        p.source = "./.salvos/saida/Sbr_t.png"
        
    