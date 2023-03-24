#include "ai.hpp"

/* To compile this as a shared library, use:
 * g++ ai.cpp -shared -O3 -o libai.so
or another program that would output the same thing
*/

/*
The reason we are using (internally) a 8x8 board is because we are using an
unsigned long long (so 64 bits long) variable to put the pieces in places. We
could use a 7*7 board or even a 7x6 but it would require to rework how the
pieces are handled, and it may slow down a lot the algorithm.
*/

#define NBR_LINE 6
#define NBR_COL 7
#define BOARDLEN 64
#define SYMBOL_AI "x"
#define SYMBOL_HUMAN "o"

int Game::putPiece(unsigned long long *player, int col, uint8_t *heights) {
    if (heights[col] < 16 || col < 0 || col > 6) {
        return 1;
    }
    *player ^= 1ULL << (BOARDLEN - 1 - heights[col]);
    heights[col] -= 8;
    return 0;
}

void Game::removePiece(unsigned long long *player, int col, uint8_t *heights) {
    heights[col] += 8;
    *player &= ~(1UL << (BOARDLEN - 1 - heights[col]));
}

bool Game::winning(unsigned long long bitboard) {
    unsigned long long m;
    m = (bitboard & (bitboard >> 8));
    if ((m & (m >> 16)) != 0) {
        return true;
    }
    m = (bitboard & (bitboard >> 1));
    if ((m & (m >> 2)) != 0) {
        return true;
    }
    m = (bitboard & (bitboard >> 7));
    if ((m & (m >> 14)) != 0) {
        return true;
    }
    m = (bitboard & (bitboard >> 9));
    if ((m & (m >> 18)) != 0) {
        return true;
    }
    return false;
}

int Game::evaluateBoard(unsigned long long bitboard, unsigned long long oppBitboard, int depth) {
    int score = 0;

    // Vertical check
    if (winning(bitboard)) {
        return 100000;
    } else if (winning(oppBitboard)) {
        return -100000;
    }

    // Points when there are 3 next to each other
    if ((bitboard & (bitboard >> 8) & (bitboard >> 16)) != 0) {
        score += 6;
    }
    if ((bitboard & (bitboard >> 1) & (bitboard >> 2)) != 0) {
        score += 6;
    }
    if ((bitboard & (bitboard >> 7) & (bitboard >> 14)) != 0) {
        score += 6;
    }
    if ((bitboard & (bitboard >> 9) & (bitboard >> 18)) != 0) {
        score += 6;
    }

    // if board is maxed out (excluding top row)
    if ((bitboard | oppBitboard) == 280371153272574) {
        return 0;
    }

    if (!depth) {
        return score;
    }
    return 111;
}

int Game::minimax(unsigned long long *player, unsigned long long *opponent, uint8_t *heights, int depth, bool isMaximising, double alpha, double beta) {
    int result = evaluateBoard(*player, *opponent, depth);
    if (depth == 0 || result != 111)
        return result;

    if (isMaximising) {
        double bestScore = -INFINITY;
        for (int i = 0; i < NBR_COL; i++) {
            bool dpRes = putPiece(player, i, heights);
            if (dpRes != 0) {
                continue;
            }

            int score = minimax(player, opponent, heights, depth - 1, false, alpha, beta);
            removePiece(player, i, heights);

            if (score > bestScore) {
                bestScore = score;
            }
            if (alpha > score) {
                alpha = score;
            }
            if (beta <= alpha) {
                break;
            }
        }
        return bestScore;
    } else {
        double bestScore = INFINITY;
        for (int i = 0; i < NBR_COL; i++) {
            bool dpRes = putPiece(opponent, i, heights);
            if (dpRes != 0) {
                continue;
            }

            int score = minimax(player, opponent, heights, depth - 1, true, alpha, beta);
            removePiece(opponent, i, heights);

            if (score < bestScore) {
                bestScore = score;
            }
            if (beta < score) {
                beta = score;
            }
            if (beta <= alpha) {
                break;
            }
        }
        return bestScore;
    }
}

int Game::aiSearchMove(unsigned long long *player, unsigned long long *opponent, int depth, uint8_t *heights) {
    int bestMove = 0;
    double bestScore = -INFINITY;

    for (int i = 0; i < NBR_COL; i++) {
        bool dpRes = putPiece(player, i, heights);
        if (dpRes != 0) {
            continue;
        }

        int score = minimax(player, opponent, heights, depth, false, -INFINITY, INFINITY);
        removePiece(player, i, heights);
        if (score > bestScore) {
            bestScore = score;
            bestMove = i;
        }
    }
    return bestMove;
}

int Game::aiMove(int depth) {
    int ai_col = aiSearchMove(&ai_board, &human_board, depth, col_heights);
    return putPiece(&ai_board, ai_col, col_heights);
}

int Game::humanMove(int col) {
    return putPiece(&human_board, col, col_heights);
}

void Game::printBoard() {
    unsigned short column = 0;
    unsigned long long place = 1UL << 47;
    for (int i = 16; i < BOARDLEN; i++) {
        if ((i % 8 == 7)) {
            place >>= 1;
            continue;
        }
        column++;
        printf("|");
        if ((ai_board & place) == place)
            printf(" %s ", SYMBOL_AI);
        else if ((human_board & place) == place)
            printf(" %s ", SYMBOL_HUMAN);
        else
            printf(" . ");

        if (!(column % 7))
            printf("|\n");
        place >>= 1;
    }
    printf("-----------------------------\n ");
    for (int i = 1; i < NBR_COL + 1; i++)
        printf(" %d  ", i);
    printf("\n");
}

int Game::run() {
    int depth;
    printf("AI depth: ");
    scanf("%d", &depth);
    while (true) {
        if (current_player == HUMAN) {
            printBoard();
            int col;
            printf("Your move [1-7]: ");
            scanf("%d", &col);
            while (humanMove(col - 1) != 0) {
                printf("Reenter your move [1-7]: ");
                scanf("%d", &col);
            }
        } else {
            clock_t start = clock();
            printf("AI is thinking... ");
            aiMove(depth);
            clock_t end = clock();
            printf("and it took %lf seconds\n", (double)(end - start) / CLOCKS_PER_SEC);
        }
        current_player = ((current_player == HUMAN) ? AI : HUMAN);
        int result = evaluateBoard(ai_board, human_board, 1);
        if (result == 100000) {
            printf("AI WINS!\n");
            printBoard();
            return EXIT_SUCCESS;
        } else if (result == -100000) {
            printf("HUMAN WINS!\n");
            printBoard();
            return EXIT_SUCCESS;
        } else if (result == 0) {
            printf("DRAW!\n");
            printBoard();
            return EXIT_SUCCESS;
        }
        if (result == 111) {
            continue;
        }
    }

    return EXIT_SUCCESS;
}
