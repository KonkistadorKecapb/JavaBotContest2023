import sys
import numpy as np

from . import randomMove
from . import maxValue as collectMaxValue


def getGreedyMoveFunction(customVisionRadius):
    def getGreedyRadiusMove(board, rowIndex, columnIndex, movesLeft):
        BOARD_SIDE_SIZE = board.shape[0]
        # wrong radius. it must be less (see getGreedyCorrectMoveFunction). Actually correct one
        FULL_BOARD_VISION_RADIUS = BOARD_SIDE_SIZE - 1

        if customVisionRadius < 2:
            return getGreedySimpleMove(board, rowIndex, columnIndex, movesLeft)

        if customVisionRadius >= FULL_BOARD_VISION_RADIUS:
            return getGreedyFullVisionMove(board, rowIndex, columnIndex, movesLeft)

        return getGreedyPartialVisionMove(board, rowIndex, columnIndex, customVisionRadius, movesLeft)

    return getGreedyRadiusMove


def getGreedyCorrectMoveFunction(customVisionRadius):
    def getGreedyRadiusMove(board, rowIndex, columnIndex, movesLeft):
        BOARD_SIDE_SIZE = board.shape[0]
        # Actually incorrect radius calculation (see getGreedyMoveFunction for correct one)
        FULL_BOARD_VISION_RADIUS = max(0 + rowIndex - 1,
                                       0 + columnIndex - 1,
                                       BOARD_SIDE_SIZE - rowIndex - 1,
                                       BOARD_SIDE_SIZE - columnIndex - 1)

        if customVisionRadius < 2:
            return getGreedySimpleMove(board, rowIndex, columnIndex, movesLeft)

        if customVisionRadius >= FULL_BOARD_VISION_RADIUS:
            return getGreedyFullVisionMove(board, rowIndex, columnIndex, movesLeft)

        return getGreedyPartialVisionMove(board, rowIndex, columnIndex, customVisionRadius, movesLeft)

    return getGreedyRadiusMove


def getGreedySimpleMove(board, rowIndex, columnIndex, movesLeft):
    FIRST_PLAYER_IDENTIFIER = -1
    SECOND_PLAYER_IDENTIFIER = -2

    BOARD_SIDE_SIZE = board.shape[0]

    nextRowDiff = 0
    nextColumnDiff = 0
    maxValue = 0

    if rowIndex - 1 >= 0:
        value = board[rowIndex - 1][columnIndex]
        if value > maxValue:
            maxValue = value
            nextRowDiff = -1

    if rowIndex + 1 < BOARD_SIDE_SIZE:
        value = board[rowIndex + 1][columnIndex]
        if value > maxValue:
            maxValue = value
            nextRowDiff = +1

    if columnIndex - 1 >= 0:
        value = board[rowIndex][columnIndex - 1]
        if value > maxValue:
            maxValue = value
            nextRowDiff = 0
            nextColumnDiff = -1

    if columnIndex + 1 < BOARD_SIDE_SIZE:
        value = board[rowIndex][columnIndex + 1]
        if value > maxValue:
            maxValue = value
            nextRowDiff = 0
            nextColumnDiff = +1

    if nextRowDiff == 0 and nextColumnDiff == 0:
        # make custom move in case there is no values greater than 0 around
        return collectMaxValue.getCollectMaxValuesMove(board, rowIndex, columnIndex, movesLeft)

    nextRowIndex = rowIndex + nextRowDiff
    nextColumnIndex = columnIndex + nextColumnDiff

    nextFieldValue = board[nextRowIndex][nextColumnIndex]
    if nextFieldValue == FIRST_PLAYER_IDENTIFIER or nextFieldValue == SECOND_PLAYER_IDENTIFIER:
        return collectMaxValue.getCollectMaxValuesMove(board, rowIndex, columnIndex, movesLeft)

    return (nextRowIndex, nextColumnIndex)


