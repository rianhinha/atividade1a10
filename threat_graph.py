from kivy.uix.widget import Widget
from kivy.graphics import Color, Line

class ThreatGraph(Widget):
    def update_plot(self, data):
        self.canvas.clear()
        if not data:
            return

        with self.canvas:
            Color(1, 0, 0)
            points = []
            w, h = self.width, self.height
            step_x = w / max(1, len(data) - 1)
            for i, value in enumerate(data):
                x = i * step_x
                y = h * value / 100
                points.extend([x, y])
            Line(points=points, width=2)