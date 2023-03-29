#include <boost/python.hpp>
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
#define NOT_ALLOWED -1

/**
 * @brief The class that contains all information about the game
 * 
 */
class Game {
private:
    int HUMAN = 1;
    int AI = ~HUMAN; // This way we are sure they are not the same
    int current_player = HUMAN;

    unsigned long long human_board = 0b0;
    unsigned long long ai_board = 0b0;
    uint8_t col_heights[7] = {56, 57, 58, 59, 60, 61, 62};

    /**
     * @brief Place the new piece on the board
     * 
     * @param player The board representation
     * @param col The column in which we want to put the new piece
     * @param heights The list of the heights of the different columns
     * @return Return NOT_ALLOWED if the column is not valid (full or out of bound), or the column otherwise
     */
    int putPiece(unsigned long long *player, const int col, uint8_t *heights);

    /**
     * @brief Remove the piece at the top of the column choosen
     * 
     * @param player The board representation
     * @param col The column we want to remove the piece
     * @param heights The list of the heights of the different columns
     */
    void removePiece(unsigned long long *player, const int col, uint8_t *heights);

    /**
     * @brief Check if a player is winning
     * 
     * @param bitboard The board representation
     * @return true if the player has won
     * @return false if the player has not won
     */
    bool winning(const unsigned long long bitboard);

    int countNbrOne(const unsigned long long bitboard);
    int nbr3InLine(const unsigned long long bitboard);
    int nbr2InLine(const unsigned long long bitboard);

    /**
     * @brief Compute the score of the board
     * 
     * @param bitboard The board representation
     * @param oppBitboard The opponent board representation
     * @param depth The depth at wich we are looking
     * @return The score computed
     */
    int evaluateBoard(const unsigned long long bitboard, const unsigned long long oppBitboard, const int depth);

    /**
     * @brief Apply the minmax algorithm with alpha-beta prunning
     * 
     * @param player The board representation of the player
     * @param opponent The board representation of the opponent
     * @param heights The list of the heights of the different columns
     * @param depth The maximum depth of the minmax algorithm at this moment
     * @param isMaximising Is we want to maximize or minimize the score the player
     * @param alpha The alpha parameter
     * @param beta The beta parameter
     * @return The score of the minmax algorithm at this level
     */
    int minimax(unsigned long long *player, unsigned long long *opponent, uint8_t *heights, const int depth, const bool isMaximising, double alpha, double beta);

    /**
     * @brief Search the best move the AI can make
     * 
     * @param player The bitboard of the AI
     * @param opponent The bitboard of the opponent
     * @param depth The depth at which we want the AI to look
     * @param heights The list of the heights of the different columns
     * @return The number of the column in which we should play
     */
    int aiSearchMove(unsigned long long *player, unsigned long long *opponent, const int depth, uint8_t *heights);

public:

    /**
     * @brief A wrapper around the AI
     * 
     * @param depth The depth at which the AI should look
     * @return The column in which the AI played or NOT_ALLOWED if the col is not valid
     */
    int aiMove(const int depth);

    /**
     * @brief A wrapper around the Human
     * 
     * @param col The column in which the human want to play
     * @return The column in which the Human played or NOT_ALLOWED if the col is not valid
     */
    int humanMove(const int col);

    /**
     * @brief Reset the state of the board
     * 
     */
    void clearBoard();

    /**
     * @brief Print the board on the screen
     * 
     */
    void printBoard();

    /**
     * @brief Launch a match of connect 4 against the AI
     * 
     * @return the status code
     */
    int run();
};
