import sys
import random
import numpy as np

from . import greedy
from . import randomMove


def getBestAlgorithmCascadeMove(board, rowIndex, columnIndex, movesLeft):
    nextPoint = greedy.getGreedySimpleMove(board,
                                           rowIndex,
                                           columnIndex,
                                           movesLeft)

    if board[nextPoint[0]][nextPoint[1]] > 0:
        return nextPoint
    else:
        return greedy.getGreedyFullVisionMove(board, rowIndex, columnIndex, movesLeft)


def getBestAlgorithmCascadeMove2(board, rowIndex, columnIndex, movesLeft):
    nextPoint = greedy.getGreedyMoveFunction(2)(board,
                                                rowIndex,
                                                columnIndex,
                                                movesLeft)

    if board[nextPoint[0]][nextPoint[1]] > 0:
        return nextPoint
    else:
        return greedy.getGreedyFullVisionMove(board, rowIndex, columnIndex, movesLeft)


def getBestAlgorithmCascadeMove3(board, rowIndex, columnIndex, movesLeft):
    nextPoint = greedy.getGreedyMoveFunction(3)(board,
                                                rowIndex,
                                                columnIndex,
                                                movesLeft)

    if board[nextPoint[0]][nextPoint[1]] > 0:
        return nextPoint
    else:
        return greedy.getGreedyFullVisionMove(board, rowIndex, columnIndex, movesLeft)


def getBestAlgorithmCascadeMove4(board, rowIndex, columnIndex, movesLeft):
    nextPoint = greedy.getGreedyMoveFunction(4)(board,
                                                rowIndex,
                                                columnIndex,
                                                movesLeft)

    if board[nextPoint[0]][nextPoint[1]] > 0:
        return nextPoint
    else:
        return greedy.getGreedyFullVisionMove(board, rowIndex, columnIndex, movesLeft)


def getBestAlgorithmCascadeMove5(board, rowIndex, columnIndex, movesLeft):
    nextPoint = greedy.getGreedyMoveFunction(5)(board,
                                                rowIndex,
                                                columnIndex,
                                                movesLeft)

    if board[nextPoint[0]][nextPoint[1]] > 0:
        return nextPoint
    else:
        return greedy.getGreedyFullVisionMove(board, rowIndex, columnIndex, movesLeft)


def getBestAlgorithmCascadeMove8(board, rowIndex, columnIndex, movesLeft):
    nextPoint = greedy.getGreedyMoveFunction(8)(board,
                                                rowIndex,
                                                columnIndex,
                                                movesLeft)

    if board[nextPoint[0]][nextPoint[1]] > 0:
        return nextPoint
    else:
        return greedy.getGreedyFullVisionMove(board, rowIndex, columnIndex, movesLeft)


def getBestAlgorithmCascadeMove10(board, rowIndex, columnIndex, movesLeft):
    nextPoint = greedy.getGreedyMoveFunction(10)(board,
                                                 rowIndex,
                                                 columnIndex,
                                                 movesLeft)

    if board[nextPoint[0]][nextPoint[1]] > 0:
        return nextPoint
    else:
        return greedy.getGreedyFullVisionMove(board, rowIndex, columnIndex, movesLeft)


def getBestAlgorithmCascadeMove13(board, rowIndex, columnIndex, movesLeft):
    nextPoint = greedy.getGreedyMoveFunction(13)(board,
                                                 rowIndex,
                                                 columnIndex,
                                                 movesLeft)

    if board[nextPoint[0]][nextPoint[1]] > 0:
        return nextPoint
    else:
        return greedy.getGreedyFullVisionMove(board, rowIndex, columnIndex, movesLeft)


def getBestAlgorithmCascadeFloatingMove(board, rowIndex, columnIndex, movesLeft):
    if movesLeft > 20:
        return getBestAlgorithmCascadeMove(board, rowIndex, columnIndex, movesLeft)

    return greedy.getGreedyFloatingRadiusMove(board, rowIndex, columnIndex, movesLeft)


def getBestAlgorithmCascadeFloatingMove2(board, rowIndex, columnIndex, movesLeft):
    if movesLeft > 15:
        return getBestAlgorithmCascadeMove(board, rowIndex, columnIndex, movesLeft)

    return greedy.getGreedyFloatingRadiusMove(board, rowIndex, columnIndex, movesLeft)


