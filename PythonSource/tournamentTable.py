
import pandas

GAME_WITH_SELF_MARKER = 'X'

WIN_RESULT = 2
DRAW_RESULT = 1
LOSE_RESULT = 0


def printMultipleResultsAsTable(nameResultsList):

    resultTable = [[nameResults[0]] for nameResults in nameResultsList]
    multipleResultTable = [[nameResults[0]] for nameResults in nameResultsList]
    scoreTable = [[nameResults[0]] for nameResults in nameResultsList]

    for firstPlayerIndex, nameResults in enumerate(nameResultsList):
        resultTable[firstPlayerIndex].append(GAME_WITH_SELF_MARKER)
        multipleResultTable[firstPlayerIndex].append(GAME_WITH_SELF_MARKER)
        scoreTable[firstPlayerIndex].append(GAME_WITH_SELF_MARKER)

        for gameIndex, gameResult in enumerate(nameResults[1]):
            secondPlayerIndex = firstPlayerIndex + gameIndex + 1

            firstPlayerMultipleResult = gameResult[0]
            secondPlayerMultipleResult = gameResult[1]
            firstPlayerScore = gameResult[2]
            secondPlayerScore = gameResult[3]

            if firstPlayerMultipleResult > secondPlayerMultipleResult:
                firstPlayerResult = WIN_RESULT
                secondPlayerResult = LOSE_RESULT
            elif firstPlayerMultipleResult < secondPlayerMultipleResult:
                firstPlayerResult = LOSE_RESULT
                secondPlayerResult = WIN_RESULT
            else:
                firstPlayerResult = DRAW_RESULT
                secondPlayerResult = DRAW_RESULT

            resultTable[firstPlayerIndex].append(firstPlayerResult)
            resultTable[secondPlayerIndex].append(secondPlayerResult)

            multipleResultTable[firstPlayerIndex].append(
                firstPlayerMultipleResult)
            multipleResultTable[secondPlayerIndex].append(
                secondPlayerMultipleResult)

            scoreTable[firstPlayerIndex].append(firstPlayerScore)
            scoreTable[secondPlayerIndex].append(secondPlayerScore)

    for playerResult in resultTable:
        playerResult.append(sum(
            filter(lambda x: x != GAME_WITH_SELF_MARKER, playerResult[1:])
        ))

    for playerMultipleResult in multipleResultTable:
        playerMultipleResult.append(sum(
            filter(lambda x: x != GAME_WITH_SELF_MARKER,
                   playerMultipleResult[1:])
        ))

    for playerScore in scoreTable:
        playerScore.append(sum(
            filter(lambda x: x != GAME_WITH_SELF_MARKER, playerScore[1:])
        ))

    countOfPlayers = len(nameResultsList)
    playerIndexList = range(1, countOfPlayers + 1)

    tableHeader = [''] + list(playerIndexList) + ['total']

    resultTableDataFrame = pandas.DataFrame(
        resultTable, index=playerIndexList, columns=tableHeader)

    multipleResultTableDataFrame = pandas.DataFrame(
        multipleResultTable, index=playerIndexList, columns=tableHeader)

    scoreTableDataFrame = pandas.DataFrame(
        scoreTable, index=playerIndexList, columns=tableHeader)

    print(resultTableDataFrame)
    print('-----------------------------------------------------------------------')
    print(resultTableDataFrame.sort_values(by='total', ascending=False))
    print('\n=======================================================================\n')
    print(multipleResultTableDataFrame)
    print('-----------------------------------------------------------------------')
    print(multipleResultTableDataFrame.sort_values(by='total', ascending=False))
    print('\n=======================================================================\n')
    print(scoreTableDataFrame)
    print('-----------------------------------------------------------------------')
    print(scoreTableDataFrame.sort_values(by='total', ascending=False))


def printResultsAsTable(nameWithResultsList):

    resultTable = [[nameResults[0]] for nameResults in nameWithResultsList]
    scoreTable = [[nameResults[0]] for nameResults in nameWithResultsList]

    for firstPlayerIndex, nameWithResults in enumerate(nameWithResultsList):
        resultTable[firstPlayerIndex].append(GAME_WITH_SELF_MARKER)
        scoreTable[firstPlayerIndex].append(GAME_WITH_SELF_MARKER)

        for gameIndex, gameResult in enumerate(nameWithResults[1]):
            secondPlayerIndex = firstPlayerIndex + gameIndex + 1

            result = gameResult[0]
            firstPlayerScore = gameResult[1]
            secondPlayerScore = gameResult[2]

            if result == WIN_RESULT:
                firstPlayerResult = WIN_RESULT
                secondPlayerResult = LOSE_RESULT
            elif result == LOSE_RESULT:
                firstPlayerResult = LOSE_RESULT
                secondPlayerResult = WIN_RESULT
            else:
                firstPlayerResult = DRAW_RESULT
                secondPlayerResult = DRAW_RESULT

            resultTable[firstPlayerIndex].append(firstPlayerResult)
            resultTable[secondPlayerIndex].append(secondPlayerResult)

            scoreTable[firstPlayerIndex].append(firstPlayerScore)
            scoreTable[secondPlayerIndex].append(secondPlayerScore)

    for playerResult in resultTable:
        playerResult.append(sum(
            filter(lambda x: x != GAME_WITH_SELF_MARKER, playerResult[1:])
        ))

    for playerScore in scoreTable:
        playerScore.append(sum(
            filter(lambda x: x != GAME_WITH_SELF_MARKER, playerScore[1:])
        ))

    countOfPlayers = len(nameWithResultsList)
    playerIndexList = range(1, countOfPlayers + 1)

    tableHeader = [''] + list(playerIndexList) + ['total']

    resultTableDataFrame = pandas.DataFrame(
        resultTable, index=playerIndexList, columns=tableHeader)

    scoreTableDataFrame = pandas.DataFrame(
        scoreTable, index=playerIndexList, columns=tableHeader)

    print(resultTableDataFrame)
    print('-----------------------------------------------------------------------')
    print(resultTableDataFrame.sort_values(by='total', ascending=False))
    print('\n=======================================================================\n')
    print(scoreTableDataFrame)
    print('-----------------------------------------------------------------------')
    print(scoreTableDataFrame.sort_values(by='total', ascending=False))


