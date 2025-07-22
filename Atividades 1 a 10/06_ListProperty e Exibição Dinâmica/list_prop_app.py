from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty

class ListaItensWidget(BoxLayout):
    lista_de_compras = ListProperty(['Pão', 'Leite'])

    def adicionar_item(self, item):
        if item:
            self.lista_de_compras.append(item)

class ListPropApp(App):
    def build(self):
        return ListaItensWidget()

if __name__ == '__main__':
    ListPropApp().run()
