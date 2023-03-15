import sys
import time
import numpy as np

import tournamentTable
import randomBoard

from algorithm import *

FIRST_PLAYER_IDENTIFIER = -1
SECOND_PLAYER_IDENTIFIER = -2

STEP_ON_OPPONENT_PENALTY = -9999999

BOARD_SIDE_SIZE = 11

IS_TESTING_ONLY_FIRST_ALGORITHM = True
COUNT_OF_MOVES = 100
COUNT_OF_BOARDS = 100

WIN_POINTS = 2
DRAW_POINTS = 1
LOSE_POINTS = 0


def makeMove(board, playerRowIndex, playerColumnIndex, getMoveFunction, movesLeft):
    playerIdentifier = board[playerRowIndex][playerColumnIndex]

    score = 0

    nextRowIndex, nextColumnIndex = getMoveFunction(board,
                                                    playerRowIndex,
                                                    playerColumnIndex,
                                                    movesLeft)

    if not (0 <= nextRowIndex < BOARD_SIDE_SIZE) or not (0 <= nextColumnIndex < BOARD_SIDE_SIZE):
        # sys.exit(
        print(
            f"ERROR: Invalid move outside the board. Row: {nextRowIndex}, Column: {nextColumnIndex}, Algorithm: {getMoveFunction}")
        return (0, playerRowIndex, playerColumnIndex)

    if ((playerRowIndex == nextRowIndex) and (abs(playerColumnIndex - nextColumnIndex) == 1)) or \
            ((abs(playerRowIndex - nextRowIndex) == 1) and (playerColumnIndex == nextColumnIndex)):

        board[playerRowIndex][playerColumnIndex] = 0

        playerRowIndex, playerColumnIndex = nextRowIndex, nextColumnIndex

        score = board[playerRowIndex][playerColumnIndex]

        if score == FIRST_PLAYER_IDENTIFIER or score == SECOND_PLAYER_IDENTIFIER:
            return (STEP_ON_OPPONENT_PENALTY, playerRowIndex, playerColumnIndex)
    elif (playerRowIndex == nextRowIndex) and (playerColumnIndex == nextColumnIndex):
        ''
        # print(
        #     f"\n\n\nWARNING: No move. Row: {nextRowIndex}, Column: {nextColumnIndex}")
    else:
        sys.exit(
            f"ERROR: Ineligible move. Row: {playerRowIndex} -> {nextRowIndex}, " +
            f"Column: {playerColumnIndex} -> {nextColumnIndex}, Algorithm: {getMoveFunction}")

    board[playerRowIndex][playerColumnIndex] = playerIdentifier

    return (score, playerRowIndex, playerColumnIndex)


def runSimulation(board, firstPlayerMoveFunction, secondPlayerMoveFunction):
    firstPlayerScore = 0
    firstPlayerRowIndex = 0
    firstPlayerColumnIndex = 0

    secondPlayerScore = 0
    secondPlayerRowIndex = BOARD_SIDE_SIZE - 1
    secondPlayerColumnIndex = BOARD_SIDE_SIZE - 1

    # countOfMoves = 0
    # while countOfMoves < COUNT_OF_MOVES:
    #     countOfMoves += 1
    movesLeft = COUNT_OF_MOVES + 1
    while movesLeft > 0:
        movesLeft -= 1

        firstPlayerMoveReward, firstPlayerNewRowIndex, firstPlayerNewColumnIndex = makeMove(board,
                                                                                            firstPlayerRowIndex,
                                                                                            firstPlayerColumnIndex,
                                                                                            firstPlayerMoveFunction,
                                                                                            movesLeft)
        firstPlayerScore += firstPlayerMoveReward
        firstPlayerRowIndex = firstPlayerNewRowIndex
        firstPlayerColumnIndex = firstPlayerNewColumnIndex

        if firstPlayerMoveReward == STEP_ON_OPPONENT_PENALTY:
            break

        secondPlayerMoveReward, secondPlayerNewRowIndex, secondPlayerNewColumnIndex = makeMove(board,
                                                                                               secondPlayerRowIndex,
                                                                                               secondPlayerColumnIndex,
                                                                                               secondPlayerMoveFunction,
                                                                                               movesLeft)
        secondPlayerScore += secondPlayerMoveReward
        secondPlayerRowIndex = secondPlayerNewRowIndex
        secondPlayerColumnIndex = secondPlayerNewColumnIndex

        if secondPlayerMoveReward == STEP_ON_OPPONENT_PENALTY:
            break

        indexOfMaxValue = np.argmax(board)
        maxValueRowIndex = indexOfMaxValue // BOARD_SIDE_SIZE
        maxValueColumnIndex = indexOfMaxValue - maxValueRowIndex * BOARD_SIDE_SIZE
        if board[maxValueRowIndex][maxValueColumnIndex] <= 0:
            break

    return (firstPlayerScore, secondPlayerScore)


