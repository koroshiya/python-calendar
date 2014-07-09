from __future__ import division
import pygame
from pygame.locals import Color
from pygame import key
import Scene
import math
import cairo
import rsvg
import array

class ControlsScreen(Scene.Scene):

    def __init__(self, size):
        super(ControlsScreen, self).__init__()

        screen = pygame.display.set_mode(size, pygame.HWSURFACE|pygame.DOUBLEBUF)

        #screen.fill(white)
        self.bg = pygame.image.load('./refinery.png').convert() #repeating bg
        for x in range(0, screen.get_width(), self.bg.get_width()):
            for y in range(0, screen.get_height(), self.bg.get_height()):
                screen.blit(self.bg, (x,y))
        self.bgcache = screen.copy()
        pygame.display.flip()

        self.months = [
            ["January", 31],
            ["February", 28],
            ["March", 31],
            ["April", 30],
            ["May", 31],
            ["June", 30],
            ["July", 31],
            ["August", 31],
            ["September", 30],
            ["October", 31],
            ["November", 30],
            ["December", 31]
        ]
        self.month = 5
        self.oldmonth = 5

        self.loadText(screen, 48, self.months[self.month][0], (50, 25), 100, 100)

        newsize = screen.get_height() / 4
        self.scalesize = newsize * 2 / 3
        self.scalesize = int(math.floor(self.scalesize))
        self.btn = self.loadsvg('./gray.svg', screen, self.scalesize)
        
        self.imgSize = newsize #width of button; should be same as height
        self.baseX = screen.get_width() / 2 - 9 * self.imgSize / 2
        posX = self.baseX
        self.posY = screen.get_height() / 2 - 96 / 2

        self.dayofmonth = 29
        self.direction = 1
        
        for i in xrange(-3, 7):
            screen.blit(self.btn, (posX, self.posY))
            self.loadText(screen, 24, self.getRelativeDay(i, True), (posX, self.posY), self.scalesize, self.scalesize)
            posX += self.imgSize

        self.frame = self.loadsvg('./onyx.svg', screen, self.scalesize + self.scalesize / 10)
        self.framepos = (screen.get_width() / 2 - self.imgSize / 2 - self.imgSize / 25, self.posY - 3)
        screen.blit(self.frame, self.framepos)

        pygame.display.update()
        self.curmove = self.imgSize
        self.moved = 0
        self.moving = False
        self.lastMove = False
        self.nextMonth = False
        self.monthPos = 25
        self.monthHalf = False
        self.speed = self.imgSize / 30
        self.curmonth = "June"

    def getRelativeDay(self, mv, boolStart):
        if boolStart:
            start = self.dayofmonth - 1
        else:
            start = self.dayofmonth - 2 if self.direction > 0 else self.dayofmonth
        newVal = start + mv
        if newVal < 1:
            if self.month == 0:
                newVal = self.months[11][1] + newVal
            else:
                newVal = self.months[self.month - 1][1] + newVal
        elif newVal > self.months[self.month][1]:
            newVal -= self.months[self.month][1]

        return str(newVal)

    def render(self, screen):
        if self.moving:
            screen.blit(self.bgcache, (0, 0))
                #start animation
            #screen.blit(self.getTextAsImage(self.months[self.month][0]), (50, self.monthPos))
            month = self.oldmonth if not self.monthHalf else self.month
            self.loadText(screen, 48, self.months[month][0], (50, self.monthPos), 200, 100) #TODO month

            posX = self.baseX - self.curmove
            for i in xrange(-3, 7):
                screen.blit(self.btn, (posX, self.posY))
                self.loadText(screen, 24, self.getRelativeDay(i, False), (posX, self.posY), self.scalesize, self.scalesize)
                posX += self.imgSize
            screen.blit(self.frame, self.framepos)
            if self.lastMove:
                self.moving = False
                self.lastMove = False
                if not math.fabs(self.curmove) >= self.imgSize * math.fabs(self.direction):
                    if self.direction > 0:
                        self.direction -= 1
                    elif self.direction < 0:
                        self.direction += 1
                    self.move(self.direction)
                if self.nextMonth:
                    self.monthHalf = False
                    self.nextMonth = False
                    self.oldmonth = self.month

            pygame.display.update()

    def loadText(self, screen, size, text, pos, targetWidth, targetHeight):
        font_path = "./Ubuntu-M.ttf"
        fontObj = pygame.font.Font(font_path, size)

        txt = fontObj.render(text, 1, (255,255,255))
        fSize = fontObj.size(text)
        fPos = (pos[0] + ((targetWidth - fSize[0]) / 2), pos[1] + ((targetHeight - fSize[1]) / 2))
        screen.blit(txt, fPos)

    def update(self):
        if self.moving:
            self.curmove += self.speed * self.direction
            if math.fabs(self.curmove) >= self.imgSize:
                self.lastMove = True
    
    def moveRight(self):
        self.move(25)
    
    def moveLeft(self):
        self.move(-25)
    
    def move(self, direction):
        if not self.moving:
            self.direction = direction
            self.curmove = 0
            self.moving = True
            if direction > 0:
                if self.dayofmonth < self.months[self.month][1]:
                    self.dayofmonth += 1
                else:
                    self.dayofmonth = 1
                    self.nextMonth = True
                    self.oldmonth = self.month
                    if self.month == 11:
                        self.month = 0
                    else:
                        self.month += 1
            else:
                if self.dayofmonth == 1:
                    self.nextMonth = True
                    self.oldmonth = self.month
                    if self.month == 0:
                        self.month = 11
                    else:
                        self.month -= 1
                    if self.oldmonth == 0:
                        self.dayofmonth = self.months[11][1]
                    else:
                        self.dayofmonth = self.months[self.month][1]
                else:
                    self.dayofmonth -= 1

    def handle_event(self, event):
        pass

    def processEvent(self, arg):
        pass

    def processKey(self, arg):
        return self.processEvent(arg)

    def loadsvg(self, filename, surface, targetWidth):
        WIDTH = surface.get_width()
        HEIGHT = surface.get_height()
        data = array.array('c', chr(0) * WIDTH * HEIGHT * 4)
        cairosurface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, WIDTH, HEIGHT, WIDTH * 4)
        svg = rsvg.Handle(filename)

        dimens = svg.get_dimension_data()
        scale = targetWidth / dimens[0]
        targetHeight = scale * dimens[1]
        ctx = cairo.Context(cairosurface)
        if scale != 1:
            ctx.scale(scale, scale)
        svg.render_cairo(ctx)
        image = pygame.image.frombuffer(data.tostring(), (WIDTH, HEIGHT),"RGBA")
        print "displaying image at", WIDTH, HEIGHT
        return image
