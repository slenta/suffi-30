# Natürliche Bewegungen mit Pygame

Bei all meinen bisherigen Experimenten mit der Spieleprogrammierung habe ich die Akteure immer ganz naiv mit gleichbleibender Geschwindigkeit sich durch die Spielewelten bewegen lassen. Das heißt: Pfeiltaste links → x Pixel nach links; Pfeiltaste rechts → x Pixel nach rechts, etc. Für die meisten einfachen Spiele reicht dies aus, aber genaugenommen ist dies eine unnatürliche Bewegung, denn wie wir spätestens seit [Isaac Newton](https://de.wikipedia.org/wiki/Newtonsche_Gesetze) wissen, beschleunigt kein Körper sofort von Null auf 100 oder bremst sofort auf Null ab. Sondern die neue Position eines Körpers ist eine (vektorielle) Addition von Geschwindigkeit und Beschleunigung (*velocity* und *acceleration*). Und dann spielen auch noch Reibung und Widerstand (*friction*) eine Rolle, die dafür sorgen, daß die Geschwindigkeit des Körpers nicht ins Unendliche steigt. Und selbst da, wo es weder Reibung noch Widerstand gibt – also zum Beispiel in den unendlichen Welten des *Star-Trek-Universums* – deckelt eine Maximalgeschwindigkeit (außerhalb des *Star-Trek-Universums* ist das spätestens die Lichtgeschwindigkeit) unseren Beschleunigungswahn. Also gelten folgende physikalischen Gesetzmäßigkeiten (als Pseudo-Python-Code):

~~~python
acc(n) = acc(n-1) + vel(n-1)*friction
vel(n) = acc(n)
pos(n) = pos(n-1) + vel(n)
~~~

Um zu zeigen, wie dies funktioniert, habe ich ein kleines Pygame-Programm geschrieben, das dies demonstriert. Es setzt auf mein kleines, hier vorgestelltes Pygame-Template auf, das nahezu unverändert bleibt. Die ganze Action habe ich in einer Klasse `Player()` untergebracht, die in der Datei `sprites.py`wohnt:

~~~python
# Sprite Klassen
import pygame as pg
from settings import Settings
vec = pg.math.Vector2

s = Settings()

class Player(pg.sprite.Sprite):
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((32, 32))
        self.image.fill(s.YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (s.WIDTH/2, s.HEIGHT/2)
        self.pos =vec(s.WIDTH/2, s.HEIGHT/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
    
    
    def update(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -s.PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = s.PLAYER_ACC
        # Bewegungsgleichungen nach Newton
        self.acc.x += self.vel.x*s.PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel
        
        # Randbehandlung
        if self.pos.x >= s.WIDTH - s.TILESIZE/2:
            self.pos.x = s.WIDTH - s.TILESIZE/2
        if self.pos.x <= s.TILESIZE/2:
            self.pos.x = s.TILESIZE/2

        self.rect.center = self.pos
~~~

Pygame besitzt dankenswerterweise eine Klasse `Vector2` für zweidimensionale Vektoren, so daß ich nciht auf meine eigene Python-Implementierung `PVector`zurückgreifen muß. Neben `pygame`und `settings` habe ich diese im Kopf der Datei importiert. Alles weitere habe ich in eine Klasse `Player()`gepackt, die von `pygame.sprite.Sprite`erbt. Diese Pygame-Sprite-Klasse ist extrem mächtig und einer der Hauptgründe, warum ich die Spieleprogrammierung mit Pygame so faszinierend finde.

Der »Spieler« sollte möglichst einfach sein, also habe ich ihn als ein gelbes Quadrat implementiert, das zu Beginn in die Mitte des Bildschirms positioniert wird. Dieser Vektor ist seine Startposition, Geschwindigkeit und Beschleunigung sind ebenfalls Vektoren, die zum Start jeweils mit *(0, 0)* initialisiert werden.

Die eigentliche Berechnung findet in der Methode `update()` statt: Abhängig davon, ob die linke oder die rechte Pfeiltaste gedrückt ist die Beschleunigung (eine Konstante aus der Klasse `Settings()` entweder positiv oder negativ.

Und in den nächsten Zeilen wird dann das berechnet, was ich im obigen Pseudocode aufgeschrieben hatte:

~~~python
        self.acc.x += self.vel.x*s.PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel
~~~

Da ich nicht wollte, daß der Spieler über den Bildschirmrand hinausschießt, lasse ich ihn in den folgenden Zeilen

~~~python
        if self.pos.x >= s.WIDTH - s.TILESIZE/2:
            self.pos.x = s.WIDTH - s.TILESIZE/2
        if self.pos.x <= s.TILESIZE/2:
            self.pos.x = s.TILESIZE/2
~~~

brutal an den Bildschirmrändern rechts und links abbremsen. Das geht bestimmt auch schöner zum Beispiel mit einer Berechnung des Bresmweges, aber ich hatte es implementiert und es war kaum ein Unterschied zur obigen Impelmentierung festzustellen. Daraufhin hatte ich beschlossen, die ressourcenfressende Berechnung des Bremsweges wieder fallen zu lassen.

Das ich mit der Zeile

~~~python
        self.rect.center = self.pos
~~~

Pygame erst nach Abschluß aller Berechnungen die Position des Players mitteile, liegt daran, daß ich Rundungsfehelr möglichst vermeiden wollte. Position, Beschleunigung und Geschwindigkeit sind Fließkommazahlen, die Position des Spielers im Bildschirmfenster sind aber ganzzahlige x- und y-Werte. Pygame schneidet da die Nachkommazahlen gnadenlos ab, würde ich also statt mit `pos` direkt mit `rect`-Werten arbeiten, sind Rundungsfehler von vorneherein mit vorprogrammiert.

Am Hauptprogramm hat sich gegenüber dem Template kaum etwas verändert. Natürlich muß der Spieler aus `sprite`importiert werden und in der `World`-Methode `new()` auch instantiiert und zur Gruppe `all_sprites` hinzugefügt werden. Aber sie sollte Euch bekannt vorkommen:

~~~python
import pygame as pg
from settings import Settings
from sprites import Player
import random
import os

class World:
    
    def __init__ (self):
        # Initialisiert die Spielewelt
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((s.WIDTH, s.HEIGHT))
        pg.display.set_caption(s.TITLE)
        self.clock = pg.time.Clock()
        self.keep_going = True
    
    def new(self):
        # Initializes and Resets the Game
        self.all_sprites = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.run()
        
    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(s.FPS)
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        # Game-Loop Update
        self.all_sprites.update()

    def events(self):
        # Game-Loop Events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if self.playing:
                    self.playing = False
                self.keep_going = False

    def draw(self):
        # Game-Loop Draw 
        self.screen.fill(s.BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def splash_screen(self):
        # Start-Screen
        pass

    def game_over(self):
        pass

s = Settings()
w = World()
w.splash_screen()
while w.keep_going:
    w.new()
    w.game_over()
    
pg.quit()
~~~

In der Klasse `Sttings()` habe ich den Titel angepaßt und die Eigenschaften des Spielers hinzugefügt:

~~~python
        # Player Eigenschaften
        self.PLAYER_ACC = 0.8
        self.PLAYER_FRICTION = -0.12
~~~

In einer virtuellen Spielewelt haben diese Werte keine reale Entsprechung – ich habe sie einfach esperimentell herausgefunden. Für die Akten: Die vollständige Datei `settings.py` sieht jetzt so aus:

~~~python
# Konstanten und Einstellungen für das Spiel
import pygame as pg

class Settings():
    
    def __init__(self):

        # Einige nützliche Konstanten
        self.TITLE = "Motion Demo 🚀"
        self.WIDTH = 640
        self.HEIGHT = 480
        self.FPS = 60   # Framerate
        self.TILESIZE = 32
        
        # Player Eigenschaften
        self.PLAYER_ACC = 0.8
        self.PLAYER_FRICTION = -0.12

        # Nützliche Farbdefinitionen 
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.GREY = (160, 160, 160)
~~~

Wenn Ihr das Progrämmchen ablaufen laßt, werdet Ihr feststellen, daß die Bewegungen des geleben Quarates nun viel natürlicher anmuten. Beim Richtungswechsel schießt es ein wenig über das Ziel hinaus und bremst ab, bevor die Richtung tatsächlich geändert und langsam wieder auf die Maximalgeschwindigkeit beschleunigt wird.

Ich habe schon eine Idee, wie man dies in einem oder zwei Beispielspielen ausnutzen kann. Außerdem überlege ich ernsthaft, diesen Algorithmus auch in Processing.py zu implementieren. Wartet also weitere Beispiele hier im <del>Blog</del> Kritzelheft ab. *Still digging!*