def runGame(board, firstPlayerMoveFunction, secondPlayerMoveFunction):
    firstPlayerGameScore = 0
    secondPlayerGameScore = 0

    game1FirstPlayerSimulationScore, game1SecondPlayerSimulationScore = runSimulation(board.copy(),
                                                                                      firstPlayerMoveFunction,
                                                                                      secondPlayerMoveFunction)
    if game1FirstPlayerSimulationScore > game1SecondPlayerSimulationScore:
        firstPlayerGameScore += 1
    elif game1FirstPlayerSimulationScore < game1SecondPlayerSimulationScore:
        secondPlayerGameScore += 1

    game2SecondPlayerSimulationScore, game2FirstPlayerSimulationScore = runSimulation(board.copy(),
                                                                                      secondPlayerMoveFunction,
                                                                                      firstPlayerMoveFunction)
    if game2FirstPlayerSimulationScore > game2SecondPlayerSimulationScore:
        firstPlayerGameScore += 1
    elif game2FirstPlayerSimulationScore < game2SecondPlayerSimulationScore:
        secondPlayerGameScore += 1

    if firstPlayerGameScore == secondPlayerGameScore:
        result = DRAW_POINTS
    elif firstPlayerGameScore > secondPlayerGameScore:
        result = WIN_POINTS
    else:
        result = LOSE_POINTS

    return (result,
            game1FirstPlayerSimulationScore + game2FirstPlayerSimulationScore,
            game1SecondPlayerSimulationScore + game2SecondPlayerSimulationScore)


