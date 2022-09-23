import constant as const
from itertools import product

class Player():
    def __init__(self, position, color, name, baseName):
        self.position = position
        self.color = color
        self.keysSaved = 0
        self.keysOnPocket = 0
        self.yourTurn = False
        self.name = name
        self.baseName = baseName
        self.keysLimit = 1
        self.onBase = True
        self.pieceInUse = const.KNIGHT_PIECE
        self.IAvisitedNodes = []


    '''
        Create the players pieces
    '''
    def possibleMovements(self, board, column, pieceInUse=const.KNIGHT_PIECE):
        possiblePositions = []

        if self.onBase:
            self.position = [self.position[0], column]

        '''
            Verifica as posições possíveis de uma peça no tabuleiro
        '''
        if pieceInUse == const.ROOK_PIECE: # Movimentos da torre
            for line in range(self.position[0] - const.ROOK_MAX_MOVEMENT, (self.position[0] + const.ROOK_MAX_MOVEMENT) + 1):
                for column in range(self.position[1] - const.ROOK_MAX_MOVEMENT, (self.position[1] + const.ROOK_MAX_MOVEMENT) + 1):
                    if self.__movementPossibleRook([line, column], board):
                        possiblePositions.append([line, column])
                    else:
                        continue
            return possiblePositions
        elif pieceInUse == const.BISHOP_PIECE: # Movimentos do bispo
            return self.__movementPossibleBishop(board)
        else:
            return self.__movementPossibleKnight(board) # Movimentos do cavalo

    '''
        Define as posições possíveis da torre no tabuleiro
    '''
    def __movementPossibleRook(self, move, board):
        if move[0] >= 0 and move[0] < len(board) and move[1] >= 0 and move[1] < len(board[0]):
            piece = board[move[0]][move[1]]
            if self.position[0] == move[0] or self.position[1] == move[1]:
                if self.__isBlankSpace(piece) or self.__isHighlightMovement(piece) or self.__isPlayerBase(piece) or self.__hasKeyOnPocket(piece):
                    return True

        return False

    '''
        Define as posições possíveis do bispo no tabuleiro
    '''
    def __movementPossibleBishop(self, board):
        boardLenght = len(board) - 1
        directions = [[1,1],[-1,1],[-1,-1],[1,-1]]
        moves = []

        for direction in directions:
            row = self.position[0]
            col = self.position[1]
            for _ in range(const.BISHOP_MAX_MOVEMENT):

                row = row + direction[0]
                col = col + direction[1]

                if (row > boardLenght):
                    continue

                if int(row) > 0 and int(col) > 0:
                    moves.append([row, col])
        return moves

    '''
        Define as posições possíveis para o cavalo no tabuleiro
    '''
    def __movementPossibleKnight(self, board):
        boardLenght = len(board) - 1
        row = self.position[0]
        col = self.position[1]

        directions = [(-3, -1), (-3, +1), (+3, -1), (+3, +1), (-1, -3), (-1, +3), (+1, -3), (+1, +3)]
        moves = []
        for direction in directions:
            x_row = row + direction[0]
            y_col = col + direction[1]

            if (x_row > boardLenght or y_col > boardLenght):
                continue

            if (x_row > 0 and y_col > 0):
                moves.append([x_row, y_col])

        return moves

    '''
        Create the players pieces
    '''
    def __isBlankSpace(self, piece):
        return piece == const.BLANK_SPACE

    '''
        Create the players pieces
    '''
    def __isHighlightMovement(self, piece):
        return piece == const.HIGHLIGHT_MOVEMENT

    '''
        Create the players pieces
    '''
    def __isPlayerBase(self, piece):
        return piece == self.baseName

    '''
        Create the players pieces
    '''
    def __hasKeyOnPocket(self, piece):
        return (piece == const.KEY and self.keysOnPocket < self.keysLimit)

    '''
        Create the players pieces
    '''
    def makeMove(self, move, chessEngine, player2):
        #pega o nome das posicoes iniciais e finais
        startPlay = chessEngine.board[self.position[0]][self.position[1]]
        endPlay = chessEngine.board[move[0]][move[1]]

        #seta os nomes das posicoes depois do movimento
        if startPlay != self.baseName:
            chessEngine.board[self.position[0]][self.position[1]] = const.BLANK_SPACE
        chessEngine.board[move[0]][move[1]] = self.name

        #seta que saimos da base
        self.onBase = False

        '''
            Verificando se uma chave foi pega no movimento
            Se pegou a chave incrementa as chaves no bolso e remove a chave da lista de chaves
        '''
        if [move[0], move[1]] in chessEngine.getKeyList():
            self.keysOnPocket = self.keysOnPocket + 1
            chessEngine.getKeyList().remove([move[0], move[1]])

        if endPlay == const.IS_KEY_SELECTED:
            chessEngine.board[move[0]][move[1]] = self.name
            self.keysOnPocket = self.keysOnPocket + 1

        elif move[0] != self.position[0]:
            startline = self.position[0] if self.position[0] < move[0] else move[0]
            endLine = move[0] if move[0] > self.position[0] else self.position[0]
            for line in range(startline, endLine):
                piece = chessEngine.board[line][move[1]]
                if piece == const.IS_KEY_SELECTED and self.keysOnPocket < self.keysLimit:
                    chessEngine.board[line][move[1]] = const.BLANK_SPACE
                    self.keysOnPocket = self.keysOnPocket + 1
                elif piece == player2.name and player2.keysOnPocket > 0 and self.keysOnPocket < self.keysLimit:
                    player2.keysOnPocket = player2.keysOnPocket - 1
                    self.keysOnPocket = self.keysOnPocket + 1
        elif move[1] != self.position[1]:
            startColumn = self.position[1] if self.position[1] < move[1] else move[1]
            endColumn = move[1] if move[1] > self.position[1] else self.position[1]
            for column in range(startColumn, endColumn):
                piece = chessEngine.board[move[0]][column]
                if piece == const.IS_KEY_SELECTED and self.keysOnPocket < self.keysLimit:
                    chessEngine.board[move[0]][column] = const.BLANK_SPACE
                    self.keysOnPocket = self.keysOnPocket + 1
                elif piece == player2.name and player2.keysOnPocket > 0 and self.keysOnPocket < self.keysLimit:
                    player2.keysOnPocket = player2.keysOnPocket - 1
                    self.keysOnPocket = self.keysOnPocket + 1

        if endPlay == self.baseName:
            chessEngine.board[move[0]][move[1]] = self.baseName
            self.onBase = True
            if self.keysOnPocket > 0:
                self.keysSaved = self.keysSaved + self.keysOnPocket
                self.keysOnPocket = 0

        self.position = move
        self.yourTurn = False
        chessEngine.endGame(self)




