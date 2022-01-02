import pyglet
import random
from pyglet.window import mouse
from pyglet import shapes
print("Alege dificultatea (1/2/3): ")
DIFICULTATE = int(input())
window = pyglet.window.Window()
window.set_size(600, 300)
pyglet.gl.glClearColor(111/255, 145/255, 47/255, 1)

AI_FIRST = 2
PLAYER_FIRST = 1
X_TURN = 0
O_TURN = 1

class Application:
    pozitii = ((1, 1), (0, 0), (2, 2), (2, 0), (0, 2), (1, 0), (0, 1), (2, 1), (1, 2) ) 
    def __init__(self, dificultate):
        self.scoreX = 0
        self.scoreO = 0
        self.drawables = list()
        self.board = Board(0, window.height - 180)
        self.tabla = [ [ 0 for i in range(3) ] for j in range(3) ]
        self.turn = 0
        self.mode = PLAYER_FIRST
        self.dif = dificultate
        self.rand_picker = list(Application.pozitii)
        self.dif_turn = 0 if self.dif < 3 else 1
        self.lin = [ 0, 0, 0]
        self.col = [ 0, 0, 0]
        self.diag1 = 0
        self.diag2 = 0
        self.finished = 0
        self.freeSpace = 9
        self.winLabel = pyglet.text.Label('', font_name = 'Century Gothic',
         font_size=20, x=450, y=150, color = (156, 78, 86, 255), bold = 1, anchor_x='center', anchor_y='center')
        self.scoreLabel = pyglet.text.Label('', font_name = 'Century Gothic',
         font_size=20, x=390, y=275, color = (156, 78, 86, 255), bold = 1)
    def isFree(self, x, y):
        x2, y2 = self.normalize(x, y)
        return self.tabla[x2][y2] == 0
    def draw(self, p):
        self.scoreLabel.text = "X:{x}\t\tO:{o}".format(x=self.scoreX, o=self.scoreO)
        self.winLabel.draw()
        self.board.draw(p)
        self.scoreLabel.draw()
        for e in self.drawables:
            e.draw(p)
    def put(self, x, y, el):
        if x >= self.board.x and x <= self.board.lineWidth * 2 + self.board.size * 3:
            if y <= self.board.y and y >= self.board.y-(self.board.lineWidth * 2 + self.board.size * 3):
                x2, y2 = self.normalize(x, y)
                if self.tabla[x2][y2] == 0:
                    self.place(x2, y2, el)
    def place(self, x, y, el):
        aux = self.board.size + self.board.lineWidth
        threshold = -1 if el == 'X' else 1
        self.lin[x] = self.lin[x] + threshold
        self.col[y] = self.col[y] + threshold
        if x == y: self.diag1 = self.diag1 + threshold
        if x + y == 2 : self.diag2 = self.diag2 + threshold
        self.tabla[x][y] = 1
        self.turn = (self.turn + 1) % 2
        if el == 'X':
            self.drawables.append(Xobj(int(x * aux + aux / 4), int((y + 1) * aux - aux / 4)))
        else:
            self.drawables.append(Oobj(int(x * aux + aux / 2 - 12), int((y + 1) * aux - aux / 2 + 12)))
        self.freeSpace = self.freeSpace - 1
    def normalize(self, x, y):
        aux = self.board.size + self.board.lineWidth
        x2 = int(x / aux)
        y2 = int(y / aux)
        if y2 > 2:
            y2 = 2
        if x2 > 2:
            x2 = 2
        return (x2, y2)        
    def findOnLine(self, line):
        for i in range(3):
           if self.tabla[line][i] == 0:
            return i
        return -1
    def findOnCol(self, col):
        for i in range(3):
           if self.tabla[i][col] == 0:
            return i
        return -1
    def findOnDiag1(self):
        for i in range(3):
            if self.tabla[i][i] == 0:
                return i
        return -1
    def findOnDiag2(self):
        for i in range(3):
            if self.tabla[i][2-i] == 0:
                return i
        return -1
    def checkWin(self):
        if self.finished == 0:
            for i in range(3):
                if self.lin[i] and self.lin[i] % 3 == 0: 
                    self.winLabel.text = "A câștigat " + ('O' if self.lin[i] > 0 else 'X'); self.finished = 1
                    if self.lin[i] > 0 : self.scoreO = self.scoreO + 1
                    else : self.scoreX = self.scoreX + 1
                    return
                elif self.col[i] and self.col[i] % 3 == 0: 
                    self.winLabel.text = "A câștigat " + ('O' if self.col[i] > 0 else 'X'); self.finished = 1
                    if self.col[i] > 0 : self.scoreO = self.scoreO + 1
                    else : self.scoreX = self.scoreX + 1
                    return
            if self.diag1 and self.diag1 % 3 == 0: 
                self.winLabel.text = "A câștigat " + ('O' if self.diag1 > 0 else 'X'); self.finished = 1
                if self.diag1 > 0 : self.scoreO = self.scoreO + 1
                else : self.scoreX = self.scoreX + 1
                return
            elif self.diag2 and self.diag2 % 3 == 0: 
                self.winLabel.text = "A câștigat " + ('O' if self.diag2 > 0 else 'X'); self.finished = 1
                if self.diag2 > 0 : self.scoreO = self.scoreO + 1
                else : self.scoreX = self.scoreX + 1
                return
        # verif remiza
            if self.finished == 0:
                if self.freeSpace == 0:
                        self.finished = 1     
                        self.winLabel.text = "Remiză."
    def calcMove(self):
        if self.dif_turn == 0:
            index = random.randint(0, len(self.rand_picker) - 1)
            while len(self.rand_picker)>0 and self.tabla[self.rand_picker[index][0]][self.rand_picker[index][1]] == 1:
                del self.rand_picker[index]
                if len(self.rand_picker)>0: index = random.randint(0, len(self.rand_picker) - 1)
            if len(self.rand_picker)>0:
                self.place(self.rand_picker[index][0], self.rand_picker[index][1], 'X' if self.mode == AI_FIRST else 'O')
                del self.rand_picker[index]
        else:
            # caut mai intai sa vad daca pot face 3 in linie
            if self.mode == AI_FIRST and self.diag1 == -2: self.place(self.findOnDiag1(), self.findOnDiag1(), 'X'); return
            if self.mode == PLAYER_FIRST and self.diag1 == 2: self.place(self.findOnDiag1(), self.findOnDiag1(), 'O'); return
            if self.mode == AI_FIRST and self.diag2 == -2: self.place(self.findOnDiag2(), 2-self.findOnDiag2(), 'X'); return
            if self.mode == PLAYER_FIRST and self.diag2 == 2: self.place(self.findOnDiag2(), 2-self.findOnDiag2(), 'O'); return
            for i in range(3):
                if self.mode == AI_FIRST:
                    if self.lin[i] == -2:
                        self.place(i, self.findOnLine(i), 'X'); return
                    if self.col[i] == -2:
                        self.place(self.findOnCol(i), i, 'X'); return
                elif self.mode == PLAYER_FIRST:
                    if self.lin[i] == 2:
                        self.place(i, self.findOnLine(i), 'O'); return
                    if self.col[i] == 2:
                        self.place(self.findOnCol(i), i, 'O'); return
            # dupa caut daca pot bloca 2 in linie de alea adversarului
            for i in range(3):
                if self.mode == AI_FIRST:
                    if self.lin[i] == 2:
                        self.place(i, self.findOnLine(i), 'X'); return
                    if self.col[i] == 2:
                        self.place(self.findOnCol(i), i, 'X'); return
                elif self.mode == PLAYER_FIRST:
                    if self.lin[i] == -2:
                        self.place(i, self.findOnLine(i), 'O'); return
                    if self.col[i] == -2:
                        self.place(self.findOnCol(i), i, 'O'); return
            if self.mode == AI_FIRST and self.diag1 == 2: self.place(self.findOnDiag1(), self.findOnDiag1(), 'X'); return
            if self.mode == PLAYER_FIRST and self.diag1 == -2: self.place(self.findOnDiag1(), self.findOnDiag1(), 'O'); return
            if self.mode == AI_FIRST and self.diag2 == 2: self.place(self.findOnDiag2(), 2-self.findOnDiag2(), 'X'); return
            if self.mode == PLAYER_FIRST and self.diag2 == -2: self.place(self.findOnDiag2(), 2-self.findOnDiag2(), 'O'); return
            # caut pozitia optima buna si pun pe ea
            for p in Application.pozitii:
                threshold = -1 if self.mode == AI_FIRST else 1
                if self.tabla[p[0]][p[1]] == 0:
                    if self.lin[p[0]] + threshold == 2 * threshold or self.col[p[1]] + threshold == 2 * threshold:
                        self.place(p[0], p[1], 'X' if self.mode == AI_FIRST else 'O')
                        print(p)
                        return
                    if ((p[0] == p[1] and self.diag1 + threshold == 2 * threshold) or (p[0] + p[1]==2 and self.diag2 + threshold == 2 * threshold)):
                        self.place(p[0], p[1], 'X' if self.mode == AI_FIRST else 'O')
                        print(p)
                        return
            for p in Application.pozitii:
                if self.tabla[p[0]][p[1]] == 0:
                    self.place(p[0], p[1], 'X' if self.mode == AI_FIRST else 'O')
                    print(p)
                    return
        if self.dif == 2: self.dif_turn = (self.dif_turn + 1) % 2
    def reset(self):
        for i in range(3):
            self.lin[i] = self.col[i] = 0
        self.diag1 = self.diag2 = self.turn = self.finished = 0
        self.rand_picker = list(Application.pozitii)
        self.dif_turn = 0 if self.dif < 3 else 1
        self.freeSpace = 9
        self.drawables = self.drawables[0:0]
        self.winLabel.text = ''
        for i in range(3):
            for j in range(3):
                self.tabla[i][j] = 0
        if self.mode == AI_FIRST:
            self.calcMove()