def runTournament():
    algorithmList = [
        ('dynamicFloatingCascade', cascade.getBestAlgorithmCascadeDynamicFloatingMove),

        ('bestFloatingCascade', cascade.getBestAlgorithmCascadeFloatingMove),

        # ('bestFloatingCascade7', cascade.getBestAlgorithmCascadeFloatingMove7),
        # ('bestFloatingCascade5', cascade.getBestAlgorithmCascadeFloatingMove5),
        # ('getGreedyFloatingRadiusMove', greedy.getGreedyFloatingRadiusMove),
        # ('bestFloatingCascade2', cascade.getBestAlgorithmCascadeFloatingMove2),
        # ('bestFloatingCascade3', cascade.getBestAlgorithmCascadeFloatingMove3),
        # ('bestFloatingCascade4', cascade.getBestAlgorithmCascadeFloatingMove4),
        # ('bestFloatingCascade6', cascade.getBestAlgorithmCascadeFloatingMove6),
        # ('bestFloatingCascade8', cascade.getBestAlgorithmCascadeFloatingMove8),

        # ('getBestAlgorithmCascadeMove', cascade.getBestAlgorithmCascadeMove),
        # ('getBestAlgorithmCascadeMove2', cascade.getBestAlgorithmCascadeMove2),
        # ('getBestAlgorithmCascadeMove3', cascade.getBestAlgorithmCascadeMove3),

        # ('getBestAlgorithmCascadeMove4', cascade.getBestAlgorithmCascadeMove4),
        # ('getBestAlgorithmCascadeMove5', cascade.getBestAlgorithmCascadeMove5),

        # ('getGreedyMoveFunction(8)', greedy.getGreedyMoveFunction(8)),
        # ('getGreedyMoveFunction(9)', greedy.getGreedyMoveFunction(9)),
        # ('getGreedyMoveFunction(10)', greedy.getGreedyMoveFunction(10)),
        # ('getGreedyMoveFunction(11)', greedy.getGreedyMoveFunction(11)),
        # ('getGreedyMoveFunction(12)', greedy.getGreedyMoveFunction(12)),
        # ('getGreedyMoveFunction(13)', greedy.getGreedyMoveFunction(13)),

        # ('getGreedyCorrectMoveFunction(8)', greedy.getGreedyCorrectMoveFunction(8)),
        # ('getGreedyCorrectMoveFunction(9)', greedy.getGreedyCorrectMoveFunction(9)),

        # ('getGreedyMoveFunction(5)', greedy.getGreedyMoveFunction(5)),
        # ('getGreedyMoveFunction(6)', greedy.getGreedyMoveFunction(6)),
        # ('getGreedyMoveFunction(7)', greedy.getGreedyMoveFunction(7)),

        # ('getGreedyMoveFunction(7)', greedy.getGreedyMoveFunction(7)),
        # ('getGreedyMoveFunction(6)', greedy.getGreedyMoveFunction(6)),
        # ('getGreedyCorrectMoveFunction(6)', greedy.getGreedyCorrectMoveFunction(6)),

        # below are less successful:
        # ('randomMove', randomMove.getRandomMove),
        # ('maxValue', maxValue.getCollectMaxValuesMove),
        # ('getGreedySimpleMove', greedy.getGreedySimpleMove),
        # ('getGreedyFullVisionMove', greedy.getGreedyFullVisionMove),

        # ('getBestAlgorithmCascadeMove8', cascade.getBestAlgorithmCascadeMove8),
        # ('getBestAlgorithmCascadeMove10', cascade.getBestAlgorithmCascadeMove10),
        # ('getBestAlgorithmCascadeMove13', cascade.getBestAlgorithmCascadeMove13),

        # ('getGreedyMoveFunction(10)', greedy.getGreedyMoveFunction(10)),
        # ('getGreedyMoveFunction(8)', greedy.getGreedyMoveFunction(8)),
        # ('getGreedyMoveFunction(9)', greedy.getGreedyMoveFunction(9)),
        # ('getGreedyCorrectMoveFunction(7)', greedy.getGreedyCorrectMoveFunction(7)),
    ]

    # for i in range(2, BOARD_SIDE_SIZE):
    #     algorithmList.append(
    #         (f'getGreedyMoveFunction({i})', greedy.getGreedyMoveFunction(i))
    #     )

    # for i in range(2, BOARD_SIDE_SIZE):
    #     algorithmList.append(
    #         (f'getGreedyCorrectMoveFunction({i})',
    #          greedy.getGreedyCorrectMoveFunction(i))
    #     )

    boardList = []
    for i in range(0, COUNT_OF_BOARDS):
        board = randomBoard.generateActualGameBoard(BOARD_SIDE_SIZE,
                                                    FIRST_PLAYER_IDENTIFIER,
                                                    SECOND_PLAYER_IDENTIFIER)
        boardList.append(board)

    battleResultList = []
    for algorithmIndex, algorithm in enumerate(algorithmList):
        algorithmName = algorithm[0]
        algorithmFunction = algorithm[1]

        print(f"playing {algorithmName} with index {algorithmIndex}")

        algorithmResultList = []

        for opponentIndex in range(algorithmIndex + 1, len(algorithmList)):
            opponentAlgorithm = algorithmList[opponentIndex]
            opponentAlgorithmFunction = opponentAlgorithm[1]

            firstPlayerResultSum = 0
            secondPlayerResultSum = 0
            firstPlayerScoreSum = 0
            secondPlayerScoreSum = 0
            for board in boardList:
                result, firstPlayerScore, secondPlayerScore = runGame(board,
                                                                      algorithmFunction,
                                                                      opponentAlgorithmFunction)
                if result == WIN_POINTS:
                    firstPlayerResultSum += WIN_POINTS
                elif result == LOSE_POINTS:
                    secondPlayerResultSum += WIN_POINTS
                else:
                    firstPlayerResultSum += DRAW_POINTS
                    secondPlayerResultSum += DRAW_POINTS

                firstPlayerScoreSum += firstPlayerScore
                secondPlayerScoreSum += secondPlayerScore

            algorithmResultList.append(
                (firstPlayerResultSum, secondPlayerResultSum, firstPlayerScoreSum, secondPlayerScoreSum))

        battleResultList.append([algorithmName, algorithmResultList])

        if IS_TESTING_ONLY_FIRST_ALGORITHM:
            for opponentIndex in range(algorithmIndex + 1, len(algorithmList)):
                battleResultList.append([algorithmList[opponentIndex][0], []])
            break

    for value in battleResultList:
        print(value)

    tournamentTable.printMultipleResultsAsTable(battleResultList)


# runTournament()


firstPlayerScore = 0
firstPlayerRowIndex = 0
firstPlayerColumnIndex = 0

secondPlayerScore = 0
secondPlayerRowIndex = BOARD_SIDE_SIZE - 1
secondPlayerColumnIndex = BOARD_SIDE_SIZE - 1

