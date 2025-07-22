from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty

class ToggleStateWidget(BoxLayout):
    is_active = BooleanProperty(False)

    def on_toggle_state(self, instance, state):
        self.is_active = (state == 'down')

class BoolPropApp(App):
    def build(self):
        return ToggleStateWidget()

if __name__ == '__main__':
    BoolPropApp().run()
