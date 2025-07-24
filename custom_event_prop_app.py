from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.event import EventDispatcher

class MyCustomWidget(BoxLayout, EventDispatcher):  # Herda de ambos
    __events__ = ('on_message_changed',)
    message = StringProperty('Mensagem inicial')
    
    def on_message(self, instance, value):
        self.dispatch('on_message_changed', value)

class CustomEventPropApp(App):
    def build(self):
        return MyCustomWidget()

if __name__ == '__main__':
    CustomEventPropApp().run()