# board = randomBoard.generateActualGameBoard(BOARD_SIDE_SIZE,
#                                             FIRST_PLAYER_IDENTIFIER,
#                                             SECOND_PLAYER_IDENTIFIER)

# ???
# stuck in the middle and then ok
# board = np.array([[-1,   0,   0,   0,   0,   0,  14,   0,   0,   0,   0],
#                   [29,   0,  43, -16,   0, -16, -16,  16,  35,   0,   0],
#                   [0,   0,   0, -16,   0, -16,  37,   0,   0,  44,   0],
#                   [0, -16, -16, -16,   0,  15,   7,   0,   0, -16,  39],
#                   [0, -16,   0, -16,  19,   0,   0,   0,   0, -16,   0],
#                   [0,   0,  36, -16,   0,   0,   0, -16,  36,   0,   0],
#                   [0, -16,   0,   0,   0,   0,  19, -16,   0, -16,   0],
#                   [39, -16,   0,   0,   7,  15,   0, -16, -16, -16,   0],
#                   [0,  44,   0,   0,  37, -16,   0, -16,   0,   0,   0],
#                   [0,   0,  35,  16, -16, -16,   0, -16,  43,   0,  29],
#                   [0,   0,   0,   0,  14,   0,   0,   0,   0,   0,  -2]]
#                  )

# ???
# stuck in the middle (seems random sometimes help)
# board = np.array([[-1,   0,   0,   0,   0, -16, -16, -16,   0,   0,  0],
#                   [0, -16, -16, -16, -16, -16,   0,   0, -16,  13,   0],
#                   [0,   0,   0,   0,  19,   0,  39,   0, -16,   0,   0],
#                   [0, -16,   0,   0, -16,   0, -16, -16, -16,   0,   0],
#                   [6, -16,   7,   0, -16,   0, -16,   0,   0,   0,   0],
#                   [22, -16, -16,   0, -16,   0, -16,   0, -16, -16,  22],
#                   [0,   0,   0,   0, -16,   0, -16,   0,   7, -16,   6],
#                   [0,   0, -16, -16, -16,   0, -16,   0,   0, -16,   0],
#                   [0,   0, -16,   0,  39,   0,  19,   0,   0,   0,   0],
#                   [0,  13, -16,   0,   0, -16, -16, -16, -16, -16,   0],
#                   [0,   0,   0, -16, -16, -16,   0,   0,   0,   0,  -2]])
#  [[  0.   0.   0.   0.   0. -16. -16. -16.   0.   0.   0.]
#  [  0. -16. -16. -16. -16. -16.   0.   0. -16.  -2.   0.]
#  [  0.   0.   0.   0.   0.   0.   0.   0. -16.   0.   0.]
#  [  0. -16.   0.   0. -16.   0. -16. -16. -16.   0.   0.]
#  [  0. -16.   7.   0. -16.   0. -16.   0.   0.   0.   0.]
#  [  0. -16. -16.   0. -16.   0. -16.   0. -16. -16.   0.]
#  [  0.   0.   0.   0. -16.   0. -16.   0.   7. -16.   0.]
#  [  0.   0. -16. -16. -16.   0. -16.   0.   0. -16.   0.]
#  [  0.   0. -16.   0.   0.   0.   0.   0.   0.   0.   0.]
#  [  0.  -1. -16.   0.   0. -16. -16. -16. -16. -16.   0.]
#  [  0.   0.   0. -16. -16. -16.   0.   0.   0.   0.   0.]]
#  =====================================================================================
# board = np.array([[-2,   0,   0,   6,  18,   0,   0, -16,  25,   0,  -1],
#                   [0, -16, -16, -16, -16,   0,   0, -16, -16, -16,   0],
#                   [0,   0,   0,   0,   0,   0,   0, -16, -16, -16,   0],
#                   [0, -16,   0,   0,   0,   0,   0, -16,   0,   0,   0],
#                   [0, -16, -16, -16, -16, -16,   0,   0,   0,   0,   0],
#                   [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
#                   [0,   0,   0,   0,   0, -16, -16, -16, -16, -16,   0],
#                   [0,   0,   0, -16,   0,   0,   0,   0,   0, -16,   0],
#                   [0, -16, -16, -16,   0,   0,   0,   0,   0,   0,   0],
#                   [0, -16, -16, -16,   0,   0, -16, -16, -16, -16,   0],
#                   [0,   0,  25, -16,   0,   0,  18,   6,   0,   0,   0]])

