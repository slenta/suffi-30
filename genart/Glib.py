import pygame
from pygame import *
import os
from Lib import inspect
from math import *
#from OpenGL.GL import *
#from OpenGL.GLU import *
#from OpenGL.GLUT import *
from random import *
from array import *
import colorsys
import numpy
import sounddevice as sd
import cv2 as _cv


class Gimage:
    def __init__(self):
        self.im = None  # Image
        self.pixels = None  # Pixels data
        self.w = 0
        self.h = 0

    def setIm(self, x):
        self.im = x
        z = x.get_size()
        self.w = z[0]
        self.h = z[1]

    def width(self):
        return self.w

    def height(self):
        return self.h

    def get(self, x, y, w=0, h=0):
        if h == 0:
            return self.im.get_at((x, y))
        else:
            n = createImage(w, h)
            n.im.blit(self.im, (0, 0), (x, y, w, h))
            return n

    def set(self, x, y, c):
        self.im.set_at((x, y), (c[0], c[1], c[2]))  # Old bug in pygame??

    def save(self, s):
        pygame.image.save(self.im, (s))

    def draw(self, canvas, x, y):
        canvas.blit(self.im, (x, y))

    def copy(self):
        g = Gimage()
        g.setIm(self.im.copy())
        return g

    def resize(self, ww, hh):
        if ww == 0 and hh == 0:
            return None
        if ww == 0:
            ww = int(self.w * hh / self.h)
        elif hh == 0:
            hh = int(self.h * ww / self.w)
        self.im = pygame.transform.scale(self.im, (ww, hh))
        self.w = ww
        self.h = hh


_loaded = False

# To-Do: 1. Symbolic names for special charaters (LEFT, etc)
# These are global variables that are used by the user
# or are phantoms
K_BACKSPACE = pygame.K_BACKSPACE
K_TAB = pygame.K_TAB
K_CLEAR = pygame.K_CLEAR
K_RETURN = pygame.K_RETURN
K_PAUSE = pygame.K_PAUSE
K_ESCAPE = pygame.K_ESCAPE
K_SPACE = pygame.K_SPACE
K_EXCLAIM = pygame.K_EXCLAIM
K_QUOTEDBL = pygame.K_QUOTEDBL
K_HASH = pygame.K_HASH
K_DOLLAR = pygame.K_DOLLAR
K_AMPERSAND = pygame.K_AMPERSAND
K_QUOTE = pygame.K_QUOTE
K_LEFTPAREN = pygame.K_LEFTPAREN
K_RIGHTPAREN = pygame.K_RIGHTPAREN
K_ASTERISK = pygame.K_ASTERISK
K_PLUS = pygame.K_PLUS
K_COMMA = pygame.K_COMMA
K_MINUS = pygame.K_MINUS
K_PERIOD = pygame.K_PERIOD
K_SLASH = pygame.K_SLASH
K_0 = pygame.K_0
K_1 = pygame.K_1
K_2 = pygame.K_2
K_3 = pygame.K_3
K_4 = pygame.K_4
K_5 = pygame.K_5
K_6 = pygame.K_6
K_7 = pygame.K_7
K_8 = pygame.K_8
K_9 = pygame.K_9
K_COLON = pygame.K_COLON
K_SEMICOLON = pygame.K_SEMICOLON
K_LESS = pygame.K_LESS
K_EQUALS = pygame.K_EQUALS
K_GREATER = pygame.K_GREATER
K_QUESTION = pygame.K_QUESTION
K_AT = pygame.K_AT
K_LEFTBRACKET = pygame.K_LEFTBRACKET
K_BACKSLASH = pygame.K_BACKSLASH
K_RIGHTBRACKET = pygame.K_RIGHTBRACKET
K_CARET = pygame.K_CARET
K_UNDERSCORE = pygame.K_UNDERSCORE
K_BACKQUOTE = pygame.K_BACKQUOTE
K_a = pygame.K_a
K_b = pygame.K_b
K_c = pygame.K_c
K_d = pygame.K_d
K_e = pygame.K_e
K_f = pygame.K_f
K_g = pygame.K_g
K_h = pygame.K_h
K_i = pygame.K_i
K_j = pygame.K_j
K_k = pygame.K_k
K_l = pygame.K_l
K_m = pygame.K_m
K_n = pygame.K_n
K_o = pygame.K_o
K_p = pygame.K_p
K_q = pygame.K_q
K_r = pygame.K_r
K_s = pygame.K_s
K_t = pygame.K_t
K_u = pygame.K_u
K_v = pygame.K_v
K_w = pygame.K_w
K_x = pygame.K_x
K_y = pygame.K_y
K_z = pygame.K_z
K_DELETE = pygame.K_DELETE
K_KP0 = pygame.K_KP0
K_KP1 = pygame.K_KP1
K_KP2 = pygame.K_KP2
K_KP3 = pygame.K_KP3
K_KP4 = pygame.K_KP4
K_KP5 = pygame.K_KP5
K_KP6 = pygame.K_KP6
K_KP7 = pygame.K_KP7
K_KP8 = pygame.K_KP8
K_KP9 = pygame.K_KP9
K_KP_PERIOD = pygame.K_KP_PERIOD
K_KP_DIVIDE = pygame.K_KP_DIVIDE
K_KP_MULTIPLY = pygame.K_KP_MULTIPLY
K_KP_MINUS = pygame.K_KP_MINUS
K_KP_PLUS = pygame.K_KP_PLUS
K_KP_ENTER = pygame.K_KP_ENTER
K_KP_EQUALS = pygame.K_KP_EQUALS
K_UP = pygame.K_UP
K_DOWN = pygame.K_DOWN
K_RIGHT = pygame.K_RIGHT
K_LEFT = pygame.K_LEFT
K_INSERT = pygame.K_INSERT
K_HOME = pygame.K_HOME
K_END = pygame.K_END
K_PAGEUP = pygame.K_PAGEUP
K_PAGEDOWN = pygame.K_PAGEDOWN
K_F1 = pygame.K_F1
K_F2 = pygame.K_F2
K_F3 = pygame.K_F3
K_F4 = pygame.K_F4
K_F5 = pygame.K_F5
K_F6 = pygame.K_F6
K_F7 = pygame.K_F7
K_F8 = pygame.K_F8
K_F9 = pygame.K_F9
K_F10 = pygame.K_F10
K_F11 = pygame.K_F11
K_F12 = pygame.K_F12
K_F13 = pygame.K_F13
K_F14 = pygame.K_F14
K_F15 = pygame.K_F15
K_NUMLOCK = pygame.K_NUMLOCK
K_CAPSLOCK = pygame.K_CAPSLOCK
K_SCROLLOCK = pygame.K_SCROLLOCK
K_RSHIFT = pygame.K_RSHIFT
K_LSHIFT = pygame.K_LSHIFT
K_RCTRL = pygame.K_RCTRL
K_LCTRL = pygame.K_LCTRL
K_RALT = pygame.K_RALT
K_LALT = pygame.K_LALT
K_RMETA = pygame.K_RMETA
K_LMETA = pygame.K_LMETA
K_LSUPER = pygame.K_LSUPER
K_RSUPER = pygame.K_RSUPER
K_MODE = pygame.K_MODE
K_HELP = pygame.K_HELP
K_PRINT = pygame.K_PRINT
K_SYSREQ = pygame.K_SYSREQ
K_BREAK = pygame.K_BREAK
K_MENU = pygame.K_MENU
K_POWER = pygame.K_POWER
K_EURO = pygame.K_EURO
K_A = 65
K_B = 66
K_C = 67
K_D = 68
K_E = 69
K_F = 70
K_G = 71
K_H = 72
K_I = 73
K_J = 74
K_K = 75
K_L = 76
K_M = 77
K_N = 78
K_O = 79
K_P = 80
K_Q = 81
K_R = 82
K_S = 83
K_T = 84
K_U = 85
K_V = 86
K_W = 87
K_X = 88
K_Y = 89
K_Z = 90
mousex = 9  # X position of the mouse right now
mousey = 10  # Y position of the mouse right now
_user = None
drawOK = False
_keyp = False
_keyr = False
_mousep = False
_mouser = False
_uppercase = False
_fvid = 0
_xvid = 0
_yvid = 0
_xwid = 0
_ywid = 0
_time = 0
_pausedv = False
savedFrame = None
width = 100  # Default canvas width
height = 100  # Default canvas height
_fillcol = (255, 255, 255, 255)  # Current fill color
_strokecol = (0, 0, 0, 255)  # Current stroke color
_bgcol = (200, 200, 200, 255)  # Current background color
_ELLIPSEMODE = 0  # Mode for drawing an ellipse
CENTER = 0  # 0 = center
RADIUS = 1  # 1 = radius
CORNER = 2  # 2 = corner
CORNERS = 3  # 3 = corners
_RECTMODE = CORNER  # Mode for drawing rectangles

