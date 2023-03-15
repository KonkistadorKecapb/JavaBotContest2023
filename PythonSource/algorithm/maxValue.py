import numpy as np

from . import randomMove


def getCollectMaxValuesMove(board, rowIndex, columnIndex, movesLeft):
    FIRST_PLAYER_IDENTIFIER = -1
    SECOND_PLAYER_IDENTIFIER = -2

    BOARD_SIDE_SIZE = board.shape[1]

    indexOfMaxValue = np.argmax(board)
    maxValueRowIndex = indexOfMaxValue // BOARD_SIDE_SIZE
    maxValueColumnIndex = indexOfMaxValue - maxValueRowIndex * BOARD_SIDE_SIZE

    # finding direction of max value
    rowIndexDiff = rowIndex - maxValueRowIndex
    columnIndexDiff = columnIndex - maxValueColumnIndex

    nextRowDiff = 0
    if rowIndexDiff < 0:
        nextRowDiff = +1
    if rowIndexDiff > 0:
        nextRowDiff = -1

    nextColumnDiff = 0
    if columnIndexDiff < 0:
        nextColumnDiff = +1
    if columnIndexDiff > 0:
        nextColumnDiff = -1

    # take local max value (from 2 values) while going to global max value
    if (nextRowDiff != 0) and (nextColumnDiff != 0):
        if board[rowIndex + nextRowDiff][columnIndex] > board[rowIndex][columnIndex + nextColumnDiff]:
            nextColumnDiff = 0
        else:
            nextRowDiff = 0

    if nextRowDiff == 0 and nextColumnDiff == 0:
        return (rowIndex, columnIndex)

    nextRowIndex = rowIndex + nextRowDiff
    nextColumnIndex = columnIndex + nextColumnDiff

    nextFieldValue = board[nextRowIndex][nextColumnIndex]
    if nextFieldValue == FIRST_PLAYER_IDENTIFIER or nextFieldValue == SECOND_PLAYER_IDENTIFIER:
        return randomMove.getRandomMove(board, rowIndex, columnIndex, movesLeft)

    return (nextRowIndex, nextColumnIndex)