def getGreedyFullVisionMove(board, rowIndex, columnIndex, movesLeft):

    BOARD_SIDE_SIZE = board.shape[0]
    BOARD_SIZE_WITH_BORDER = BOARD_SIDE_SIZE + 1*2  # board size + both borders

    scoreMatrix = np.zeros((BOARD_SIZE_WITH_BORDER, BOARD_SIZE_WITH_BORDER))
    scoreMatrix[1: BOARD_SIDE_SIZE + 1, 1: BOARD_SIDE_SIZE + 1] = board

    SCORE_MATRIX_PLAYER_ROW_INDEX = rowIndex + 1
    SCORE_MATRIX_PLAYER_COLUMN_INDEX = columnIndex + 1

    FIRST_PLAYER_IDENTIFIER = -1
    SECOND_PLAYER_IDENTIFIER = -2
    if board[rowIndex][columnIndex] == FIRST_PLAYER_IDENTIFIER:
        opponentIdentifier = SECOND_PLAYER_IDENTIFIER
    else:
        opponentIdentifier = FIRST_PLAYER_IDENTIFIER
    opponentPosition = np.where(scoreMatrix == opponentIdentifier)
    opponentRowIndex = opponentPosition[0][0]
    opponentColumnIndex = opponentPosition[1][0]
    scoreMatrix[opponentRowIndex][opponentColumnIndex] = -9999999

    # filling score matrix corners (without vertical and horizontal lines)
    leftUpCornerRowIndex = 0
    while leftUpCornerRowIndex < SCORE_MATRIX_PLAYER_ROW_INDEX:
        downColumnIndex = 1
        while downColumnIndex < SCORE_MATRIX_PLAYER_COLUMN_INDEX:
            scoreMatrix[leftUpCornerRowIndex][downColumnIndex] += max(
                scoreMatrix[leftUpCornerRowIndex - 1][downColumnIndex],
                scoreMatrix[leftUpCornerRowIndex][downColumnIndex - 1])

            downColumnIndex += 1
        leftUpCornerRowIndex += 1

    rightUpCornerRowIndex = 0
    while rightUpCornerRowIndex < SCORE_MATRIX_PLAYER_ROW_INDEX:
        downColumnIndex = BOARD_SIZE_WITH_BORDER - 2
        while downColumnIndex > SCORE_MATRIX_PLAYER_COLUMN_INDEX:
            scoreMatrix[rightUpCornerRowIndex][downColumnIndex] += max(
                scoreMatrix[rightUpCornerRowIndex - 1][downColumnIndex],
                scoreMatrix[rightUpCornerRowIndex][downColumnIndex + 1])

            downColumnIndex -= 1
        rightUpCornerRowIndex += 1

    leftDownCorderRowIndex = BOARD_SIZE_WITH_BORDER - 2
    while leftDownCorderRowIndex > SCORE_MATRIX_PLAYER_ROW_INDEX:
        downColumnIndex = 1
        while downColumnIndex < SCORE_MATRIX_PLAYER_COLUMN_INDEX:
            scoreMatrix[leftDownCorderRowIndex][downColumnIndex] += max(
                scoreMatrix[leftDownCorderRowIndex + 1][downColumnIndex],
                scoreMatrix[leftDownCorderRowIndex][downColumnIndex - 1])

            downColumnIndex += 1
        leftDownCorderRowIndex -= 1

    rightDownCorderRowIndex = BOARD_SIZE_WITH_BORDER - 2
    while rightDownCorderRowIndex > SCORE_MATRIX_PLAYER_ROW_INDEX:
        downColumnIndex = BOARD_SIZE_WITH_BORDER - 2
        while downColumnIndex > SCORE_MATRIX_PLAYER_COLUMN_INDEX:
            scoreMatrix[rightDownCorderRowIndex][downColumnIndex] += max(
                scoreMatrix[rightDownCorderRowIndex + 1][downColumnIndex],
                scoreMatrix[rightDownCorderRowIndex][downColumnIndex + 1])

            downColumnIndex -= 1
        rightDownCorderRowIndex -= 1

    # filling cross (vertical and horizontal lines)
    upRowIndex = 1
    while upRowIndex < SCORE_MATRIX_PLAYER_ROW_INDEX:
        scoreMatrix[upRowIndex][SCORE_MATRIX_PLAYER_COLUMN_INDEX] += max(
            scoreMatrix[upRowIndex - 1][SCORE_MATRIX_PLAYER_COLUMN_INDEX],
            scoreMatrix[upRowIndex][SCORE_MATRIX_PLAYER_COLUMN_INDEX - 1],
            scoreMatrix[upRowIndex][SCORE_MATRIX_PLAYER_COLUMN_INDEX + 1])
        upRowIndex += 1

    downRowIndex = BOARD_SIZE_WITH_BORDER - 2
    while downRowIndex > SCORE_MATRIX_PLAYER_ROW_INDEX:
        scoreMatrix[downRowIndex][SCORE_MATRIX_PLAYER_COLUMN_INDEX] += max(
            scoreMatrix[downRowIndex + 1][SCORE_MATRIX_PLAYER_COLUMN_INDEX],
            scoreMatrix[downRowIndex][SCORE_MATRIX_PLAYER_COLUMN_INDEX - 1],
            scoreMatrix[downRowIndex][SCORE_MATRIX_PLAYER_COLUMN_INDEX + 1])
        downRowIndex -= 1

    leftColumnIndex = 1
    while leftColumnIndex < SCORE_MATRIX_PLAYER_COLUMN_INDEX:
        scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX][leftColumnIndex] += max(
            scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX][leftColumnIndex - 1],
            scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX + 1][leftColumnIndex],
            scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX - 1][leftColumnIndex])
        leftColumnIndex += 1

    rightColumnIndex = BOARD_SIZE_WITH_BORDER - 2
    while rightColumnIndex > SCORE_MATRIX_PLAYER_COLUMN_INDEX:
        scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX][rightColumnIndex] += max(
            scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX][rightColumnIndex + 1],
            scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX + 1][rightColumnIndex],
            scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX - 1][rightColumnIndex])
        rightColumnIndex -= 1

    # getting max score direction and return new indexes
    upRowIndex = SCORE_MATRIX_PLAYER_ROW_INDEX - 1
    if upRowIndex < 1:
        upScore = -1000
    else:
        upScore = scoreMatrix[upRowIndex][SCORE_MATRIX_PLAYER_COLUMN_INDEX]

    downRowIndex = SCORE_MATRIX_PLAYER_ROW_INDEX + 1
    if downRowIndex > BOARD_SIZE_WITH_BORDER - 1:
        downScore = -1000
    else:
        downScore = scoreMatrix[downRowIndex][SCORE_MATRIX_PLAYER_COLUMN_INDEX]

    leftColumnIndex = SCORE_MATRIX_PLAYER_COLUMN_INDEX - 1
    if leftColumnIndex < 1:
        leftScore = -1000
    else:
        leftScore = scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX][leftColumnIndex]

    rightColumnIndex = SCORE_MATRIX_PLAYER_COLUMN_INDEX + 1
    if rightColumnIndex > BOARD_SIZE_WITH_BORDER - 1:
        rightScore = -1000
    else:
        rightScore = scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX][rightColumnIndex]

    directionList = [upScore, downScore, leftScore, rightScore]
    maxIndex = np.argmax(directionList)

    if directionList[maxIndex] < 1:
        return randomMove.getRandomMove(board, rowIndex, columnIndex, movesLeft)

    match maxIndex:
        case 0: return (rowIndex - 1, columnIndex)
        case 1: return (rowIndex + 1, columnIndex)
        case 2: return (rowIndex, columnIndex - 1)
        case 3: return (rowIndex, columnIndex + 1)