def getBestAlgorithmCascadeFloatingMove3(board, rowIndex, columnIndex, movesLeft):
    if movesLeft > 10:
        return getBestAlgorithmCascadeMove(board, rowIndex, columnIndex, movesLeft)

    return greedy.getGreedyFloatingRadiusMove(board, rowIndex, columnIndex, movesLeft)


def getBestAlgorithmCascadeFloatingMove4(board, rowIndex, columnIndex, movesLeft):
    if movesLeft > 5:
        return getBestAlgorithmCascadeMove(board, rowIndex, columnIndex, movesLeft)

    return greedy.getGreedyFloatingRadiusMove(board, rowIndex, columnIndex, movesLeft)


def getBestAlgorithmCascadeFloatingMove5(board, rowIndex, columnIndex, movesLeft):
    if movesLeft > 25:
        return getBestAlgorithmCascadeMove(board, rowIndex, columnIndex, movesLeft)

    return greedy.getGreedyFloatingRadiusMove(board, rowIndex, columnIndex, movesLeft)


def getBestAlgorithmCascadeFloatingMove6(board, rowIndex, columnIndex, movesLeft):
    if movesLeft > 30:
        return getBestAlgorithmCascadeMove(board, rowIndex, columnIndex, movesLeft)

    return greedy.getGreedyFloatingRadiusMove(board, rowIndex, columnIndex, movesLeft)


def getBestAlgorithmCascadeFloatingMove7(board, rowIndex, columnIndex, movesLeft):
    if movesLeft > 35:
        return getBestAlgorithmCascadeMove(board, rowIndex, columnIndex, movesLeft)

    return greedy.getGreedyFloatingRadiusMove(board, rowIndex, columnIndex, movesLeft)


def getBestAlgorithmCascadeFloatingMove8(board, rowIndex, columnIndex, movesLeft):
    if movesLeft > 40:
        return getBestAlgorithmCascadeMove(board, rowIndex, columnIndex, movesLeft)

    return greedy.getGreedyFloatingRadiusMove(board, rowIndex, columnIndex, movesLeft)


def getBestAlgorithmCascadeDynamicFloatingMove(board, rowIndex, columnIndex, movesLeft):
    if movesLeft > 20:
        nextPoint = getGreedySimpleMove_cascade(board,
                                                rowIndex,
                                                columnIndex)

        if board[nextPoint[0]][nextPoint[1]] > 0:
            return nextPoint

        nextRowIndex, nextColumnIndex = getGreedyFullVisionMove_cascade(board,
                                                                        rowIndex,
                                                                        columnIndex)
        if nextRowIndex != rowIndex or nextColumnIndex != columnIndex:
            return (nextRowIndex, nextColumnIndex)
    else:
        nextRowIndex, nextColumnIndex = getGreedyFloatingRadiusMove_cascade(board,
                                                                            rowIndex,
                                                                            columnIndex,
                                                                            movesLeft)
        if nextRowIndex != rowIndex or nextColumnIndex != columnIndex:
            return (nextRowIndex, nextColumnIndex)

    radiusVision = 4
    while radiusVision > 1:
        nextRowIndex, nextColumnIndex = getGreedyPartialVisionMove_cascade(board,
                                                                           rowIndex,
                                                                           columnIndex,
                                                                           radiusVision)
        if nextRowIndex != rowIndex or nextColumnIndex != columnIndex:
            return (nextRowIndex, nextColumnIndex)

        radiusVision -= 1

    return getRandomMove_cascade(board, rowIndex, columnIndex)


def getRandomMove_cascade(board, rowIndex, columnIndex):
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


def getGreedySimpleMove_cascade(board, rowIndex, columnIndex):
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

    nextRowIndex = rowIndex + nextRowDiff
    nextColumnIndex = columnIndex + nextColumnDiff

    return (nextRowIndex, nextColumnIndex)


def getGreedyFullVisionMove_cascade(board, rowIndex, columnIndex):

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
    scoreMatrix[opponentRowIndex][opponentColumnIndex] = -99  # -9999999

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

    return getNearestDirection(board, rowIndex, columnIndex, upScore, downScore, leftScore, rightScore)


