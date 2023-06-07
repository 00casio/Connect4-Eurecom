/* To compile this as a shared library, use:
 * g++ -shared ai.cpp -o libai.so -O3 -I /usr/include/python3.11 -lboost_python311 -fPIC
 * or another program that would output the same thing
 * The benchmark STRONGLY suggest that clang++ is better
*/

#include "ai.h"

int Game::putPiece(uint64_t *player, const int col, uint8_t *heights) {
    if (heights[col] > MAX_ALLOWED_HEIGHT) {
        return NOT_ALLOWED;
    }
    *player ^= 1ULL << heights[col];
    heights[col] += 8;
    current_depth++;
    return col;
}

void Game::removePiece(uint64_t *player, const int col, uint8_t *heights) {
    heights[col] -= 8;
    current_depth--;
    *player &= ~(1ULL << heights[col]);
}

int Game::countNbrOne(const uint64_t bitboard) {
    int count_one = 0;
    int64_t gaëtan = 1;
    for (int i = 0; i < NBR_LINE; i++) {
        for (int j = 0; j < NBR_COL; j++) {
            if ((gaëtan & bitboard) != 0) {
                count_one++;
            }
            gaëtan <<= 1;
        }
        gaëtan <<= 1;
    }
    return count_one;
}

bool Game::human_winning() {
    bool winning = false;
    countPoints(human_board, &winning);
    return winning;
}

bool Game::ai_winning() {
    bool winning = false;
    countPoints(ai_board, &winning);
    return winning;
}

bool Game::draw() {
    if ((human_board | ai_board) == 280371153272574) {
        return true;
    }
    return false;
}

int Game::countPoints(const uint64_t bitboard, bool *state) {
    int nbr_3_in_line = 0;
    int nbr_2_in_line = 0;

    uint64_t tmp = bitboard & (bitboard >> 8);
    if (tmp != 0) {
        nbr_2_in_line += countNbrOne(tmp);
        tmp &= (bitboard >> 16);
        if (tmp != 0) {
            if (tmp & (bitboard >> 24)) {
                *state = true;
                return 0;
            }
            nbr_3_in_line += countNbrOne(tmp);
        }
    }

    tmp = bitboard & (bitboard >> 1);
    if (tmp != 0) {
        nbr_2_in_line += countNbrOne(tmp);
        tmp &= (bitboard >> 2);
        if (tmp != 0) {
            if (tmp & (bitboard >> 3)) {
                *state = true;
                return 0;
            }
            nbr_3_in_line += countNbrOne(tmp);
        }
    }

    tmp = bitboard & (bitboard >> 7);
    if (tmp != 0) {
        nbr_2_in_line += countNbrOne(tmp);
        tmp &= (bitboard >> 14);
        if (tmp != 0) {
            if (tmp & (bitboard >> 21)) {
                *state = true;
                return 0;
            }
            nbr_3_in_line += countNbrOne(tmp);
        }
    }

    tmp = bitboard & (bitboard >> 9);
    if (tmp != 0) {
        nbr_2_in_line += countNbrOne(tmp);
        tmp &= (bitboard >> 18);
        if (tmp != 0) {
            if (tmp & (bitboard >> 27)) {
                *state = true;
                return 0;
            }
            nbr_3_in_line += countNbrOne(tmp);
        }
    }

    return nbr_3_in_line * 20 + nbr_2_in_line * 2;
}

bool Game::quickWinning(const uint64_t bitboard) {
    // |
    if ((bitboard & (bitboard >> 8) & (bitboard >> 16) & (bitboard >> 24)) != 0) {
        return true;
    }
    // -
    if ((bitboard & (bitboard >> 1) & (bitboard >> 2) & (bitboard >> 3)) != 0) {
        return true;
    }
    // /
    if ((bitboard & (bitboard >> 7) & (bitboard >> 14) & (bitboard >> 21)) != 0) {
        return true;
    }
    // \ _
    if ((bitboard & (bitboard >> 9) & (bitboard >> 18) & (bitboard >> 27)) != 0) {
        return true;
    }
    return false;
}

