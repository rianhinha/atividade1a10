from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class MyContainer(BoxLayout):
    pass

class KvBindApp(App):
    def build(self):
        return MyContainer()

if __name__ == '__main__':
    KvBindApp().run()
