import pygame
from permutationApproach import bestPermutation
from geneticAlgorithmApproach import bestOrder
pygame.init()
pygame.display.set_caption("Travelling Salesman") # caption fromt the display class

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 660
TOP = 60
ROWS = 20
COLUMNS = 20


class Board:
    def __init__(self, rows, cols, width, height, maxCities=10):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.cities = [[City(i, j, j * width / cols, i * height / rows + TOP, width / cols, height / rows) for j in range(cols)] for i in range(rows)]
        self.MAX_CITIES = maxCities
        self.numCities = 0
        self.travellingCities = []
        self.order = list(range(len(self.travellingCities)))

    def draw(self):
        global win
        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cities[i][j].draw(win)

        # Draw Grid Lines
        x_gap = self.width / self.cols
        y_gap = self.height / self.rows
        thick = 1
        for i in range(self.rows + 1):
            pygame.draw.line(win, (0, 0, 0), (0, i * y_gap + TOP), (self.width, i * y_gap + TOP), thick)

        for j in range(self.cols + 1):
            pygame.draw.line(win, (0, 0, 0), (j * x_gap, TOP), (j * x_gap, self.height + TOP), thick)

    def getCoordinates(self, pos):
        if pos[0] < self.width and pos[1] < self.height + TOP and pos[1] > TOP:
            x_gap = self.width / self.cols
            y_gap = self.height / self.rows

            col = pos[0] // x_gap
            row = (pos[1] - TOP) // y_gap
            return int(row), int(col)
        else:
            return None

    def updateCity(self, row, col):
        if not self.cities[row][col].selected and self.numCities < self.MAX_CITIES:
            self.cities[row][col].clicked()
            self.numCities += 1

    def updateTravellingSelected(self):
        self.travellingCities = []
        self.ordering = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cities[i][j].selected:
                    self.travellingCities.append(self.cities[i][j])

        # self.order = bestPermutation(self.travellingCities)
        self.order = bestOrder(self.travellingCities, 5)


    def clear(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cities[i][j].selected = False

        board.numCities = 0
        board.travellingCities = []
        self.order = []

class City:

    def __init__(self, row, col, x, y, width, height):
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (255, 255, 255)
        self.center = [self.x + self.width / 2, self.y + self.height / 2]
        self.selected = False

    def draw(self, surface):
        if self.selected:
            pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.width, self.height))

    def clicked(self):
        self.selected = not self.selected

class Button:

    def __init__(self, x, y, width, height, color, text, textSize, textColor):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.textSize = textSize
        self.textColor = textColor

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height), 2)

        fnt = pygame.font.SysFont("comicsans", self.textSize)
        text = fnt.render(self.text, 1, self.textColor)
        win.blit(text, (self.x + self.width / 2 - text.get_width() / 2, self.y + self.height / 2 - text.get_height() / 2))

    def isclicked(self, pos):
        x, y = pos
        if x < self.x + self.width and x > self.x:
            if y < self.y + self.height and y > self.y:
                return True
        return False

def redrawWindow(board, getPathbutton, clearButton):
    global win
    win.fill((255, 255, 255))
    board.draw()
    getPathbutton.draw()
    clearButton.draw()

    # Show Text at top
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Choose up to 10 Cities", 1, (0, 0, 0))
    win.blit(text, (0, TOP / 2 - text.get_height() / 2))

def drawPath(board, ordering, color, thickness):
    global win

    for i in range(len(board.travellingCities) - 1):
        pygame.draw.line(win, color, (board.travellingCities[ordering[i]].center[0], board.travellingCities[ordering[i]].center[1]), (board.travellingCities[ordering[i + 1]].center[0], board.travellingCities[ordering[i + 1]].center[1]), thickness)


win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # creates window (width, height)

board = Board(ROWS, COLUMNS, WINDOW_WIDTH, WINDOW_HEIGHT - TOP)
getPathbutton = Button(WINDOW_WIDTH - 150, 10, 140, TOP - 20, (0, 255, 0), "Get Shortest Path!", 20, (255, 255, 255))
clearButton = Button(WINDOW_WIDTH - 270, 10, 100, TOP - 20, (255, 0, 0), "Clear", 20, (255, 255, 255))
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # Handle City clicks
            coordinates = board.getCoordinates(pos)
            if coordinates:
                row, col = coordinates
                if not board.cities[row][col].selected and board.numCities < board.MAX_CITIES:
                    board.cities[row][col].clicked()
                    board.numCities += 1
                elif board.cities[row][col].selected:
                    board.cities[row][col].clicked()
                    board.numCities -= 1

            # Handle Button Click
            if getPathbutton.isclicked(pos):
                board.updateTravellingSelected()

            # Handle Clear Button Click
            if clearButton.isclicked(pos):
                board.clear()

    redrawWindow(board, getPathbutton, clearButton)
    drawPath(board, board.order, (0, 0, 255), 4)
    pygame.display.update()

pygame.quit()
