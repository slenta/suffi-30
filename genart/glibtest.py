from random import *
from Glib import *


startdraw(400, 400)
for i in range(0,50):
  fill (randint(0,256),randint(0,256),randint(0, 256), 60)
  siz = randint(5, 40)
  ellipse (randint(0, width), randint(0, width), siz, siz)
enddraw()
