#include "threads.hpp"
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <ctime>

/*
The reason we are using (internally) a 8x8 board is because we are using an
uint64_t (so 64 bits long) variable to put the pieces in places. We
could use a 7*7 board or even a 7x6 but it would require to rework how the
pieces are handled, and it may slow down a lot the algorithm.
*/

#define NBR_LINE 6
#define NBR_COL 7
#define BOARDLEN 64
#define MAX_ALLOWED_HEIGHT 48
#define SYMBOL_AI "x"
#define SYMBOL_HUMAN "o"
#define NOT_ALLOWED -1
#define SCORE_NOT_ALLOWED 42587268

/**
 * @brief The class that contains all information about the game
 * 
 */
class Game {
private:
    // Multithreading variables
    int8_t thread_count = 4;

    // Players variables
    int8_t HUMAN = 1;
    int8_t AI = ~HUMAN; // This way we are sure they are not the same
    int8_t current_player = HUMAN; // Not used when in mode shared library

    // The depth of the current move
    int16_t current_depth = 0;

    int8_t col_ordering[7] = {3, 4, 2, 5, 1, 6, 0};

    // The bitboards for the two players
    uint64_t human_board = 0b0;
    uint64_t ai_board = 0b0;
    uint8_t col_heights[7] = {7, 6, 5, 4, 3, 2, 1};

    int64_t count = 0; // This is used to know how many times something is done

    /**
     * @brief Place the new piece on the board
     * 
     * @param player The board representation
     * @param col The column in which we want to put the new piece
     * @param heights The list of the heights of the different columns
     * @return Return NOT_ALLOWED if the column is not valid (full or out of bound), or the column otherwise
     */
    int8_t putPiece(uint64_t *player, const int8_t col, uint8_t *heights);

    /**
     * @brief Remove the piece at the top of the column chosen
     * 
     * @param player The board representation
     * @param col The column we want to remove the piece
     * @param heights The list of the heights of the different columns
     */
    void removePiece(uint64_t *player, const int8_t col, uint8_t *heights);

    /**
     * @brief Count the number of 1 in bitboard
     * 
     * @param bitboard The board representation
     * @return the number of 1
     */
    int8_t countNbrOne(const uint64_t bitboard);

    /**
     * @brief Count the number of 4, 3, and 2 aligned disks
     * 
     * @param bitboard The board representation
     * @param state The state of the board (if winning or not)
     * @return the score associated with the bitboard
     */
    int8_t countPoints(const uint64_t bitboard, bool *state);

    /**
     * @brief Compute the score of the board
     * 
     * @param bitboard The board representation
     * @param oppBitboard The opponent board representation
     * @param depth The depth at wich we are looking
     * @return The score computed
     */
    double evaluateBoard(const uint64_t bitboard, const uint64_t oppBitboard, const int8_t depth);

    /**
     * @brief The negamax variant of the minimax algorithm
     * 
     * @param player The board representation of the player
     * @param opponent The board representation of the opponent
     * @param heights The list of the heights of the different columns
     * @param alpha The alpha parameter
     * @param beta The beta parameter
     * @return The score of the negamax algorithm at this level
     */
    double negamax(uint64_t *player, uint64_t *opponent, uint8_t *heights, double alpha, double beta);

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
     * @return The score of the minimax algorithm at this level
     */
    double minimax(uint64_t *player, uint64_t *opponent, uint8_t *heights, const int8_t depth, const bool isMaximising, double alpha, double beta);

    /**
     * @brief Return the best starting move when no evaluation is done
     * 
     * @param heights The list of the heights of the different columns
     * @return the column played
     */
    int8_t bestStartingMove(const uint8_t *heights);

    /**
     * @brief A structure to copy the important values for multithreading
     * 
     */
    struct value_search {
        uint64_t player;
        uint64_t opponent;
        int8_t depth;
        uint8_t heights[7];

        value_search(uint64_t p, uint64_t o, int8_t d, uint8_t *h) {
            player = p;
            opponent = o;
            depth = d;
            for (int8_t i = 0; i < 7; i++) {heights[i] = h[i];}
        }
    };

    /**
     * @brief The function used for multithreading
     * 
     * @param values The structure for the values copied
     * @param column_played The column for the first move
     * @param best_score A pointer to the variable storing the best score
     * @param best_move A pointer to the variable storing the best move
     */
    void start_search(value_search values, int8_t column_played, double *best_score, int8_t *best_move);

    /**
     * @brief Search the best move the AI can make
     * 
     * @param player The bitboard of the AI
     * @param opponent The bitboard of the opponent
     * @param depth The depth at which we want the AI to look
     * @param heights The list of the heights of the different columns
     * @return The number of the column in which we should play
     */
    int8_t aiSearchMove(uint64_t *player, uint64_t *opponent, const int8_t depth, uint8_t *heights);

public:

    /**
     * @brief A wrapper around the AI
     * 
     * @param depth The depth at which the AI should look
     * @return The column in which the AI played or NOT_ALLOWED if the col is not valid
     */
    int8_t aiMove(const int8_t depth);

    /**
     * @brief A wrapper around the Human
     * 
     * @param col The column in which the human want to play
     * @return The column in which the Human played or NOT_ALLOWED if the col is not valid
     */
    int8_t humanMove(const int8_t col);

    /**
     * @brief Reset the state of the board
     * 
     */
    void resetBoard();

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
    int8_t run();

    /**
     * @brief Get the count object
     * 
     * @return long 
     */
    int64_t get_count() {
        return count;
    }

    int8_t human_winning();

    int8_t ai_winning();

    bool draw();

    int8_t forceAIMove(const int8_t col);
    int8_t scoreAIpos();
};