class Drawable:
    def __init__(self, x, y, color = (0, 0, 0), size = 10):
        self.x = x
        self.y = y
        self.color = color
        self.size = size

class Xobj(Drawable):
    def __init__(self, x, y, color = (179, 104, 12), size = 40, lineWidth = 10 ):
        super().__init__(x, y, color, size)
        self.lineWidth = lineWidth
    def draw(self, p):
        p.gl.glLineWidth(self.lineWidth)
        p.graphics.draw(4, p.gl.GL_LINES,
        ('v2i', (self.x, self.y, self.x + self.size, self.y - self.size, 
        self.x + self.size, self.y, self.x, self.y - self.size )),
        ('c3B', (self.color * 4))
        )

class Oobj(Drawable):
    batch = pyglet.graphics.Batch()
    def __init__(self, x, y, color = (179, 104, 12), radius = 35, secColor = (111, 145,47), lineWidth = 10):
        super().__init__(x, y, color, radius)
        self.circle1 = shapes.Circle(x, y, radius, color = self.color, batch = Oobj.batch)
        self.circle2 = shapes.Circle(x, y, radius-lineWidth%radius, color = secColor, batch = Oobj.batch)
    def draw(self, p):
        self.circle1.draw()
        self.circle2.draw()


class Board(Drawable):
    def __init__(self, x = 0, y = 0, color = (179, 104, 12), size = 90, lineWidth = 10,):
        super().__init__(x, y, color, size)
        self.lineWidth = lineWidth
    def draw(self, p):
        p.gl.glLineWidth(self.lineWidth)
        p.graphics.draw(8, p.gl.GL_LINES,
        ('v2i', (self.x + self.size, self.y, self.x + self.size, self.y - 3*self.size - self.lineWidth,
        self.x + self.lineWidth + 2*self.size, self.y, self.x + self.lineWidth + 2*self.size, self.y - 3*self.size - self.lineWidth,
        self.x, self.y - self.size, self.x + 3*self.size + self.lineWidth, self.y - self.size,
        self.x, self.y - 2*self.size - self.lineWidth, self.x + 3*self.size + self.lineWidth, self.y - 2*self.size - self.lineWidth)),
        ('c3B', (self.color * 8))
        )

app = Application(DIFICULTATE)
if app.mode == AI_FIRST:
    app.calcMove()

@window.event
def on_draw():
    window.clear()
    global app
    app.draw(pyglet)

@window.event
def on_mouse_release(x, y, button, modifiers):
        if(button == mouse.LEFT):
            global app
            if app.finished == 0 and app.isFree(x, y):
                if app.mode == PLAYER_FIRST:
                    if app.turn == X_TURN:
                        app.checkWin()
                        app.put(x, y, 'X')
                        app.checkWin()
                        app.calcMove()
                        app.checkWin()
                elif app.mode == AI_FIRST:
                    if app.turn == O_TURN:
                        app.checkWin()
                        app.put(x, y, 'O')
                        app.checkWin()
                        app.calcMove()
                        app.checkWin()
            elif app.finished == 1:
                app.reset()
pyglet.app.run()


# de rezolvat cand apasa playerul pe o casuta ocupata vine randul ai-ului