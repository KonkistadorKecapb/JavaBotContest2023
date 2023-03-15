import java.util.Random;
import java.util.ArrayList;

final public class KecapbBot implements LabyrinthPlayer {
    private final static int FIRST_PLAYER_IDENTIFIER = -1;
    private final static int SECOND_PLAYER_IDENTIFIER = -2;

    private final static int BOARD_SIDE_SIZE = GameState.WIDTH;

    private int opponentIdentifier = SECOND_PLAYER_IDENTIFIER;

    private int playerIdentifier = FIRST_PLAYER_IDENTIFIER;
    private int playerRowIndex = 0;
    private int playerColumnIndex = 0;

    final public void takeYourNumber(int number) {
        playerIdentifier = number;

        if (number == FIRST_PLAYER_IDENTIFIER) {
            opponentIdentifier = SECOND_PLAYER_IDENTIFIER;
        } else {
            opponentIdentifier = FIRST_PLAYER_IDENTIFIER;
        }
    }

    final public String getTelegramNick() {
        return "Just for fun yolo gaming";
    }

    final public Direction step(GameState gameState) {
        int movesLeft = gameState.getRoundsToEnd();
        int[][] board = gameState.getMap();

        findPlayerPosition(board);

        int[] point = getBestAlgorithmCascadeDynamicFloatingMove(board, movesLeft);

        Direction direction = getDirectionByPoint(point);

        // TODO: remove
        // board[this.playerRowIndex][this.playerColumnIndex] = 0;

        this.playerRowIndex = point[0];
        this.playerColumnIndex = point[1];

        // TODO: remove
        // board[this.playerRowIndex][this.playerColumnIndex] = playerIdentifier;

        return direction;
    }

    final private void findPlayerPosition(int[][] board) {
        if (board[this.playerRowIndex][this.playerColumnIndex] == this.playerIdentifier) {
            return;
        }

        for (int rowIndex = 0; rowIndex < BOARD_SIDE_SIZE; ++rowIndex) {
            for (int columnIndex = 0; columnIndex < BOARD_SIDE_SIZE; ++columnIndex) {
                if (board[rowIndex][columnIndex] == this.playerIdentifier) {
                    this.playerRowIndex = rowIndex;
                    this.playerColumnIndex = columnIndex;

                    return;
                }
            }
        }
    }

    final private int[] getOpponentPositionOrNull(int[][] scoreMatrix) {
        for (int rowIndex = 0; rowIndex < scoreMatrix.length; ++rowIndex) {
            for (int columnIndex = 0; columnIndex < scoreMatrix.length; ++columnIndex) {
                if (scoreMatrix[rowIndex][columnIndex] == this.opponentIdentifier) {
                    return new int[] { rowIndex, columnIndex };
                }
            }
        }
        return null;
    }

    final private Direction getDirectionByPoint(int[] point) {
        int rowIndex = point[0];
        int columnIndex = point[1];

        if (rowIndex < this.playerRowIndex) {
            return Direction.UP;
        }
        if (rowIndex > this.playerRowIndex) {
            return Direction.BOTTOM;
        }
        if (columnIndex < this.playerColumnIndex) {
            return Direction.LEFT;
        }
        if (columnIndex > this.playerColumnIndex) {
            return Direction.RIGHT;
        }

        return Direction.NONE;
    }

    final private static void insertArrayIntoArray(
            int[][] destinationArray,
            int[][] sourceArray,
            int startRowIndex,
            int startColumnIndex) {

        for (int rowIndex = 0; rowIndex < sourceArray.length; ++rowIndex) {
            for (int columnIndex = 0; columnIndex < sourceArray.length; ++columnIndex) {
                destinationArray[startRowIndex + rowIndex][startColumnIndex
                        + columnIndex] = sourceArray[rowIndex][columnIndex];
            }
        }
    }

    final private static int[][] getSubArray(int[][] sourceArray, int startVisionIndex, int size) {
        int[][] subArray = new int[size][size];
        for (int rowIndex = 0; rowIndex < size; ++rowIndex) {
            for (int columnIndex = 0; columnIndex < size; ++columnIndex) {
                subArray[rowIndex][columnIndex] = sourceArray[startVisionIndex + rowIndex][startVisionIndex
                        + columnIndex];
            }
        }
        return subArray;
    }