_buttons = (False, False, False)  # Button presses.
key = ""  # Last key that was pressed
_noloop = False  # Does DRAW loop?
_dofill = True  # Should polygons be filled?
_dostroke = True  # Should polygons be outlined?
_linewidth = 1  # Line width in pixels
_framerate = 30
clock = pygame.time.Clock()
_hex = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
_font_family = "helvetica"
_font_size = 12
_font_weight = "normal"
_font_slant = "roman"
POLY_LINE = 1
POLY_FILL = 0
POLY_POINT = 2
camera = None  # For videoCapture
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BACKSPACE = K_BACKSPACE
PIESLICE = "pieslice"
font = None
canvas = 0
renderer = 1  # 3d
frequencies = []
_sample_rate = 22050
_bits = 16
_buf = None
_playing = False


def map(x, x0, x1, y0, y1):
    t0 = (x - x0) / (x1 - x0)
    t1 = t0 * (y1 - y0)
    t2 = y0 + t1
    return t2


def mouseX():
    global mousex
    return mousex


def mouseY():
    global mousey
    return mousey


def pmouseX():
    global mousex, pmousex
    return pmousex


def pmouseY():
    global mousey, pmousey
    return pmousey


def Width():
    global width
    return width


def Height():
    global height
    return height


#  Turn on filling. Set the fill color for polygons,          **
#  text color too.                                            **
def fill(r, g=1000, b=1000, a=255):
    global _fillcol, _dofill
    _dofill = True
    if isinstance(r, (tuple, pygame.Color)):
        _fillcol = r
        return
    if r > 255:
        r = 255
    elif r < 0:
        r = 0
    if g == 1000:
        _fillcol = (r, r, r, a)
    else:
        if g > 255:
            g = 255
        elif g < 0:
            g = 0
        if b > 255:
            b = 255
        elif b < 0:
            b = 0
        _fillcol = (r, g, b, a)


