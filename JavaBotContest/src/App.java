public class App {
    private final static int FIRST_PLAYER_IDENTIFIER = -1;
    private final static int BOARD_SIDE_SIZE = GameState.WIDTH;

    public static void main(String[] args) throws Exception {
        KecapbBot bot = new KecapbBot();
        bot.takeYourNumber(FIRST_PLAYER_IDENTIFIER);

        int roundsToEnd = 100;
        int[][] map = getMap();
        printMap(map);
        System.out.println();

        GameState gameState = new GameState(roundsToEnd, map);

        while (roundsToEnd > 0) {
            long startTime = System.nanoTime();
            Direction direction = bot.step(gameState);
            long stopTime = System.nanoTime();
            System.out.println((stopTime - startTime) / 1_000_000.0);
            System.out.println(direction);
            printMap(map);
            System.out.println("=====================" + roundsToEnd + "==========================");
            System.in.read();
            System.in.read();

            roundsToEnd -= 1;
            gameState.roundsToEnd = roundsToEnd;
        }
    }

    final private static int[][] getMap() {
        return new int[][] {
                { -1, 45, 0, 0, 0, 0, 0, -16, -16, -16, 1, 0, 44, 27, 0, },
                { 0, -16, 0, 0, 0, 0, 0, 0, 17, 0, 0, 3, -16, 0, 28, },
                { 0, 28, 0, 0, 0, 19, 7, -16, -16, 0, 0, 19, -16, 0, 6, },
                { 0, 45, 36, 12, 0, 0, 31, -16, 34, 0, 0, 0, -16, 46, 0, },
                { 0, 0, 0, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0, 0, },
                { 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 18, 0, 0, 0, },
                { 0, 0, 0, 26, 0, 0, 36, 0, 0, 0, 0, 0, 40, 0, 0, },
                { 0, 0, 46, 10, 0, 18, 0, 0, 0, 18, 0, 10, 46, 0, 0, },
                { 0, 0, 40, 0, 0, 0, 0, 0, 36, 0, 0, 26, 0, 0, 0, },
                { 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, },
                { 0, 0, 0, 0, 0, 0, 0, 41, 0, 0, 0, 0, 0, 0, 0, },
                { 0, 46, -16, 0, 0, 0, 34, -16, 31, 0, 0, 12, 36, 45, 0, },
                { 6, 0, -16, 19, 0, 0, -16, -16, 7, 19, 0, 0, 0, 28, 0, },
                { 28, 0, -16, 3, 0, 0, 17, 0, 0, 0, 0, 0, 0, -16, 0, },
                { 0, 27, 44, 0, 1, -16, -16, -16, 0, 0, 0, 0, 0, 45, -2, },
        };
    }

    final private static void printMap(int[][] map) {
        for (int rowIndex = 0; rowIndex < BOARD_SIDE_SIZE; ++rowIndex) {
            for (int columnIndex = 0; columnIndex < BOARD_SIDE_SIZE; ++columnIndex) {
                System.out.print(String.format("%1$4s", map[rowIndex][columnIndex]));
            }
            System.out.println();
        }
    }
}
