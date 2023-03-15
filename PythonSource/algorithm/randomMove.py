import random


def getRandomMove(board, rowIndex, columnIndex, movesLeft):
    BOARD_SIDE_SIZE = board.shape[0]

    nextMoveList = [
        (rowIndex - 1, columnIndex),
        (rowIndex + 1, columnIndex),
        (rowIndex, columnIndex - 1),
        (rowIndex, columnIndex + 1),
    ]

    while len(nextMoveList) > 0:
        nextMoveIndex = random.randint(0, len(nextMoveList) - 1)
        nextMovePoint = nextMoveList[nextMoveIndex]

        nextRowIndex = nextMovePoint[0]
        nextColumnIndex = nextMovePoint[1]

        if (0 <= nextRowIndex < BOARD_SIDE_SIZE) and (0 <= nextColumnIndex < BOARD_SIDE_SIZE):
            fieldValue = board[nextRowIndex][nextColumnIndex]
            if fieldValue >= 0:
                return (nextRowIndex, nextColumnIndex)

        del nextMoveList[nextMoveIndex]

    return (rowIndex, columnIndex)