    final private int[] getBestAlgorithmCascadeDynamicFloatingMove(int[][] board, int movesLeft) {
        if (movesLeft > 20) {
            int[] nextPoint = getGreedySimpleMove(board);

            if (board[nextPoint[0]][nextPoint[1]] > 0) {
                return nextPoint;
            }

            int[] nextMovePoint = getGreedyFullVisionMove(board);
            if ((nextMovePoint[0] != playerRowIndex) || (nextMovePoint[1] != playerColumnIndex)) {
                return nextMovePoint;
            }
        } else {
            int[] nextPoint = getGreedyFloatingRadiusMove(board, movesLeft);
            int nextRowIndex = nextPoint[0];
            int nextColumnIndex = nextPoint[1];

            if ((nextRowIndex != playerRowIndex) || (nextColumnIndex != playerColumnIndex)) {
                return new int[] { nextRowIndex, nextColumnIndex };
            }
        }

        int radiusVision = 4;
        while (radiusVision > 1) {
            int[] point = getGreedyPartialVisionMove(board, radiusVision);
            int nextRowIndex = point[0];
            int nextColumnIndex = point[1];

            if ((nextRowIndex != playerRowIndex) || (nextColumnIndex != playerColumnIndex)) {
                return new int[] { nextRowIndex, nextColumnIndex };
            }

            radiusVision -= 1;
        }

        return getRandomMove(board);
    }

    final private int[] getRandomMove(int[][] board) {
        Random random = new Random();

        ArrayList<int[]> nextMoveList = new ArrayList<int[]>();
        nextMoveList.add(new int[] { playerRowIndex - 1, playerColumnIndex });
        nextMoveList.add(new int[] { playerRowIndex + 1, playerColumnIndex });
        nextMoveList.add(new int[] { playerRowIndex, playerColumnIndex - 1 });
        nextMoveList.add(new int[] { playerRowIndex, playerColumnIndex + 1 });

        while (nextMoveList.size() > 0) {
            int nextMoveIndex = random.nextInt(0, nextMoveList.size());
            int[] nextMovePoint = nextMoveList.get(nextMoveIndex);

            int nextRowIndex = nextMovePoint[0];
            int nextColumnIndex = nextMovePoint[1];

            if (nextRowIndex >= 0
                    && nextRowIndex < BOARD_SIDE_SIZE
                    && nextColumnIndex >= 0
                    && nextColumnIndex < BOARD_SIDE_SIZE) {

                int fieldValue = board[nextRowIndex][nextColumnIndex];
                if (fieldValue >= 0) {
                    return nextMovePoint;
                }
            }

            nextMoveList.remove(nextMoveIndex);
        }

        return new int[] { playerRowIndex, playerColumnIndex };
    }

    final private int[] getGreedySimpleMove(int[][] board) {
        int nextRowDiff = 0;
        int nextColumnDiff = 0;
        int maxValue = 0;

        if (playerRowIndex - 1 >= 0) {
            int value = board[playerRowIndex - 1][playerColumnIndex];
            if (value > maxValue) {
                maxValue = value;
                nextRowDiff = -1;
            }
        }

        if (playerRowIndex + 1 < BOARD_SIDE_SIZE) {
            int value = board[playerRowIndex + 1][playerColumnIndex];
            if (value > maxValue) {
                maxValue = value;
                nextRowDiff = +1;
            }
        }

        if (playerColumnIndex - 1 >= 0) {
            int value = board[playerRowIndex][playerColumnIndex - 1];
            if (value > maxValue) {
                maxValue = value;
                nextRowDiff = 0;
                nextColumnDiff = -1;
            }
        }

        if (playerColumnIndex + 1 < BOARD_SIDE_SIZE) {
            int value = board[playerRowIndex][playerColumnIndex + 1];
            if (value > maxValue) {
                maxValue = value;
                nextRowDiff = 0;
                nextColumnDiff = +1;
            }
        }

        int nextRowIndex = playerRowIndex + nextRowDiff;
        int nextColumnIndex = playerColumnIndex + nextColumnDiff;

        return new int[] { nextRowIndex, nextColumnIndex };
    }