# board = np.array([[0,   0,   0,   0,   1,   0,   0,   0,   0,   0,   0],
#                   [0, -16,   0, -16, -16, -16, -16, -16, -16,   0,   0],
#                   [0, -16,   0, -16, -16,   0, -16, -16, -16, -16,  47],
#                   [0, -16, -16, -16, -16,   0,  -2,   0,   0,   0,   0],
#                   [0, -16, -16, -16, -16,   0,   0, -16, -16,   0,   0],
#                   [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
#                   [0,  -1, -16, -16,   0,   0, -16, -16, -16, -16,   0],
#                   [0,   0,   0,   0,   0,   0, -16, -16, -16, -16,   0],
#                   [47, -16, -16, -16, -16,   0, -16, -16,   0, -16,   0],
#                   [0,   0, -16, -16, -16, -16, -16, -16,   0, -16,   0],
#                   [0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0]])

# ???
# board = np.array([[-1,  0,   0,   0,   1,   0,   0,   0,   0,   0,  -2],
#                   [0, -16,   0, -16, -16, -16, -16, -16, -16,   0,   0],
#                   [0, -16,   0, -16, -16,   0, -16, -16, -16, -16,   0],
#                   [0, -16, -16, -16, -16,   0,   0,   0,   0,   0,   0],
#                   [0, -16, -16, -16, -16,   0,   0, -16, -16,   0,   0],
#                   [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
#                   [0,  -1, -16, -16,   0,   0, -16, -16, -16, -16,   0],
#                   [0,   0,   0,   0,   0,   0, -16, -16, -16, -16,   0],
#                   [0, -16, -16, -16, -16,   0, -16, -16,   0, -16,   0],
#                   [0,   0, -16, -16, -16, -16, -16, -16,   0, -16,   0],
#                   [0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0]])

# board = np.array([[0,   0,   0,   0,   0,   0,   0,  -1,   0,   0,   0],
#                   [0,   0,  43, -16,   0, -16, -16,   0,   0,   0,   0],
#                   [0,   0,   0, -16,   0, -16,   0,   0,   0,  44,   0],
#                   [0, -16, -16, -16,   0,   0,   0,   0,   0, -16,  39],
#                   [0, -16,   0,   0,   0,   0,   0,   0,   0, -16,   0],
#                   [0,   0,  -2, -16,   0,   0,   0, -16,   0,   0,   0],
#                   [0, -16,   0,   0,   0,   0,   0,   0,   0, -16,   0],
#                   [39, -16,   0,   0,   0,   0,   0, -16, -16, -16,   0],
#                   [0,   0,   0,   0,   0, -16,   0, -16,   0,   0,   0],
#                   [0,   0,   0,   0, -16, -16,   0, -16,  43,   0,   0],
#                   [0,   0,   0,   0,  14,   0,   0,   0,   0,   0,   0]]
#                  )

# for dynamic radius vision (from 4 to 2)
# board = np.array([[0,    0,    0,    0,    0,    0,    0,    0,  -16,    0,    0],
#                   [0,  -16,    0,    0,    0,    0,    0,  -16,  -16,  -16,    0],
#                   [0,  -16,  -16,    0,    0,    0,    0,    0,    0,    0,    0],
#                   [0,  -16,  -16,    0,    0,    0,  -16,  -16,  -16,  -16,    0],
#                   [0,    0,    0,    0,    0,    0,    0,    0,  -16,  -16,    0],
#                   [0,  -16,  -16,    0,    0,    0,    0,    0,  -16,  -16,   -1],
#                   [0,  -16,  -16,    0,    0,    0,    0,    0,  -16,    9,    0],
#                   [0,  -16,  -16,  -16,  -16,    0,    0,    0,  -16,  -16,    0],
#                   [0,    0,  -16,   -2,  -16,    0,    0,    0,  -16,  -16,    0],
#                   [0,  -16,  -16,  -16,    0,    0,    0,    0,    0,  -16,    0],
#                   [0,    0,  -16,    0,    0,    0,    0,    0,    0,    0,    0]]
#                  )
board = np.array([[0,    0,    0,    0,    0,    0,    0,    0,  -16,    0,    0],
                  [0,  -16,    0,    0,    0,    0,    0,  -16,  -16,  -16,    0],
                  [0,  -16,  -16,    0,    0,    0,    0,    0,    0,    0,    0],
                  [0,  -16,  -16,    0,    0,    0,    0,    0,    0,    0,   -1],
                  [0,    0,    0,    0,    0,    0,    0,    0,  -16,  -16,    0],
                  [0,  -16,  -16,    0,    0,    0,    0,    0,  -16,  -16,    0],
                  [0,  -16,  -16,    0,    0,    0,    0,    0,  -16,    9,    0],
                  [0,  -16,  -16,  -16,  -16,    0,    0,    0,  -16,  -16,    0],
                  [0,    0,  -16,   -2,  -16,    0,    0,    0,  -16,  -16,    0],
                  [0,  -16,  -16,  -16,    0,    0,    0,    0,    0,  -16,    0],
                  [0,    0,  -16,    0,    0,    0,    0,    0,    0,    0,    0]]
                 )

