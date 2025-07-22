from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle, Ellipse
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.properties import ListProperty
from kivy.core.window import Window

class MyPaintWidget(Widget):
    current_draw_color = ListProperty([1, 0, 0, 1])  # Cor inicial: vermelho

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.line_width = 2
        self.shape = 'Line'
        self.start_pos = {}

    def on_touch_down(self, touch):
        with self.canvas:
            Color(*self.current_draw_color)
            if self.shape == 'Line':
                touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.line_width)
            elif self.shape == 'Rectangle':
                self.start_pos[touch] = (touch.x, touch.y)
                touch.ud['rect'] = Rectangle(pos=(touch.x, touch.y), size=(1, 1))
            elif self.shape == 'Ellipse':
                self.start_pos[touch] = (touch.x, touch.y)
                touch.ud['ellipse'] = Ellipse(pos=(touch.x, touch.y), size=(1, 1))

    def on_touch_move(self, touch):
        if self.shape == 'Line' and 'line' in touch.ud:
            touch.ud['line'].points += [touch.x, touch.y]
        elif self.shape in ['Rectangle', 'Ellipse'] and touch in self.start_pos:
            x0, y0 = self.start_pos[touch]
            width = touch.x - x0
            height = touch.y - y0
            size = (abs(width), abs(height))
            pos = (min(x0, touch.x), min(y0, touch.y))
            if self.shape == 'Rectangle':
                touch.ud['rect'].pos = pos
                touch.ud['rect'].size = size
            elif self.shape == 'Ellipse':
                touch.ud['ellipse'].pos = pos
                touch.ud['ellipse'].size = size

    def clear_canvas(self, instance):
        self.canvas.clear()

    def set_line_width(self, instance, value):
        self.line_width = value

    def set_shape(self, spinner, text):
        self.shape = text

    def set_draw_color(self, color_list):
        self.current_draw_color = color_list


class MyPaintApp(App):
    def build(self):
        root = FloatLayout()
        paint_widget = MyPaintWidget()
        root.add_widget(paint_widget)

        # Botões de cor
        btn_red = Button(text='Vermelho', size_hint=(0.15, 0.07), pos_hint={'x': 0.02, 'y': 0.8})
        btn_red.bind(on_release=lambda instance: paint_widget.set_draw_color([1, 0, 0, 1]))
        root.add_widget(btn_red)

        btn_green = Button(text='Verde', size_hint=(0.15, 0.07), pos_hint={'x': 0.20, 'y': 0.8})
        btn_green.bind(on_release=lambda instance: paint_widget.set_draw_color([0, 1, 0, 1]))
        root.add_widget(btn_green)

        btn_blue = Button(text='Azul', size_hint=(0.15, 0.07), pos_hint={'x': 0.38, 'y': 0.8})
        btn_blue.bind(on_release=lambda instance: paint_widget.set_draw_color([0, 0, 1, 1]))
        root.add_widget(btn_blue)

        # Botão Limpar
        btn_clear = Button(text='Limpar', size_hint=(0.15, 0.1), pos_hint={'x': 0.82, 'y': 0.88})
        btn_clear.bind(on_release=paint_widget.clear_canvas)
        root.add_widget(btn_clear)

        # Slider de Espessura
        slider = Slider(min=1, max=10, value=2, size_hint=(0.5, 0.05), pos_hint={'x': 0.02, 'y': 0.9})
        slider.bind(value=paint_widget.set_line_width)
        root.add_widget(slider)

        # Spinner de Forma
        spinner = Spinner(
            text='Line',
            values=('Line', 'Rectangle', 'Ellipse'),
            size_hint=(0.2, 0.07),
            pos_hint={'x': 0.55, 'y': 0.88}
        )
        spinner.bind(text=paint_widget.set_shape)
        root.add_widget(spinner)

        return root


if __name__ == '__main__':
    MyPaintApp().run()
