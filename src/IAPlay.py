from scipy import spatial
import constant as const

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

class IAPlay():
    def __init__(self, gameState, player, board, keyList):
        self.gameState = gameState
        self.player = player
        self.board = board
        self.keyList = keyList

    '''
        Responsável por realizar a avaliação das jogadas da IA
    '''
    def makeMove(self):
        # Retorna o caminho para os movimentos que levarão a IA até as chaves
        IAMoves = self.getMoves()

        # Constrói a lista de caminhos até as chaves
        paths = []
        for path in IAMoves:
            if type(path['path']) is list:
                for movePath in path['path']:
                    paths.append([movePath[0], movePath[1]])
            else:
                paths.append([path['path'][0], path['path'][1]])

        # Busca os movimentos permitidos para cada jogada
        possibleMoves = self.getLegalMoves()

        # Retorna as coordenadas do movimento realizado pela IA
        return self.getMovementCoords(possibleMoves, paths)

    '''
        Realiza a busca pelos melhores movimentos possíveis da IA dada a sua posição atual
    '''
    def getMoves(self):
        if self.player.keysOnPocket > 0:
            return self.findBestPathToBase(
                const.IA_PLAYABLE_BOARD,
                self.player.position,
                [len(self.board) -1, 0]
            )

        return self.findBestPathToKey(
            const.IA_PLAYABLE_BOARD,
            [len(self.board)-1, 0],
            self.keyList
        )

    '''
        Responsável por verificar os movimentos permitidos para cada peça que IA pode usar
    '''
    def getLegalMoves(self):
        possibleMoves = []
        for piece in [const.KNIGHT_PIECE, const.BISHOP_PIECE, const.ROOK_PIECE]:
            if self.player.onBase:
                for i in range(len(self.board)-1):
                    moves = self.player.possibleMovements(self.board, i, pieceInUse=piece)
                    possibleMoves.append(moves)
                    self.gameState.showMovements(moves)
            else:
                moves = self.player.possibleMovements(self.board, self.player.position[1], pieceInUse=piece)
                possibleMoves.append(moves)
                self.gameState.showMovements(moves)

        return possibleMoves

    '''
        Responsável por retornar os pontos [X, Y] de movimentação da peça da Ia no tabuleiro
    '''
    def getMovementCoords(self, possibleMoves, paths):
        coords = self.getIABestMovement(possibleMoves, paths)

        if coords is None:
            return self.getIANearMovement(possibleMoves, paths)

        return coords

    '''
        Procura o melhor caminho no tabuleiro dada a posição inicial e a posição final de um elemento
    '''
    def pathFinder(self, board, base, keyLocation, pathToBase=False):
        # Cria o nó da base e o nó da localização da chave
        base_node = Node(None, base)
        base_node.g = base_node.h = base_node.f = 0
        key_node = Node(None, keyLocation)
        key_node.g = key_node.h = key_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Adiciona o nó da base na lista
        open_list.append(base_node)

        # Roda até encontrar a chave
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Remove o nó corrente da lista aberta e adiciona a lista de nós próximos
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Encontrou a chave
            if current_node == key_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent

                return path[::-1] # Retorna o caminho até a chave

            # Generate children
            children = []
            for new_position in const.IA_PLAYABLE_MOVEMENTS: # IA movements
                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(board) - 1) or node_position[0] < 0 or node_position[1] > (len(board[len(board)-1]) -1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if board[node_position[0]][node_position[1]] != 0 and not pathToBase:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:
                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - key_node.position[0]) ** 2) + ((child.position[1] - key_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)

    '''
        Procura o melhor caminho dada a posição atual até as chaves
    '''
    def findBestPathToKey(self, board, base, keysLocation):
        base = (12, 6)
        IAMoves = [0, 0]

        paths = []
        for key in keysLocation:
            keyLocation = (key[0], key[1])
            path = self.pathFinder(board, base, keyLocation)
            paths.append({"path" : keyLocation, "len" : len(path)})

        IAMoves = sorted(paths, key = lambda i: i['len'])
        return IAMoves

    '''
        Procura o melhor caminho dada a posição atual até a base da IA
    '''
    def findBestPathToBase(self, board, position, base):
        paths = []

        path = self.pathFinder(
            board,
            (position[0], position[1]),
            (base[0], position[1]),
            pathToBase=True
        )
        paths.append({"path" : path, "len" : len(path)})
        return sorted(paths, key = lambda i: i['len'])

    '''
        Retorna o melhor caminho ate a chave
    '''
    def getIABestMovement(self, possibleMoves, paths):
        for pieceMoves in possibleMoves:
            for move in pieceMoves:
                if move in self.player.IAvisitedNodes:
                    continue

                if move in paths:
                    if abs(self.player.position[0] - move[0]) > const.ADJACENT_MAX_MOVEMENT:
                        continue

                    if abs(self.player.position[1] - move[1]) > const.ADJACENT_MAX_MOVEMENT:
                        continue

                    self.player.IAvisitedNodes.append(move)
                    return move

    '''
        Retorna as coordenadas de caminho mas próxima até as chaves
    '''
    def getIANearMovement(self, possibleMoves, paths):
        nearPaths = []
        for pieceMoves in possibleMoves:
            for move in pieceMoves:
                if move in self.player.IAvisitedNodes:
                    continue

                if abs(self.player.position[0] - move[0]) > const.ADJACENT_MAX_MOVEMENT:
                    continue

                if not self.player.onBase:
                    if abs(self.player.position[1] - move[1]) > const.ADJACENT_MAX_MOVEMENT:
                        continue

                nearPaths.append(move)

        coords = nearPaths[spatial.KDTree(nearPaths).query(paths[0])[1]]
        self.player.IAvisitedNodes.append(coords)
        return coords
