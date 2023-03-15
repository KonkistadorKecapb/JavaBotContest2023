import random
import numpy as np

WALL_NUMBER = -16
# WALL_IDENTIFIER = -666
WALL_IDENTIFIER = WALL_NUMBER


def generateSymmetricBoard(boardSideSize, firstPlayerIdentifier, secondPlayerIdentifier):
    BOARD_SIDE_SIZE = boardSideSize
    FIRST_PLAYER_IDENTIFIER = firstPlayerIdentifier
    SECOND_PLAYER_IDENTIFIER = secondPlayerIdentifier

    board = generateBoard(BOARD_SIDE_SIZE, FIRST_PLAYER_IDENTIFIER)
    symmetricPart = board[0:BOARD_SIDE_SIZE//2]
    upSideDown = np.rot90(symmetricPart, 2)

    board[BOARD_SIDE_SIZE//2 + 1:] = upSideDown
    board[BOARD_SIDE_SIZE - 1, BOARD_SIDE_SIZE - 1] = SECOND_PLAYER_IDENTIFIER

    return board


def generateBoard(boardSideSize, firstPlayerIdentifier):
    BOARD_SIDE_SIZE = boardSideSize
    FIRST_PLAYER_IDENTIFIER = firstPlayerIdentifier

    RANDOM_VALUE_FUNCTION_TYPE = random.randint(0, 1)

    # board = np.random.randint(
    #     low=0,
    #     high=9,
    #     size=(BOARD_SIDE_SIZE, BOARD_SIDE_SIZE))

    board = np.zeros((BOARD_SIDE_SIZE, BOARD_SIDE_SIZE))
    getRandomValue = getRandomValueFunction(RANDOM_VALUE_FUNCTION_TYPE)

    for rowIndex in range(0, board.shape[0]):
        for columnIndex in range(0, board.shape[1]):
            board[rowIndex][columnIndex] = getRandomValue()

    # playerRowIndex = playerColumnIndex = BOARD_SIDE_SIZE // 2
    playerRowIndex = playerColumnIndex = 0
    board[playerRowIndex][playerColumnIndex] = FIRST_PLAYER_IDENTIFIER

    return board


def generateActualGameBoard(boardSideSize, firstPlayerIdentifier, secondPlayerIdentifier):
    BOARD_SIDE_SIZE = boardSideSize
    FIRST_PLAYER_IDENTIFIER = firstPlayerIdentifier
    SECOND_PLAYER_IDENTIFIER = secondPlayerIdentifier

    MAX_CELL_VALUE = 50

    MIN_WALL_LENGTH = 3
    MAX_WALL_LENGTH = 7
    MIN_WALLS_AT_HALF = 5
    MAX_WALLS_AT_HALF = 15

    # !!! must be commented because of wrong implementation in the original java project !!!
    # board = np.zeros((BOARD_SIDE_SIZE, BOARD_SIDE_SIZE))
    # !!! ones required because of wrong implementation in the original java project !!!
    board = np.ones((BOARD_SIDE_SIZE, BOARD_SIDE_SIZE))
    for rowIndex in range(0, BOARD_SIDE_SIZE):
        for columnIndex in range(0, BOARD_SIDE_SIZE):
            # !!! required because of wrong implementation in the original java project !!!
            board[rowIndex][columnIndex] = 0
            if random.randint(0, 3) == 0:
                cellValue = random.randint(0, MAX_CELL_VALUE - 1)

                symmetricRowIndex = BOARD_SIDE_SIZE - rowIndex - 1
                symmetricColumnIndex = BOARD_SIDE_SIZE - columnIndex - 1

                board[rowIndex][columnIndex] = cellValue
                board[symmetricRowIndex][symmetricColumnIndex] = cellValue

    wallsNumber = MIN_WALLS_AT_HALF + \
        random.randint(0, MAX_WALLS_AT_HALF - MIN_WALLS_AT_HALF - 1)
    for k in range(0, wallsNumber):
        wallLength = MIN_WALL_LENGTH + \
            random.randint(0, MAX_WALL_LENGTH - MIN_WALL_LENGTH - 1)
        randomI = random.randint(0, BOARD_SIDE_SIZE - 1)
        randomJ = random.randint(0, BOARD_SIDE_SIZE // 2)
        isHorizontal = random.randint(0, 1) == 0
        for l in range(0, wallLength - 1):
            i, j = randomI, randomJ
            if isHorizontal:
                j = j - l
            else:
                i = i - l

            if i <= 0 or j <= 0:
                break

            if i >= BOARD_SIDE_SIZE or j >= BOARD_SIDE_SIZE:
                break

            board[i][j] = WALL_NUMBER
            board[BOARD_SIDE_SIZE - i - 1][BOARD_SIDE_SIZE - j - 1] = WALL_NUMBER

    board[0][0] = FIRST_PLAYER_IDENTIFIER
    board[BOARD_SIDE_SIZE - 1][BOARD_SIDE_SIZE - 1] = SECOND_PLAYER_IDENTIFIER

    # !!! required to reset non-symmetrical values because of wrong implementation in the original java project !!!
    for i in range(0, BOARD_SIDE_SIZE):
        for j in range(0, BOARD_SIDE_SIZE):
            if not (board[i][j] == FIRST_PLAYER_IDENTIFIER or board[i][j] == SECOND_PLAYER_IDENTIFIER):
                if board[i][j] != board[BOARD_SIDE_SIZE - i - 1][BOARD_SIDE_SIZE - j - 1]:
                    board[i][j] = 0
                    board[BOARD_SIDE_SIZE - i - 1][BOARD_SIDE_SIZE - j - 1] = 0

    return board


def getRandomValueFunction(randomType):
    if randomType == 1:
        return getHighRandomValue

    return getLowRandomValue


def getLowRandomValue():
    value = random.random()

    if value < 0.1:
        return WALL_IDENTIFIER
    if value < 0.3:
        return 0
    if value < 0.4:
        return 1
    if value < 0.5:
        return 2
    if value < 0.6:
        return 3
    if value < 0.7:
        return 4
    if value < 0.8:
        return 5
    if value < 0.88:
        return 6
    if value < 0.94:
        return 7
    if value < 0.98:
        return 8
    return 9


def getHighRandomValue():
    value = random.random()

    if value < 0.2:
        return WALL_IDENTIFIER
    if value < 0.8:
        return 0
    if value < 0.90:
        return 5
    if value < 0.95:
        return 15
    if value < 0.97:
        return 25
    if value < 0.985:
        return 30
    if value < 0.99:
        return 35
    if value < 0.997:
        return 40
    return 50
