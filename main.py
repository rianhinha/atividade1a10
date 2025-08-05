import json
import threading
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

class IAController(BoxLayout):
    status = StringProperty("Online")
    threat_level = NumericProperty(20)
    log_entries = ListProperty([])
    graph_data = ListProperty([])
    sound = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_state()
        self.update_graph_data()
        Clock.schedule_interval(self.update_graph_data, 5)

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self.log_entries.append(entry)
        self.ids.log_label.text = "\n".join(self.log_entries[-50:])

    def update_graph_data(self, *args):
        self.graph_data.append(self.threat_level)
        if len(self.graph_data) > 20:
            self.graph_data.pop(0)
        self.ids.threat_graph.update_plot(self.graph_data)

    def send_command(self, command):
        self.log(f"Comando recebido: {command}")

        def process():
            if command == "injetar_virus":
                self.status = "Sob ataque!"
                self.threat_level += 20
                self.log("IA: Vírus detectado e isolado.")
            elif command == "desligar_sistemas":
                self.status = "Desligando..."
                self.threat_level += 10
                self.log("IA: Sistemas auxiliares offline.")
            elif command == "acessar_dados":
                self.status = "Acessando dados..."
                self.threat_level += 5
                self.log("IA: Dados acessados com sucesso.")
            else:
                self.status = "Comando desconhecido"
                self.log("IA: Comando não reconhecido.")
            
            if self.threat_level >= 80:
                self.trigger_alert()

            Clock.schedule_once(lambda dt: self.save_state())

        threading.Thread(target=process).start()

    def trigger_alert(self):
        self.log("ALERTA: Nível de ameaça crítico!")
        if not self.sound:
            self.sound = SoundLoader.load("assets/sounds/alert.wav")
        if self.sound:
            self.sound.play()

    def save_state(self):
        state = {
            "status": self.status,
            "threat_level": self.threat_level
        }
        with open("data.json", "w") as f:
            json.dump(state, f)

    def load_state(self):
        try:
            with open("data.json", "r") as f:
                state = json.load(f)
                self.status = state.get("status", "Online")
                self.threat_level = state.get("threat_level", 20)
        except FileNotFoundError:
            self.status = "Online"
            self.threat_level = 20

class IAApp(App):
    def build(self):
        return IAController()

if __name__ == "__main__":
    IAApp().run()