def printScoresAsTable(nameWithScoresList):
    resultTable = [[nameScores[0]] for nameScores in nameWithScoresList]
    scoreTable = [[nameScores[0]] for nameScores in nameWithScoresList]

    for firstPlayerIndex, nameWithScores in enumerate(nameWithScoresList):
        resultTable[firstPlayerIndex].append(GAME_WITH_SELF_MARKER)
        scoreTable[firstPlayerIndex].append(GAME_WITH_SELF_MARKER)

        for gameIndex, gameScore in enumerate(nameWithScores[1]):
            secondPlayerIndex = firstPlayerIndex + gameIndex + 1

            firstPlayerScore = gameScore[0]
            secondPlayerScore = gameScore[1]

            if firstPlayerScore > secondPlayerScore:
                firstPlayerResult = WIN_RESULT
                secondPlayerResult = LOSE_RESULT
            elif firstPlayerScore < secondPlayerScore:
                firstPlayerResult = LOSE_RESULT
                secondPlayerResult = WIN_RESULT
            else:
                firstPlayerResult = DRAW_RESULT
                secondPlayerResult = DRAW_RESULT

            resultTable[firstPlayerIndex].append(firstPlayerResult)
            resultTable[secondPlayerIndex].append(secondPlayerResult)

            scoreTable[firstPlayerIndex].append(firstPlayerScore)
            scoreTable[secondPlayerIndex].append(secondPlayerScore)

    for playerResult in resultTable:
        playerResult.append(sum(
            filter(lambda x: x != GAME_WITH_SELF_MARKER, playerResult[1:])
        ))

    for playerScore in scoreTable:
        playerScore.append(sum(
            filter(lambda x: x != GAME_WITH_SELF_MARKER, playerScore[1:])
        ))

    countOfPlayers = len(nameWithScoresList)
    playerIndexList = range(1, countOfPlayers + 1)

    tableHeader = [''] + list(playerIndexList) + ['total']

    resultTableDataFrame = pandas.DataFrame(
        resultTable, index=playerIndexList, columns=tableHeader)

    scoreTableDataFrame = pandas.DataFrame(
        scoreTable, index=playerIndexList, columns=tableHeader)

    print(resultTableDataFrame)
    print('-----------------------------------------------------------------------')
    print(resultTableDataFrame.sort_values(by='total', ascending=False))
    print('\n=======================================================================\n')
    print(scoreTableDataFrame)
    print('-----------------------------------------------------------------------')
    print(scoreTableDataFrame.sort_values(by='total', ascending=False))


# nameScoresList = [
#     ['someLongName', [(8, 2, 5, 4), (4, 6, 1, 4), (0, 10, 100, 200)]],
#     ['someName', [(8, 2, 785, 500), (2, 8, 300, 400)]],
#     ['someLongLongName', [(3, 7, 3, 6)]],
#     ['anotherName', []],
# ]
# print(pandas.DataFrame(nameScoresList))
# print('***********************************************************************\n')

# printMultipleResultsAsTable(nameScoresList)
# print('***********************************************************************\n')
# print('***********************************************************************\n')
# print('***********************************************************************\n')

# nameScoresList = [
#     ['someLongName', [(2, 5, 4), (0, 1, 4), (0, 100, 200)]],
#     ['someName', [(2, 785, 500), (0, 300, 400)]],
#     ['someLongLongName', [(0, 3, 6)]],
#     ['anotherName', []],
# ]
# print(pandas.DataFrame(nameScoresList))
# print('***********************************************************************\n')

# printResultsAsTable(nameScoresList)
# print('***********************************************************************\n')
# print('***********************************************************************\n')
# print('***********************************************************************\n')

# nameScoresList = [
#     ['someLongName', [(5, 4), (1, 4), (100, 200)]],
#     ['someName', [(785, 500), (300, 400)]],
#     ['someLongLongName', [(3, 6)]],
#     ['anotherName', []],
# ]
# print(pandas.DataFrame(nameScoresList))
# print('***********************************************************************\n')

# printScoresAsTable(nameScoresList)
