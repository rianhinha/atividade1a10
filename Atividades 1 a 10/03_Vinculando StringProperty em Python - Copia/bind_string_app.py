from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty

class StatusWidget(BoxLayout):
    status_message = StringProperty("Offline")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.label = Label()
        self.button = Button(text="Alternar Status")
        self.button.bind(on_release=self.mudar_status)

        # Adiciona o Label e o Button ao layout
        self.add_widget(self.label)
        self.add_widget(self.button)

        # Vincula a StringProperty à atualização do Label
        self.bind(status_message=self.update_label_text)

        # Atualiza o texto do Label inicialmente
        self.update_label_text(self, self.status_message)

    def update_label_text(self, instance, value):
        self.label.text = f"Status: {value}"

    def mudar_status(self, instance):
        self.status_message = "Online" if self.status_message == "Offline" else "Offline"

class BindStringApp(App):
    def build(self):
        return StatusWidget()

if __name__ == '__main__':
    BindStringApp().run()