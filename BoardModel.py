class Board():

    '''
    Clockwise from the Top, all directions for each ray
    And then all the knight rotations, it doesn't matter since DIRECTIONS will restrict the rays anyways
    '''
    RAYS = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1),
            (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

    '''
    After generating a full ray in every direction for each piece, restrict it to the following conditions.
    '''
    DIRECTIONS = {"P": lambda index, dx, dy: (8 - index // 8) > 1 and abs(dy) <= 1 and dx == 1,
                  "p": lambda index, dx, dy: (8 - index // 8) < 8 and abs(dy) <= 1 and dx == -1,
                  "n": lambda index, dx, dy: (abs(dx) + abs(dy) == 3) and abs(dx) >= 1 and abs(dy) >= 1,
                  "b": lambda index, dx, dy: abs(dx) == abs(dy),
                  "r": lambda index, dx, dy: dx == 0 or dy == 0,
                  "q": lambda index, dx, dy: dx == 0 or dy == 0 or abs(dx) == abs(dy),
                  "k": lambda index, dx, dy: abs(dx) <= 1 and abs(dy) <= 1}

    default_fen = " " * 64

    def __init__(self, fen=default_fen):
        self.board = []
        self.set_board(fen)

    def __str__(self): # returns FEN str of Board
        result = []

        for i in range(64): # Iterates with index i through all 64 slots
            piece = self.board[i]
            if i != 0 and i % 8 == 0:
                result.append("/")

            if piece != " ": # if it's not a space, append the piece
                result.append(piece)
            elif piece == " ": # if it is a space, append a digit of 1, and if there's already an integer there, add one to it
                if result and result[-1].isdigit():
                    result[-1] = str(int(result[-1]) + 1)
                else:
                    result.append("1")

        return "".join(result)

    def set_board(self, fen):
        self.board = []

        for char in fen:
            if char == "/":
                continue
            elif char.isdigit():
                for _ in range(int(char)):
                    self.board.append(" ")
            else:
                self.board.append(char)

    def move_piece(self, start, end, piece):
        self.board[end] = piece
        self.board[start] = " "

    def index_to_notation(self, index): # chr(97) = "a"
        file = chr(97 + index % 8)
        rank = str(8 - index // 8)
        return file + rank

    def all_moves(self):
        MOVES = {}
        for i in range(64):
            moves = self.moves(i)
            if moves:
                MOVES[str(i)] = moves

        return MOVES

    def moves(self, index):
        PIECE_MOVES = []
        
        for dir in self.RAYS: # for each ray, append it to the piece's moves
            ray = self.rays(dir, index)

            if ray == None or not ray:
                continue
            else:
                PIECE_MOVES.append(ray)

        return PIECE_MOVES # in the form of a list in each direction cycling clockwise from the top

    def rays(self, direction, index):
        piece = self.board[index]

        if piece == " ":
            return None
        
        if piece != "P":
            piece = piece.lower()

        if piece == "k":
            pass

        RAY = []

        dx = direction[0]
        dy = direction[1]

        Rank = 8 - index // 8
        File = index % 8

        originalRank = Rank
        originalFile = File

        while 1 <= Rank <= 8 and 0 <= File < 8: # Extend ray until edge is hit
            endIndex = 8 * (8 - Rank) + File

            if self.DIRECTIONS[piece](endIndex, Rank - originalRank, File - originalFile) and index != endIndex:
                RAY.append(endIndex)

            Rank += dy
            File += dx

        return RAY
        
        

            
