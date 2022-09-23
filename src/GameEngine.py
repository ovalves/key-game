from random import randrange
import pygame
from sys import exit
import constant as const

class GameState():
    def __init__(self, pyGame, screen, surfaceBoard, surfaceScore):
        self.board = const.BOARD
        self.whiteToMove = True
        self.moveLog = []
        self.pyGame = pyGame
        self.screen = screen
        self.surfaceBoard = surfaceBoard
        self.surfaceScore = surfaceScore
        self.myFont = pyGame.font.SysFont('Comic Sans MS', 30)
        self.listKeys = []
        self.__showKeys()

    def __showKeys(self):
        for line in range(3, 10):
            column = randrange(len(self.board))
            self.board[line][column] = const.KEY
            self.listKeys.append([line, column])

    def getKeyList(self):
        return self.listKeys

    def endGame(self, player):
        if player.keysSaved == 4:
            imageGameOver = pygame.image.load("images/gameover.png")
            self.screen.blit(imageGameOver, (0, 0))
            textsurface = self.myFont.render('{name} ganhou!!!'.format(name=player.name), True, pygame.Color("black"))
            self.screen.blit(textsurface, (const.WIDTH/4, 40))
            pygame.display.flip()
            done = False
            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        done = True
                        exit()

    def showMovements(self, possiblePositions):
        for position in possiblePositions:
            try:
                piece = self.board[position[0]][position[1]]
                if piece == const.KEY:
                    self.board[position[0]][position[1]] = const.IS_KEY_SELECTED
                elif piece != const.PLAYER_ONE_PIECE and piece != const.PLAYER_TWO_PIECE:
                    self.board[position[0]][position[1]] = const.HIGHLIGHT_MOVEMENT
            except IndexError:
                '''
                    A posição a ser desenha está fora do tabuleiro
                    Continua para a próxima iteração de posições
                '''
                continue

    def clearMovements(self):
        for line in range(len(self.board)):
            for column in range(len(self.board[0])):
                piece = self.board[line][column]
                if piece == const.HIGHLIGHT_MOVEMENT:
                    self.board[line][column] = const.BLANK_SPACE
                elif piece == const.IS_KEY_SELECTED:
                    self.board[line][column] = const.KEY

    def isInsideBoard(self, x, y):
        return ((x < 0) or (x > len(self.board[0])) or (y < 0) or (y > len(self.board)))

    def choosePiece(self, playerMove, coluna):
        imageGameOver = pygame.image.load("images/opcoes.png")
        self.screen.blit(imageGameOver, (const.WIDTH_BOARD/1.67, 3))
        pygame.display.flip()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    col = location[0]
                    row = location[1]

                    if(row >= 0 and row <= 49 and col >= 379):
                        #cavalo
                        if(col >= 379 and col <= 466):
                            movementsPossibles = playerMove.possibleMovements(self.board, coluna, const.KNIGHT_PIECE)
                            self.showMovements(movementsPossibles)
                        #torre
                        elif(col >= 467 and col <= 554):
                            movementsPossibles = playerMove.possibleMovements(self.board, coluna, const.ROOK_PIECE)
                            self.showMovements(movementsPossibles)
                        #bispo
                        elif(col >= 555):
                            movementsPossibles = playerMove.possibleMovements(self.board, coluna, const.BISHOP_PIECE)
                            self.showMovements(movementsPossibles)
                        done = True
                        return movementsPossibles
                    else:
                        return None




