# Turn filling off.                                            **
def nofill():
    global _dofill
    _dofill = False


# Set the line and outline color.                              **
def stroke(r, g=1000, b=1000, a=255):
    global _strokecol, _dostroke

    if isinstance(r, (tuple, pygame.Color)):
        _strokecol = r
        _dostroke = True
        return
    if r > 255:
        r = 255
    elif r < 0:
        r = 0
    if g == 1000:
        _strokecol = (r, r, r, a)
    else:
        if g > 255:
            g = 255
        elif g < 0:
            g = 0
        if b > 255:
            b = 255
        elif b < 0:
            b = 0
        _strokecol = (r, g, b, a)
    _dostroke = True
    if renderer == 1:
        glColor3f(r, g, b)


# Turn off outline drawing.                                    **
def nostroke():
    global _dostroke
    _dostroke = False
    _strokecol = ""


# Set the mode for drawing ellipses.                           **
def ellipsemode(z):
    global _ELLIPSEMODE
    _ELLIPSEMODE = z


# Draw an ellipse. Also used for circles. Four modes as described in doc.           **
def ellipse(xpos, ypos, width, height):
    global canvas, _ELLIPSEMODE
    ccanvas = canvas.copy()
    if _ELLIPSEMODE == CENTER:  # Mode 0 is CENTER
        if _dofill:
            pygame.draw.ellipse(ccanvas, _fillcol, (xpos - width / 2, ypos - height / 2, width, height), 0)
        else:
            pygame.draw.ellipse(ccanvas, _fillcol, (xpos - width / 2, ypos - height / 2, width, height), 1)
        if _dostroke:
            if width // 2 < _linewidth:
                width = _linewidth * 2
            if height // 2 < _linewidth:
                height = _linewidth * 2
            pygame.draw.ellipse(ccanvas, _strokecol, (xpos - width / 2, ypos - height / 2, width, height), _linewidth)
    elif _ELLIPSEMODE == RADIUS:  # Mode 1 is Radius
        if _dofill:
            pygame.draw.ellipse(ccanvas, _fillcol, (xpos - width, ypos - height, width * 2, height * 2), 0)
        else:
            pygame.draw.ellipse(ccanvas, _fillcol, (xpos - width, ypos - height, width * 2, height * 2), 1)
        if _dostroke:
            pygame.draw.ellipse(ccanvas, _strokecol, (xpos - width, ypos - height, width * 2, height * 2), _linewidth)
    elif _ELLIPSEMODE == CORNER:
        if _dofill:
            pygame.draw.ellipse(ccanvas, _fillcol, (xpos, ypos, width, height), 0)
        else:
            pygame.draw.ellipse(ccanvas, _fillcol, (xpos, ypos, width, height), 1)
        if _dostroke:
            pygame.draw.ellipse(ccanvas, _strokecol, (xpos, ypos, width, height), _linewidth)
    elif _ELLIPSEMODE == CORNERS:
        if _dofill:
            pygame.draw.ellipse(ccanvas, _fillcol, (xpos, ypos, width - xpos, height - ypos), 0)
        else:
            pygame.draw.ellipse(ccanvas, _fillcol, (xpos, ypos, width - xpos, height - ypos), 1)
        if _dostroke:
            pygame.draw.ellipse(ccanvas, _strokecol, (xpos, ypos, width - xpos, height - ypos), _linewidth)
    else:
        print("Error: Illegal value for ELLIPSEMODE", _ELLIPSEMODE)  # 101
    ccanvas.set_alpha(_fillcol[3])
    canvas.blit(ccanvas, (0, 0))


def arc2(x0, y0, x1, y1, a1, ap, mode="PIESLICE"):
    global canvas, _strokecol, _linewidth, _fillcol
    pygame.draw.arc(canvas, pygame.Rect(x0, y0, x1 - x0, y1 - y0), a1, ap, _linewidth)


def arc(x0, y0, x1, y1, a1, ap, mode="PIESLICE"):
    global canvas, _strokecol, _linewidth, _fillcol
    ccanvas = canvas.copy()
    conv = 3.1415 / 180.0
    r = (x1 - x0) / 2
    xc = x0 + r
    yc = y0 + r
    xs = x = xc + r * cos(-a1 * conv)
    ys = y = yc + r * sin(-a1 * conv)
    xe = xc + r * cos(-(a1 + ap) * conv)
    ye = yc + r * sin(-(a1 + ap) * conv)
    a = a1 * 1.0
    pts = ((x, y),)
    while a <= a1 + ap:
        xx = xc + r * cos(-a * conv)
        yy = yc + r * sin(-a * conv)
        line(x, y, xx, yy)
        pts = pts + ((x, y),)
        x = xx
        y = yy
        a = a + 1
        if (a1 + ap) - a < 1:
            break
    xx = xc + r * cos(-(a1 + ap) * conv)
    yy = yc + r * sin(-(a1 + ap) * conv)
    pts = pts + ((xx, yy),)
    line(x, y, xx, yy)
    x = xx
    y = yy
    if mode == "CHORD":
        line(xe, ye, xs, ys)
        pts = pts + ((xs, ys),)
        pygame.draw.polygon(ccanvas, _fillcol, pts, 0)
        pygame.draw.polygon(ccanvas, _strokecol, pts, _linewidth)
    elif mode == "PIESLICE":
        line(x, y, xc, yc)
        pts = pts + ((xc, yc),)
        line(xc, yc, xs, ys)
        pts = pts + ((xs, ys),)
        pygame.draw.polygon(ccanvas, _fillcol, pts, 0)
        pygame.draw.polygon(ccanvas, _strokecol, pts, _linewidth)
    elif mode == "ARC":
        pygame.draw.polygon(ccanvas, _strokecol, pts, _linewidth)
    ccanvas.set_alpha(_fillcol[3])
    canvas.blit(ccanvas, (0, 0))