int Game::evaluateBoard(const uint64_t bitboard, const uint64_t oppBitboard, const int depth) {
    int score = 0;
    bool winning = false;
    bool losing = false;
    count++;

    score += countPoints(bitboard, &winning);
    if (winning) {
        return SCORE_SOMEONE_WIN;
    }
    score -= countPoints(oppBitboard, &losing);
    if (losing) {
        return - SCORE_SOMEONE_WIN;
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

/* int Game::negamax(uint64_t *player, uint64_t *opponent, uint8_t *heights, const int max_depth, double alpha, double beta) {
// double Game::negamax(uint64_t *player, uint64_t *opponent, uint8_t *heights, const int depth, const int sign_result, double alpha, double beta) {
    count++;
    if (this->current_depth >= NBR_COL*NBR_LINE) {
        return 0;
    }
    // if (max_depth <= 0) {
    //     return evaluateBoard(*player, *opponent, 0);
    // }

    bool winning = false;
    for (int col = 0; col < NBR_COL; col++) {
        int dpRes = putPiece(player, col, heights);
        if (dpRes == NOT_ALLOWED) {
            continue;
        }
        countPoints(*player, &winning);
        removePiece(player, col, heights);
        if (winning) {
            // return (NBR_COL*NBR_LINE + 1 - this->current_depth)/2;
            return INFINITY;
        }
    }

    int maxScore = (NBR_COL*NBR_LINE - 1 - this->current_depth)/2;
    if (int value = transTable.get(*player)) {
        maxScore = value + MIN_SCORE - 1;
    }
    if (beta > maxScore) {
        beta = maxScore;
        if (alpha >= beta) {
            return beta;
        }
    }

    // int bestScore = - NBR_COL*NBR_LINE;
    for (int i = 0; i < NBR_COL; i++) {
        int col = col_ordering[i];
        int dpRes = putPiece(player, col, heights);
        if (dpRes == NOT_ALLOWED) {
            continue;
        }
        double score = - negamax(opponent, player, heights, max_depth - 1, - beta, - alpha);
        removePiece(player, col, heights);

        if (score >= beta) {
            return score;
        }
        if (score > alpha) {
            alpha = score;
        }
    }
    transTable.put(2**player+*opponent, alpha - MIN_SCORE + 1);
    // 2* the value of player + the value of opponent
    return alpha;
} */

int Game::negamax(uint64_t *player, uint64_t *opponent, uint8_t *heights, const int depth, int alpha, int beta) {
    int result = evaluateBoard(*player, *opponent, depth);
    if (depth <= 0) {
        return result - current_depth;
    }

    if (result != 111) {
        return result - current_depth;
    }

    int maxScore = SCORE_SOMEONE_WIN - current_depth;
    // if (int value = transTable.get(*player)) {
    //     maxScore = value + result - 1;
    // }
    if (beta > maxScore) {
        beta = maxScore;
        if (alpha >= beta) {
            return beta;
        }
    }

    // Testing if the player can win with his next move
    for (int i = 0; i < NBR_COL; i++) {
        int dpRes = putPiece(player, i, heights);
        if (dpRes == NOT_ALLOWED) {
            continue;
        }
        if (quickWinning(*player)) {
            removePiece(player, dpRes, heights);
            return SCORE_SOMEONE_WIN - current_depth;
        }
        removePiece(player, dpRes, heights);
    }

    // Do all move and look for the result of the opponent
    for (int i = 0; i < NBR_COL; i++) {
        int col = col_ordering[i];
        int dpRes = putPiece(player, col, heights);
        if (dpRes == NOT_ALLOWED) {
            continue;
        }

        int score = - negamax(opponent, player, heights, depth - 1, - beta, - alpha);
        removePiece(player, col, heights);

        if (score >= beta) {
            return score;
        }
        if (score > alpha) {
            alpha = score;
        }
    }
    // transTable.put(2**player+*opponent, alpha - result + 1);
    // 2* the value of player + the value of opponent
    return alpha;
}

int Game::bestStartingMove(const uint8_t *heights) {
    if (heights[3] < MAX_ALLOWED_HEIGHT) return 3;
    if (heights[2] < MAX_ALLOWED_HEIGHT) return 2;
    if (heights[4] < MAX_ALLOWED_HEIGHT) return 4;
    if (heights[1] < MAX_ALLOWED_HEIGHT) return 1;
    if (heights[5] < MAX_ALLOWED_HEIGHT) return 5;
    if (heights[0] < MAX_ALLOWED_HEIGHT) return 0;
    if (heights[6] < MAX_ALLOWED_HEIGHT) return 6;
    printBoard();
    for (int i = 0; i < NBR_COL; i++){
        printf(" %d  ", heights[i]);
    }
    printf("\n");
    fprintf(stderr, "All columns are full\n");
    exit(-1);
}

int Game::aiSearchMove(uint64_t *player, uint64_t *opponent, const int depth, uint8_t *heights) {
    // if ((ai_board == 0) && (human_board == 0)) {
    //     return 3;
    // }
    int bestMove = bestStartingMove(heights);
    int alpha = - SCORE_SOMEONE_WIN;
    int beta = SCORE_SOMEONE_WIN;

    for (int i = 0; i < NBR_COL; i++) {
        int col = col_ordering[i];
        int dpRes = putPiece(player, col, heights);
        if (dpRes == NOT_ALLOWED) {
            continue;
        }
        int score = - negamax(opponent, player, heights, depth - 1, - beta, - alpha);
        removePiece(player, col, heights);

        if (score > alpha) {
            alpha = score;
            bestMove = col;
        }
    }
    return bestMove;

    // return negamax(player, opponent, heights, depth, +1, - INFINITY, +INFINITY);
/*     ThreadPool thread_pool(thread_count);
    int bestMove = bestStartingMove(heights);
    double bestScore = - INFINITY;
    value_search tmp(*player, *opponent, depth, heights);

    for (int i = 0; i < NBR_COL; i++) {
        //thread_pool.addTask([this, tmp, i, &bestScore, &bestMove]{
        //     start_search(tmp, i, &bestScore, &bestMove);
        // });
        start_search(tmp, i, &bestScore, &bestMove);
    }
    thread_pool.waitForCompletion();
    return bestMove; */
}

int Game::aiMove(const int depth) {
    int ai_col = aiSearchMove(&ai_board, &human_board, depth, col_heights);
    return putPiece(&ai_board, ai_col, col_heights);
}

int Game::humanMove(const int col) {
    if (col < 0 || col > 6) {
        return NOT_ALLOWED;
    }
    return putPiece(&human_board, col, col_heights);
}

int Game::forceAIMove(const int col) {
    return putPiece(&ai_board, col, col_heights);
}

int Game::scoreAIpos() {
    return negamax(&ai_board, &human_board, col_heights, 13, - SCORE_SOMEONE_WIN, SCORE_SOMEONE_WIN);
}

void Game::resetBoard() {
    this->human_board = 0b0;
    this->ai_board = 0b0;
    this->current_depth = 0;
    this->count = 0;
    for (int i = 0; i < NBR_COL; i++) {
        this->col_heights[i] = NBR_COL - i;
    }
    for (int i = 0; i < SIZE_VECT; i++) {
        this->transTable.t[i].id = 0;
        this->transTable.t[i].value = 0;
    }
}

void Game::printBoard() {
    unsigned short column = 0;
    uint64_t place = 1UL << 47;
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
    for (int i = 0; i < NBR_COL; i++)
        printf(" %d  ", i);
    printf("\n");
}

int Game::run() {
    int depth;
    int trash;
    printf("AI depth: ");
    trash = scanf("%d", &depth);
    while (true) {
        if (current_player == HUMAN) {
            printBoard();
            int col;
            printf("Your move [0-6]: ");
            trash = scanf("%d", &col);
            while (humanMove(col) == NOT_ALLOWED) {
                printf("Reenter your move [0-6]: ");
                trash = scanf("%d", &col);
            }
        } else {
            clock_t start = clock();
            printf("AI is thinking... \n");
            aiMove(depth);
            clock_t end = clock();
            printf("and it took %lf seconds\n", (double)(end - start) / CLOCKS_PER_SEC);
        }
        current_player = ((current_player == HUMAN) ? AI : HUMAN);
        int32_t result = evaluateBoard(ai_board, human_board, 1);
        if (result > 30000) {
            printf("AI WINS!\n");
            printBoard();
            return EXIT_SUCCESS;
        } else if (result < -30000) {
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

int main(int argc, char **argv) {
    Game g;
    return g.run();
    // char *tmp;
    // g.human_board = strtoul(argv[1], &tmp, 10);
    // g.ai_board = strtoul(argv[2], &tmp, 10);

    // g.printBoard();
    // printf("%i", g.aiMove(*argv[3] - '0'));
    // return 0;
}
