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
        
    

class CalculoScreen(Screen):
    def __init__(self, *args, **kw):
        super(CalculoScreen, self).__init__(*args, **kw)
        self._font_size = sp(20)
        self.layout = BoxLayout(spacing=10, size_hint_y=None, orientation="vertical")
        self.layout.bind(minimum_height=self.layout.setter('height'))
        #self.layout.add_widget(self.criar_parte_ativa())
        #self.layout.add_widget(self.criar_parte_reativa())
        ativa = [
            "PARTE ATIVA",
            ["A0 (sjksjakjsksj)", "A1 (jsksjksajk)", "A2 (ssss)"],
            "a0 a1 a2".split(),
            "0 0.22 0.78".split()
            ]
        reativa = [
            "PARTE REATIVA",
            ["B0 (sjksjakjsksj)", "B1 (jsksjksajk)", "B2 (ssss)"],
            "b0 b1 b2".split(),
            "1 0 0".split()
            ]
        self.layout.add_widget(self.criar_campo(*ativa))
        self.layout.add_widget(self.criar_campo(*reativa))


        scroll = ScrollView(size_hint_y=None, height=Window.height)
        #scroll.add_widget(self.layout)
        box = BoxLayout(spacing=10, size_hint_y=None, orientation="vertical")
        box.bind(minimum_height=self.layout.setter('height'))
        box.add_widget(scroll)
        self.add_widget(self.layout)

        self.layout.add_widget(self.criar_botoes(["Calcular", "Voltar"], ["calcular", "voltar"]))

    def criar_botoes(self, nomes: list, ids: list) -> BoxLayout:
        box = GridLayout(cols=1, padding=[f"{i}sp" for i in (100, 15, 100, 15)], spacing="10sp")
        box.size_hint_y = None
        box.height = Window.height * .2

        for nome, id in zip(nomes, ids):
            bnt = Button(text=nome, font_size=self._font_size)
            box.add_widget(bnt)
            self.ids.update({f"bnt_{id}": bnt})

        return box

    def criar_campo(self, nome: str, nomes_labels: list, nomes_campos: list, valores_campos: list) -> BoxLayout:
        box = BoxLayout(
                orientation="vertical", 
                padding=[f"{i}sp" for i in (20, 10, 20, 10)], 
                spacing="10sp")

        box.orientation = "vertical"
        label = Label(
                text=nome,
                size_hint_y=None,
                height=Window.size[1] * .1)
        label.text_size = (Window.width, Window.height * .1)
        label.halign = "center"
        label.valign = "middle"

        label.font_size = "20sp"
        box.add_widget(label)
        padding=[f"{i}sp" for i in (10, 0, 20, 0)]

        for nome, campo, valores in zip(nomes_labels, nomes_campos, valores_campos):
            b = BoxLayout(orientation="horizontal", spacing="10sp", padding=padding)
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


    def criar_parte_ativa(self):
        box = BoxLayout(
                orientation="vertical", 
                padding=[f"{i}sp" for i in (20, 10, 20, 10)], 
                spacing="10sp")

        box.orientation = "vertical"
        label = Label(
                text="PARTE ATIVA",
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
            b = BoxLayout(orientation="horizontal", spacing="10sp", padding=[f"{i}sp" for i in (10, 15, 20, 15)])
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
        box = BoxLayout(
                orientation="vertical", 
                padding=[f"{i}sp" for i in (20, 0, 20, 20)], 
                spacing="10sp")

        box.orientation = "vertical"
        label = Label(
                text="PARTE REATIVA",
                size_hint_y=None,
                height=Window.size[1] * .1)
        label.text_size = (Window.width, Window.height * .1)
        label.halign = "center"
        label.valign = "middle"

        label.font_size = "20sp"
        box.add_widget(label)

        nomes_labels = [
                "B0 (sjksjakjsksj)",
                "B1 (jsksjksajk)",
                "B2 (ssss)"]
        nomes_campos = "b0 b1 b2".split()
        valores_campos = "1, 0, 0".split()

        for nome, campo, valores in zip(nomes_labels, nomes_campos, valores_campos):
            b = BoxLayout(orientation="horizontal", spacing="10sp", padding=[f"{i}sp" for i in (10, 15, 20, 15)])
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