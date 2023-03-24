#include <cmath>
#include <cstdint>
#include <cstdio>
#include <ctime>

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

class Game {
private:
    int HUMAN = 1;
    int AI = ~HUMAN; // This way we are sure they are not the same
    int current_player = HUMAN;
    
    unsigned long long human_board = 0b0;
    unsigned long long ai_board = 0b0;
    uint8_t col_heights[7] = {56, 57, 58, 59, 60, 61, 62};
    
    int putPiece(unsigned long long *player, int col, uint8_t *heights);
    void removePiece(unsigned long long *player, int col, uint8_t *heights);
    bool winning(unsigned long long bitboard);
    int evaluateBoard(unsigned long long bitboard, unsigned long long oppBitboard, int depth);
    int minimax(unsigned long long *player, unsigned long long *opponent, uint8_t *heights, int depth, bool isMaximising, double alpha, double beta);
    int aiSearchMove(unsigned long long *player, unsigned long long *opponent, int depth, uint8_t *heights);
public:
    int aiMove(int depth);
    int humanMove(int col);
    void printBoard();
    int run();
};
