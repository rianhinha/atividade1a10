from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class InputWidget(BoxLayout):
    def confirmar(self):
        self.ids.label_resultado.text = self.ids.meu_input_texto.text

class InputPropApp(App):
    def build(self):
        return InputWidget()

if __name__ == '__main__':
    InputPropApp().run()