# COUNT_OF_MOVES = 30
result = np.where(board == -1)
firstPlayerRowIndex = result[0][0]
firstPlayerColumnIndex = result[1][0]
result = np.where(board == -2)
secondPlayerRowIndex = result[0][0]
secondPlayerColumnIndex = result[1][0]

print("\n\n\n", board)

algo1 = cascade.getBestAlgorithmCascadeDynamicFloatingMove
algo2 = cascade.getBestAlgorithmCascadeFloatingMove

# countOfMoves = 0
# while countOfMoves < COUNT_OF_MOVES:
#     countOfMoves += 1
movesLeft = COUNT_OF_MOVES + 1
while movesLeft > 0:
    movesLeft -= 1

    firstPlayerMoveReward, firstPlayerNewRowIndex, firstPlayerNewColumnIndex = makeMove(board,
                                                                                        firstPlayerRowIndex,
                                                                                        firstPlayerColumnIndex,
                                                                                        algo1,
                                                                                        movesLeft)
    firstPlayerScore += firstPlayerMoveReward
    firstPlayerRowIndex = firstPlayerNewRowIndex
    firstPlayerColumnIndex = firstPlayerNewColumnIndex

    if firstPlayerMoveReward == STEP_ON_OPPONENT_PENALTY:
        break

    # print("\n\n\n", board)
    # print(f"First player score: {firstPlayerScore}")
    # print(f"Second player score: {secondPlayerScore}")

    firstPlayerPosition = np.where(board == FIRST_PLAYER_IDENTIFIER)
    if firstPlayerPosition[0][0] != firstPlayerRowIndex or firstPlayerPosition[1][0] != firstPlayerColumnIndex:
        sys.exit(
            f"Invalid first player position: {firstPlayerPosition[0][0]}-{firstPlayerPosition[1][0]} <=> {firstPlayerRowIndex}-{firstPlayerColumnIndex}")

    secondPlayerMoveReward, secondPlayerNewRowIndex, secondPlayerNewColumnIndex = makeMove(board,
                                                                                           secondPlayerRowIndex,
                                                                                           secondPlayerColumnIndex,
                                                                                           algo2,
                                                                                           movesLeft)
    secondPlayerScore += secondPlayerMoveReward
    secondPlayerRowIndex = secondPlayerNewRowIndex
    secondPlayerColumnIndex = secondPlayerNewColumnIndex

    if secondPlayerMoveReward == STEP_ON_OPPONENT_PENALTY:
        break

    # print("\n", board)
    # print(f"First player score: {firstPlayerScore}")
    # print(f"Second player score: {secondPlayerScore}")

    secondPlayerPosition = np.where(board == SECOND_PLAYER_IDENTIFIER)
    if secondPlayerPosition[0][0] != secondPlayerRowIndex or secondPlayerPosition[1][0] != secondPlayerColumnIndex:
        sys.exit(
            f"Invalid second player position: {secondPlayerPosition[0][0]}-{secondPlayerPosition[1][0]} <=> {secondPlayerRowIndex}-{secondPlayerColumnIndex}")

    print("\n", board)
    print(f"First player score: {firstPlayerScore}")
    print(f"Second player score: {secondPlayerScore}")

    input()
    # time.sleep(0.4)

    indexOfMaxValue = np.argmax(board)
    maxValueRowIndex = indexOfMaxValue // BOARD_SIDE_SIZE
    maxValueColumnIndex = indexOfMaxValue - maxValueRowIndex * BOARD_SIDE_SIZE
    if board[maxValueRowIndex][maxValueColumnIndex] <= 0:
        print("Game finished: no more score on the board")
        break

print("\n", board)
print("\n\n\nFinal score:")
print(f"First player score: {firstPlayerScore}")
print(f"Second player score: {secondPlayerScore}")
