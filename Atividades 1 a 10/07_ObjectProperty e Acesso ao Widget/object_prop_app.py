from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

class ControleWidget(BoxLayout):
    target_label = ObjectProperty(None)

    def mudar_texto_alvo(self):
        if self.target_label:
            self.target_label.text = "Texto Mudado!"

class ObjectPropApp(App):
    def build(self):
        return ControleWidget()

if __name__ == '__main__':
    ObjectPropApp().run()
