/* To compile this as a shared library, use:
 * g++ -shared ai.cpp -o libai.so -O3 -I /usr/include/python3.11 -lboost_python311 -fPIC
 * or another program that would output the same thing
*/

#include "ai.hpp"
#include <cstdio>

int Game::putPiece(unsigned long long *player, const int col, uint8_t *heights) {
    if (heights[col] < 16 || col < 0 || col > 6) {
        return NOT_ALLOWED;
    }
    *player ^= 1ULL << (BOARDLEN - 1 - heights[col]);
    heights[col] -= 8;
    return col;
}

void Game::removePiece(unsigned long long *player, const int col, uint8_t *heights) {
    heights[col] += 8;
    *player &= ~(1ULL << (BOARDLEN - 1 - heights[col]));
}

bool Game::winning(const unsigned long long bitboard) {
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

int Game::countNbrOne(const unsigned long long bitboard) {
    int count = 0;
    int gaëtan = 1;
    for (int i = 0; i < BOARDLEN; i++) {
        if ((gaëtan & bitboard) != 0) {
            count++;
        }
        gaëtan <<= 1;
    }
    return count;
}

int Game::nbr3InLine(const unsigned long long bitboard) {
    int nbr_3_in_line = 0;
    // Points when there are 3 disks next to each other
    int tmp = bitboard & (bitboard >> 8) & (bitboard >> 16);
    if (tmp != 0) {
        nbr_3_in_line += countNbrOne(tmp);
    }
    tmp = bitboard & (bitboard >> 1) & (bitboard >> 2);
    if (tmp != 0) {
        nbr_3_in_line += countNbrOne(tmp);
    }
    tmp = bitboard & (bitboard >> 7) & (bitboard >> 14);
    if (tmp != 0) {
        nbr_3_in_line += countNbrOne(tmp);
    }
    tmp = bitboard & (bitboard >> 9) & (bitboard >> 18);
    if (tmp != 0) {
        nbr_3_in_line += countNbrOne(tmp);
    }
    return nbr_3_in_line;
}

int Game::nbr2InLine(const unsigned long long bitboard) {
    int nbr_2_in_line = 0;
    // Points when there are 2 disks next to each other
    int tmp = bitboard & (bitboard >> 8);
    if (tmp != 0) {
        nbr_2_in_line += countNbrOne(tmp);
    }
    tmp = bitboard & (bitboard >> 1);
    if (tmp != 0) {
        nbr_2_in_line += countNbrOne(tmp);
    }
    tmp = bitboard & (bitboard >> 7);
    if (tmp != 0) {
        nbr_2_in_line += countNbrOne(tmp);
    }
    tmp = bitboard & (bitboard >> 9);
    if (tmp != 0) {
        nbr_2_in_line += countNbrOne(tmp);
    }
    return nbr_2_in_line;
}

double Game::evaluateBoard(const unsigned long long bitboard, const unsigned long long oppBitboard, const int depth) {
    int score = 0;

    // Vertical check
    if (winning(bitboard)) {
        return INFINITY;
    } else if (winning(oppBitboard)) {
        return -INFINITY;
    }

    score += nbr3InLine(bitboard) * 20;
    score -= nbr3InLine(oppBitboard) * 20;
    score += nbr2InLine(bitboard) * 2;
    score -= nbr2InLine(oppBitboard) * 2;

    // if board is maxed out (excluding top row)
    if ((bitboard | oppBitboard) == 280371153272574) {
        return 0;
    }

    if (!depth) {
        return score;
    }
    return 111;
}

double Game::minimax(unsigned long long *player, unsigned long long *opponent, uint8_t *heights, const int depth, const bool isMaximising, double alpha, double beta) {
    double result = evaluateBoard(*player, *opponent, depth);
    if (depth == 0 || result != 111)
        return result;

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
    if (heights[3] > 15) return 3;
    if (heights[2] > 15) return 2;
    if (heights[4] > 15) return 4;
    if (heights[1] > 15) return 1;
    if (heights[5] > 15) return 5;
    if (heights[0] > 15) return 0;
    if (heights[6] > 15) return 6;
    fprintf(stderr, "All columns are full\n");
    exit(-1);
}

int Game::aiSearchMove(unsigned long long *player, unsigned long long *opponent, const int depth, uint8_t *heights) {
    int bestMove = bestStartingMove(heights);
    double bestScore = -INFINITY;

    for (int i = 0; i < NBR_COL; i++) {
        int dpRes = putPiece(player, i, heights);
        if (dpRes == NOT_ALLOWED) {
            continue;
        }

        double score = minimax(player, opponent, heights, depth, false, -INFINITY, INFINITY);
        removePiece(player, i, heights);
        if (score > bestScore) {
            bestScore = score;
            bestMove = i;
        }
    }
    return bestMove;
}

int Game::aiMove(const int depth) {
    int ai_col = aiSearchMove(&ai_board, &human_board, depth, col_heights);
    return putPiece(&ai_board, ai_col, col_heights);
}

int Game::humanMove(const int col) {
    return putPiece(&human_board, col, col_heights);
}

void Game::clearBoard() {
    human_board = 0b0;
    ai_board = 0b0;
    uint8_t col_heights[7] = {56, 57, 58, 59, 60, 61, 62};
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
    printf("AI depth: ");
    scanf("%d", &depth);
    while (true) {
        if (current_player == HUMAN) {
            printBoard();
            int col;
            printf("Your move [0-6]: ");
            scanf("%d", &col);
            while (humanMove(col) == NOT_ALLOWED) {
                printf("Reenter your move [0-6]: ");
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
        if (result > 10000) {
            printf("AI WINS!\n");
            printBoard();
            return EXIT_SUCCESS;
        } else if (result < -10000) {
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

/**
 * @brief Allow to use those functions in a python program
 * 
 */
BOOST_PYTHON_MODULE(libai) {
    boost::python::class_<Game>("Game")
        .def("aiMove", &Game::aiMove)
        .def("humanMove", &Game::humanMove)
        .def("clearBoard", &Game::clearBoard)
        .def("printBoard", &Game::printBoard)
        .def("run", &Game::run)
    ;
}
