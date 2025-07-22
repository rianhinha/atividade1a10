from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class MyWidget(BoxLayout):
    # Propriedade do tipo String
    saudacao = StringProperty("Olá, Kivy!")

class StringPropApp(App):
    def build(self):
        return MyWidget()

if __name__ == '__main__':
    StringPropApp().run()