    final private int[] getGreedyFullVisionMove(int[][] board) {
        final int BOARD_SIZE_WITH_BORDER = BOARD_SIDE_SIZE + 1 * 2; // board size + both borders

        int[][] scoreMatrix = new int[BOARD_SIZE_WITH_BORDER][BOARD_SIZE_WITH_BORDER];
        int startRowIndex = 1;
        int startColumnIndex = 1;
        insertArrayIntoArray(scoreMatrix, board, startRowIndex, startColumnIndex);

        final int SCORE_MATRIX_PLAYER_ROW_INDEX = playerRowIndex + 1;
        final int SCORE_MATRIX_PLAYER_COLUMN_INDEX = playerColumnIndex + 1;

        int[] opponentPosition = getOpponentPositionOrNull(scoreMatrix);
        if (opponentPosition != null) {
            int opponentRowIndex = opponentPosition[0];
            int opponentColumnIndex = opponentPosition[1];
            scoreMatrix[opponentRowIndex][opponentColumnIndex] = -9999999;
        }

        // filling score matrix corners (without vertical and horizontal lines)
        int leftUpCornerRowIndex = 1;
        while (leftUpCornerRowIndex < SCORE_MATRIX_PLAYER_ROW_INDEX) {
            int downColumnIndex = 1;
            while (downColumnIndex < SCORE_MATRIX_PLAYER_COLUMN_INDEX) {
                scoreMatrix[leftUpCornerRowIndex][downColumnIndex] += max(
                        scoreMatrix[leftUpCornerRowIndex - 1][downColumnIndex],
                        scoreMatrix[leftUpCornerRowIndex][downColumnIndex - 1]);

                downColumnIndex += 1;
            }
            leftUpCornerRowIndex += 1;
        }

        int rightUpCornerRowIndex = 1;
        while (rightUpCornerRowIndex < SCORE_MATRIX_PLAYER_ROW_INDEX) {
            int downColumnIndex = BOARD_SIZE_WITH_BORDER - 2;
            while (downColumnIndex > SCORE_MATRIX_PLAYER_COLUMN_INDEX) {
                scoreMatrix[rightUpCornerRowIndex][downColumnIndex] += max(
                        scoreMatrix[rightUpCornerRowIndex - 1][downColumnIndex],
                        scoreMatrix[rightUpCornerRowIndex][downColumnIndex + 1]);

                downColumnIndex -= 1;
            }
            rightUpCornerRowIndex += 1;
        }

        int leftDownCorderRowIndex = BOARD_SIZE_WITH_BORDER - 2;
        while (leftDownCorderRowIndex > SCORE_MATRIX_PLAYER_ROW_INDEX) {
            int downColumnIndex = 1;
            while (downColumnIndex < SCORE_MATRIX_PLAYER_COLUMN_INDEX) {
                scoreMatrix[leftDownCorderRowIndex][downColumnIndex] += max(
                        scoreMatrix[leftDownCorderRowIndex + 1][downColumnIndex],
                        scoreMatrix[leftDownCorderRowIndex][downColumnIndex - 1]);

                downColumnIndex += 1;
            }
            leftDownCorderRowIndex -= 1;
        }

        int rightDownCorderRowIndex = BOARD_SIZE_WITH_BORDER - 2;
        while (rightDownCorderRowIndex > SCORE_MATRIX_PLAYER_ROW_INDEX) {
            int downColumnIndex = BOARD_SIZE_WITH_BORDER - 2;
            while (downColumnIndex > SCORE_MATRIX_PLAYER_COLUMN_INDEX) {
                scoreMatrix[rightDownCorderRowIndex][downColumnIndex] += max(
                        scoreMatrix[rightDownCorderRowIndex + 1][downColumnIndex],
                        scoreMatrix[rightDownCorderRowIndex][downColumnIndex + 1]);

                downColumnIndex -= 1;
            }
            rightDownCorderRowIndex -= 1;
        }

        // filling cross (vertical and horizontal lines)
        int upRowIndex = 1;
        while (upRowIndex < SCORE_MATRIX_PLAYER_ROW_INDEX) {
            scoreMatrix[upRowIndex][SCORE_MATRIX_PLAYER_COLUMN_INDEX] += max(
                    scoreMatrix[upRowIndex - 1][SCORE_MATRIX_PLAYER_COLUMN_INDEX],
                    scoreMatrix[upRowIndex][SCORE_MATRIX_PLAYER_COLUMN_INDEX - 1],
                    scoreMatrix[upRowIndex][SCORE_MATRIX_PLAYER_COLUMN_INDEX + 1]);
            upRowIndex += 1;
        }

        int downRowIndex = BOARD_SIZE_WITH_BORDER - 2;
        while (downRowIndex > SCORE_MATRIX_PLAYER_ROW_INDEX) {
            scoreMatrix[downRowIndex][SCORE_MATRIX_PLAYER_COLUMN_INDEX] += max(
                    scoreMatrix[downRowIndex + 1][SCORE_MATRIX_PLAYER_COLUMN_INDEX],
                    scoreMatrix[downRowIndex][SCORE_MATRIX_PLAYER_COLUMN_INDEX - 1],
                    scoreMatrix[downRowIndex][SCORE_MATRIX_PLAYER_COLUMN_INDEX + 1]);
            downRowIndex -= 1;
        }

        int leftColumnIndex = 1;
        while (leftColumnIndex < SCORE_MATRIX_PLAYER_COLUMN_INDEX) {
            scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX][leftColumnIndex] += max(
                    scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX][leftColumnIndex - 1],
                    scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX + 1][leftColumnIndex],
                    scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX - 1][leftColumnIndex]);
            leftColumnIndex += 1;
        }

        int rightColumnIndex = BOARD_SIZE_WITH_BORDER - 2;
        while (rightColumnIndex > SCORE_MATRIX_PLAYER_COLUMN_INDEX) {
            scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX][rightColumnIndex] += max(
                    scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX][rightColumnIndex + 1],
                    scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX + 1][rightColumnIndex],
                    scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX - 1][rightColumnIndex]);
            rightColumnIndex -= 1;
        }

        // getting max score direction and return new indexes
        int topScoreRowIndex = SCORE_MATRIX_PLAYER_ROW_INDEX - 1;
        int upperScore = -1000;
        if (topScoreRowIndex >= 1) {
            upperScore = scoreMatrix[topScoreRowIndex][SCORE_MATRIX_PLAYER_COLUMN_INDEX];
        }

        int downScoreRowIndex = SCORE_MATRIX_PLAYER_ROW_INDEX + 1;
        int bottomScore = -1000;
        if (downScoreRowIndex <= BOARD_SIZE_WITH_BORDER - 2) {
            bottomScore = scoreMatrix[downScoreRowIndex][SCORE_MATRIX_PLAYER_COLUMN_INDEX];
        }

        int leftScoreColumnIndex = SCORE_MATRIX_PLAYER_COLUMN_INDEX - 1;
        int leftScore = -1000;
        if (leftScoreColumnIndex >= 1) {
            leftScore = scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX][leftScoreColumnIndex];
        }

        int rightScoreColumnIndex = SCORE_MATRIX_PLAYER_COLUMN_INDEX + 1;
        int rightScore = -1000;
        if (rightScoreColumnIndex <= BOARD_SIZE_WITH_BORDER - 2) {
            rightScore = scoreMatrix[SCORE_MATRIX_PLAYER_ROW_INDEX][rightScoreColumnIndex];
        }

        return getNearestDirection(board, upperScore, bottomScore, leftScore, rightScore);
    }

    final private int[] getGreedyPartialVisionMove(int[][] board, int visionRadius) {
        if (visionRadius > BOARD_SIDE_SIZE - 1) {
            throw new RuntimeException(
                    "ERROR: Invalid size of radius. Try to use full vision. "
                            + "Board size: " + BOARD_SIDE_SIZE + ", Radius: " + visionRadius);
        }
        if (visionRadius < 2) {
            throw new RuntimeException("ERROR: Radius must be greater than 2. Radius: " + visionRadius);
        }

        final int CENTER_SIZE = 1;
        final int VISION_DIAMETER = visionRadius * 2 + CENTER_SIZE;

        final int EXTENDED_SCORE_MATRIX_SIDE_SIZE = BOARD_SIDE_SIZE * 2 + CENTER_SIZE;
        final int EXTENDED_SCORE_MATRIX_CENTER_INDEX = EXTENDED_SCORE_MATRIX_SIDE_SIZE / 2;

        int[][] extendedScoreMatrix = new int[EXTENDED_SCORE_MATRIX_SIDE_SIZE][EXTENDED_SCORE_MATRIX_SIDE_SIZE];

        int startBoardRowIndex = EXTENDED_SCORE_MATRIX_CENTER_INDEX - playerRowIndex;
        int startBoardColumnIndex = EXTENDED_SCORE_MATRIX_CENTER_INDEX - playerColumnIndex;
        insertArrayIntoArray(extendedScoreMatrix, board, startBoardRowIndex, startBoardColumnIndex);

        int startVisionIndex = EXTENDED_SCORE_MATRIX_CENTER_INDEX - visionRadius;
        int[][] scoreMatrix = getSubArray(extendedScoreMatrix, startVisionIndex, VISION_DIAMETER);

        final int SCORE_MATRIX_CENTER_INDEX = scoreMatrix.length / 2;
        final int SCORE_MATRIX_BOTTOM_INDEX = scoreMatrix.length - 1;
        final int SCORE_MATRIX_RIGHT_INDEX = SCORE_MATRIX_BOTTOM_INDEX;

        int[] opponentPosition = getOpponentPositionOrNull(scoreMatrix);
        if (opponentPosition != null) {
            int opponentRowIndex = opponentPosition[0];
            int opponentColumnIndex = opponentPosition[1];
            scoreMatrix[opponentRowIndex][opponentColumnIndex] = -9999999;
        }

        int zeroUpRowIndex = 0;
        int columnThreshold = SCORE_MATRIX_CENTER_INDEX;
        while (zeroUpRowIndex < SCORE_MATRIX_CENTER_INDEX) {
            int zeroDownRowIndex = SCORE_MATRIX_BOTTOM_INDEX - zeroUpRowIndex;

            int zeroLeftColumnIndex = 0;
            while (zeroLeftColumnIndex < columnThreshold) {
                int zeroRightColumnIndex = SCORE_MATRIX_RIGHT_INDEX - zeroLeftColumnIndex;

                scoreMatrix[zeroUpRowIndex][zeroLeftColumnIndex] = 0;
                scoreMatrix[zeroUpRowIndex][zeroRightColumnIndex] = 0;
                scoreMatrix[zeroDownRowIndex][zeroLeftColumnIndex] = 0;
                scoreMatrix[zeroDownRowIndex][zeroRightColumnIndex] = 0;

                zeroLeftColumnIndex += 1;
            }

            columnThreshold -= 1;
            zeroUpRowIndex += 1;
        }

        int scoreUpperCornersRowIndex = 1;
        int scoreLeftUpperCornerFillingStartIndex = SCORE_MATRIX_CENTER_INDEX - 1;
        while (scoreUpperCornersRowIndex < SCORE_MATRIX_CENTER_INDEX) {
            int scoreBottomCornersRowIndex = SCORE_MATRIX_BOTTOM_INDEX - scoreUpperCornersRowIndex;

            int scoreLeftColumnIndex = scoreLeftUpperCornerFillingStartIndex;
            while (scoreLeftColumnIndex < SCORE_MATRIX_CENTER_INDEX) {
                int scoreRightColumnIndex = SCORE_MATRIX_RIGHT_INDEX - scoreLeftColumnIndex;

                scoreMatrix[scoreUpperCornersRowIndex][scoreLeftColumnIndex] += max(
                        scoreMatrix[scoreUpperCornersRowIndex][scoreLeftColumnIndex - 1],
                        scoreMatrix[scoreUpperCornersRowIndex - 1][scoreLeftColumnIndex]);

                scoreMatrix[scoreUpperCornersRowIndex][scoreRightColumnIndex] += max(
                        scoreMatrix[scoreUpperCornersRowIndex][scoreRightColumnIndex + 1],
                        scoreMatrix[scoreUpperCornersRowIndex - 1][scoreRightColumnIndex]);

                scoreMatrix[scoreBottomCornersRowIndex][scoreLeftColumnIndex] += max(
                        scoreMatrix[scoreBottomCornersRowIndex][scoreLeftColumnIndex - 1],
                        scoreMatrix[scoreBottomCornersRowIndex + 1][scoreLeftColumnIndex]);

                scoreMatrix[scoreBottomCornersRowIndex][scoreRightColumnIndex] += max(
                        scoreMatrix[scoreBottomCornersRowIndex][scoreRightColumnIndex + 1],
                        scoreMatrix[scoreBottomCornersRowIndex + 1][scoreRightColumnIndex]);

                scoreLeftColumnIndex += 1;
            }

            scoreLeftUpperCornerFillingStartIndex -= 1;
            scoreUpperCornersRowIndex += 1;
        }

        int upperVerticalIndex = 1;
        while (upperVerticalIndex < SCORE_MATRIX_CENTER_INDEX) {
            int bottomVerticalIndex = SCORE_MATRIX_BOTTOM_INDEX - upperVerticalIndex;
            int leftHorizontalIndex = upperVerticalIndex;
            int rightHorizontalIndex = SCORE_MATRIX_RIGHT_INDEX - upperVerticalIndex;

            scoreMatrix[upperVerticalIndex][SCORE_MATRIX_CENTER_INDEX] += max(
                    scoreMatrix[upperVerticalIndex - 1][SCORE_MATRIX_CENTER_INDEX],
                    scoreMatrix[upperVerticalIndex][SCORE_MATRIX_CENTER_INDEX - 1],
                    scoreMatrix[upperVerticalIndex][SCORE_MATRIX_CENTER_INDEX + 1]);

            scoreMatrix[bottomVerticalIndex][SCORE_MATRIX_CENTER_INDEX] += max(
                    scoreMatrix[bottomVerticalIndex + 1][SCORE_MATRIX_CENTER_INDEX],
                    scoreMatrix[bottomVerticalIndex][SCORE_MATRIX_CENTER_INDEX - 1],
                    scoreMatrix[bottomVerticalIndex][SCORE_MATRIX_CENTER_INDEX + 1]);

            scoreMatrix[SCORE_MATRIX_CENTER_INDEX][leftHorizontalIndex] += max(
                    scoreMatrix[SCORE_MATRIX_CENTER_INDEX][leftHorizontalIndex - 1],
                    scoreMatrix[SCORE_MATRIX_CENTER_INDEX - 1][leftHorizontalIndex],
                    scoreMatrix[SCORE_MATRIX_CENTER_INDEX + 1][leftHorizontalIndex]);

            scoreMatrix[SCORE_MATRIX_CENTER_INDEX][rightHorizontalIndex] += max(
                    scoreMatrix[SCORE_MATRIX_CENTER_INDEX][rightHorizontalIndex + 1],
                    scoreMatrix[SCORE_MATRIX_CENTER_INDEX - 1][rightHorizontalIndex],
                    scoreMatrix[SCORE_MATRIX_CENTER_INDEX + 1][rightHorizontalIndex]);

            upperVerticalIndex += 1;
        }

        int upperScore = scoreMatrix[SCORE_MATRIX_CENTER_INDEX - 1][SCORE_MATRIX_CENTER_INDEX];
        int bottomScore = scoreMatrix[SCORE_MATRIX_CENTER_INDEX + 1][SCORE_MATRIX_CENTER_INDEX];
        int leftScore = scoreMatrix[SCORE_MATRIX_CENTER_INDEX][SCORE_MATRIX_CENTER_INDEX - 1];
        int rightScore = scoreMatrix[SCORE_MATRIX_CENTER_INDEX][SCORE_MATRIX_CENTER_INDEX + 1];

        return getNearestDirection(board, upperScore, bottomScore, leftScore, rightScore);
    }

    final private int[] getNearestDirection(
            int[][] board,
            int upperScore,
            int bottomScore,
            int leftScore,
            int rightScore) {

        int maxValue = max(upperScore, bottomScore, leftScore, rightScore);

        if (maxValue < 1) {
            return new int[] { playerRowIndex, playerColumnIndex };
        }

        int countOfMaxValues = 0;
        if (upperScore == maxValue) {
            countOfMaxValues += 1;
        }
        if (bottomScore == maxValue) {
            countOfMaxValues += 1;
        }
        if (leftScore == maxValue) {
            countOfMaxValues += 1;
        }
        if (rightScore == maxValue) {
            countOfMaxValues += 1;
        }

        if (countOfMaxValues == 1) {
            if (upperScore == maxValue) {
                return new int[] { playerRowIndex - 1, playerColumnIndex };
            } else if (bottomScore == maxValue) {
                return new int[] { playerRowIndex + 1, playerColumnIndex };
            } else if (leftScore == maxValue) {
                return new int[] { playerRowIndex, playerColumnIndex - 1 };
            } else {
                return new int[] { playerRowIndex, playerColumnIndex + 1 };
            }
        }

        int nearestUpperLength = 1000;
        if (upperScore == maxValue) {
            int nearestRowIndex = playerRowIndex - 1;
            while (nearestRowIndex >= 0) {
                if (board[nearestRowIndex][playerColumnIndex] > 0) {
                    int length = playerRowIndex - nearestRowIndex;
                    if (length < nearestUpperLength) {
                        nearestUpperLength = length;
                    }
                    break;
                }

                int nearestLeftColumnIndex = playerColumnIndex - 1;
                while (nearestLeftColumnIndex >= 0) {
                    if (board[nearestRowIndex][nearestLeftColumnIndex] > 0) {
                        int length = playerColumnIndex - nearestLeftColumnIndex + playerRowIndex - nearestRowIndex;
                        if (length < nearestUpperLength) {
                            nearestUpperLength = length;
                        }
                        break;
                    }
                    nearestLeftColumnIndex -= 1;
                }

                int nearestRightColumnIndex = playerColumnIndex + 1;
                while (nearestRightColumnIndex < BOARD_SIDE_SIZE) {
                    if (board[nearestRowIndex][nearestRightColumnIndex] > 0) {
                        int length = nearestRightColumnIndex - playerColumnIndex + playerRowIndex - nearestRowIndex;
                        if (length < nearestUpperLength) {
                            nearestUpperLength = length;
                        }
                        break;
                    }
                    nearestRightColumnIndex += 1;
                }

                nearestRowIndex -= 1;
            }
        }

        int nearestBottomLength = 1000;
        if (bottomScore == maxValue) {
            int nearestRowIndex = playerRowIndex + 1;
            while (nearestRowIndex < BOARD_SIDE_SIZE) {
                if (board[nearestRowIndex][playerColumnIndex] > 0) {
                    int length = nearestRowIndex - playerRowIndex;
                    if (length < nearestBottomLength) {
                        nearestBottomLength = length;
                    }
                    break;
                }

                int nearestLeftColumnIndex = playerColumnIndex - 1;
                while (nearestLeftColumnIndex >= 0) {
                    if (board[nearestRowIndex][nearestLeftColumnIndex] > 0) {
                        int length = playerColumnIndex - nearestLeftColumnIndex + nearestRowIndex - playerRowIndex;
                        if (length < nearestBottomLength) {
                            nearestBottomLength = length;
                        }
                        break;
                    }
                    nearestLeftColumnIndex -= 1;
                }

                int nearestRightColumnIndex = playerColumnIndex + 1;
                while (nearestRightColumnIndex < BOARD_SIDE_SIZE) {
                    if (board[nearestRowIndex][nearestRightColumnIndex] > 0) {
                        int length = nearestRightColumnIndex - playerColumnIndex + nearestRowIndex - playerRowIndex;
                        if (length < nearestBottomLength) {
                            nearestBottomLength = length;
                        }
                        break;
                    }
                    nearestRightColumnIndex += 1;
                }

                nearestRowIndex += 1;
            }
        }

        int nearestLeftLength = 1000;
        if (leftScore == maxValue) {
            int nearestColumnIndex = playerColumnIndex - 1;
            while (nearestColumnIndex >= 0) {
                if (board[playerRowIndex][nearestColumnIndex] > 0) {
                    int length = playerColumnIndex - nearestColumnIndex;
                    if (length < nearestLeftLength) {
                        nearestLeftLength = length;
                    }
                    break;
                }

                int nearestTopRowIndex = playerRowIndex - 1;
                while (nearestTopRowIndex >= 0) {
                    if (board[nearestTopRowIndex][nearestColumnIndex] > 0) {
                        int length = playerColumnIndex - nearestColumnIndex + playerRowIndex - nearestTopRowIndex;
                        if (length < nearestLeftLength) {
                            nearestLeftLength = length;
                        }
                        break;
                    }
                    nearestTopRowIndex -= 1;
                }

                int nearestBottomRowIndex = playerRowIndex + 1;
                while (nearestBottomRowIndex < BOARD_SIDE_SIZE) {
                    if (board[nearestBottomRowIndex][nearestColumnIndex] > 0) {
                        int length = playerColumnIndex - nearestColumnIndex + nearestBottomRowIndex - playerRowIndex;
                        if (length < nearestLeftLength) {
                            nearestLeftLength = length;
                        }
                        break;
                    }
                    nearestBottomRowIndex += 1;
                }

                nearestColumnIndex -= 1;
            }
        }

        int nearestRightLength = 1000;
        if (rightScore == maxValue) {
            int nearestColumnIndex = playerColumnIndex + 1;
            while (nearestColumnIndex < BOARD_SIDE_SIZE) {
                if (board[playerRowIndex][nearestColumnIndex] > 0) {
                    int length = nearestColumnIndex - playerColumnIndex;
                    if (length < nearestRightLength) {
                        nearestRightLength = length;
                    }
                    break;
                }

                int nearestTopRowIndex = playerRowIndex - 1;
                while (nearestTopRowIndex >= 0) {
                    if (board[nearestTopRowIndex][nearestColumnIndex] > 0) {
                        int length = nearestColumnIndex - playerColumnIndex + playerRowIndex - nearestTopRowIndex;
                        if (length < nearestRightLength) {
                            nearestRightLength = length;
                        }
                        break;
                    }
                    nearestTopRowIndex -= 1;
                }

                int nearestBottomRowIndex = playerRowIndex + 1;
                while (nearestBottomRowIndex < BOARD_SIDE_SIZE) {
                    if (board[nearestBottomRowIndex][nearestColumnIndex] > 0) {
                        int length = nearestColumnIndex - playerColumnIndex + nearestBottomRowIndex - playerRowIndex;
                        if (length < nearestRightLength) {
                            nearestRightLength = length;
                        }
                        break;
                    }
                    nearestBottomRowIndex += 1;
                }

                nearestColumnIndex += 1;
            }
        }

        int minValue = min(nearestUpperLength, nearestBottomLength, nearestLeftLength, nearestRightLength);

        if (nearestUpperLength == minValue) {
            return new int[] { playerRowIndex - 1, playerColumnIndex };
        } else if (nearestBottomLength == minValue) {
            return new int[] { playerRowIndex + 1, playerColumnIndex };
        } else if (nearestLeftLength == minValue) {
            return new int[] { playerRowIndex, playerColumnIndex - 1 };
        } else {
            return new int[] { playerRowIndex, playerColumnIndex + 1 };
        }
    }

    final private int[] getGreedyFloatingRadiusMove(int[][] board, int movesLeft) {
        final int FULL_BOARD_VISION_RADIUS = BOARD_SIDE_SIZE - 1;
        final int CURRENT_RADIUS_VISION = movesLeft;

        if (CURRENT_RADIUS_VISION < 2) {
            return getGreedySimpleMove(board);
        }

        if (CURRENT_RADIUS_VISION >= FULL_BOARD_VISION_RADIUS) {
            return getGreedyFullVisionMove(board);
        }

        return getGreedyPartialVisionMove(board, CURRENT_RADIUS_VISION);
    }

    final private static int max(int first, int second) {
        return Math.max(first, second);
    }

    final private static int max(int first, int second, int third) {
        return max(max(first, second), third);
    }

    final private static int max(int first, int second, int third, int fourth) {
        return max(max(first, second, third), fourth);
    }

    final private static int min(int first, int second, int third, int fourth) {
        return Math.min(Math.min(Math.min(first, second), third), fourth);
    }
}