# Draw a line                                                  **
def line(x0, y0, x1, y1):
    global canvas, _strokecol, _linewidth
    ccanvas = canvas.copy()
    pygame.draw.line(ccanvas, _strokecol, (x0, y0), (x1, y1), _linewidth)
    ccanvas.set_alpha(_strokecol[3])
    canvas.blit(ccanvas, (0, 0))


# Draw a point.                                                **
def point(x, y):
    global _fillcol, canvas
    # ccanvas = canvas.copy()
    ccanvas = pygame.Surface((1, 1), 0, 32)
    ccanvas.fill(_fillcol)
    # pygame.draw.line(ccanvas, _fillcol, (x,y), (x,y), 1)
    ccanvas.set_alpha(_fillcol[3])
    canvas.blit(ccanvas, (x, y))


# Draw a rectangle. Same 4 modes as ellipse.                   **
def rect(xpos, ypos, x2, y2):
    global canvas, _RECTMODE
    ccanvas = canvas.copy()
    if _RECTMODE == CENTER:  # Mode 0 is CENTER
        if _dofill:
            pygame.draw.rect(ccanvas, _fillcol, (xpos - x2 / 2, ypos - y2 / 2, x2, y2), 0)
        else:
            pygame.draw.rect(ccanvas, _fillcol, (xpos - x2 / 2, ypos - y2 / 2, x2, y2), 1)
        if _dostroke:
            pygame.draw.rect(ccanvas, _strokecol, (xpos - x2 / 2, ypos - y2 / 2, x2, y2), _linewidth)
    elif _RECTMODE == RADIUS:  # RADIUS mode
        if _dofill:
            pygame.draw.rect(ccanvas, _fillcol, (xpos - x2, ypos - y2, x2 + x2, y2 + y2), 0)
        else:
            pygame.draw.rect(ccanvas, _fillcol, (xpos - x2, ypos - y2, x2 + x2, y2 + y2), 1)
        if _dostroke:
            pygame.draw.rect(ccanvas, _strokecol, (xpos - x2, ypos - y2, x2 + x2, y2 + y2), _linewidth)
    elif _RECTMODE == CORNER:  # CORNER mode
        if _dofill:
            pygame.draw.rect(ccanvas, _fillcol, (xpos, ypos, x2, y2), 0)
        else:
            pygame.draw.rect(ccanvas, _fillcol, (xpos, ypos, x2, y2), 1)
        if _dostroke:
            pygame.draw.rect(ccanvas, _strokecol, (xpos, ypos, x2, y2), _linewidth)
    elif _RECTMODE == CORNERS:  # CORNERS
        if _dofill:
            pygame.draw.rect(ccanvas, _fillcol, (xpos, ypos, x2 - xpos, y2 - ypos), 0)
        else:
            pygame.draw.rect(ccanvas, _fillcol, (xpos, ypos, x2 - xpos, y2 - ypos), 1)
        if _dostroke:
            pygame.draw.rect(ccanvas, _strokecol, (xpos, ypos, x2 - xpos, y2 - ypos), _linewidth)
    if len(_fillcol) > 3:
        ccanvas.set_alpha(_fillcol[3])
    canvas.blit(ccanvas, (0, 0))


# Draw a triangle specified by three points.                   **
def triangle(x0, y0, x1, y1, x2, y2):
    global canvas, _fillcol
    ccanvas = canvas.copy()
    if _dofill:
        pygame.draw.polygon(ccanvas, _fillcol, ((x0, y0), (x1, y1), (x2, y2)), 0)
    else:
        pygame.draw.polygon(ccanvas, _fillcol, ((x0, y0), (x1, y1), (x2, y2)), 1)
    if _dostroke:
        pygame.draw.polygon(ccanvas, _strokecol, ((x0, y0), (x1, y1), (x2, y2)), _linewidth)
    if len(_fillcol) > 3:
        ccanvas.set_alpha(_fillcol[3])
    canvas.blit(ccanvas, (0, 0))


# Set the frame rate                                           **
def frameRate(r):
    global _framerate
    _framerate = r
    clock.tick(_framerate)


def quad(x0, y0, x1, y1, x2, y2, x3, y3):
    global canvas, _fillcol
    ccanvas = canvas.copy()
    if _dofill:
        pygame.draw.polygon(ccanvas, _fillcol, ((x0, y0), (x1, y1), (x2, y2), (x3, y3)), 0)
    else:
        pygame.draw.polygon(ccanvas, _fillcol, ((x0, y0), (x1, y1), (x2, y2), (x3, y3)), 1)
    if _dostroke:
        pygame.draw.polygon(ccanvas, _strokecol, ((x0, y0), (x1, y1), (x2, y2), (x3, y3)), _linewidth)
    ccanvas.set_alpha(_fillcol[3])
    canvas.blit(ccanvas, (0, 0))


