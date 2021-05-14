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

from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

from tela_calculos import TelaCalulos
from tela_resultados import TelaResultados

from multiprocessing import Process
import json, os

Builder.load_file("app.kv")

class HomeScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        
    
class TccApp(App):
    title = "Soma de Potencias"

    def build(self):
        manager = ScreenManager()
        manager.add_widget(HomeScreen(name="home"))
        
        return manager

    def on_start(self):

        if not os.path.isdir("./.salvos/"):
            os.mkdir("./.salvos/")

        #self.root.ids.botoes_home.height = Window.height * .2

        calculo = TelaCalulos(name="calculo")
        self.root.add_widget(calculo)

        self.root.ids.update(calculo.ids)

        calculo.ids["bnt_voltar"].bind(on_release=self.vai_para_tela("home"))
        calculo.ids["bnt_calcular"].bind(on_release=self.botao_calcular)

        resultado = TelaResultados(name="resultado")
        self._carrega_imagens = resultado.carrega_imagens
        self.root.add_widget(resultado)

        resultado.ids["home"].bind(on_release=self.vai_para_tela("home"))
        
        self.process = Process()

    def vai_para_tela(self, nome):
        def dentro(*args, **kw):
            print("Passou aqui")
            self.root.current = nome
        return dentro

    def botao_calcular(self, *args):
        if self.process.is_alive():
            print("Ja esta calculando") #TODO logica para o caso de já esta calculando
        else:
            print("Iniciando o processo de calculo")
            self.gravar_dados_de_entrada()
            self._calculando = True
            self.process = Process(target=self._calculo, args=())
            self.process.start()
            Clock.schedule_interval(self.verifica_calculo_finalizado, .5)
            self._verifica = True

    def verifica_calculo_finalizado(self, *args):
        if not self.process.is_alive() and self.root.current == "calculo" and self._verifica:
            print("Calculo Realizado com sucesso ...", args)
            self.root.current = "resultado"
            self._carrega_imagens()
            self._verifica = False
            return 

        elif self.root.current == "calculo":
            print("Ainda nao ...")

    def _calculo(self, *args):
        print("Calculando ...")
        import rede_radial

    def gravar_dados_de_entrada(self):
        file_name = "./.salvos/entrada.json"
        
        dados = {}
        for key, value in self.root.ids.items():
            if "input" in key:
                key = key.replace("input_", "")
                dados[key] = float(value.text)

        with open(file_name, "w") as file:
            json.dump(dados, file)



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

    Window.clearcolor = get_color_from_hex("4C6B8A")
    #Window.clearcolor = get_color_from_hex("1ABC9C")
    #Window.clearcolor = get_color_from_hex("#22A178")
    Window.clearcolor = get_color_from_hex("#040348")

    print(altura, largura)
    TccApp().run()