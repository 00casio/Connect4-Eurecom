/* To compile this as a shared library, use:
 * g++ -shared ai.cpp -o libai.so -O3 -I /usr/include/python3.11 -lboost_python311 -fPIC
 * or another program that would output the same thing
 * The benchmark STRONGLY suggest that clang++ is better
*/

#include "ai.h"

int Game::putPiece(uint64_t *player, const int col) {
    if (col_heights[col] > MAX_ALLOWED_HEIGHT) {
        return NOT_ALLOWED;
    }
    *player ^= 1ULL << col_heights[col];
    col_heights[col] += 8;
    current_depth++;
    return col;
}

void Game::removePiece(uint64_t *player, const int col) {
    col_heights[col] -= 8;
    current_depth--;
    *player &= ~(1ULL << col_heights[col]);
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
    return quickWinning(human_board);
}

bool Game::ai_winning() {
    return quickWinning(ai_board);
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

int Game::negamax(uint64_t *player, uint64_t *opponent, const int depth, int alpha, int beta) {
    int result = evaluateBoard(*player, *opponent, depth);
    if ((depth <= 0) | (result != 111)) {
        return result - current_depth;
    }

    int maxScore = SCORE_SOMEONE_WIN - current_depth;
    if (int value = transTable.get(*player)) {
        maxScore = value + result - 1;
    }
    if (beta > maxScore) {
        beta = maxScore;
        if (alpha >= beta) {
            return beta;
        }
    }

    // Testing if the player can win with his next move
    for (int i = 0; i < NBR_COL; i++) {
        int dpRes = putPiece(player, i);
        if (dpRes == NOT_ALLOWED) {
            continue;
        }
        if (quickWinning(*player)) {
            removePiece(player, dpRes);
            return SCORE_SOMEONE_WIN - current_depth;
        }
        removePiece(player, dpRes);
    }

    // Do all move and look for the result of the opponent
    for (int i = 0; i < NBR_COL; i++) {
        int col = col_ordering[i];
        int dpRes = putPiece(player, col);
        if (dpRes == NOT_ALLOWED) {
            continue;
        }

        int score = - negamax(opponent, player, depth - 1, - beta, - alpha);
        // printBoard();
        // printf("depth = %d, score = %d\n", current_depth, score);
        removePiece(player, col);

        if (score >= beta) {
            return score;
        }
        if (score > alpha) {
            alpha = score;
        }
    }
    transTable.put(2**player+*opponent, alpha - result + 1);
    // 2* the value of player + the value of opponent
    return alpha;
}

int Game::bestStartingMove() {
    if (col_heights[3] < MAX_ALLOWED_HEIGHT) return 3;
    if (col_heights[2] < MAX_ALLOWED_HEIGHT) return 2;
    if (col_heights[4] < MAX_ALLOWED_HEIGHT) return 4;
    if (col_heights[1] < MAX_ALLOWED_HEIGHT) return 1;
    if (col_heights[5] < MAX_ALLOWED_HEIGHT) return 5;
    if (col_heights[0] < MAX_ALLOWED_HEIGHT) return 0;
    if (col_heights[6] < MAX_ALLOWED_HEIGHT) return 6;
    printBoard();
    for (int i = 0; i < NBR_COL; i++){
        printf(" %d  ", col_heights[i]);
    }
    printf("\n");
    fprintf(stderr, "All columns are full\n");
    exit(-1);
}

int Game::aiSearchMove(uint64_t *player, uint64_t *opponent, const int depth) {
    int bestMove = bestStartingMove();
    // int bestScore = - SCORE_SOMEONE_WIN;
    int alpha = - SCORE_SOMEONE_WIN;
    int beta = SCORE_SOMEONE_WIN;

    for (int i = 0; i < NBR_COL; i++) {
        int dpRes = putPiece(player, i);
        if (dpRes == NOT_ALLOWED) {
            continue;
        }
        if (quickWinning(*player)) {
            removePiece(player, dpRes);
            return i;
        }
        removePiece(player, dpRes);
    }

    // int scores[7] = {-SCORE_SOMEONE_WIN, -SCORE_SOMEONE_WIN, -SCORE_SOMEONE_WIN, -SCORE_SOMEONE_WIN, -SCORE_SOMEONE_WIN, -SCORE_SOMEONE_WIN, -SCORE_SOMEONE_WIN};

    for (int i = 0; i < NBR_COL; i++) {
        int col = col_ordering[i];
        int dpRes = putPiece(player, col);
        if (dpRes == NOT_ALLOWED) {
            continue;
        }
        int score = - negamax(opponent, player, depth - 1, - beta, - alpha);
        // printBoard();
        // printf("depth = %d, score = %d\n", current_depth, score);
        removePiece(player, col);

        // scores[col] = score;
        if (score > alpha) {
            alpha = score;
            bestMove = col;
        }
    }
    // bestMove = 3;
    // bestScore = scores[bestMove];
    // for (int i = 0; i < NBR_COL; i++) {
    //     int col = col_ordering[i];
    //     if (scores[col] > bestScore) {
    //         bestScore = scores[col];
    //         bestMove = col;
    //     }
    //     // printf("%d => %d, ", i, scores[i]);
    // }
    return bestMove;
}

int Game::aiMove(const int depth) {
    int ai_col = aiSearchMove(&ai_board, &human_board, depth);
    return putPiece(&ai_board, ai_col);
}

int Game::humanMove(const int col) {
    if (col < 0 || col > 6) {
        return NOT_ALLOWED;
    }
    return putPiece(&human_board, col);
}

int Game::forceAIMove(const int col) {
    return putPiece(&ai_board, col);
}

int Game::scoreAIpos() {
    return negamax(&ai_board, &human_board, 13, - SCORE_SOMEONE_WIN, SCORE_SOMEONE_WIN);
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
    // printf("nbr human: %d, nbr ai: %d\n", countNbrOne(human_board), countNbrOne(ai_board));
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

        if (quickWinning(ai_board)) {
            printf("AI WINS!\n");
            printBoard();
            return EXIT_SUCCESS;
        } else if (quickWinning(human_board)) {
            printf("HUMAN WINS!\n");
            printBoard();
            return EXIT_SUCCESS;
        } else if (draw()) {
            printf("DRAW!\n");
            printBoard();
            return EXIT_SUCCESS;
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