def getGreedyPartialVisionMove(board, rowIndex, columnIndex, visionRadius, movesLeft):
    CENTER_SIZE = 1
    BOARD_SIDE_SIZE = board.shape[0]

    if visionRadius > BOARD_SIDE_SIZE - 1:
        sys.exit(
            f"ERROR: Invalid size of radius. Try to use full vision. Board size: {BOARD_SIDE_SIZE}, Radius: {visionRadius}")
    if visionRadius < 2:
        sys.exit(
            f"ERROR: Radius must be greater than 2. Radius: {visionRadius}")

    VISION_DIAMETER = visionRadius*2 + CENTER_SIZE

    EXTENDED_SCORE_MATRIX_SIDE_SIZE = BOARD_SIDE_SIZE * 2 + CENTER_SIZE
    EXTENDED_SCORE_MATRIX_CENTER_INDEX = EXTENDED_SCORE_MATRIX_SIDE_SIZE // 2

    extendedScoreMatrix = np.zeros(
        (EXTENDED_SCORE_MATRIX_SIDE_SIZE, EXTENDED_SCORE_MATRIX_SIDE_SIZE))

    startBoardRowIndex = EXTENDED_SCORE_MATRIX_CENTER_INDEX - rowIndex
    endBoardRowIndex = startBoardRowIndex + BOARD_SIDE_SIZE
    startBoardColumnIndex = EXTENDED_SCORE_MATRIX_CENTER_INDEX - columnIndex
    endBoardColumnIndex = startBoardColumnIndex + BOARD_SIDE_SIZE
    extendedScoreMatrix[startBoardRowIndex:endBoardRowIndex,
                        startBoardColumnIndex:endBoardColumnIndex] = board

    startVisionIndex = EXTENDED_SCORE_MATRIX_CENTER_INDEX - visionRadius
    endVisionIndex = startVisionIndex + VISION_DIAMETER
    scoreMatrix = extendedScoreMatrix[startVisionIndex:endVisionIndex,
                                      startVisionIndex:endVisionIndex]
    SCORE_MATRIX_CENTER_INDEX = scoreMatrix.shape[0] // 2
    SCORE_MATRIX_BOTTOM_INDEX = scoreMatrix.shape[0] - 1
    SCORE_MATRIX_RIGHT_INDEX = SCORE_MATRIX_BOTTOM_INDEX

    FIRST_PLAYER_IDENTIFIER = -1
    SECOND_PLAYER_IDENTIFIER = -2
    if board[rowIndex][columnIndex] == FIRST_PLAYER_IDENTIFIER:
        opponentIdentifier = SECOND_PLAYER_IDENTIFIER
    else:
        opponentIdentifier = FIRST_PLAYER_IDENTIFIER
    opponentPosition = np.where(scoreMatrix == opponentIdentifier)
    if len(opponentPosition[0]) > 0:
        opponentRowIndex = opponentPosition[0][0]
        opponentColumnIndex = opponentPosition[1][0]
        scoreMatrix[opponentRowIndex][opponentColumnIndex] = -9999999

    zeroUpRowIndex = 0
    columnThreshold = SCORE_MATRIX_CENTER_INDEX

    while zeroUpRowIndex < SCORE_MATRIX_CENTER_INDEX:
        zeroDownRowIndex = SCORE_MATRIX_BOTTOM_INDEX - zeroUpRowIndex

        zeroLeftColumnIndex = 0
        while zeroLeftColumnIndex < columnThreshold:
            zeroRightColumnIndex = SCORE_MATRIX_RIGHT_INDEX - zeroLeftColumnIndex

            scoreMatrix[zeroUpRowIndex][zeroLeftColumnIndex] = 0
            scoreMatrix[zeroUpRowIndex][zeroRightColumnIndex] = 0
            scoreMatrix[zeroDownRowIndex][zeroLeftColumnIndex] = 0
            scoreMatrix[zeroDownRowIndex][zeroRightColumnIndex] = 0

            zeroLeftColumnIndex += 1

        columnThreshold -= 1
        zeroUpRowIndex += 1

    scoreUpperCornersRowIndex = 1
    scoreLeftUpperCornerFillingStartIndex = SCORE_MATRIX_CENTER_INDEX - 1
    while scoreUpperCornersRowIndex < SCORE_MATRIX_CENTER_INDEX:
        scoreBottomCornersRowIndex = SCORE_MATRIX_BOTTOM_INDEX - scoreUpperCornersRowIndex

        scoreLeftColumnIndex = scoreLeftUpperCornerFillingStartIndex
        while scoreLeftColumnIndex < SCORE_MATRIX_CENTER_INDEX:
            scoreRightColumnIndex = SCORE_MATRIX_RIGHT_INDEX - scoreLeftColumnIndex

            scoreMatrix[scoreUpperCornersRowIndex][scoreLeftColumnIndex] += max(
                scoreMatrix[scoreUpperCornersRowIndex][scoreLeftColumnIndex - 1],
                scoreMatrix[scoreUpperCornersRowIndex - 1][scoreLeftColumnIndex])

            scoreMatrix[scoreUpperCornersRowIndex][scoreRightColumnIndex] += max(
                scoreMatrix[scoreUpperCornersRowIndex][scoreRightColumnIndex + 1],
                scoreMatrix[scoreUpperCornersRowIndex - 1][scoreRightColumnIndex])

            scoreMatrix[scoreBottomCornersRowIndex][scoreLeftColumnIndex] += max(
                scoreMatrix[scoreBottomCornersRowIndex][scoreLeftColumnIndex - 1],
                scoreMatrix[scoreBottomCornersRowIndex + 1][scoreLeftColumnIndex])

            scoreMatrix[scoreBottomCornersRowIndex][scoreRightColumnIndex] += max(
                scoreMatrix[scoreBottomCornersRowIndex][scoreRightColumnIndex + 1],
                scoreMatrix[scoreBottomCornersRowIndex + 1][scoreRightColumnIndex])

            scoreLeftColumnIndex += 1

        scoreLeftUpperCornerFillingStartIndex -= 1
        scoreUpperCornersRowIndex += 1

    upperVerticalIndex = 1
    while upperVerticalIndex < SCORE_MATRIX_CENTER_INDEX:
        bottomVerticalIndex = SCORE_MATRIX_BOTTOM_INDEX - upperVerticalIndex
        leftHorizontalIndex = upperVerticalIndex
        rightHorizontalIndex = SCORE_MATRIX_RIGHT_INDEX - upperVerticalIndex

        scoreMatrix[upperVerticalIndex][SCORE_MATRIX_CENTER_INDEX] += max(
            scoreMatrix[upperVerticalIndex - 1][SCORE_MATRIX_CENTER_INDEX],
            scoreMatrix[upperVerticalIndex][SCORE_MATRIX_CENTER_INDEX - 1],
            scoreMatrix[upperVerticalIndex][SCORE_MATRIX_CENTER_INDEX + 1])

        scoreMatrix[bottomVerticalIndex][SCORE_MATRIX_CENTER_INDEX] += max(
            scoreMatrix[bottomVerticalIndex + 1][SCORE_MATRIX_CENTER_INDEX],
            scoreMatrix[bottomVerticalIndex][SCORE_MATRIX_CENTER_INDEX - 1],
            scoreMatrix[bottomVerticalIndex][SCORE_MATRIX_CENTER_INDEX + 1])

        scoreMatrix[SCORE_MATRIX_CENTER_INDEX][leftHorizontalIndex] += max(
            scoreMatrix[SCORE_MATRIX_CENTER_INDEX][leftHorizontalIndex - 1],
            scoreMatrix[SCORE_MATRIX_CENTER_INDEX - 1][leftHorizontalIndex],
            scoreMatrix[SCORE_MATRIX_CENTER_INDEX + 1][leftHorizontalIndex])

        scoreMatrix[SCORE_MATRIX_CENTER_INDEX][rightHorizontalIndex] += max(
            scoreMatrix[SCORE_MATRIX_CENTER_INDEX][rightHorizontalIndex + 1],
            scoreMatrix[SCORE_MATRIX_CENTER_INDEX - 1][rightHorizontalIndex],
            scoreMatrix[SCORE_MATRIX_CENTER_INDEX + 1][rightHorizontalIndex])

        upperVerticalIndex += 1

    shortCenterName = SCORE_MATRIX_CENTER_INDEX  # required for autoformatting
    upperScore = scoreMatrix[shortCenterName - 1][shortCenterName]
    bottomScore = scoreMatrix[shortCenterName + 1][shortCenterName]
    leftScore = scoreMatrix[shortCenterName][shortCenterName - 1]
    rightScore = scoreMatrix[shortCenterName][shortCenterName + 1]

    directionList = [upperScore, bottomScore, leftScore, rightScore]
    maxIndex = np.argmax(directionList)

    if directionList[maxIndex] < 1:
        return randomMove.getRandomMove(board, rowIndex, columnIndex, movesLeft)

    match maxIndex:
        case 0: return (rowIndex - 1, columnIndex)
        case 1: return (rowIndex + 1, columnIndex)
        case 2: return (rowIndex, columnIndex - 1)
        case 3: return (rowIndex, columnIndex + 1)


def getGreedyFloatingRadiusMove(board, rowIndex, columnIndex, movesLeft):
    BOARD_SIDE_SIZE = board.shape[0]
    FULL_BOARD_VISION_RADIUS = BOARD_SIDE_SIZE - 1
    CURRENT_RADIUS_VISION = movesLeft

    if CURRENT_RADIUS_VISION < 2:
        return getGreedySimpleMove(board, rowIndex, columnIndex, movesLeft)

    if CURRENT_RADIUS_VISION >= FULL_BOARD_VISION_RADIUS:
        return getGreedyFullVisionMove(board, rowIndex, columnIndex, movesLeft)

    return getGreedyPartialVisionMove(board, rowIndex, columnIndex, CURRENT_RADIUS_VISION, movesLeft)