def strokeweight(s):
    global _linewidth
    _linewidth = s


def cvtColor(z):  # Convert an integer to a color (grey)
    return (z, z, z, 255)


def cvtColor3(r, g, b, a=255):
    return (r, g, b, a)


def noloop():
    global _noloop
    _noloop = True


def noLoop():
    noloop()


def rectmode(z):
    global _RECTMODE
    _RECTMODE = z


def background(r, g=255, b=255, a=255):
    global canvas, width, height, _xvid, _yvid, _xwid, _ywid, renderer

    if renderer == 1:
        glClearColor(r, g, b, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        return

    ccanvas = canvas.copy()
    if isinstance(r, (tuple, pygame.Color)):
        f = r
    elif g >= 1000:
        f = cvtColor(r)
    else:
        f = (r, g, b, a)
    ccanvas.fill(f)
    if len(f) >= 4:
        ccanvas.set_alpha(f[3])
    canvas.blit(ccanvas, (0, 0))


def setfont(s):
    global _font_family, _font_size
    font = pygame.font.SysFont(_font_family, _font_size)


def textsize(n):
    global _font_family, _font_size, _font_weight, _font_slant, font
    _font_size = n
    font = pygame.font.SysFont(_font_family, _font_size)


# Draw a text string at the given point.                       **
def text(s, x, y):
    global canvas, font

    if font == None:  # Create a font if needed
        font = pygame.font.Font(None, 18)
    text = font.render(s, 1, _fillcol)  # Render the string in the fill color
    textpos = text.get_rect()  # Get the rectangle that encloses the text
    textpos.bottomleft = [x, y]
    canvas.blit(text, textpos)


def _draw():
    global _user
    global mousex, mousey, pmousex, pmousey
    global i, j, canvas, _buttons, mp

    mp = pygame.mouse.get_pos()  # Get mouse coordinates
    pmousex = mousex
    mousex = mp[0]
    pmousey = mousey
    mousey = mp[1]
    mb = pygame.mouse.get_pressed()  # Get mouse buttons.
    for i in range(0, 3):
        if mb[i] and not _buttons[i]:  # Button i pressed.
            _mousePressed(i)
        elif not mb[i] and _buttons[i]:  # Button i released
            _mouseReleased(i)
    _buttons = mb
    if drawOK:
        _user.draw()  # Call the user's draw() function if it exists


def _keyPressed(k):
    global _user, _keyp
    if _keyp:
        if len(k) > 0:
            _user.keyPressed(ord(k[0]))


def _keyReleased(k):
    global _user, _keyr
    if _keyr:
        _user.keyReleased(k)


def _mouseReleased(b):
    global _user, _mouser
    if _mouser:
        _user.mouseReleased(b)  # Method exists, and was used.


def _mousePressed(b):
    global _user, _mousep
    if _mousep:
        _user.mousePressed(b)


# ---------------------- Images ---------------------------
def loadImage(s):
    try:
        myImage = pygame.image.load(s)
    except pygame.error:
        return None
    gim = Gimage()
    gim.setIm(myImage)
    return (gim)


def image(s, x, y):
    global canvas
    if hasattr(s, "draw"):
        s.draw(canvas, x, y)
    elif hasattr(s, "blit"):
        canvas.blit(s, (x, y))


def getpixel(im, x, y):
    return im.get(x, y)


def setpixel(im, i, j, c):
    im.set(i, j, c)


def set(i, j, c):
    canvas.set_at((i, j), c)


def get(i, j, w=0, h=0):
    if w == 0 and h == 0:
        return canvas.get_at((i, j))
    sub = self.im.subsurface((x0, y0, w, h))
    return sub


def image_rotate(im, a):
    r = pygame.transform.rotate(im.im, a)
    g = Gimage()
    g.setIm(r)
    return g


def cv2_convert(x):
    w = x.shape[1]
    h = x.shape[0]
    im = createImage(w, h)
    for i in range(0, w):
        for j in range(0, h):
            setpixel(im, i, j, x[j][i])
    return im


def grab(c=0):
    global camera
    if camera is None:
        camera = _cv.VideoCapture(c)
        print("Opening camera")
        if camera is None:
            print("No camera.")
            return None
    result, nim = camera.read()
    if result:
        nim = _cv.cvtColor(nim, _cv.COLOR_BGR2RGB)
        im = cv2_convert(nim)
        return im
    return None


def createImage(x, y):
    g = Gimage()
    img = pygame.Surface((x, y))
    g.setIm(img)
    return g


def resize(im, w, h):
    im.resize(int(w), int(h))
    return im


def save(s):
    pygame.image.save(canvas, s)


def red(c):
    return c[0]


def green(c):
    return c[1]


def blue(c):
    return c[2]


def grey(c):
    return (c[0] + c[1] + c[2]) / 3


def hue(c):
    cc = colorsys.rgb_to_hsv(c[0] / 255, c[1] / 255, c[2] / 255)
    return cc[0] * 255


def saturation(c):
    cc = colorsys.rgb_to_hsv(c[0] / 255, c[1] / 255, c[2] / 255)
    return cc[1] * 255


def brightness(c):
    cc = colorsys.rgb_to_hsv(c[0] / 255, c[1] / 255, c[2] / 255)
    return cc[2] * 255


def rgb2hsb(c):
    cc = colorsys.rgb_to_hsv(c[0] / 255., c[1] / 255., c[2] / 255.)
    return (cc[0] * 255., cc[1] * 255, cc[2] * 255)


def hsb2rgb(c):
    cc = colorsys.hsv_to_rgb(c[0] / 255., c[1] / 255., c[2] / 255.)
    return (cc[0] * 255., cc[1] * 255, cc[2] * 255)


# ------------------- Audio --------------------------------
def loadSound(s):
    m = pygame.mixer.Sound(s)
    return m
def is_playing():
    if pygame.mixer.get_busy() >= 1:
        return True
    if _playing:
        return True
    return False


def loadSoundDataLive(s=1, sr=44100):
    x = sd.rec(int(s * sr), samplerate=sr, channels=1)
    return x


def silence(s=1, sr=44100):
    x = numpy.zeros([int(s * sr), 2])
    return x


def soundWait():
    sd.wait()


def playSound(a, freq=44100):
    global _playing
    if isinstance(a, pygame.mixer.Sound):
        a.play()
    elif type(a) == numpy.ndarray:
        sd.play(a)
        _playing = True
    elif type(a) is list:
        x = numpy.array(a)
        _playing = True
        sd.play(x)
    elif type(a) is bytes:
        print("Bytes")
        y = numpy.frombuffer(a)
        x = []
        for i in range (0, len(y)-1):
            x.append( [float(y[i]), float(y[i+1])])
        x = numpy.array(x)
        sd.play(x, 11000)


def loopSound(a, freq=44100):
    global _playing
    if isinstance(a, pygame.mixer.Sound):
        a.play(-1)
    elif type(a) == numpy.ndarray:
        sd.play(a, loop=True)
        _playing = True
    elif type(a) is list:
        x = numpy.array(a)
        sd.play(x, loop=True)
        _playing = True
    elif type(a) is bytes:
        print("Bytes")
        y = numpy.frombuffer(a)
        x = []
        for i in range (0, len(y)):
            x.append( [float(y[i]), float(y[i+1])])
        x = numpy.array(x)
        sd.play(x, 11000)


def stopSound(a):
    a.stop()


def volumeSound(a, v):
    a.set_volume(v)


def durationSound(a):
    return a.get_length()


def soundData(a):
    return a.get_raw()


def initializeKeys():
    global frequencies
    frequencies = [0.0 for i in range(0, 120)]
    frequencies[0] = 16.35
    frequencies[1] = 17.32
    frequencies[2] = 18.35
    frequencies[3] = 19.45
    frequencies[4] = 20.60
    frequencies[5] = 21.83
    frequencies[6] = 23.12
    frequencies[7] = 24.5
    frequencies[8] = 25.96
    frequencies[9] = 27.50
    frequencies[10] = 29.14
    frequencies[11] = 30.87
    for i in range(12, 89):
        frequencies[i] = frequencies[i - 12] * 2


def noteSine(f):
    global note, _playing, _buf
    frequency_l = round(frequencies[f])
    n_samples = int(round(_sample_rate))

    for i in range(1, 2000):
        n_samples = n_samples + 1
        d = n_samples/frequency_l - int(n_samples/frequency_l)
        if d< 0.001:
            break

    
    max_sample = 2 ** (_bits - 1) - 1
    if _buf is None:
        _buf = numpy.zeros(n_samples)
    elif len(_buf) < n_samples:
        _buf = numpy.zeros(n_samples)

    for s in range(n_samples):
        t = float(s) / _sample_rate  # time in seconds
        _buf[s] = int(round(max_sample * sin(pi * frequency_l * t)))  # left
    return _buf


def noteSquare(f):
    global note, _playing, _buf
    frequency_l = int(frequencies[f])
    n_samples = int(round(_sample_rate))
    spp = int(_sample_rate / frequency_l)
    max_sample = 2 ** (_bits - 1) - 1
    if _buf is None:
        _buf = numpy.zeros(n_samples)
    elif len(_buf) < n_samples:
        _buf = numpy.zeros(n_samples)
    k = 0
    v = 1
    for s in range(n_samples):
        _buf[s] = v * max_sample
        k = k + 1
        if k >= spp / 2:
            k = 0
            v = -v
    return _buf


def notePulse(f, w):  # Frequency f pulse width w% as 0-1
    global note, _playing, _buf
    frequency_l = int(frequencies[f])
    n_samples = int(round(_sample_rate))
    spp = int(_sample_rate / frequency_l)
    max_sample = 2 ** (_bits - 1) - 1
    if _buf is None:
        _buf = numpy.zeros(n_samples)
    elif len(_buf) < n_samples:
        _buf = numpy.zeros(n_samples)
    width = int(spp * w)
    k = 0
    v = 1
    dc = width
    for s in range(n_samples):
        _buf[s] = v * max_sample
        k = k + 1
        if k >= dc:
            k = 0
            v = -v
            if dc <= width:
                dc = spp - width
            else:
                dc = width
    return _buf


def noteTriangle(f):  # Frequency f pulse width w% as 0-1
    global note, _playing, _buf
    frequency_l = int(frequencies[f])
    n_samples = round(_sample_rate)
    spp = int(_sample_rate / frequency_l)
    max_sample = 2 ** (_bits - 1) - 1
    if _buf is None:
        _buf = numpy.zeros(n_samples)
    elif len(_buf) < n_samples:
        _buf = numpy.zeros(n_samples)
    k = 0
    v = 1
    for s in range(n_samples):
        if k <= spp / 2:
            z = round(map(k, 0, int(spp / 2), -1, 1) * max_sample)
            _buf[s] = z
            k = k + 1
        elif k < spp:
            z = round(map(k, int(spp / 2), spp, 1, -1) * max_sample)
            _buf[s] = z
            k = k + 1
        else:
            _buf[s] = -max_sample
            k = 0
    return _buf


def noteSaw(f):  # Frequency f pulse width w% as 0-1
    global note, _playing,  _buf
    frequency_l = int(frequencies[f])
    n_samples = int(round(_sample_rate))
    spp = int(_sample_rate / frequency_l)
    max_sample = 2 ** (_bits - 1) - 1
    if _buf is None:
        _buf = numpy.zeros(n_samples)
    elif len(_buf) < n_samples:
        _buf = numpy.zeros(n_samples)
    k = 0
    v = 1
    for s in range(0, n_samples):
        if k <= spp:
            z = round(map(k, 0, int(spp), -1, 1) * max_sample)
            _buf[s] = z
            k = k + 1
        else:
            _buf[s] = -max_sample
            k = 0
    return _buf


def endNote():
    global  _playing
    if _playing:
        sd.stop()
        _playing = False


# ---------------------     Noise   ------------------------
def lerpm(x, a, b, m, n):
    zz = x - a
    d = b - a
    return zz / d * (n - m) + m


def noise(x, y, z):
    xx = floor(x) & 255  # FIND UNIT CUBE THAT
    Y = floor(y) & 255  # CONTAINS POINT.
    Z = floor(z) & 255
    x -= floor(x)  # FIND RELATIVE X,Y,Z
    y -= floor(y)  # OF POINT IN CUBE.
    z -= floor(z)
    u = fade(x)  # COMPUTE FADE CURVES
    v = fade(y)  # FOR EACH OF X,Y,Z.
    w = fade(z)
    A = p[xx] + Y
    AA = p[A] + Z
    AB = p[A + 1] + Z  # HASH COORDINATES OF
    B = p[xx + 1] + Y
    BA = p[B] + Z
    BB = p[B + 1] + Z  # THE 8 CUBE CORNERS,

    return lerp(w, lerp(v, lerp(u, grad(p[AA], x, y, z), grad(p[BA], x - 1, y, z)),
                        lerp(u, grad(p[AB], x, y - 1, z), grad(p[BB], x - 1, y - 1, z))), \
                lerp(v, lerp(u, grad(p[AA + 1], x, y, z - 1), grad(p[BA + 1], x - 1, y, z - 1)),
                     lerp(u, grad(p[AB + 1], x, y - 1, z - 1), grad(p[BB + 1], x - 1, y - 1, z - 1))))


def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


def lerp(t, a, b):
    return a + t * (b - a)


def grad(hsh, x, y, z):
    h = hsh & 15  # CONVERT LO 4 BITS OF HASH CODE
    if h < 8:
        u = x
    else:
        u = y

    #   v = h<4 ? y : h==12||h==14 ? x : z;
    if h < 4:
        v = y
    elif h == 12 or h == 14:
        v = x
    else:
        v = z

    # Thus a ? b, c : d is interpreted as a ? (b, c) : d, and not as the meaningless (a ? b), (c : d).
    # So, the expression in the middle of the conditional operator (between ? and :) is
    # parsed as if parenthesized.
    if (h & 1) == 0:
        ret = u
    else:
        ret = -u
    if (h & 2) == 0:
        r = v
    else:
        r = -v
    return ret + r


permutation = [151, 160, 137, 91, 90, 15,
               131, 13, 201, 95, 96, 53, 194, 233, 7, 225, 140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23,
               190, 6, 148, 247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32, 57, 177, 33,
               88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175, 74, 165, 71, 134, 139, 48, 27, 166,
               77, 146, 158, 231, 83, 111, 229, 122, 60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244,
               102, 143, 54, 65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169, 200, 196,
               135, 130, 116, 188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64, 52, 217, 226, 250, 124, 123,
               5, 202, 38, 147, 118, 126, 255, 82, 85, 212, 207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42,
               223, 183, 170, 213, 119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9,
               129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104, 218, 246, 97, 228,
               251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241, 81, 51, 145, 235, 249, 14, 239, 107,
               49, 192, 214, 31, 181, 199, 106, 157, 184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254,
               138, 236, 205, 93, 222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180]
p = []
for i in range(0, 256):
    p.append(permutation[i])
for i in range(0, 256):
    p.append(permutation[i])


def repermute():
    global permutation, p
    for i in range(0, 256):
        k = randint(0, 255)
        tmp = permutation[i]
        permutation[i] = permutation[k]
        permutation[k] = tmp
        p[i] = permutation[i]
    for i in range(0, 256):
        p[i + 256] = permutation[i]


def noise1d(x):
    x = noise(x, x, x)
    x = (x + 0.87) / 1.62
    if x < 0:
        x = 0
    if x > 1:
        x = 1
    return x


def noise2d(x, y):
    z = noise(x, y, (x + y) / 2)
    z = (z + 0.84) / 1.62
    if z < 0:
        z = 0
    if z > 1:
        z = 1
    return z


def noise3d(x, y, z):
    return noise(x, y, z)


# --------------------- Interaction ------------------------

def mouse():
    global mousex, mousey
    mp = pygame.mouse.get_pos()  # Get mouse coordinates
    mousex = mp[0]
    mousey = mp[1]
    return mp

'''     
# ------------------ 3D -----------------
def perspective(fovy, aspect, zNear, zFar):
    gluPerspective(fovy, aspect, zNear, zFar)


def translate3d(x, y, z):
    glTranslatef(x, y, z)


def rotate3d(angle, x, y, z):
    glRotatef(angle, x, y, z)


def scale3d(x, y, z):
    glScale(x, y, z)


#def beginDraw(code=GL_LINES):
#    glBegin(code)


#def endDraw():
#    glEnd()


#def vertex(v):
#    glVertex3fv(v)


def box():
    verticies = ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1), \
                 (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1))
    edges = ((0, 1), (0, 3), (0, 4), (2, 1), (2, 3), \
             (2, 7), (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7))
    glBegin(GL_LINES)
    for edge in edges:
        for v in edge:
            vertex(verticies[v])
    endDraw()


def polygonMode(mode):
    if mode == POLY_FILL:
        glPolygonMode(GL_FRONT, GL_FILL)
        glPolygonMode(GL_BACK, GL_FILL)
    elif mode == POLY_LINE:
        glPolygonMode(GL_FRONT, GL_LINE)
        glPolygonMode(GL_BACK, GL_LINE)
    elif mode == POLY_POINT:
        glPolygonMode(GL_FRONT, GL_POINT)
        glPolygonMode(GL_BACK, GL_POINT)


def sphere(r, nx, ny):
    s = gluNewQuadric()
    gluSphere(s, r, nx, ny)
    gluDeleteQuadric(s)

'''

# Random
def randRange(a, b):
    d = b - a
    return random() * d + a


def randomVal(v):
    return random() * v


def normal(mean, sd):
    return numpy.random.normal(loc=mean, scale=sd, size=None)


def distanceManhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def distanceChessboard(p1, p2):
    return max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))


