/* To compile this as a shared library, use:
 * g++ -shared ai.cpp -o libai.so -O3 -I /usr/include/python3.11 -lboost_python311 -fPIC
 * or another program that would output the same thing
*/

#include "ai.h"

int Game::putPiece(unsigned long long *player, const int col, uint8_t *heights) {
    if (heights[col] > MAX_ALLOWED_HEIGHT) {
        return NOT_ALLOWED;
    }
    count++;
    *player ^= 1ULL << heights[col];
    heights[col] += 8;
    this->current_depth++;
    return col;
}

void Game::removePiece(unsigned long long *player, const int col, uint8_t *heights) {
    heights[col] -= 8;
    this->current_depth--;
    *player &= ~(1ULL << heights[col]);
}

int Game::countNbrOne(const unsigned long long bitboard) {
    int count_one = 0;
    int gaëtan = 1;
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

int Game::human_winning() {
    bool winning = false;
    countPoints(human_board, &winning);
    return winning;
}

int Game::ai_winning() {
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

int Game::countPoints(const unsigned long long bitboard, bool *state) {
    int nbr_3_in_line = 0;
    int nbr_2_in_line = 0;

    unsigned long long tmp = bitboard & (bitboard >> 8);
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

double Game::evaluateBoard(const unsigned long long bitboard, const unsigned long long oppBitboard, const int depth) {
    double score = 0;
    bool winning = false;
    bool losing = false;

    score += countPoints(bitboard, &winning);
    if (winning) {
        return INFINITY;
    }
    score -= countPoints(oppBitboard, &losing);
    if (losing) {
        return -INFINITY;
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

double Game::negamax(unsigned long long *player, unsigned long long *opponent, uint8_t *heights, const int depth, const int sign_result, double alpha, double beta) {
    if (this->current_depth >= NBR_COL*NBR_LINE) {
        return 0;
    }

    bool winning = false;
    for (int i = 0; i < NBR_COL; i++) {
        int dpRes = putPiece(player, i, heights);
        if (dpRes == NOT_ALLOWED) {
            continue;
        }
        countPoints(*player, &winning);
        removePiece(player, i, heights);
        if (winning) {
            return (double) (NBR_COL*NBR_LINE + 1 - this->current_depth)/2;
        }
    }

    int maxScore = (NBR_COL*NBR_LINE - 1 - this->current_depth)/2;
    if (beta > maxScore) {
        beta = maxScore;
        if (alpha >= beta) {
            return beta;
        }
    }

    // int bestScore = - NBR_COL*NBR_LINE;
    for (int i = 0; i < NBR_COL; i++) {
        int dpRes = putPiece(player, i, heights);
        if (dpRes == NOT_ALLOWED) {
            continue;
        }
        double score = - negamax(opponent, player, heights, depth - 1, - sign_result, - beta, - alpha);
        removePiece(player, i, heights);

        if (score >= beta) {
            return score;
        }
        if (score > alpha) {
            alpha = score;
        }
    }
    return alpha;

/*     double result = evaluateBoard(*player, *opponent, depth);
    if (depth <= 0) {
        return result;
    }

    if (result != 111) {
        return result - sign_result * depth;
    }

    double bestScore = - INFINITY;
    for (int i = 0; i < NBR_COL; i++) {
        int dpRes = putPiece(player, i, heights);
        if (dpRes == NOT_ALLOWED) {
            continue;
        }

        double score = - negamax(opponent, player, heights, depth - 1, - sign_result, - beta, - alpha);
        removePiece(player, i, heights);

        if (score > bestScore) {
            bestScore = score;
        }
        if (alpha > score) {
            alpha = score;
        }
        if (alpha >= beta) {
            break;
        }
    }
    return bestScore; */
}

double Game::minimax(unsigned long long *player, unsigned long long *opponent, uint8_t *heights, const int depth, const bool isMaximising, double alpha, double beta) {
    double result = evaluateBoard(*player, *opponent, depth);
    if (depth <= 0) {
        return result;
    }

    if (result != 111) {
        if (isMaximising) {
            return result - depth;
        }
        return result + depth;
    }

    if (isMaximising) {
        double bestScore = -INFINITY;
        for (int i = 0; i < NBR_COL; i++) {
            int dpRes = putPiece(player, i, heights);
            if (dpRes == NOT_ALLOWED) {
                continue;
            }

            double score = minimax(player, opponent, heights, depth - 1, false, alpha, beta);
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
            int dpRes = putPiece(opponent, i, heights);
            if (dpRes == NOT_ALLOWED) {
                continue;
            }

            double score = minimax(player, opponent, heights, depth - 1, true, alpha, beta);
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

void Game::start_search(value_search values, int column_played, double *best_score, int *best_move) {
    int dpRes = putPiece(&values.player, column_played, values.heights);
    if (dpRes == NOT_ALLOWED) {
        return;
    }

    double score;
    if (true) {
        score = minimax(&values.player, &values.opponent, values.heights, values.depth - 1, false, - INFINITY, + INFINITY);
    } else {
        score = - negamax(&values.opponent, &values.player, values.heights, values.depth - 1, -1, - INFINITY, + INFINITY);
        // score += column_played;
    }
    removePiece(&values.player, column_played, values.heights);

    if (score > *best_score) {
        *best_score = score;
        *best_move = column_played;
    }
}

int Game::aiSearchMove(unsigned long long *player, unsigned long long *opponent, const int depth, uint8_t *heights) {
<<<<<<< HEAD
    int bestMove = bestStartingMove(heights);
    int bestScore = - NBR_COL*NBR_LINE;
    double alpha = - INFINITY;
    double beta = INFINITY;

    for (int i = 0; i < NBR_COL; i++) {
        int dpRes = putPiece(player, i, heights);
        if (dpRes == NOT_ALLOWED) {
            continue;
        }
        double score = - negamax(opponent, player, heights, depth - 1, - 1, - beta, - alpha);
        removePiece(player, i, heights);

        if (score > bestScore) {
            bestScore = score;
            bestMove = i;
        }
        if (score > alpha) {
            alpha = score;
        }
    }
    return bestMove;

    // return negamax(player, opponent, heights, depth, +1, - INFINITY, +INFINITY);
/*     ThreadPool thread_pool(thread_count);
=======
    if ((*player == 0) && (*opponent == 0)) {
        return 3;
    }
    ThreadPool thread_pool(thread_count);
>>>>>>> d2effdc (criteria tests + weird stats)
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

int Game::aiMove(int depth) {
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
    return negamax(&ai_board, &human_board, col_heights, 0, +1, -INFINITY, INFINITY);
}

void Game::resetBoard() {
    this->human_board = 0b0;
    this->ai_board = 0b0;
    this->current_depth = 0;
    for (int i = 0; i < NBR_COL; i++) {
        this->col_heights[i] = NBR_COL - i;
    }
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
        int result = evaluateBoard(ai_board, human_board, 1);
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
