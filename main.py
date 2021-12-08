import pyglet
from pyglet.window import mouse
from pyglet import shapes

window = pyglet.window.Window()
window.set_size(400, 360)
pyglet.gl.glClearColor(111/255, 145/255, 47/255, 1)
#pyglet.gl.glClearColor(173/255, 142/255, 28/255, 1)
#pyglet.gl.glClearColor(179/255, 104/255, 12/255,1)

#label = pyglet.text.Label('Hello, world',
 #                         font_name='Times New Roman',
  #                        font_size=36,
   #                       x=window.width//2, y=window.height//2,
    #                      anchor_x='center', anchor_y='center')



class Drawable:
    def __init__(self, x, y, color = (0, 0, 0), size = 10):
        self.x = x
        self.y = y
        self.color = color
        self.size = size

class Xobj(Drawable):
    def __init__(self, x, y, color = (179, 104, 12), size = 20, lineWidth = 10 ):
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
    def __init__(self, x, y, color = (179, 104, 12), radius = 40, secColor = (111, 145,47), lineWidth = 10):
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



listX = list()

@window.event
def on_draw():
    window.clear()
    Board(10, 350).draw(pyglet)
    global listX
    for x in listX:
        x.draw(pyglet)

@window.event
def on_mouse_release(x, y, button, modifiers):
        if(button == mouse.LEFT):
            
            global listX
            listX.append(Xobj(x, y))


pyglet.app.run()