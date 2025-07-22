from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

class PongBall(Widget):
    # Velocidade da bola nos eixos x e y
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    
    # Propriedade de referência para velocity_x e velocity_y
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    # Função que move a bola de acordo com sua velocidade
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        
    # Função para quicar a bola nas raquetes
    def bounce_paddle(self, paddle):
        if self.collide_widget(paddle):
            vx, vy = self.velocity
            offset = (self.center_y - paddle.center_y) / (paddle.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1  # Aumenta um pouco a velocidade a cada rebatida
            self.velocity = vel.x, vel.y + offset

class PongPaddle(Widget):
    score = NumericProperty(0)  # Pontuação do jogador
    
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    score_label = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        
        # Variáveis para controle de movimento
        self.p1_up = False
        self.p1_down = False
        self.p2_up = False
        self.p2_down = False
        
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Controles do jogador 1 (W e S)
        if keycode[1] == 'w':
            self.p1_up = True
        elif keycode[1] == 's':
            self.p1_down = True
        # Controles do jogador 2 (seta para cima e para baixo)
        elif keycode[1] == 'up':
            self.p2_up = True
        elif keycode[1] == 'down':
            self.p2_down = True
        return True
        
    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[1] == 'w':
            self.p1_up = False
        elif keycode[1] == 's':
            self.p1_down = False
        elif keycode[1] == 'up':
            self.p2_up = False
        elif keycode[1] == 'down':
            self.p2_down = False
        return True
    
    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(45 if self.player1.score % 2 else -45)
        
    def update(self, dt):
        # Movimento dos jogadores
        paddle_speed = 10
        if self.p1_up and self.player1.top < self.top:
            self.player1.y += paddle_speed
        if self.p1_down and self.player1.y > self.y:
            self.player1.y -= paddle_speed
        if self.p2_up and self.player2.top < self.top:
            self.player2.y += paddle_speed
        if self.p2_down and self.player2.y > self.y:
            self.player2.y -= paddle_speed
            
        # Movimento da bola
        self.ball.move()
        
        # Colisão com as paredes superior e inferior
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1
            
        # Colisão com as raquetes
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        
        # Pontuação
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball()
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball()
            
        # Atualizar placar
        self.score_label.text = f"{self.player1.score} - {self.player2.score}"

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    from kivy.core.window import Window
    PongApp().run()