def getGreedyPartialVisionMove_cascade(board, rowIndex, columnIndex, visionRadius):
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

    return getNearestDirection(board, rowIndex, columnIndex, upperScore, bottomScore, leftScore, rightScore)


def getNearestDirection(board, rowIndex, columnIndex, upperScore, bottomScore, leftScore, rightScore):
    # directionList = [upperScore, bottomScore, leftScore, rightScore]
    # maxIndex = np.argmax(directionList)

    # if directionList[maxIndex] < 1:
    #     return randomMove.getRandomMove(board, rowIndex, columnIndex, 1000)

    # match maxIndex:
    #     case 0: return (rowIndex - 1, columnIndex)
    #     case 1: return (rowIndex + 1, columnIndex)
    #     case 2: return (rowIndex, columnIndex - 1)
    #     case 3: return (rowIndex, columnIndex + 1)

    maxValue = max(upperScore, bottomScore, leftScore, rightScore)

    if maxValue < 1:
        return (rowIndex, columnIndex)

    countOfMaxValues = 0
    if upperScore == maxValue:
        countOfMaxValues += 1
    if bottomScore == maxValue:
        countOfMaxValues += 1
    if leftScore == maxValue:
        countOfMaxValues += 1
    if rightScore == maxValue:
        countOfMaxValues += 1

    if countOfMaxValues == 1:
        if upperScore == maxValue:
            return (rowIndex - 1, columnIndex)
        elif bottomScore == maxValue:
            return (rowIndex + 1, columnIndex)
        elif leftScore == maxValue:
            return (rowIndex, columnIndex - 1)
        else:
            return (rowIndex, columnIndex + 1)

    BOARD_SIDE_SIZE = board.shape[0]

    nearestUpperLength = 1000
    if upperScore == maxValue:
        nearestRowIndex = rowIndex - 1
        while nearestRowIndex >= 0:
            if board[nearestRowIndex][columnIndex] > 0:
                length = rowIndex - nearestRowIndex
                if length < nearestUpperLength:
                    nearestUpperLength = length
                break

            nearestLeftColumnIndex = columnIndex - 1
            while nearestLeftColumnIndex >= 0:
                if board[nearestRowIndex][nearestLeftColumnIndex] > 0:
                    length = columnIndex - nearestLeftColumnIndex + rowIndex - nearestRowIndex
                    if length < nearestUpperLength:
                        nearestUpperLength = length
                    break
                nearestLeftColumnIndex -= 1

            nearestRightColumnIndex = columnIndex + 1
            while nearestRightColumnIndex < BOARD_SIDE_SIZE:
                if board[nearestRowIndex][nearestRightColumnIndex] > 0:
                    length = nearestRightColumnIndex - columnIndex + rowIndex - nearestRowIndex
                    if length < nearestUpperLength:
                        nearestUpperLength = length
                    break
                nearestRightColumnIndex += 1

            nearestRowIndex -= 1

    nearestBottomLength = 1000
    if bottomScore == maxValue:
        nearestRowIndex = rowIndex + 1
        while nearestRowIndex < BOARD_SIDE_SIZE:
            if board[nearestRowIndex][columnIndex] > 0:
                length = nearestRowIndex - rowIndex
                if length < nearestBottomLength:
                    nearestBottomLength = length
                break

            nearestLeftColumnIndex = columnIndex - 1
            while nearestLeftColumnIndex >= 0:
                if board[nearestRowIndex][nearestLeftColumnIndex] > 0:
                    length = columnIndex - nearestLeftColumnIndex + nearestRowIndex - rowIndex
                    if length < nearestBottomLength:
                        nearestBottomLength = length
                    break
                nearestLeftColumnIndex -= 1

            nearestRightColumnIndex = columnIndex + 1
            while nearestRightColumnIndex < BOARD_SIDE_SIZE:
                if board[nearestRowIndex][nearestRightColumnIndex] > 0:
                    length = nearestRightColumnIndex - columnIndex + nearestRowIndex - rowIndex
                    if length < nearestBottomLength:
                        nearestBottomLength = length
                    break
                nearestRightColumnIndex += 1

            nearestRowIndex += 1

    nearestLeftLength = 1000
    if leftScore == maxValue:
        nearestColumnIndex = columnIndex - 1
        while nearestColumnIndex >= 0:
            if board[rowIndex][nearestColumnIndex] > 0:
                length = columnIndex - nearestColumnIndex
                if length < nearestLeftLength:
                    nearestLeftLength = length
                break

            nearestTopRowIndex = rowIndex - 1
            while nearestTopRowIndex >= 0:
                if board[nearestTopRowIndex][nearestColumnIndex] > 0:
                    length = columnIndex - nearestColumnIndex + rowIndex - nearestTopRowIndex
                    if length < nearestLeftLength:
                        nearestLeftLength = length
                    break
                nearestTopRowIndex -= 1

            nearestBottomRowIndex = rowIndex + 1
            while nearestBottomRowIndex < BOARD_SIDE_SIZE:
                if board[nearestBottomRowIndex][nearestColumnIndex] > 0:
                    length = columnIndex - nearestColumnIndex + nearestBottomRowIndex - rowIndex
                    if length < nearestLeftLength:
                        nearestLeftLength = length
                    break
                nearestBottomRowIndex += 1

            nearestColumnIndex -= 1

    nearestRightLength = 1000
    if rightScore == maxValue:
        nearestColumnIndex = columnIndex + 1
        while nearestColumnIndex < BOARD_SIDE_SIZE:
            if board[rowIndex][nearestColumnIndex] > 0:
                length = nearestColumnIndex - columnIndex
                if length < nearestRightLength:
                    nearestRightLength = length
                break

            nearestTopRowIndex = rowIndex - 1
            while nearestTopRowIndex >= 0:
                if board[nearestTopRowIndex][nearestColumnIndex] > 0:
                    length = nearestColumnIndex - columnIndex + rowIndex - nearestTopRowIndex
                    if length < nearestRightLength:
                        nearestRightLength = length
                    break
                nearestTopRowIndex -= 1

            nearestBottomRowIndex = rowIndex + 1
            while nearestBottomRowIndex < BOARD_SIDE_SIZE:
                if board[nearestBottomRowIndex][nearestColumnIndex] > 0:
                    length = nearestColumnIndex - columnIndex + nearestBottomRowIndex - rowIndex
                    if length < nearestRightLength:
                        nearestRightLength = length
                    break
                nearestBottomRowIndex += 1

            nearestColumnIndex += 1

    # print(nearestUpperLength,
    #       nearestBottomLength,
    #       nearestLeftLength,
    #       nearestRightLength)

    minValue = min(nearestUpperLength,
                   nearestBottomLength,
                   nearestLeftLength,
                   nearestRightLength)

    if nearestUpperLength == minValue:
        return (rowIndex - 1, columnIndex)
    elif nearestBottomLength == minValue:
        return (rowIndex + 1, columnIndex)
    elif nearestLeftLength == minValue:
        return (rowIndex, columnIndex - 1)
    else:
        return (rowIndex, columnIndex + 1)


def getGreedyFloatingRadiusMove_cascade(board, rowIndex, columnIndex, movesLeft):
    BOARD_SIDE_SIZE = board.shape[0]
    FULL_BOARD_VISION_RADIUS = BOARD_SIDE_SIZE - 1
    CURRENT_RADIUS_VISION = movesLeft

    if CURRENT_RADIUS_VISION < 2:
        return getGreedySimpleMove_cascade(board, rowIndex, columnIndex)

    if CURRENT_RADIUS_VISION >= FULL_BOARD_VISION_RADIUS:
        return getGreedyFullVisionMove_cascade(board, rowIndex, columnIndex)

    return getGreedyPartialVisionMove_cascade(board, rowIndex, columnIndex, CURRENT_RADIUS_VISION)


# rowIndex = 2
# colIndex = 2
# board = np.array([
#     [1, 0, 1, 0, 1],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0],
#     [1, 0, 0, 0, 1],
# ])
# res = getNearestDirection(board, rowIndex, colIndex, 1, 0, 0, 1)
# print(res)