# Module control -----------------------
def modulename(s):
    for i in range(len(s) - 1, 0, -1):
        if s[i] == '/' or s[i] == '\\':
            return s[i + 1:len(s) - 3]


def capture(s):
    pygame.image.save(canvas, s)


# Equialent of Processing function size, which sets up the display window.
def size(xs, ys, render=0):
    global width, height, canvas, renderer
    width = xs
    height = ys
    if render == 0:
        canvas = pygame.display.set_mode((xs, ys), DOUBLEBUF)
        #        canvas = pygame.display.set_mode((xs, ys), pygame.DOUBLEBUF, 32)   # Make the sketch window
        renderer = 0
    elif render == 1:
        canvas = pygame.display.set_mode((xs, ys), DOUBLEBUF | OPENGL)
        renderer = 1
    pygame.display.set_caption('Drawing')


def startdraw(w=50, h=50, render=0):
    global font, _framerate, clock, _user, drawOK
    global _keyp, _keyr, _mousep, _mouser

    username = inspect.stack()[1][1]  # Get the path of the caller's source
    username = modulename(username)  # extract the file name
    pygame.mixer.pre_init(22050, -_bits, 1)
    pygame.init()  # Initialize pygame, obviously
    size(w, h, render)
    ellipsemode(CENTER)
    rectmode(CORNER)
    stroke(0)
    fill(0)
    _user = __import__(username)  # Import names from user source
    if hasattr(_user, "initialize"):
        if callable(_user.initialize):
            _user.initialize()  # Call the user's SETUP() function if it exists
    if hasattr(_user, "keyPressed"):
        if callable(_user.keyPressed):
            _keyp = True
    if hasattr(_user, "keyReleased"):
        if callable(_user.keyReleased):
            _keyr = True
    if hasattr(_user, "mouseReleased"):
        if callable(_user.mouseReleased):
            _mouser = True
    if hasattr(_user, "mousePressed"):
        if callable(_user.mousePressed):
            _mousep = True
    background(200)  # Initial empty window
    #   ico = loadImage ('c:/pyp/ico/pyp.ico')
    #   pygame.display.set_icon(ico.im)
    pygame.display.set_caption("Glib (2022)")
    font = pygame.font.Font(None, 18)
    clock.tick(_framerate)
    if hasattr(_user, "draw"):
        if callable(_user.draw):
            drawOK = True
    initializeKeys()


def enddraw():
    global mousex, mousey
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                try:
                    _keyPressed(event.unicode)
                except:
                    continue
            elif event.type == pygame.KEYUP:
                try:
                    _keyReleased(event.key)
                except Exception as e:
                    print(" LOOP ERROR")
                    continue
        try:
            if _noloop == False:
                _draw()
                clock.tick(_framerate)
            p = pygame.mouse.get_pos()
            mousex = p[0]
            mousey = p[1]
            pygame.display.flip()
        except KeyboardInterrupt:
            print("INTERRUPTED!")
            exit()
